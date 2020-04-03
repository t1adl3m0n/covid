# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 10:33:09 2019

@author: me1vi
"""
import requests
import urllib.request
import pandas as pd

#url = 'https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv'
#Set Johns Hopkins github data urls
#COVIDRecovered ="https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"
#COVIDDeaths = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
#COVIDConfirmed = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
COVIDUSConfirmed = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv"
COVIDUSDeaths = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv"
ans=''
def read_from_url(COVIDUSConfirmed, timeout=0):
    try:
        ans = requests.get(COVIDUSConfirmed, proxies=urllib.request.getproxies())
        if ans.status_code == 200:
            return ans.text
    except Exception as e:
        print(e)
        return None
ans=read_from_url(COVIDUSConfirmed, timeout=0)
test=ans.replace('\r','').replace('/','_')
with open(r"D:\data\covid\cases\time_series_covid19_confirmed_US.csv",'w') as file:
    file.write(test) 
file.close()
df=pd.read_csv(r"D:\data\covid\cases\time_series_covid19_confirmed_US.csv")
startDT=df.columns.get_loc('Combined_Key')+1
endDT=len(df.columns)
print(startDT,endDT)
CO=df[df['Province_State']=='Colorado']
with open(r"D:\data\covid\cases\CO_covid19_confirmed_US.csv",'w') as fileCO:
    fileCO.write(test) 
fileCO.close()
with open(r"D:\data\covid\cases\time_series_CO.csv",'w') as cofile:
    for row in range(1,len(CO)): 
        for col in range(df.columns.get_loc('Combined_Key')+1,len(CO.columns)):  
            newRow=CO.Admin2.values[row]+','+CO.columns[col]+','+str(CO.iloc[row,col])
            cofile.write(newRow)
            cofile.write('\n') 
cofile.close()
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



