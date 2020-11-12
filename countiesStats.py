# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 12:52:32 2020

@author: me1vi
"""

import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
counties = ['Adams', 'Alamosa', 'Arapahoe', 'Archuleta', 'Baca', 'Bent', 'Boulder', 'Broomfield', 'Chaffee', 'Cheyenne', 'Clear Creek', 'Conejos', 'Costilla', 'Crowley', 'Custer', 'Delta', 'Denver', 'Dolores', 'Douglas', 'Eagle', 'El Paso', 'Elbert', 'Fremont', 'Garfield', 'Gilpin', 'Grand', 'Gunnison', 'Hinsdale', 'Huerfano', 'Jackson', 'Jefferson', 'Kiowa', 'Kit Carson', 'La Plata', 'Lake', 'Larimer', 'Las Animas', 'Lincoln', 'Logan', 'Mesa', 'Mineral', 'Moffat', 'Montezuma', 'Montrose', 'Morgan', 'Otero', 'Ouray', 'Park', 'Phillips', 'Pitkin', 'Prowers', 'Pueblo', 'Rio Blanco', 'Rio Grande', 'Routt', 'Saguache', 'San Juan', 'San Miguel', 'Sedgwick', 'Summit', 'Teller', 'Washington', 'Weld', 'Yuma']
age=['AGE_0_9', 'AGE_10_19', 'AGE_20_29','AGE_30_39', 'AGE_40_49', 'AGE_50_59', 'AGE_60_69', 'AGE_70_79','AGE_80_PL']
beds=['NUM_LICENSED_BEDS', 'NUM_STAFFED_BEDS', 'NUM_ICU_BEDS','ADULT_ICU_BEDS', 'PEDI_ICU_BEDS']
ethnicity= ['HISPANIC', 'WHITE_NH', 'BLACK_NH', 'NTVAM_NH', 'ASIAN_NH','HAWPI_NH', 'OTHER_NH']
df2=pd.read_csv("D:\data\covid\demogHospitalByCounty.csv") #Open csv file into pandas Data Frame
    
plt.hist(figsize=(16,12),df[age],  rwidth=.9, align='right', label=age)
plt.legend()
plt.show()  
plt.hist(figsize=(16,12),df[beds], rwidth=.9, align='right', label=beds)
plt.legend()
plt.show()  

plt.hist(figsize=(16,12),df[ethnicity],  rwidth=.9, align='right', label=ethnicity)
plt.legend()
plt.show()  
#    print("ethnicity, beds")
#    for x in ethnicity:    
#        for y in beds:
#            df3=df2.fillna(value=0).astype({y: 'int32'}).dtypes
#            #print(c,x,y,df[x].fillna(value=0).values[0],df[y].values[0],df[x].fillna(value=0).corr(other=df[y]))
#            break
#        break