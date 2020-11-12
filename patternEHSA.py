# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import arcpy
import pandas as pd
import datetime as dt
states={"Alabama":"AL","Alaska":"AK","American Samoa":"AS","Arizona":"AZ","Arkansas":"AR","California":"CA","Colorado":"CO","Connecticut":"CT","Delaware":"DE","District of Columbia":"DC","Federated States of Micronesia":"FM","Florida":"FL","Georgia":"GA","Guam":"GU","Hawaii":"HI","Idaho":"ID","Illinois":"IL","Indiana":"IN","Iowa":"IA","Kansas":"KS","Kentucky":"KY","Louisiana":"LA","Maine":"ME","Marshall Islands":"MH","Maryland":"MD","Massachusetts":"MA","Michigan":"MI","Minnesota":"MN","Mississippi":"MS","Missouri":"MO","Montana":"MT","Nebraska":"NE","Nevada":"NV","New Hampshire":"NH","New Jersey":"NJ","New Mexico":"NM","New York":"NY","North Carolina":"NC","North Dakota":"ND","Northern Mariana Islands":"MP","Ohio":"OH","Oklahoma":"OK","Oregon":"OR","Palau":"PW","Pennsylvania":"PA","Puerto Rico":"PR","Rhode Island":"RI","South Carolina":"SC","South Dakota":"SD","Tennessee":"TN","Texas":"TX","Utah":"UT","Vermont":"VT","Virgin Islands":"VI","Virginia":"VA","Washington":"WA","West Virginia":"WV","Wisconsin":"WI","Wyoming":"WY"}
x='Colorado'
tdate=dt.datetime.strftime(dt.date.today(),'%Y%m%d')
newfolder =os.path.join( r"D:\data\covid",states[x]+"_"+tdate)
if __name__ == "__main__":
    arcpy.env.workspace = r'D:\data\covid\CO_20200514\CO_20200514.gdb'
    feature_classes = arcpy.ListFeatureClasses()
    df3= pd.DataFrame(columns=['GEONUM', 'CATEGORY', 'PATTERN','DATE'])
    for fc in feature_classes:
        fileDate=dt.datetime.strptime(fc[7:15],'%Y%m%d')
        field_names = [i.name for i in arcpy.ListFields(fc) if i.type != 'OID']
        # Open a cursor to extract results from stats table
        cursor = arcpy.da.SearchCursor(fc, field_names)
        # Create a pandas dataframe to display results
        df = pd.DataFrame(data=[row for row in cursor],
                              columns=field_names,dtype=int)
        df2=df[['GEONUM', 'CATEGORY', 'PATTERN']]
        print(fc,df2.PATTERN.unique())
        df2['DATE'] = fileDate
        df3=df3.append(df2)
df3.rename(columns={"GEONUM": "FIPS"},inplace=True)
patternCSV = os.path.join(newfolder,states[x]+'patternEHSA'+tdate+".csv")
df3.to_csv(patternCSV, sep = ',', index = None, header = 1)