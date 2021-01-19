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
import re
import arcpy
import sys
import glob 
import numpy as np

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

      
COVIDUSConfirmed =  "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv"
COVIDUSDeaths = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv"

states={"Alabama":"AL","Alaska":"AK","American Samoa":"AS","Arizona":"AZ","Arkansas":"AR","California":"CA","Colorado":"CO","Connecticut":"CT","Delaware":"DE","District of Columbia":"DC","Federated States of Micronesia":"FM","Florida":"FL","Georgia":"GA","Guam":"GU","Hawaii":"HI","Idaho":"ID","Illinois":"IL","Indiana":"IN","Iowa":"IA","Kansas":"KS","Kentucky":"KY","Louisiana":"LA","Maine":"ME","Marshall Islands":"MH","Maryland":"MD","Massachusetts":"MA","Michigan":"MI","Minnesota":"MN","Mississippi":"MS","Missouri":"MO","Montana":"MT","Nebraska":"NE","Nevada":"NV","New Hampshire":"NH","New Jersey":"NJ","New Mexico":"NM","New York":"NY","North Carolina":"NC","North Dakota":"ND","Northern Mariana Islands":"MP","Ohio":"OH","Oklahoma":"OK","Oregon":"OR","Palau":"PW","Pennsylvania":"PA","Puerto Rico":"PR","Rhode Island":"RI","South Carolina":"SC","South Dakota":"SD","Tennessee":"TN","Texas":"TX","Utah":"UT","Vermont":"VT","Virgin Islands":"VI","Virginia":"VA","Washington":"WA","West Virginia":"WV","Wisconsin":"WI","Wyoming":"WY"}
capstoneStates={"Colorado":"CO","Kansas":"KS","Missouri":"MO","Nebraska":"NE","Oklahoma":"OK"}#"Colorado":"CO","Kansas":"KS","Missouri":"MO","Nebraska":"NE","Oklahoma":"OK"
def read_from_url(COVIDUSConfirmed, timeout=0):
    try:
        ans = requests.get(COVIDUSConfirmed, proxies=urllib.request.getproxies()) #Download data from URL
        if ans.status_code == 200:
            return ans.text
    except:
        getTraceback()
def CountFrequency(my_list):  
    # Creating an empty dictionary  
    freq = {} 
    lastValue=0
    for item in my_list: 
        if (item in freq): 
            freq[item] += 1
        else: 
            freq[item] = 1 
    for k, v in freq.items(): 
        if k-lastValue > v:
            freq[k]=int((k-lastValue)/v)
            lastValue =k
        print ("% d : % d"%(k, v)) 
    return freq
if __name__ == '__main__':    
    try:         
        fullDS = r"D:\data\covid\KS_20201229\All_series20201229.csv"# full dataset down load from raw.githubusercontent.com
        df=pd.read_csv(fullDS) #Open csv file into pandas Data Frame
        stateDF=df[df['Province_State'].isin(['Colorado', 'Kansas', 'Missouri', 'Nebraska', 'Oklahoma'])] #Create new data frame with state specific data
        for row in stateDF.iterrows():
            cdf=df[df['FIPS']==row[1][4]]
            cdf[cdf.columns[13:]].diff(axis=1)
            countyValues = cdf.T[12:].values.flatten()
            freqL=CountFrequency(countyValues) 
            print(freqL)
    except:
        getTraceback()
