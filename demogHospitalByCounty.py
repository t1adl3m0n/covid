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
hdf = pd.read_csv(hdata)
ddf = pd.read_csv(ddata)
df=ddf.set_index('geonum').join(hdf.set_index('GEONUM'))
#print(df.head())
df2=df.fillna(value=0)
df2['GEONUM']=df2.index
df2.info()
for col in df2.columns:
    df2[col]=df2[col].astype(int)
    print(df2[col])
df2.to_csv('D:\data\covid\demogHospitalByCounty.csv',sep=',',index=None,header=1)
for col in df2.columns('hispanic', 'white_nh', 'black_nh', 'ntvam_nh', 'asian_nh', 'hawpi_nh', 'other_nh', 'age_0_9'):
    print(df2[col])