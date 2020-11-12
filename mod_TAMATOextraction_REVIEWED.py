##Script: TOMATOExtraction.py
##Author: ###COMMENT REMOVED
##Date Created: 03 July 2014
##Date Modified: 09 July 2014
##Purpose: To provide a module that contains all of the core functionality for converting
##         "TOMATO" data into emitter points, emitter areas and collection areas with associated
##         attributes. This will enable the user to conduct trending and other forms of analysis


#Standard Modules
import sys, os, string, datetime, re
import arcpy


"""


Overview:
---------
The TOMATO Extraction module provides all neccessary functions for
converting TOMATO data in raster format into a point featureclass or shp file
that represents all of the potential TOMATO emitters in raster TOMATO scene.

The module consists of several classes:

    Parent Class: TOMATOEXTRACTION
    Parent to: ###COMMENT REMOVED
    Purpose: Contains the logic for extracting emitters from any TOMATO dataset.
    
        Child Class: ###COMMENT REMOVED
        Inherits From: TOMATOEXTRACTION
        Purpose: Contains the logic for extracting emitters specific to ###COMMENT REMOVED data

    Parent Class: FILTER
    Purpose: Contains the logic for extracting emi
    Parent to: None
    Purpose: Contains all the logic for pre and post filtering emitter data


Usage:
------

TOMATOEXTRACTION
Properties:
    msgs                                    :Instance of MESSAGING class from custom snippets module. Handles common messaging functionality
    arcsn                                   :Instance of ARCSNIPPETS class from custom snippets module. Handles common arc functionality. 
    filter                                  :Instance of FILTER class which defines filtering behaviour on an input TOMATO dataset. *optional
    
Public Functions:
    extract_attributes()                    :Extra
    Purpose: Contains the logic for extracting emict core attributes and populate attribute table of output features
    extract_collection()                    :Extract a boundary feature file from an input "TOMATO" raster dataset
    extract_collection_batch()              :Extract the boundary features from all rasters in an input directory
    extract_emitters()                      :Extract emitters from an input "TOMATO" raster
    extract_emitter_batch()                 :Extract emitters from all "TOMATO" rasters in an input directory
    extract_emitters_polygon()              :Extract a polygon outline of emitter areas from an input "TOMATO" raster
    extract_emitters_polygon_batch()        :Extract polygon outlines of emitter areas from all "TOMATO" rasters in a directory
    set_relative_intensity()                :Set the "relative" intensity for all features in an input raster dataset.

Private Functions
    __clip_data__()                         :Clip data by optional AOI
    __delete_fields()                       :Delete unneccessary fields
    __get_relative_intensity_classes__()    :Determine the relative intensity classes
    __get_relative_intensity_class__()      :Set the relative intensity class



    Purpose: Contains the logic for extracting emiSEARCHTOMATOEXTRACTION
Properties:

Public Functions:
    *extract_attributes()
    extract_emitters()
    extract_emitters_batch()
    extract_emitters_polygon()
    set_relative_intensity()

Private Functions:
    __clip_data__()
    __get_relative_intensity_classes__()
    __get_relative_intensity_class__()
    __set_workspace__()
    __set_license__()

*Polymorphed from parent
**Additional to parent


FILTER
Propeties:
self.preFilter
self.preFilterLevel
self.postFilter

Public Functions:
run_prefilter()

Private Functions:
__run_prefilter_simple__()
__set_up__()
__set_up_prefilter_simple__()

"""


