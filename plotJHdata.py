# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 14:45:25 2020

@author: me1vi
""" 
import pandas as pd 

df=pd.read_csv(r"D:\data\covid\cases\CO_covid19_confirmed_US.csv") 
CO=df[df['Province_State']=='Colorado']  
cDay=CO.columns[-1]
cDayCO=CO[CO[cDay]>0] 
startDate=cDayCO.columns.get_loc('Combined_Key')+1
endDT=cDayCO.columns.get_loc(df.columns[-1]) 
with open(r"D:\data\covid\cases\time_series_CO.csv",'w') as cofile:
    cofile.write("COUNTY,DATE,COUNT\n")
    for row in range(1,len(cDayCO)): 
        for col in range(cDayCO.columns.get_loc('3_6_20'),len(cDayCO.columns)):  
            newRow=cDayCO.Admin2.values[row]+','+cDayCO.columns[col]+','+str(cDayCO.iloc[row,col])
            cofile.write(newRow)
            cofile.write('\n') 
cofile.close()
df=pd.read_csv(r"D:\data\covid\cases\time_series_CO.csv") 
for county in df.COUNTY.unique():
    cdf=df[df['COUNTY']==county]
    cdf.plot(x='DATE',y='COUNT',label=county)