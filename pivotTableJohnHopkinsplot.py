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
tdate=dt.datetime.strftime(dt.date.today(),'%Y%m%d')
fullDS=r"D:\data\covid\cases\time_series_covid19_confirmed_US_"+tdate+".csv"
stateDS=("D:\data\covid\cases\time_series_covid19_confirmed_state"+tdate+".csv")
def read_from_url(COVIDUSConfirmed, timeout=0):
    try:
        ans = requests.get(COVIDUSConfirmed, proxies=urllib.request.getproxies())
        if ans.status_code == 200:
            return ans.text
    except Exception as e:
        print(e)
        return None
if __name__ == '__main__':    
    #read URL
    #type=[COVIDUSConfirmed,COVIDUSDeaths]
    ans=read_from_url(COVIDUSConfirmed, timeout=0)
    test=ans.replace('\r','').replace('/','_')
    with open(fullDS,'w') as fileFull:
        fileFull.write(test) 
    fileFull.close()
    
    #Save Individual State
    df=pd.read_csv(fullDS) 
    stateDF=df[df['Province_State']=='Colorado']
    with open(r"D:\data\covid\cases\KS_covid19_confirmed_US.csv",'w') as fileState:
        fileKS.write(stateDF) 
    fileState.close()
    
    with open(r"D:\data\covid\cases\time_series_KS.csv",'w') as KSfile:
        for row in range(1,len(KS)): 
            for col in range(df.columns.get_loc('Combined_Key')+1,len(KS.columns)):  
                newRow=KS.Admin2.values[row]+','+KS.columns[col]+','+str(KS.iloc[row,col])
                KSfile.write(newRow)
                KSfile.write('\n') 
    KSfile.close() 
    cDay=KS.columns[-1]
    cDayKS=KS[KS[cDay]>0] 
    with open(r"D:\data\covid\cases\time_series_KS.csv",'w') as KSfile:
        KSfile.write("COUNTY,DATE,COUNT\n")
        for row in range(1,len(cDayKS)): 
            for col in range(cDayKS.columns.get_loc('3_6_20'),len(cDayKS.columns)):  
                newRow=cDayKS.Admin2.values[row]+','+cDayKS.columns[col]+','+str(cDayKS.iloc[row,col])
                KSfile.write(newRow)
                KSfile.write('\n') 
    KSfile.close() 
    #Plot Counties
    plotDF=pd.read_csv(r"D:\data\covid\cases\time_series_KS.csv") 
    for county in plotDF.COUNTY.unique():
        cdf=plotDF[plotDF['COUNTY']==county]
        cdf.plot(x='DATE',y='COUNT',label=county)



