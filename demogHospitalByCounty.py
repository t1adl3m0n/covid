# -*- coding: utf-8 -*-
"""
Spyder Editor
D:\data\covid\scripts\demogHospitalByCounty.py
This is a temporary script file.
"""

import pandas as pd
import numpy as np
def histogram_intersection(a, b):
    v = np.minimum(a, b).sum().round(decimals=1)
    return v
hdata = r'D:\data\covid\hospitalsbycounty.csv'
ddata = r'D:\data\covid\countyDemographics.csv'
cdata = r'D:\data\covid\countyGEONUM.csv'
hdf = pd.read_csv(hdata)
ddf = pd.read_csv(ddata)
cdf = pd.read_csv(cdata)
hdf.rename(str.upper,axis='columns',inplace=True)
ddf.rename(str.upper,axis='columns',inplace=True)
cdf.rename(str.upper,axis='columns',inplace=True)
ndf=cdf.merge(ddf, how='inner', on='GEONUM', left_on=None, right_on=None, left_index=False, right_index=False, sort=False, suffixes=('_x', '_y'), copy=True, indicator=False, validate=None)
df=ndf.merge(hdf, how='inner', on='GEONUM', left_on=None, right_on=None, left_index=False, right_index=False, sort=False, suffixes=('_x', '_y'), copy=True, indicator=False, validate=None)

#print(df.head())
df2=df.fillna(value=0) 
for col in df2.columns:
    if df2[col].dtype == 'O':pass
    if not df2[col].dtype == 'O':
        df2[col]=df2[col].astype(int) 
for col in df2.columns:
    print(df2[col].name)
df2.drop(columns='BED_UTILIZATION',inplace=True)
df2.info()
   
df2.to_csv('D:\data\covid\demogHospitalByCounty.csv',sep=',',index=None,header=1)