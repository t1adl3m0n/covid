# -*- KSding: utf-8 -*-
"""
Created on Sun Mar 24 10:33:09 2019

@author: me1vi
"""
import requests
import urllib.request
import pandas as pd
import datetime as dt

#url = 'https://github.KSm/CSSEGISandData/KSVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_KSnfirmed_US.csv'
#Set Johns Hopkins github data urls
#COVIDRecovered= "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"
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
tdate=dt.datetime.strftime(dt.date.today(),'%Y%m%d')
fullDS = r"D:\data\covid\cases\time_series_covid19_confirmed_US_"+tdate+".csv"
stateDS = r"D:\data\covid\cases\time_series_covid19_confirmed_state_"+tdate+".csv"
currDaystatefile=r"D:\data\covid\cases\time_series_confirmed_state_"+tdate+".csv"
if __name__ == '__main__':    
    #read URL
    type=[COVIDUSConfirmed,COVIDUSDeaths]
    ans=read_from_url(COVIDUSConfirmed, timeout=0)
    test=ans.replace('\r','').replace('/','_')
    with open(fullDS,'w') as fileFull:
        fileFull.write(test) 
    fileFull.close() 
    df=pd.read_csv(fullDS) 
    x = input('Enter your State:')
    print('State: ' + x)
    stateDF=df[df['Province_State']==x]
    currDay=stateDF.columns[-1]
    currDaystateDF=stateDF[stateDF[currDay]>0]  
    for col in range(currDaystateDF.columns.get_loc('Combined_Key')+1,len(currDaystateDF.columns)):
        if len(currDaystateDF[currDaystateDF.columns[col]].unique())>1: 
            firstCaseDay= currDaystateDF.columns[col]  
            break
    with open(currDaystatefile,'w') as cDstatefile:
        cDstatefile.write("COUNTY,DATE,COUNT\n")
        for row in range(1,len(currDaystateDF)): 
            for col in range(currDaystateDF.columns.get_loc(firstCaseDay),len(currDaystateDF.columns)):  
                newRow=currDaystateDF.Admin2.values[row]+','+currDaystateDF.columns[col]+','+str(currDaystateDF.iloc[row,col])
                cDstatefile.write(newRow)
                cDstatefile.write('\n') 
    cDstatefile.close() 
    #Plot Counties
    plotDF=pd.read_csv(currDaystatefile) 
    for county in plotDF.COUNTY.unique():
        cdf=plotDF[plotDF['COUNTY']==county]
        cdf.plot(x='DATE',y='COUNT',label=county) 