class TOMATOEXTRACTION():
    def __init__(self, **kwargs):
        """
        Purpose:
            - Overarching class to deal with all components of extracting vector data
              from TOMATO raster files.
            - Parent class to:
                ###COMMENT REMOVED
            
        Argumemts:
            **kwargs
                verbose = True|False
                TOMATOfilter =TOMATOFILTER object
                
        Returns:
            None
        """
        
        #Import custom modules
        import mod_snippets as sn
        self.msgs = sn.MESSAGES(**kwargs)
        self.arcsn = sn.ARCSNIPPETS(**kwargs)

        #Check out spatial analyst license
        self.arcsn.get_license("spatial")
        
        #kwargs
        ##Set up filter
        self.filter = None
        if kwargs.get("TOMATOFilter")!= None:
            self.filter = kwargs.get("TOMATOFilter")
            
        ##Set up workspaces
        self.GDBDel = False
        if kwargs.get("workspace") == None:
            self.workspace = os.getcwd() 
            try:
                self.workspaceGDB = arcpy.env.scratchGDB #ArcGIS 10.1
            except:
                self.workspaceGDB = self.arcsn.set_workspaceGDB(self.workspace) #ArcGIS 10.0
            self.delworkspace = False
        else:
            #User specified worksspace
            self.workspace = kwargs["workspace"]
            self.workspaceGDB = self.arcsn.set_workspaceGDB(kwargs["workspace"], "TOMATOExtract.gdb")
            arcpy.env.scratchWorkspace  = self.workspaceGDB
            self.delworkspace = True
        
        #Overwrite output
        arcpy.env.overwriteOutput = True
        
    ##__________________________
    ##     PUBLIC FUNCTIONS
    ##__________________________
            
    def extract_attributes(self, inputTOMATORaster, outputEmitterFile, **kwargs):
        """
        Purpose:
            - Extract key attributes from filename and write into feature table
            
        Argumemts:
            inputTOMATORaster - input TOMATO raster
            outputEmitterFile - output emitter feature file
            **kwargs

        Returns:
            None
        """
        self.__extract_attributes__(inputTOMATORaster, outputEmitterFile, **kwargs)
    
    def extract_collection(self, inputTOMATORaster, outputCollectionFile, **kwargs):
        self.msgs.message("\n...creating outline feature for..." + inputTOMATORaster)
        outputCollectionFile = self.arcsn.get_raster_footprint(inputTOMATORaster, outputCollectionFile, "POLYGON", **kwargs)
        self.msgs.message("\n...inputTOMATORaster " + inputTOMATORaster + "...outline created...")
                          
        return outputCollectionFile

    def extract_collection_batch(self, inputDirectory, outputCollectionFile, **kwargs):
        #Get Raster List
        arcpy.AddMessage("")
        #self.msgs.message_core("\nExtracting collection outlines from all rasters in directory " + inputDirectory + "...")
        if kwargs.get("walk")!= None:
            walk = kwargs["walk"]
        else:
            walk = False
        rasterList = self.arcsn.get_rasters(inputDirectory, [], walk)

        x = 0
        outlineFiles = []
        errorList = []
        self.msgs.message("\n..." + str(len(rasterList)) + " rasters found...")
        for raster in rasterList:
            print raster
            try:
                outputTemp = os.path.join(self.workspaceGDB, "temp"+str(x))
                self.msgs.message_core("\n...attempting " + outputTemp + " "  + str(x+1) + " of " + str(len(rasterList)) + "...")
                outlineFiles.append(self.extract_collection(raster, outputTemp, **kwargs))
            except:
                errorList.append(raster)
                self.msgs.message("ERROR" + raster)
            x+=1

        if arcpy.Exists(outputCollectionFile) == True:
            #Append
            self.msgs.message("\n...appending outline files...")
            arcpy.Append_management(outlineFiles, outputCollectionFile, "NO_TEST")
        else:
            #Merge
            self.msgs.message("\n...merging outline files...")
            arcpy.Merge_management(outlineFiles, outputCollectionFile)
        self.msgs.message("\n...collection extraction complete...")
        
        
    def extract_emitters(self, inputTOMATORaster, outputEmitterFile, **kwargs):
        """
        Purpose:
            - Extract emitters from input TOMATO raster datset. 

        Arguments:
            inputTOMATORaster - input TOMATO raster
            outputEmitterFile - output emitter feature file
            
            **kwargs
                AOI - Area of Interest File to pre-clip data before extraction
                delete = True|False - Delete interim datasets
            
        Returns:
            outputEmitterFile
        """
    
        self.msgs.message_core("\nExtracting emitters from...")
        self.msgs.message_core("\n..." + inputTOMATORaster + "...")

        #Check outputEmitterFile name
        outputEmitterFile = self.arcsn.check_shp_gdb(outputEmitterFile)
        
        #Create list for cleanup
        cleanList = []

        #Store the original value to ensure it is not deleted
        originalTOMATORaster = inputTOMATORaster
        
        #Optional clip function
        arcpy.overwriteOutput = True
        
        if kwargs.get("AOI") != None:
            inputTOMATORaster = self.__clip_data__(inputTOMATORaster, kwargs["AOI"])
            if inputTOMATORaster != None:
                cleanList.append(inputTOMATORaster)
            else:
                inputTOMATORaster = originalTOMATORaster

        #Optional filter function
        if self.filter!= None:
            if self.filter.preFilter != None:
                inputTOMATORaster = self.filter.run_prefilter(inputTOMATORaster)
                cleanList.append(inputTOMATORaster) #Delete prefilter data output
                kwargs["PreFilter"]= self.filter.preFilterLevel #Populate filter attribute
                
        #Negate input raster
        
        self.msgs.message("\n...inverting input raster...")
        outputNegate = arcpy.sa.Negate(inputTOMATORaster)
        cleanList.append(outputNegate)

        #Create flow direction raster        
        self.msgs.message("\n...creating flow direction raster...")
        arcpy.env.workspace = self.workspace
        arcpy.env.workspaceGDB = self.workspaceGDB
        arcpy.env.scratchWorkspace  = self.workspaceGDB

        outputFlowDir = arcpy.sa.FlowDirection(outputNegate)
        cleanList.append(outputNegate)

        #Create sinks
        self.msgs.message("\n...creating sinks...")
        outputSinks = arcpy.sa.Sink(outputFlowDir)
        cleanList.append(outputSinks)

        #Create sinks polygon
        self.msgs.message("\n...converting to polygons...")
        sinkPoly = os.path.join(self.workspaceGDB, "sinkPoly")
        arcpy.RasterToPolygon_conversion(outputSinks, sinkPoly, "NO_SIMPLIFY")
        cleanList.append(sinkPoly)

        #Create sinks point
        self.msgs.message("\n...converting to points...")
        sinkPoint = os.path.join(self.workspaceGDB, "sinkPoint")
        arcpy.FeatureToPoint_management(sinkPoly, sinkPoint, "INSIDE")
        cleanList.append(sinkPoint)

        #Get original intensity values
        self.msgs.message("\n...finalising emitters...")
        arcpy.sa.ExtractValuesToPoints(sinkPoint, originalTOMATORaster, outputEmitterFile)

        #Add attributes
        self.msgs.message("\n...extracting attributes...")
        self.extract_attributes(originalTOMATORaster, outputEmitterFile, **kwargs)

        #Delete Unnessary fields
        self.__delete_fields__(outputEmitterFile)

        #Set Relative Intensity value
        if kwargs.get("breaks") != None:
            breaks = kwargs[breaks]
        else:
            breaks = 4
        self.set_relative_intensity(outputEmitterFile, breaks)
        
        #Optional Cleanup
        if kwargs.get("delete") == None or kwargs.get("delete") == True:
            self.arcsn.cleanup(cleanList)
             
        self.msgs.message_core("\n...emitter extraction complete.")
        return outputEmitterFile

    def extract_emitters_batch(self, inputDirectory, outputEmitterFile, **kwargs):
        """
        Purpose:
            - Extract emitters from all TOMATO rasters in a directory

        Arguments:
            inputDirectory - input directory containing TOMATO rasters
            outputEmitterFile - output emitter feature file
            
            **kwargs
                AOI - Area of Interest File to pre-clip data before extraction
                delete = True|False - Delete interim datasets
                walk = True|False - Get rasters from all sub-directories in input directory
            
        Returns:
            outputEmitterFile
        """  
        
        #Get Raster List
        self.msgs.message_core("\nExtracting emitters from all rasters in directory " + inputDirectory + "...")
        if kwargs.get("walk")!= None:
            walk = kwargs["walk"]
        else:
            walk = False
        rasterList = self.arcsn.get_rasters(inputDirectory, [], walk)

        #Extract directory of rasters
        x = 0
        emitterFiles = []
        errorList = []
        self.msgs.message("\n..." + str(len(rasterList)) + " rasters found...")
        for raster in rasterList:
            try:
                outputTemp = os.path.join(self.workspaceGDB, "temp"+str(x))
                self.msgs.message_core("\n...attempting " + str(x+1) + " of " + str(len(rasterList)) + "...")
                emitterFiles.append(self.extract_emitters(raster, outputTemp, **kwargs))
            except:
                errorList.append(raster)
                self.msgs.message("ERROR" + raster)
            x+=1                                                            
        self.msgs.message("\n..." + str(len(rasterList)-len(errorList)) + " of " + str(len(rasterList)) + " successfully extracted...")
        
        #Append to outputFile
        if arcpy.Exists(outputEmitterFile) == True:
            #Append
            self.msgs.message("\n...appending emitter files...")
            arcpy.Append_management(emitterFiles, outputEmitterFile, "NO_TEST")
        else:
            #Merge
            self.msgs.message("\n...merging emitter files...")
            arcpy.Merge_management(emitterFiles, outputEmitterFile)

        #Cleanup
        if kwargs.get("delete") == True:
            self.arcsn.cleanup(emitterFiles)
        self.msgs.message_core("\n...batch emitter extraction complete.")

        return outputEmitterFile
        
    def extract_emitters_polygon(self, inputTOMATORaster, outputEmitterPoly, **kwargs):
        """   
        Purpose:
            - Extract an outline polygon representing locations of emitters with the TOMATO scene

        Arguments:
            inputTOMATORaster - Input TOMATO raster file
            outputEmitterFile - Ouput emitter feature file

            **kwargs
                delete = True|False - delete intermin datasets
            
        Returns:
            outputEmitterPoly - name of the output emitter polygon featureclass or shapefile
        """
        
        cleanList = []
        self.msgs.message("\nExtracting emitter polygon...")

        #Store the original value to ensure it is not deleted
        originalTOMATORaster = inputTOMATORaster
        
        #Optional clip function
        if kwargs.get("AOI") != None:
            inputTOMATORaster = self.__clip_data__(inputTOMATORaster, kwargs["AOI"])
            if inputTOMATORaster != None:
                cleanList.append(inputTOMATORaster)
            else:
                inputTOMATORaster = originalTOMATORaster

        #Optional filter function
        if self.filter!= None:
            if self.filter.preFilter != None:
                inputTOMATORaster = self.filter.run_prefilter(inputTOMATORaster)
                cleanList.append(inputTOMATORaster) #Delete prefilter data output
                kwargs["PreFilter"]= self.filter.preFilterLevel #Populate filter attribute       

        #Remap 0 values to Nodata
        if originalTOMATORaster[-4:] == ".ntf":
            maxRange = 1
        else:
            maxRange = 0
        remap = arcpy.sa.RemapRange([[0,maxRange,"NODATA"]])
        self.msgs.message("\n...removing 0 values...")
        reclass = arcpy.sa.Reclassify(inputTOMATORaster, "Value", remap, "DATA")

        #Determine Nodata vs Data
        self.msgs.message("\n...removing 'No Data'...")
        isnull = arcpy.sa.IsNull(reclass)

        #Remap Data to 1 and 0 to Nodata
        remap = arcpy.sa.RemapRange([[1,1,"NODATA"], [0,0,1]])
        reclass = arcpy.sa.Reclassify(isnull, "Value", remap)

        #Create emitter polygons
        self.msgs.message("\n...converting raster to polygon...")
        self.msgs.message(outputEmitterPoly)
        arcpy.RasterToPolygon_conversion(reclass, outputEmitterPoly, "NO_SIMPLIFY")

        #Extract attributes
        self.msgs.message("\n...extracting attributes...")
        self.extract_attributes(originalTOMATORaster, outputEmitterPoly, **kwargs)
        self.__delete_fields__(outputEmitterPoly)
        self.msgs.message("\n...emitter polygon extraction complete.")
        self.msgs.message("\n...output emitter polygon file " + outputEmitterPoly + "...created")

        #Cleanup
        cleanList.append(reclass)
        cleanList.append(isnull)
        if kwargs.get("delete") == True:
            self.arcsn.cleanup(cleanList)
            
        return outputEmitterPoly
    
    def extract_emitters_polygon_batch(self, inputDirectory, outputEmitterPoly, **kwargs):
        #Get Raster List
        self.msgs.message_core("\nExtracting emitter polygons from all rasters in directory " + inputDirectory + "...")
        if kwargs.get("walk")!= None:
            walk = kwargs["walk"]
        else:
            walk = False
        rasterList = self.arcsn.get_rasters(inputDirectory, [], walk)

        #Get Polygons
        x = 0
        polyList = []
        for raster in rasterList:
            tempPoly = os.path.join(self.workspaceGDB, "TempPoly" + str(x))
            polyList.append(self.extract_emitters_polygon(raster, tempPoly, **kwargs))
            x+=1
        
        #Append to outputFile
        if arcpy.Exists(outputEmitterPoly) == True:
            #Append
            self.msgs.message("\n...appending emitter polygon files...")
            arcpy.Append_management(polyList, outputEmitterPoly, "NO_TEST")
        else:
            #Merge
            self.msgs.message("\n...merging emitter polygon files...")
            arcpy.Merge_management(polyList, outputEmitterPoly)

        #Cleanup
        if kwargs.get("delete") == True:
            self.arcsn.cleanup(polyList)
        self.msgs.message_core("\n...batch emitter polygon extraction complete.")

    def finish(self):
        if self.delworkspace == True:
            self.msgs.message("\n...removing temporary workspace GDB...")
            self.arcsn.cleanup([self.workspaceGDB])
        self.msgs.message("\n\n...EXTRACTION PROCESSES COMPLETE...")
        del self.msgs, self.arcsn
        
    def set_relative_intensity(self, outputEmitterFile, numberBreaks):
        """
        Purpose:
            - Bin intensity values into X number of classes so as to compare
              intensity values between scenes.

        Arguments:
            outputEmitterFile - outputer emitter file
            numberBreaks - Number of classes or bins
        
        Returns:
            None

        """
        #Ensure outputEmitterFile has RIntensity field
        fields = []
        fields.append(["Rintensity", "FLOAT", "", "", ""])
        self.arcsn.add_fields(outputEmitterFile, fields)
        
        #Detemine relative intensity classes
        classes = self.__get_relative_intensity_classes__(outputEmitterFile, numberBreaks)
        
        #For each emitter determine then set relative intensity class
        self.msgs.message_core("\n...determining relative intensities...")
        cur = arcpy.UpdateCursor(outputEmitterFile)
        for row in cur:
            iClass = self.__get_relative_intensity_class__(row.getValue("RASTERVALU"), classes)
            row.setValue("Rintensity", iClass)
            cur.updateRow(row)
        self.msgs.message_core("\n...complete...")  
        del cur, row
                                                        

    #___________________________
    #     Private Functions
    #___________________________
    def __clip_data__(self, inputTOMATORaster, AOI):
        """
        Function to clip input TOMATO dataset with AOI file
        """
        arcpy.overwriteOutput = True


        if arcpy.Exists(AOI) == True:
            self.msgs.message("\n...clipping raster with " + AOI + " file...")
            outputRaster = os.path.join(self.workspaceGDB + "\AOI_Clip")
            self.msgs.message(outputRaster)
            arcpy.Clip_management(inputTOMATORaster, "", outputRaster, AOI, "", "ClippingGeometry")
        else:
            self.msgs.message_warning("...invalid AOI...")
            outputRaster = None

        return outputRaster
    
    def __delete_fields__(self, outputEmitterFile):
        """
        Function to delete unnessary fields
        """
        self.arcsn.delete_fields(outputEmitterFile, ["Id", "gridcode", "ORIG_FID"])
        
    def __extract_attributes__(self, rasterFilename, outputEmitterFile, **kwargs):
        """
        Extract core attributes and write to output emitter file
        """
        path, name = os.path.split(rasterFilename)
        kwargs["FileName"] = name
        
        #Check fields exist
        fields = []
        if kwargs.get("UserDate")!=None:
            self.arcsn.add_fields(outputEmitterFile, [["UserDate", "DATE", "", "", ""]])
        if kwargs.get("PreFilter")!=None:
            self.arcsn.add_fields(outputEmitterFile, [["PreFilter", "TEXT", "", "", "", "20"]])
        if kwargs.get("FileName")!=None:
            self.arcsn.add_fields(outputEmitterFile, [["FileName", "TEXT", "", "", "255", ""]])
    
        #Populate Fields
        cur = arcpy.UpdateCursor(outputEmitterFile)
        path, name = os.path.split(rasterFilename)
        for row in cur:
            if kwargs.get("FileName")!=None:
                row.setValue("FileName", name)
            if kwargs.get("UserDate") != None:
                row.setValue("UserDate", kwargs["UserDate"])
            if kwargs.get("PreFilter")!=None:
                row.setValue("PreFilter", kwargs["PreFilter"])
            cur.updateRow(row)

        del cur, row

    def __get_relative_intensity_classes__(self, outputEmitterFile, numberClasses):
        """
        Function to determine the relative intensity classes for the entire
        input dataset
        """
        intensity = []
        breaks = []
        
        cur = arcpy.SearchCursor(outputEmitterFile)
        for row in cur:
            intensity.append(row.getValue("RASTERVALU"))
        div = max(intensity)/numberClasses
        
        x = 1
        while x < numberClasses:
            breaks.append(x*div)
            x+=1
            
        classes = [(0, breaks[0])]
        x = 0
        for y in iter(breaks):
            if x <len(breaks)-1:
                classes.append((y, breaks[x+1]))
                x+=1
            else:
                classes.append((y, max(intensity)))
        del cur
        return classes

    def __get_relative_intensity_class__(self, intensity, classes):
        """
        Function to bin the input intensity into one of the input classes
        """
        classVal = 1
        for x in classes:
            if intensity == classes[0][0]:
                break
            if intensity>x[0] and intensity<=x[1]:
                break
            else:
                classVal+=1
        return classVal
    

        
