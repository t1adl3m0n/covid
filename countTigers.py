# -*- KSding: utf-8 -*-
"""
Created on Sun Mar 24 10:33:09 2019

@author: me1vi
"""
import os
import arcpy
import sys

arcpy.env.overwriteOutput = True
def getTraceback():
    import traceback
    # Get the traceback object
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0] 
    # Concatenate information together concerning the error into a message string
    pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
    msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n" 
    # Return python error messages for use in script tool or Python window
    arcpy.AddError(pymsg)
    arcpy.AddError(msgs) 
    # Print Python error messages for use in Python / Python window
    print(pymsg)
    print(msgs)    

if __name__ == '__main__':    
    try:
       arcpy.env.workspace = "D:\data\Tigers\MyProject1\MyProject1.gdb"   
       fc = r"D:\data\Tigers\MyProject1\MyProject1.gdb\count"
       tp = r"D:\data\Tigers\MyProject1\MyProject1.gdb\Tigers_XYX"
       arcpy.MakeFeatureLayer_management(fc,"fc_lyr")
       arcpy.MakeFeatureLayer_management(tp,"tp_lyr")
       # Make a layer from the feature class
       with arcpy.da.SearchCursor(fc,['GRID_ID','count']) as cursor:
           for row in cursor:
                arcpy.management.SelectLayerByAttribute(fc, "NEW_SELECTION", "GRID_ID = '"+row[0]+"'", None)
                arcpy.management.MakeFeatureLayer(fc, "count_Layer", "GRID_ID = '"+row[0]+"'", None, "")
                result1 = arcpy.GetCount_management("count_Layer")
                #arcpy.AddMessage(str(row) + " to " + str(result1))
                arcpy.management.SelectLayerByLocation("tp_lyr", "INTERSECT", "count_Layer", None, "NEW_SELECTION", "NOT_INVERT")
                result = arcpy.GetCount_management("tp_lyr")
                arcpy.management.CalculateField("count_Layer", "count", result, "PYTHON3", '', "")
                arcpy.AddMessage(str(row)+ " to " +str(result))
                arcpy.Delete_management("fc_lyr") 
#            # Select tiger positions inside hexagon
#            # field2 will be equal to field1 multiplied by 3.0
#            row.setValue("count", result)
#            cursor.updateRow(row)
    except:
        getTraceback()