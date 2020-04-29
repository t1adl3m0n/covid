# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import arcpy
import os
import pandas

arcpy.env.workspace   = "D:\data\covid\MyProject\MyProject.gdb"
feature_classes = []
feature_classes = arcpy.ListFeatureClasses()

for fcs in feature_classes:
    if fcs =='HealthcareBedLocations':
        field_names = [i.name for i in arcpy.ListFields(fcs) if i.type != 'OID']
        # Open a cursor to extract results from stats table
        cursor = arcpy.da.SearchCursor(fcs, field_names)
        # Create a pandas dataframe to display results
        df = pandas.DataFrame(data=[row for row in cursor],
                              columns=field_names,dtype=int)
df2=df[['NUM_LICENSED_BEDS', 'NUM_STAFFED_BEDS', 'NUM_ICU_BEDS', 'ADULT_ICU_BEDS', 'PEDI_ICU_BEDS', 'BED_UTILIZATION', 'Potential_Increase_In_Bed_Capac', 'AVG_VENTILATOR_USAGE', 'GEONUM']]
df3=pandas.DataFrame()
 
#GEONUM
df3['GEONUM']=df2.GEONUM.unique()     
#NUM_LICENSED_BEDS
NUM_LICENSED_BEDS=df2.groupby('GEONUM')['NUM_LICENSED_BEDS'].sum()
df3=df3.join(NUM_LICENSED_BEDS,on='GEONUM',how='left',lsuffix='NUM_LICENSED_BEDS', rsuffix='NUM_LICENSED_BEDS')

#NUM_STAFFED_BEDS
NUM_STAFFED_BEDS=df2.groupby('GEONUM')['NUM_STAFFED_BEDS'].sum()
#df3['NUM_STAFFED_BEDS']=NUM_STAFFED_BEDS
df3=df3.join(NUM_STAFFED_BEDS,on='GEONUM',how='left',lsuffix='NUM_STAFFED_BEDS', rsuffix='NUM_STAFFED_BEDS')

#NUM_ICU_BEDS
NUM_ICU_BEDS=df2.groupby('GEONUM')['NUM_ICU_BEDS'].sum()
df3=df3.join(NUM_ICU_BEDS,on='GEONUM',how='left',lsuffix='NUM_ICU_BEDS', rsuffix='NUM_ICU_BEDS')

##ADULT_ICU_BEDS
ADULT_ICU_BEDS=df2.groupby('GEONUM')['ADULT_ICU_BEDS'].sum()
df3=df3.join(ADULT_ICU_BEDS,on='GEONUM',how='left',lsuffix='ADULT_ICU_BEDS', rsuffix='ADULT_ICU_BEDS')

##PEDI_ICU_BEDS
PEDI_ICU_BEDS=df2.groupby('GEONUM')['PEDI_ICU_BEDS'].sum()
df3=df3.join(PEDI_ICU_BEDS,on='GEONUM',how='left',lsuffix='PEDI_ICU_BEDS', rsuffix='PEDI_ICU_BEDS')

##BED_UTILIZATION
BED_UTILIZATION=df2.groupby('GEONUM')['BED_UTILIZATION'].mean()
df3=df3.join(BED_UTILIZATION,on='GEONUM',how='left',lsuffix='BED_UTILIZATION', rsuffix='BED_UTILIZATION')
print(df3)

##Potential_Increase_In_Bed_Capac
Potential_Increase_In_Bed_Capac=df2.groupby('GEONUM')['Potential_Increase_In_Bed_Capac'].mean()
df3=df3.join(Potential_Increase_In_Bed_Capac,on='GEONUM',how='left',lsuffix='Potential_Increase_In_Bed_Capac', rsuffix='Potential_Increase_In_Bed_Capac')

##AVG_VENTILATOR_USAGE
AVG_VENTILATOR_USAGE=df2.groupby('GEONUM')['AVG_VENTILATOR_USAGE'].mean()
df3=df3.join(AVG_VENTILATOR_USAGE,on='GEONUM',how='left',lsuffix='AVG_VENTILATOR_USAGE', rsuffix='AVG_VENTILATOR_USAGE')
df3.to_csv(r"D:\data\covid\cases\hospitalsbycounty.csv",sep=',',index=None,header=1)