class ###CODE REMOVED(TOMATOEXTRACTION):
    def __init__(self, **kwargs):
        """
        Purpose:
            - Overarching logic to deal with all components of extracting vector data
              out of ###COMMENT REMOVED files. Sub-class of TOMATO extraction.
            
        Argumemts:
            **kwargs
                
            
        Returns:
            None
        """
        
        TOMATOEXTRACTION.__init__(self, **kwargs)


    #__________________________
    #     PUBLIC FUNCTIONS
    #__________________________

    def extract_attributes(self, inputTOMATORaster, outputEmitterFile, **kwargs):
        """
        Purpose:
            - Extract key attributes from filename and write into feature table.
              This function is specific to ###COMMENT REMOVED data and is dependent
              on the conventional file naming standard.
            
        Argumemts:
            inputTOMATORaster - input TOMATO raster
            outputEmitterFile - output emitter feature file

        Returns:
            None
        """
        #Extract core attributes
        self.__extract_attributes__(inputTOMATORaster, outputEmitterFile, **kwargs)

        #Extract SL Specific attributes
        self.__check_sl_attributes__(outputEmitterFile)
        path, name = os.path.split(inputTOMATORaster)
        dt, band, sensor, threshold = self.__get_sl_attributes__(name)
        self.__set_sl_attributes__(outputEmitterFile, dt, band, sensor, threshold)

    def extract_collection(self, inputTOMATORaster, outputCollectionFile, **kwargs):
        self.msgs.message("\n...creating outline feature for...\n" + inputTOMATORaster)
        outputCollectionFile = self.arcsn.get_raster_footprint(inputTOMATORaster, outputCollectionFile, "POLYGON")
        self.msgs.message("\n...outline created...")
        self.extract_attributes(inputTOMATORaster, outputCollectionFile, **kwargs)                         
        return outputCollectionFile
    #___________________________
    #     PRIVATE FUNCTIONS     
    #___________________________
      
    ##create_SLAttributes(SLFile)
    ##Purpose: check the schema of the output file as it pertains to SL Data
    def __check_sl_attributes__(self,outputEmitterFile):
        """
        Function to check input file for key ###COMMENT REMOVED attributes and add where neccessary
        """
        fields= []
        fields.append(["Sensor", "TEXT", "", "", "", "6"])
        fields.append(["Datetime", "DATE", "", "", "", ""])
        fields.append(["Date", "DATE", "", "", "", ""])
        fields.append(["Band", "TEXT", "", "", "", "6"])
        fields.append(["Threshold", "TEXT", "", "", "", "4"])
        #fields.append(["RASTERVALU", "FLOAT", "", "", "", ""])
        
        self.arcsn.add_fields(outputEmitterFile, fields)

    def __get_sl_attributes__(self, SLFilename):
        """
        Function that uses a series of regular expressions to extract key attributes
        out of a ###COMMENT REMOVED filename.
        """
        #Get Date
        datestring = self.__ptn_match__(SLFilename, r"\d{2}[A-Z]{3}\d{8}")
        dt= datestring
        if datestring !=None:
            dt = datetime.datetime.strptime(datestring, "%d%b%Y%H%M")
        
        #Get band
        band = self.__ptn_match__(SLFilename, r"###CODE REMOVED")
        if band!=None:
            band = band[1:-1]

        #Get Sensor
        sensor = self.__ptn_match__(SLFilename, r"###CODE REMOVED")
        if sensor!=None:
            sensor = sensor[1:]

        #Threshold
        threshold = self.__ptn_match__(SLFilename, r"_[L]{1}\d{1}")
        if threshold!=None:
            threshold = threshold[1:]
            
        return dt, band, sensor, threshold
    
    def __ptn_match__(self, searchString, ptn):
        """
        Function to perform a pattern match.
        """
        try:
            p = re.compile(ptn)
            result = p.findall(searchString)[0] #Finds ONLY first pattern match
            return result
        except:
            return None     
        
    def __set_sl_attributes__(self, outputEmitterFile, dt, band, sensor, threshold):
        """
        Function to set the attributes of an emitter file specific to ###COMMENT REMOVED data
        """
        cur = arcpy.UpdateCursor(outputEmitterFile)
        for row in cur:
            if dt!=None:
                row.setValue("DateTime", str(dt))
                row.setValue("Date", datetime.datetime.strftime(dt, "%m/%d/%Y"))
            if band!=None:
                row.setValue("Band", band)
            if sensor!=None:
                row.setValue("Sensor", sensor)
            if threshold!=None: 
                row.setValue("Threshold", threshold)
            cur.updateRow(row)
        del cur, row


