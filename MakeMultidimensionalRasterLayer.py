# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 09:30:00 2020

@author: me1vi
arcpy.md.MakeMultidimensionalRasterLayer(r"D:\data\VIIRS\hd5\VNP46A1.A2020287.h22v04.001.2020288071230.h5", "VNP46A1.A2020289.h22v05.001.2020290084135_M16", "BrightnessTemperature_M12;BrightnessTemperature_M13;BrightnessTemperature_M15;BrightnessTemperature_M16;DNB_At_Sensor_Radiance_500m;Glint_Angle;Granule;Lunar_Azimuth;Lunar_Zenith;Moon_Illumination_Fraction;Moon_Phase_Angle;QF_Cloud_Mask;QF_DNB;QF_VIIRS_M10;QF_VIIRS_M11;QF_VIIRS_M12;QF_VIIRS_M13;QF_VIIRS_M15;QF_VIIRS_M16;Radiance_M10;Radiance_M11;Sensor_Azimuth;Sensor_Zenith;Solar_Azimuth;Solar_Zenith;UTC_Time", "ALL", None, None, '', '', '', None, '', "40 30 50 40", "DIMENSIONS")
"""

import os 
import arcpy
import sys
import traceback 
    
def getTraceback():
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
    arcpy.Delete_management(MakeMultidim)
    
#input_fc = ['D:\data\VIIRS\hd5\VNP46A1.A2020287.h23v04.001.2020288071223.h5','D:\data\VIIRS\hd5\VNP46A1.A2020287.h22v04.001.2020288071230.h5',' D:\data\VIIRS\hd5\VNP46A1.A2020287.h22v05.001.2020288071205.h5']    
aprx = arcpy.mp.ArcGISProject("CURRENT")
#aprx =arcpy.mp.ArcGISProject(r'D:/data/VIIRS/VIIRS/VIIRS.aprx')
aprxMap = aprx.listMaps("Map")[0] 
if __name__ == '__main__':    
    try:
        input_fc = arcpy.GetParameter(0)
        for file in input_fc:
            arcpy.AddMessage(file)
            print(file)
            # MakeMultidimensionalRasterLayer
            MakeMultidim = arcpy.md.MakeMultidimensionalRasterLayer(file, "Multidim", "BrightnessTemperature_M12;BrightnessTemperature_M13;BrightnessTemperature_M15;BrightnessTemperature_M16;DNB_At_Sensor_Radiance_500m;Glint_Angle;Granule;Lunar_Azimuth;Lunar_Zenith;Moon_Illumination_Fraction;Moon_Phase_Angle;QF_Cloud_Mask;QF_DNB;QF_VIIRS_M10;QF_VIIRS_M11;QF_VIIRS_M12;QF_VIIRS_M13;QF_VIIRS_M15;QF_VIIRS_M16;Radiance_M10;Radiance_M11;Sensor_Azimuth;Sensor_Zenith;Solar_Azimuth;Solar_Zenith;UTC_Time", "ALL", None, None, '', '', '', None, '', "40 30 50 40", "DIMENSIONS")
            # Save Output
            outF=os.path.join(r'D:\data\VIIRS\crf',os.path.basename(str(file)).replace('H5','lyrx'))
            arcpy.management.SaveToLayerFile(MakeMultidim, outF,"RELATIVE")
#            aprxMap.addLayer(MakeMultidim) 
    except:
        getTraceback()        