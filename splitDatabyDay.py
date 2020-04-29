# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
create Emerging Hot Spot Analysis by day for each day since COVID-19 first reported in state.

""" 
if __name__ == '__main__':  
    import arcpy
    import os
    import pandas as pd 
    import sys
    import traceback
    
    states={"Alabama":"AL","Alaska":"AK","American Samoa":"AS","Arizona":"AZ","Arkansas":"AR","California":"CA","Colorado":"CO","Connecticut":"CT","Delaware":"DE","District of Columbia":"DC","Federated States of Micronesia":"FM","Florida":"FL","Georgia":"GA","Guam":"GU","Hawaii":"HI","Idaho":"ID","Illinois":"IL","Indiana":"IN","Iowa":"IA","Kansas":"KS","Kentucky":"KY","Louisiana":"LA","Maine":"ME","Marshall Islands":"MH","Maryland":"MD","Massachusetts":"MA","Michigan":"MI","Minnesota":"MN","Mississippi":"MS","Missouri":"MO","Montana":"MT","Nebraska":"NE","Nevada":"NV","New Hampshire":"NH","New Jersey":"NJ","New Mexico":"NM","New York":"NY","North Carolina":"NC","North Dakota":"ND","Northern Mariana Islands":"MP","Ohio":"OH","Oklahoma":"OK","Oregon":"OR","Palau":"PW","Pennsylvania":"PA","Puerto Rico":"PR","Rhode Island":"RI","South Carolina":"SC","South Dakota":"SD","Tennessee":"TN","Texas":"TX","Utah":"UT","Vermont":"VT","Virgin Islands":"VI","Virginia":"VA","Washington":"WA","West Virginia":"WV","Wisconsin":"WI","Wyoming":"WY"}
    znewfolder = r"D:\data\covid\\"+states[x]+"_"+tdate
    arcpy.env.workspace = os.path.join(newfolder, states[x]+"_"+tdate+".gdb")
    feature_classes = []
    arcTables = arcpy.ListTables()
    stateDS = r"D:\data\covid\cases"
    coCounties = r"D:\data\covid\MyProject\counties.gdb\full_county_Project"
    os.chdir(stateDS)
    try:
        for tab in arcTables:
            if tab =='COnew_time_series20200428':
                field_names = [i.name for i in arcpy.ListFields(tab) if i.type != 'OID']
                # Open a cursor to extract results from stats table
                cursor = arcpy.da.SearchCursor(tab, field_names)
                # Create a pandas dataframe to display results
                df = pd.DataFrame(data=[row for row in cursor],columns=field_names,dtype=int)
        for date in df.DATE.unique():
            tabtitle = os.path.join(r'D:\data\covid\cases','COcases'+date.strftime('%Y%m%d')+".csv")
            df2 = df[df['DATE']<=date]   
            df2.to_csv(tabtitle,sep=',',index=None,header=1)  
        for root, dirs, files in os.walk(stateDS): 
            for filename in files:
                if filename.find('xml'):pass
                inputTab = os.path.join(root,filename)
                gdbTable = os.path.basename(filename.replace('.csv',''))
                outLocation = r'D:\data\covid\MyProject\covid.gdb'
                netCDFTable = os.path.join(r"D:\data\covid\netCDF",gdbTable+".nc")#r"D:\data\covid\netCDF\\"+gdbTable+".nc"
                arcpy.env.overwriteOutput = True
                arcpy.TableToTable_conversion(inputTab, outLocation, gdbTable) 
                try:
                    arcpy.stpm.CreateSpaceTimeCubeDefinedLocations(coCounties, netCDFTable, "geonum", "NO_TEMPORAL_AGGREGATION", "DATE", "1 Days", "END_TIME", None, "COUNT SPACE_TIME_NEIGHBORS", None, os.path.join(outLocation, gdbTable), "FIPS")
                    arcpy.stpm.EmergingHotSpotAnalysis(netCDFTable, "COUNT_NONE_SPACE_TIME_NEIGHBORS", r"D:\data\covid\MyProject\EHSA.gdb\\"+gdbTable+"EHSA", "100 Kilometers", 1, None, "FIXED_DISTANCE", None, "ENTIRE_CUBE")
                except arcpy.ExecuteError: pass 
    except:
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