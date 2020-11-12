# List of functions to perform common tasks that can be called in other scripts
from mod_messages import *

#Symbolise and add to map
def add_data_to_map(input_files):
    #add files to a map document
    #input format [(input_file, optional_layer_template), ...]
   try:
           
       import os, arcpy
       add_setting = arcpy.env.addOutputsToMap
       arcpy.env.addOutputsToMap = False

       if add_setting == False:

            # set the mxd to current and get first dataframe 
            mxd = arcpy.mapping.MapDocument("CURRENT")
            df = arcpy.mapping.ListDataFrames(mxd)[0]

            x = 0
            used_lyrs = []
            msg("Adding results to MXD", 4)
            for input_file in input_files:
                try:
                    # determine input file type and create lyr file
                    dsc = arcpy.Describe(input_file[0])
                    # generate lyr name
                    if input_file[1] != "":
                    
                        #temp_lyr = os.path.splitext(os.path.basename(input_file[0]))[0]
                        lyr_dsc = arcpy.Describe(input_file[1])
                        #temp_lyr = os.path.join(arcpy.env.scratchFolder, lyr_dsc.name)
                        name = os.path.splitext(os.path.basename(input_file[0]))[0]
                        temp_lyr = r'\\' + name + "_" + lyr_dsc.name
                        msg(temp_lyr, 1)
                    else:

                        temp_lyr = os.path.splitext(os.path.basename(input_file[0]))[0]
                        if temp_lyr in used_lyrs:
                            temp_lyr = temp_lyr + str(x)
                        used_lyrs.append(temp_lyr)
                        msg(temp_lyr, 1)
                    # determine input file type and create lyr file
                    dsc = arcpy.Describe(input_file[0])
                    if str(dsc.datasetType) == "FeatureClass":
                        msg("creating feature layer", 1)
                        arcpy.MakeFeatureLayer_management(input_file[0], temp_lyr)
                    elif str(dsc.datasetType) == "RasterDataset":
                        msg("creating raster layer", 1)
                        arcpy.MakeRasterLayer_management(input_file[0], temp_lyr)
                        
                    # apply symbology from lyr if provided
                    if input_file[1] != "":
                        msg("Applying symbology", 1)
                        msg(input_file[1], 1)
                        arcpy.ApplySymbologyFromLayer_management(temp_lyr, input_file[1])
                        
                    msg("Adding " + temp_lyr + " to MXD", 1)
                    addLyr = arcpy.mapping.Layer(temp_lyr)
                    arcpy.mapping.AddLayer(df, addLyr, "TOP")
                    x+=1            
                    arcpy.RefreshActiveView()
                except:
                    pass
   except:
        pass
