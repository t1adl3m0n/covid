# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 13:38:26 2020

@author: Tia Lemon
change format of table created for covid data
"""

import pandas as pd
import numpy as np
# creating an object 
df = pd.read_csv(r"D:/data/covid/cases/time_series_covid19_confirmed_US.csv")
print(df.head())
with open(r"D:\data\covid\cases\pivotTimeSeries_covid19_US.csv",'w') as file:
    file.write("COUNTY,DATE,COUNT\n")
    for row in range(0,len(df)): 
        for col in range(1,len(df.columns)): 
                newRow=df.COUNTY[row]+','+df.columns[col]+','+str(df.iloc[row,col])
                print(newRow)
                file.write(newRow)
                file.write('\n') 
file.close()