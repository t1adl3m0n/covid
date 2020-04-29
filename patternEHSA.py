# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import arcpy
import pandas as pd
from datetime import datetime as dt

if __name__ == "__main__":
    arcpy.env.workspace = 'D:\\data\\covid\\CO_20200429\\CO_20200429.gdb'
    feature_classes = arcpy.ListFeatureClasses()
    df3= pd.DataFrame(columns=['GEONUM', 'CATEGORY', 'PATTERN','DATE'])
    for fc in feature_classes:
        fileDate=dt.strptime(fc[7:15],'%Y%m%d')
        field_names = [i.name for i in arcpy.ListFields(fc) if i.type != 'OID']
        # Open a cursor to extract results from stats table
        cursor = arcpy.da.SearchCursor(fc, field_names)
        # Create a pandas dataframe to display results
        df = pd.DataFrame(data=[row for row in cursor],
                              columns=field_names,dtype=int) 
        print(df)
        df2=df[['GEONUM', 'CATEGORY', 'PATTERN']]
        print(fc,df2.PATTERN.unique())
        df2['DATE'] = fileDate
        print(df2)
        df3=df3.append(df2)
    patternCSV = os.path.join(newfolder,states[x]+'patternEHSA'+tdate+".csv")
    df3.to_csv(patternCSV, sep = ',', index = None, header = 1)