class TOMATOFILTER():
    def __init__(self, **kwargs):
        """
        Purpose:
            - Run a filter to smooth the input raster prior to extraction in an attempt to remove noise
            
        Argumemts:
            inputTOMATORaster - input TOMATO raster
            
        Returns:
            None
        """
        #Import custom modules
        import mod_snippets as sn
        self.msgs = sn.MESSAGES(**kwargs)
        self.arcsn = sn.ARCSNIPPETS(**kwargs)
        self.msgs.message(kwargs)
        self.preFilter = None
        self.preFilterLevel = "None"
        self.postFilter = None

        self.__set_up__(**kwargs)

        ##Set up workspaces
        self.GDBDel = False
        if kwargs.get("workspace") == None:
            self.workspace = os.getcwd() 
            try:
                self.workspaceGDB = arcpy.env.scratchGDB #ArcGIS 10.1
            except:
                self.workspaceGDB = self.arcsn.set_workspaceGDB(self.workspace) #ArcGIS 10.0
        else:
            #User specified worksspace
            self.workspace = kwargs["workspace"]
            self.workspaceGDB = self.arcsn.set_workspaceGDB(kwargs["workspace"], "TOMATOExtract.gdb")

    #__________________________
    #     PUBLIC FUNCTIONS
    #__________________________
    
    def run_prefilter(self, inputTOMATORaster):
        """
        Purpose:
            - Run a filter to smooth the input raster prior to extraction in an attempt to remove noise
            
        Argumemts:
            inputTOMATORaster - input TOMATO raster
            
        Returns:
            None

        """

        self.msgs.message("\n...filling sinks...")
        fill = arcpy.sa.Fill(inputTOMATORaster, "")
        fillFile = os.path.join(self.workspace, "Fill")
        fill.save(fillFile)
        self.msgs.message("\n...complete...")
        
        if self.preFilter == "simple":
            filterTOMATORaster = self.__run_prefilter_simple__(inputTOMATORaster)
            
        elif self.preFilter == "bootstrap":
            filterTOMATORaster = self.__run_prefilter_bootstrap__(inputTOMATORaster)
        
        self.arcsn.cleanup([fillFile])
        return filterTOMATORaster
        
    #___________________________
    #     PRIVATE FUNCTIONS     
    #___________________________
    def __run_prefilter_simple__(self, inputTOMATORaster):
        """
        Function to run prefilter
        """
        x, y = str(self.filterSize[0]), str(self.filterSize[1])

        self.msgs.message("\n...executing simple prefilter with " + x + " " + y + " cell size...")
        self.msgs.message("\n...creating cell matrix...")
        cellmatrix  = arcpy.sa.NbrRectangle(x , y, "CELL")

        self.msgs.message("\n...running focal statistics...")
        smoothTOMATOs = arcpy.sa.FocalStatistics(inputTOMATORaster, cellmatrix, "MEAN")
        smoothTOMATOsFile = os.path.join(self.workspace, "Smooth" + x + y)

        smoothTOMATOs.save(smoothTOMATOsFile)
        
        self.msgs.message("\n...filter complete.")
        return smoothTOMATOsFile
    
     
    def __set_up__(self, **kwargs):
        """
        Function to set up various filter settings
        """
        #Simple prefilter
        if kwargs.get("preFilter") == "simple":
            self.preFilter = "simple"

            #Filter sizes
            if kwargs.get("cellSize") != None: #Custom filter size
                self.filterSize = kwargs["cellSize"][0], kwargs["cellSize"][1]
                
            elif kwargs.get("filterLevel") != None:
                self.preFilterLevel = kwargs["filterLevel"] #Pre-set filter size
                self.filterSize = self.__set_up_prefilter_simple__(kwargs["filterLevel"])
        
            elif self.filterSize == None: #Default filter size
                self.filterSize = self.__self_up_prefilter_simple__("Low") #Default to low pass filter
                self.preFilterLevel = "Low"
            
    def __set_up_prefilter_simple__(self, filterLevel):
        """
        Function to set up various prefilter settings
        """
        if filterLevel == "No":
            return None
        
        elif filterLevel == "Low":
            return ["3", "3"]
        
        elif filterLevel == "Medium":
            return ["5", "5"]
        
        elif filterLevel == "High":
            return ["7", "7"]
        

