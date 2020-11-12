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
#import arcpy
import sys
import glob 

#arcpy.env.overwriteOutput = True
def getTraceback():
    import traceback
    # Get the traceback object
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0] 
    # Concatenate information together concerning the error into a message string
    pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
    #msgs = "#arcpy ERRORS:\n" + #arcpy.GetMessages(2) + "\n" 
    # Return python error messages for use in script tool or Python window
    #arcpy.AddError(pymsg)
    #arcpy.AddError(msgs) 
    # Print Python error messages for use in Python / Python window
    print(pymsg)
    
COVIDUSConfirmed = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv"
COVIDUSDeaths = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv"

states={"Alabama":"AL","Alaska":"AK","American Samoa":"AS","Arizona":"AZ","Arkansas":"AR","California":"CA","Colorado":"CO","Connecticut":"CT","Delaware":"DE","District of Columbia":"DC","Federated States of Micronesia":"FM","Florida":"FL","Georgia":"GA","Guam":"GU","Hawaii":"HI","Idaho":"ID","Illinois":"IL","Indiana":"IN","Iowa":"IA","Kansas":"KS","Kentucky":"KY","Louisiana":"LA","Maine":"ME","Marshall Islands":"MH","Maryland":"MD","Massachusetts":"MA","Michigan":"MI","Minnesota":"MN","Mississippi":"MS","Missouri":"MO","Montana":"MT","Nebraska":"NE","Nevada":"NV","New Hampshire":"NH","New Jersey":"NJ","New Mexico":"NM","New York":"NY","North Carolina":"NC","North Dakota":"ND","Northern Mariana Islands":"MP","Ohio":"OH","Oklahoma":"OK","Oregon":"OR","Palau":"PW","Pennsylvania":"PA","Puerto Rico":"PR","Rhode Island":"RI","South Carolina":"SC","South Dakota":"SD","Tennessee":"TN","Texas":"TX","Utah":"UT","Vermont":"VT","Virgin Islands":"VI","Virginia":"VA","Washington":"WA","West Virginia":"WV","Wisconsin":"WI","Wyoming":"WY"}
 
#x = #arcpy.GetParameterAsText(0) 
#arcpy.AddMessage('State: ' + x)

def read_from_url(COVIDUSConfirmed, timeout=0):
    try:
        ans = requests.get(COVIDUSConfirmed, proxies=urllib.request.getproxies()) #Download data from URL
        if ans.status_code == 200:
            return ans.text
    except:
        getTraceback()

# Create new state/date folder for each run of script
tdate=dt.datetime.strftime(dt.date.today(),'%Y%m%d')
newfolder =os.path.join( r"D:\data\covid",tdate)
if not os.path.exists(newfolder):
    os.mkdir(newfolder)
    print("Create Folder "+tdate)
    print("Create FileGDB "+tdate)
#    
#    
#Set up global parameters    
fullDS = os.path.join(newfolder,"All_series"+tdate+".csv")# full dataset down load from raw.githubusercontent.com 
newDayFile=os.path.join(newfolder,"time_series"+tdate+".csv")# new cases by day for a state
ans=''
if __name__ == '__main__':    
    try:
        #arcpy.env.workspace = os.path.join(newfolder, tdate+".gdb")
        #read URL 
        #arcpy.AddMessage("read URL")
        ans=read_from_url(COVIDUSConfirmed, timeout=0)#Sownload data from raw.githubusercontent.com
        test=ans.replace('\r','').replace('/','_')#Set up text string to save to csv file
        sdmDF=pd.DataFrame()# create new dataframe for transformed dataframe
        sdtDF=pd.DataFrame()# create new dataframe for transformed dataframe
        with open(fullDS,'w') as fileFull: #Save text string  to csv file
            fileFull.write(test) 
            fileFull.close() # Close csv file after recieving test string
            df=pd.read_csv(fullDS) #Open csv file into pandas Data Frame
            for state in states:
                stateDF=df[df['Province_State']==state] #Create new data frame with state specific data
                print(state,len(stateDF))
                sdfDiff=stateDF[stateDF.columns[11:]].diff()
                sdf=stateDF[stateDF.columns[5:7]]
                sdm=sdf.merge(sdfDiff,left_index=True,right_index=True)
                sdmDF=sdmDF.append(sdm)
                sdt=sdm.T
                sdtDF=sdtDF.append(sdt)# create new dataframe for transformed dataframe
        print(sdmDF.tail(),len(sdmDF))
        print(sdtDF.tail(),len(sdtDF))
        sdmFile=os.path.join(newfolder,"sdm"+state+tdate+".csv")
        sdtFile=os.path.join(newfolder,"sdt"+state+tdate+".csv")
        sdmDF.to_csv(sdmFile, sep = ',', index = None, header = 1)
        sdtDF.to_csv(sdtFile, sep = ',', index = None, header = 1)
 
    except:
        getTraceback()