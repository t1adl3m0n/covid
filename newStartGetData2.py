# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 12:31:54 2021

@author: me1vi
"""


import os
import requests
import urllib.request
import pandas as pd
import datetime as dt
import re
import arcpy
import sys
import glob 
import math
pd.set_option('mode.chained_assignment', None)
arcpy.env.overwriteOutput = True
def getTraceback():
    import traceback
    # Get the traceback object
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0] 
    # Concatenate information together concerning the error into a message string
    pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
    msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n" 
    # Return python error messages for use in script tool or Python window
    arcpy.AddError(pymsg)
    arcpy.AddError(msgs) 
    # Print Python error messages for use in Python / Python window
    print(pymsg)
    print(msgs)    
    
COVIDUSConfirmed = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv"
COVIDUSDeaths = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv"

states={"Alabama":"AL","Alaska":"AK","American Samoa":"AS","Arizona":"AZ","Arkansas":"AR","California":"CA","Colorado":"CO","Connecticut":"CT","Delaware":"DE","District of Columbia":"DC","Federated States of Micronesia":"FM","Florida":"FL","Georgia":"GA","Guam":"GU","Hawaii":"HI","Idaho":"ID","Illinois":"IL","Indiana":"IN","Iowa":"IA","Kansas":"KS","Kentucky":"KY","Louisiana":"LA","Maine":"ME","Marshall Islands":"MH","Maryland":"MD","Massachusetts":"MA","Michigan":"MI","Minnesota":"MN","Mississippi":"MS","Missouri":"MO","Montana":"MT","Nebraska":"NE","Nevada":"NV","New Hampshire":"NH","New Jersey":"NJ","New Mexico":"NM","New York":"NY","North Carolina":"NC","North Dakota":"ND","Northern Mariana Islands":"MP","Ohio":"OH","Oklahoma":"OK","Oregon":"OR","Palau":"PW","Pennsylvania":"PA","Puerto Rico":"PR","Rhode Island":"RI","South Carolina":"SC","South Dakota":"SD","Tennessee":"TN","Texas":"TX","Utah":"UT","Vermont":"VT","Virgin Islands":"VI","Virginia":"VA","Washington":"WA","West Virginia":"WV","Wisconsin":"WI","Wyoming":"WY"}
capstoneStates={"Colorado":"CO","Kansas":"KS","Missouri":"MO","Nebraska":"NE","Oklahoma":"OK"}#"Colorado":"CO","Kansas":"KS","Missouri":"MO","Nebraska":"NE","Oklahoma":"OK"

tdate=dt.datetime.strftime(dt.date.today(),'%Y%m%d')
ans=''
gdbTable=''
mfileList=[]
def read_from_url(COVIDUSConfirmed, timeout=0):
    try:
        ans = requests.get(COVIDUSConfirmed, proxies=urllib.request.getproxies()) #Download data from URL
        if ans.status_code == 200:
            return ans.text
    except:
        getTraceback()
fullDS = r"D:\data\covid\cases\\"+"statesJHcases.csv"
capstoneStates = r"D:\data\covid\cases\\"+"capstoneStatesJHcases.csv"
newStates = r"D:\data\covid\cases\\"+"newStatesJHcases.csv"
        
if __name__ == '__main__':    
    try:
        ans=read_from_url(COVIDUSConfirmed, timeout=0)
        test=ans.replace('\r','').replace('/','_')
        with open(fullDS,'w') as fileFull:
            fileFull.write(test) 
        fileFull.close() 
        df=pd.read_csv(fullDS) 
        sDF=df[df['Province_State'].isin(['Colorado', 'Kansas', 'Missouri', 'Nebraska', 'Oklahoma'])] #Create new data frame with state specific data
        sDF=sDF.dropna()
        outof=sDF[sDF.Admin2.str.contains('Out of', na=False)]
        unassigned=sDF[sDF.Admin2.str.contains('Unassigned', na=False)]
        dropme=outof.append(unassigned)
        for ind in dropme.index:
            sDF=sDF.drop(index=ind)
        sDF.to_csv(capstoneStates,sep=',',index=None,header=1)
        newDF=pd.DataFrame(columns=['STATE','COUNTY','GEONUM','DATE','COUNT','PERDAY'])
        for row in range(0,len(sDF)):
            print(sDF[row:row+1])
            gDF=sDF[row:row+1]
            orgV=pd.DataFrame(index=gDF.T[11:].index.values,columns=['STATE','COUNTY','GEONUM','DATE','COUNT','PERDAY'])
            numF=pd.DataFrame()
            orgV['PERDAY']=gDF.T[11:].diff().fillna(0).astype('int')
            orgV['DATE']=gDF.T[11:].index.values
            orgV['DATE']=orgV['DATE'].str.replace("_","-")
            for d in range(0,len(orgV)):
                orgV.DATE[d] = str(dt.datetime.strptime(orgV.DATE[d],"%m-%d-%y"))[:10]
            orgV['COUNT']=gDF.T[11:].astype('int')
            lastVal=0
            for val in orgV['COUNT'].values: 
                if  val != lastVal:
                    orgV.PERDAY[orgV.COUNT==val] = val-lastVal
                lastVal=val
            orgV['STATE']=gDF.Province_State.values[0]
            orgV['COUNTY']=gDF.Admin2.values[0]
            orgV['GEONUM']=gDF.FIPS.values[0].astype('int')
            newDF=newDF.append(orgV,ignore_index=True) 
            newDF.PERDAY[newDF.PERDAY<0]=0
        print(newDF)
        newDF.to_csv(newStates,sep=',',index=None,header=1) 
        #161170
    except:
        getTraceback()
             