import sys, string, os, traceback

import arcpy

class MESSAGES():
    def __init__(self, **kwargs):
        if kwargs.has_key("verbose"):
            self.verbose = kwargs["verbose"]
        else:
            self.verbose = True

    def message_core(self, msg):
        verbose = self.verbose
        self.verbose = True
        self.message(msg)
        self.verbose = verbose
        
    def message(self, msg):
        
        if self.verbose == True:
            print msg
            arcpy.AddMessage(msg)
        return msg

    def message_aatc(self):
        self.message("--------------------------------------\n")
        self.message("                __   ,                ")
        self.message("              /\'  |  |\              ")
        self.message("           _/'      `~  \             ")
        self.message("          (      AATC    `\           ")
        self.message("           \     __        )          ")
        self.message("            )_,-~  `=     /           ")
        self.message("                     `---'            ")
        self.message("                      ,-,             ")
        self.message("                      `~              ")
        self.message("   XXXXX                           \n")
        self.message("")
        self.message("")
        self.message("      ___________________________     ")
        self.message("     | XXX TOOL BOX VERSION 1.5 |    ")
        self.message("      ---------------------------     ")
        self.message("")
        self.message("")
        self.message("--------------------------------------\n")
        
    def message_error(self):
        tb = sys.exc_info()[2]
        tb1 = sys.exc_info()[1]
        tbAll = traceback.format_tb(tb)
        tbinfo = ""
        for x in tbAll:
            tbinfo = tbinfo + x + "\n"
        self.message("PYTHON ERRORS:\nTraceback info:\n" + tbinfo
                       + "\nError Info:\n" + str(tb1))

    def message_warning(self, warning):
        self.message("\nWARNING:\n")
        self.message(warning)

    def message_variables(self, toolname, variables):
        '''Input is a list of t
            print msguples. Each tuple has the variable nameand the variable value'''
        verbose = self.verbose
        self.verbose = True
        self.message_aatc()
        self.message("\n")
        self.message("------" + ("-" * len(toolname)))
        self.message("User Inputs: ")
        x = 1
        for variable in variables:
            self.message(str(x).upper() + ". " + variable[0] + ": " + variable[1] + "\n")
            x+=1
        self.message("------" + ("-" * len(toolname)))
        self.verbose = verbose
        
    def set_verbose(self, verbose):
        '''Set verbose True|False'''
        self.verbose = verbose

##GENERAL CLASS TO HANDLE RANDOM ARC FUNCTIONALITY
class ARCSNIPPETS():
    def __init__(self, **kwargs):
        self.msgs = MESSAGES(**kwargs)

    def add_fields(self, infeatures, fielddata):
        currentFields = [f.name for f in arcpy.ListFields(infeatures)]
        for field in fielddata:
            if field[0] not in currentFields:
                arcpy.AddField_management(infeatures, field[0], field[1],
                                          field[2], field[3], field[4])

    def add_name_to_shape(self, shape, name):
        if shape[-4:] == ".shp":
            newshape = shape[:-4] + name + ".shp"
        else:
            newshape = shape + name
        return newshape
    
    def delete_fields(self, infeatures, fieldnames):
        for field in fieldnames:
            try:
                
                arcpy.DeleteField_management(infeatures, field)
            except:
                self.msgs.message_warning("...could not delete field.. "+ field)
            
    ##cleanup(datasets)
    ##Purpose: Use Arc functions to delete a list of datasets
    def cleanup(self, datasets, **kwargs):
        self.msgs.message("\n...removing interim datasets...")
        for dataset in datasets:
            try:
                arcpy.Delete_management(dataset)
            except:
               self.msgs.message("deleting " + dataset)

        self.msgs.message("\n...cleanup complete.")
        
    def get_license(self, esrilicense):
        try:
            if arcpy.CheckExtension(esrilicense) == "Available":
                arcpy.CheckOutExtension(esrilicense)
            
        except arcpy.ExecuteError:
            self.msgs.message(arcpy.GetMessages(2))
        except:
            self.msgs.message()

    def get_rasters(self, inputPath, rasterTypes, walk):
        pathList = []
        rasterList = []

        if walk == True:
            for dirpath, dirnames, filenames in os.walk(inputPath):
                pathList.append(dirpath)
        else:
            pathList = [inputPath]

        for path in pathList:
            arcpy.env.workspace = path

            if rasterTypes == []:
                tempList = arcpy.ListRasters()

            else:
                tempList = arcpy.ListRasters("*", rasterTypes)

            if tempList:
                newList = []
                for temp in tempList:
                    newList.append(os.path.join(path, temp))

                rasterList.extend(newList)

        return rasterList


    def get_raster_footprint(self, raster, outputFeature, outputGeometry):
        self.get_license("3d")
        dsc  = arcpy.Describe(raster)
        arcpy.env.outputCoordinateSystem = dsc.SpatialReference

        arcpy.RasterDomain_3d(raster, outputFeature, outputGeometry)
        self.__check_raster_outline_fields__(outputFeature)
        cursor = arcpy.UpdateCursor(outputFeature)
        path, name = os.path.split(raster)
        for row in cursor:
            row.setValue("FileName", name)
            row.setValue("FilePath", raster)
            row.setValue("RasterType", raster[-3:])
            row.setValue("SpatialRef", dsc.spatialReference.name)
            cursor.updateRow(row)
            
        del cursor
        self.check_license("3d")
        return outputFeature

    def get_raster_footprints(self, rasterDirectory, walk, ouputFeature, outputGeometry, **kwargs):
        rasterlist = self.get_rasters(rasterDirectory, "", walk)
        if kwargs.get("workspace") != None:
            ws = kwargs["workspace"]
        else:
            ws = arcpy.env.scratchGDB
        x = 0
        tempList = []
        for raster in rasterlist:
            tempFeat = os.path.join(ws, "TmpOLne_" + str(x))
            tempOutline = self.get_raster_footprint(raster, tempFeat, outputGeometry)
            tempList.append(tempOutline)

        if arcpy.Exists(outputFeature) == False:
            #Merge
            arcpy.Merge_management(tempList, outputFeature)
        else:
            #Check Fields, Append
            self.__check_raster_outline_fields__(outputFeature)
            arcpy.Append_management(tempList, outputFeature, "NO_TEST")
        self.cleanup(tempList)

        return outputFeature

    def check_license(self, esrilicense):
        arcpy.CheckInExtension(esrilicense)

    def check_shp_gdb(self, filename):
        if ".gdb" in filename:
            pass
        elif filename[-4:] != ".shp":
            filename = filename + ".shp"
        return filename
            
    def __check_raster_outline_fields__(self, rasterOutline):
        fields = []
        fields.append(["FileName", "TEXT", "", "", "100"])
        fields.append(["FilePath", "TEXT", "", "", "256"])
        fields.append(["RasterType", "TEXT", "", "", "4"])
        fields.append(["SpatialRef", "TEXT", "", "", "30"])
        self.add_fields(rasterOutline, fields)

    def set_workspaceGDB(self, inPath, gdbName):
        wsgdb = os.path.join(inPath, gdbName)
        if arcpy.Exists(wsgdb) == False:
            arcpy.CreateFileGDB_management(inPath, gdbName)
        try:
            #Ensure ESRI knows about ws and ws gdb
            arcpy.env.workspace = self.workspace
            arcpy.env.workspaceGDB = self.workspaceGDB
        except:
            pass
        
        return wsgdb

if __name__ == '__main__':
    arcsn = ARCSNIPPETS(verbose=False)
    
        
