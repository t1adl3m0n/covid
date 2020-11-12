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
    #msgs = "#arcpy ERRORS:\n" + arcpy.GetMessages(2) + "\n" 
    # Return python error messages for use in script tool or Python window
    #arcpy.AddError(pymsg)
    #arcpy.AddError(msgs) 
    # Print Python error messages for use in Python / Python window
    print(pymsg)
    #print(msgs)    
    
COVIDUSConfirmed = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv"
COVIDUSDeaths = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv"

states={"Alabama":"AL","Alaska":"AK","American Samoa":"AS","Arizona":"AZ","Arkansas":"AR","California":"CA","Colorado":"CO","Connecticut":"CT","Delaware":"DE","District of Columbia":"DC","Florida":"FL","Georgia":"GA","Guam":"GU","Hawaii":"HI","Idaho":"ID","Illinois":"IL","Indiana":"IN","Iowa":"IA","Kansas":"KS","Kentucky":"KY","Louisiana":"LA","Maine":"ME","Maryland":"MD","Massachusetts":"MA","Michigan":"MI","Minnesota":"MN","Mississippi":"MS","Missouri":"MO","Montana":"MT","Nebraska":"NE","Nevada":"NV","New Hampshire":"NH","New Jersey":"NJ","New Mexico":"NM","New York":"NY","North Carolina":"NC","North Dakota":"ND","Northern Mariana Islands":"MP","Ohio":"OH","Oklahoma":"OK","Oregon":"OR","Pennsylvania":"PA","Puerto Rico":"PR","Rhode Island":"RI","South Carolina":"SC","South Dakota":"SD","Tennessee":"TN","Texas":"TX","Utah":"UT","Vermont":"VT","Virgin Islands":"VI","Virginia":"VA","Washington":"WA","West Virginia":"WV","Wisconsin":"WI","Wyoming":"WY"}
 
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
    print(os.path.exists(newfolder))
#Set up global parameters    
fullDS = os.path.join(newfolder,"timeseries_All_series"+tdate+".csv")# full dataset down load from raw.githubusercontent.com
stateDS = os.path.join(newfolder,"timeseries_time_series"+tdate+".csv")# subset state dataset from raw.githubusercontent.com
cumulativeDaystatefile=os.path.join(newfolder,"timeseries_time_series"+tdate+".csv")# cumulative confirmed cases for a state
newDayfile=os.path.join(newfolder,"time_series"+tdate+".csv")# new cases by day for a state
newTable=os.path.join(newfolder,"timeseriesnew"+tdate+".csv")
ans=''
newDF=pd.DataFrame()# create new dataframe for transformed dataframe
if __name__ == '__main__':    
    try:
        #arcpy.env.workspace = os.path.join(newfolder, "timeseries_"+tdate+".gdb")
        #read URL 
        #arcpy.AddMessage("read URL")
        ans=read_from_url(COVIDUSConfirmed, timeout=0)#Sownload data from raw.githubusercontent.com
        test=ans.replace('\r','').replace('/','_')#Set up text string to save to csv file
        with open(fullDS,'w') as fileFull: #Save text string  to csv file
            fileFull.write(test) 
        fileFull.close() # Close csv file after recieving test string
        df=pd.read_csv(fullDS)  
        # print(len(df),df.head())
        #Create new data frame with state specific data
        currDay=df.columns[-1]# identify most current day column in dataset
        newCdf=-pd.DataFrame(columns=df.columns)# create new cases per day dataframe 
        cumulativeDaydf=df[df[currDay]>0]  #build dataframe for rows where cases>0
        for col in range(cumulativeDaydf.columns.get_loc('Combined_Key')+1,len(cumulativeDaydf.columns)):#for columns in range of case day columns
            if len(cumulativeDaydf[cumulativeDaydf.columns[col]].unique())>1: #Find column when first case was reported... this eliminates days/weeks/months that don't have cases for the state
                firstCaseDay= cumulativeDaydf.columns[col]  #column when first case was reported 
                break 
        for col in range(cumulativeDaydf.columns.get_loc(firstCaseDay),len(cumulativeDaydf.columns)):#  for column in cumulative data set
            try:
                if df.Province_State.values[0]== 'Washington' and col == 11:
                    #print(df.Province_State.values[0],dt.datetime.strftime(dt.datetime.strptime(df.columns[col],'%m_%d_%y'),'%Y=%m-%d'),df[df.columns[col]].sum()-0)
                    newRow=df.Province_State.values[0],dt.datetime.strftime(dt.datetime.strptime(df.columns[col],'%m_%d_%y'),'%Y=%m-%d'),df[df.columns[col]].sum()-0
                    newDF=newDF.append(pd.DataFrame([newRow])) 
                else:
                    #print(df.Province_State.values[0],dt.datetime.strftime(dt.datetime.strptime(df.columns[col],'%m_%d_%y'),'%Y=%m-%d'),df[df.columns[col]].sum()-df[df.columns[col-1]].sum())
                    newRow=df.Province_State.values[0],dt.datetime.strftime(dt.datetime.strptime(df.columns[col],'%m_%d_%y'),'%Y=%m-%d'),df[df.columns[col]].sum()-df[df.columns[col-1]].sum()
                    newDF=newDF.append(pd.DataFrame([newRow])) 
            except IndexError as error:
                pass
        newDF.columns= ['STATE', 'DATE', 'COUNT']# create new dataframe for transformed dataframe
        newDF.to_csv(newDayfile, sep=',',index=False)
    except:
        getTraceback()