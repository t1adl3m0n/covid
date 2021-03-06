# -*- KSding: utf-8 -*-
"""
Created on Sun Mar 24 10:33:09 2019

@author: me1vi
"""
import os
import requests
import urllib.request
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import re
#import arcpy

#url = 'https://github.KSm/CSSEGISandData/KSVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_KSnfirmed_US.csv'
#Set Johns Hopkins github data urls
#COVIDRecovered= "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"
#COVIDDeaths = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
#COVIDConfirmed = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
COVIDUSConfirmed = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv"
COVIDUSDeaths = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv"
ans=''
s={"Alabama":"AL","Alaska":"AK","American Samoa":"AS","Arizona":"AZ","Arkansas":"AR","California":"CA","Colorado":"CO","Connecticut":"CT","Delaware":"DE","District of Columbia":"DC","Federated s of Micronesia":"FM","Florida":"FL","Georgia":"GA","Guam":"GU","Hawaii":"HI","Idaho":"ID","Illinois":"IL","Indiana":"IN","Iowa":"IA","Kansas":"KS","Kentucky":"KY","Louisiana":"LA","Maine":"ME","Marshall Islands":"MH","Maryland":"MD","Massachusetts":"MA","Michigan":"MI","Minnesota":"MN","Mississippi":"MS","Missouri":"MO","Montana":"MT","Nebraska":"NE","Nevada":"NV","New Hampshire":"NH","New Jersey":"NJ","New Mexico":"NM","New York":"NY","North Carolina":"NC","North Dakota":"ND","Northern Mariana Islands":"MP","Ohio":"OH","Oklahoma":"OK","Oregon":"OR","Palau":"PW","Pennsylvania":"PA","Puerto Rico":"PR","Rhode Island":"RI","South Carolina":"SC","South Dakota":"SD","Tennessee":"TN","Texas":"TX","Utah":"UT","Vermont":"VT","Virgin Islands":"VI","Virginia":"VA","Washington":"WA","West Virginia":"WV","Wisconsin":"WI","Wyoming":"WY"}
x = input('Enter your :')
print(': ' + x)
x='Colorado'
x = arcpy.GetParameterAsText(0)
# read_from_url
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
currDayfile=r"D:\data\covid\cases\pivotTimeSeriesConfirmed"+tdate+".csv"
cDfile=[]
newRow={}
if __name__ == '__main__':    
    #read URL
    type=[COVIDUSConfirmed,COVIDUSDeaths]
    ans=read_from_url(COVIDUSConfirmed, timeout=0)
    test=ans.replace('\r','').replace('/','_')
    with open(fullDS,'w') as fileFull:
        fileFull.write(test) 
    fileFull.close() 
    #Create Data Frame
    df=pd.read_csv(fullDS)    
    newDF=pd.DataFrame(columns=['COUNTY','STATE','FIPS','DATE','COUNT'],index= None)
    for row in range(1,len(df)):  
        for col in range(df.columns):
            print(df[row][col])
   
newDF.to_csv(r"D:\data\covid\cases\pivotTimeSeriesConfirmed"+tdate+".csv")
##Plot Counties
##    plotDF=pd.read_csv(currDayfile) 
###    for county in plotDF.COUNTY.unique():
###        cdf=plotDF[plotDF['COUNTY']==county]
####        cdf.plot(x='DATE',y='COUNT',label=county) 
#
