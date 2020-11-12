# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 09:38:01 2020

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

capstoneStates={"Colorado":"CO","Kansas":"KS","Missouri":"MO","Nebraska":"NE","Oklahoma":"OK"}#"Colorado":"CO","Kansas":"\"+capstoneStates[x]+"","Missouri":"MO","Nebraska":"NE","Oklahoma":"OK"
#D:\data\covid\capstoneStates.nc
if __name__ == '__main__':   
    try:
            arcpy.stpm.CurveFitForecast(r"D:\data\covid\capstoneStates.nc", "COUNT_NONE_ZEROS", r"D:\data\covid\capstoneStates.gdb\capstoneStates_CFF", r"D:\data\covid\capstoneStates_CFF.nc", 7, "AUTO_DETECT", 8)
            arcpy.stpm.ExponentialSmoothingForecast(r"D:\data\covid\capstoneStates.nc", "COUNT_NONE_ZEROS", r"D:\data\covid\capstoneStates.gdb\capstoneStates_ESF", r"D:\data\covid\capstoneStates_ESF.nc", 7, None, 8)
            arcpy.stpm.ForestBasedForecast(r"D:\data\covid\capstoneStates.nc", "COUNT_NONE_ZEROS", r"D:\data\covid\capstoneStates.gdb\capstoneStates_FBF", r"D:\data\covid\capstoneStates_FBF.nc", 7, None, 8, 100, None, None, 100, "VALUE_DETREND")
            arcpy.stpm.EvaluateForecastsByLocation(r"D:\data\covid\capstoneStates_CFF.nc;D:\data\covid\capstoneStates_ESF.nc;D:\data\covid\capstoneStates_FBF.nc", r"D:\data\covid\capstoneStates.gdb\capstoneStates_EFL", r"D:\data\covid\capstoneStates_EFL.nc", "USE_VALIDATION")
    except:
        getTraceback()