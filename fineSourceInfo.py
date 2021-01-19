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
tdate=dt.datetime.strftime(dt.date.today(),'%Y%m%d')    
COVIDUSConfirmed = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv"
def read_from_url(COVIDUSConfirmed, timeout=0):
    try:
        ans = requests.get(COVIDUSConfirmed, proxies=urllib.request.getproxies()) #Download data from URL
        if ans.status_code == 200:
            return ans.text
    except:
        getTraceback()
if __name__ == '__main__':    
    try:
        newfolder ="D:\data\covid"
        fullDS = os.path.join(newfolder,"All_series"+tdate+".csv")# full dataset down load from raw.githubusercontent.com
        ans=read_from_url(COVIDUSConfirmed, timeout=0)#Sownload data from raw.githubusercontent.com
        test=ans.replace('\r','').replace('/','_')#Set up text string to save to csv file
        with open(fullDS,'w') as fileFull: #Save text string  to csv file
            fileFull.write(test) 
        fileFull.close() # Close csv file after recieving test string
        df=pd.read_csv(fullDS) #Open csv file into pandas Data Frame
    except:
        getTraceback()