if __name__ == '__main__':

    #User Variables
    ##inputs
    inputTOMATORaster = r"###CODE REMOVED"
    inputDirectory = r"###CODE REMOVED"
    AOIFile = r"###CODE REMOVED"
    ws = r"D:\Work\Test"
    ##outputs
    collectionFeature = r"###CODE REMOVED"
    collectionFeatures = r"###CODE REMOVED"
    outputEmitterFile = r"###CODE REMOVED"
    emitShape= r"###CODE REMOVED"
    polyShape = r"###CODE REMOVED"


    #Testing
    ##Objects
    LF = TOMATOFILTER(preFilter = "simple", filterLevel = "Low", workspace = ws)
    EE = ###CODE REMOVED(verbose=True, workspace = ws, TOMATOFilter=LF)
    print dir(EE)
    ##Collection Extraction
    ##EE.extract_collection(inputTOMATORaster, collectionFeature)
##    EE.extract_collection_batch(inputDirectory, collectionFeatures)


    ##Emitter Extraction   
    #EE.extract_emitters(inputTOMATORaster, emitShape, AOI = AOIFile, delete = True)
    #emitterFile = EE.extract_emitters_batch(inputDirectory, outputEmitterFile, AOI=AOIFile)

    ##Polygon Extraction
    #EE.extract_emitters_polygon(inputTOMATORaster, polyShape, delete=True, AOI = AOIFile)
    #EE.extract_emitters_polygon_batch(inputDirectory, polyShape, delete=True, AOI = AOIFile, TOMATOFilter = LF)
    
##    #EE.set_relative_intensity(outputEmitterFile, 5)
##    
##
    
