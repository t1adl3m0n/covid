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
import math

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

newDF=[]
newCdf=pd.DataFrame(columns=['GEONUM','COUNTY','STATE','DATE','COUNT','COUNTDIFF', 'FC','PERDAY'])# create new cases per day dataframe 
newDaystatefile=os.path.join(r"D:\data\covid\time_series20201230.csv")# new cases by day for a state
           
if __name__ == '__main__':    
    try: 
        for st in capstoneStates:
            ndf=pd.read_csv(newDaystatefile)
            sDF=ndf[ndf['STATE']==st].drop(columns='UID') #Create new data frame with state specific data
            for cty in sDF.COUNTY.unique():#Create new data frame with state/county specific data
               ctyDF = sDF[sDF['COUNTY']==cty]
               ctyDF.COUNTDIFF = ctyDF.COUNT.diff().fillna(0).astype('int')
#               cvc = ctyDF.COUNT.value_counts()
               cfc=ctyDF.COUNT.value_counts().to_frame(name='FC')
               ctydf=ctyDF.join(cfc,on='COUNT',lsuffix='COUNT',rsuffix=cfc.index)
               ctydf['PERDAY']=(ctydf.COUNTDIFF/ctydf.FC).round().astype('int')
               newCdf=newCdf.append(ctydf)
        newCdf.to_csv(os.path.join(r"D:\data\covid\perDayCount.csv"))
        for state in capstoneStates:
            stateDF=newCdf[newCdf['STATE']==state]
            print(stateDF)
            
    except:
        getTraceback()
#        .add(pDay, axis='columns', level=None, fill_value=math.ceil(ctydf.COUNTDIFF/ctydf.fc)
#            arcpy.AddMessage('State: ' + x)
#            print('State: ' + x)
#            newfolder =os.path.join( r"D:\data\covid",states[x]+"_"+tdate)
#            if not os.path.exists(newfolder):
#                setUpGlobalParameters(x,newfolder)
#            stateDS = os.path.join(newfolder,states[x]+"_time_series"+tdate+".csv")# subset state dataset from raw.githubusercontent.com
#            newDaystatefile=os.path.join(newfolder,states[x]+"time_series"+tdate+".csv")# new cases by day for a state
#            arcpy.env.workspace = os.path.join(newfolder, states[x]+"_"+tdate+".gdb")
#            #read URL 
#            arcpy.AddMessage("read URL")
#            ans=read_from_url(COVIDUSConfirmed, timeout=0)#Sownload data from raw.githubusercontent.com
#            test=ans.replace('\r','').replace('/','_')#Set up text string to save to csv file
#            with open(fullDS,'w') as fileFull: #Save text string  to csv file
#                fileFull.write(test) 
#            fileFull.close() # Close csv file after recieving test string
            # drop columns from '1-22-20' to today - 90 days 
#            startdf = len(df.columns)-95 # find start day today -90 days
#            for col in range(startdf-1,10,-1):
#                df.drop(df.columns[col],axis=1,inplace=True)# drop columns from '1-22-20' to today - 90 days 
#            currDay=len(stateDF.columns)# identify  current day column in dataset
#            startDay = len(stateDF.columns)-94# find start day today -90 days in state dataframe
#            newCdf=pd.DataFrame(columns=stateDF.columns)# create new cases per day dataframe 
#            with open(newDaystatefile,'w') as nDstatefile: #open new csv file to write data to
#                nDstatefile.write("UID,COUNTY,STATE,GEONUM,DATE,COUNT\n")# write headers
#                for row in range(0,len(stateDF)):
#                    cdf=stateDF[stateDF['Admin2']==county]
#                    cdf[cdf.columns[13:]].diff(axis=1)
#                    countyValues = cdf.T[12:].values.flatten()
#                    freqL=CountFrequency(countyValues)
##                    print(county,freqL)
#                    for col in range(0,startDay): #for column in cumulative data set
#                        newCdf[newCdf.columns[col]]=cdf[cdf.columns[col]]# populate first 11 columns of  new cases dataframe
#                    for col in range(startDay,currDay):#  for column in cumulative data set
#                        cVal = int(cdf[cdf.columns[col]])
#                        newCdf[newCdf.columns[col]]=freqL[cVal]
#                    for row in range(0,len(newCdf)): #transformed dataframe from column to rows
#                          for col in range(startDay,len(newCdf.columns)): # 
#                              newRow=str(cdf.UID.values[row])+','+str(cdf.Admin2.values[row])+','+str(cdf.Province_State.fillna(value='None').values[row])+','+str(int(cdf.FIPS.fillna(value='0').values[row]))+','+ str(dt.datetime.strptime(newCdf.columns[col],'%m_%d_%y'))[:10]+','+str(newCdf.iloc[row,col])#format new row for transformed dataframe
#                              if (newRow.split(',')[0] != 'None') and (newRow.split(',')[0] != 'Unassigned') and (newRow.split(',')[0] != re.match('^Out of',newRow.split(',')[0])):# data carpentry before writing to file
#                                  nDstatefile.write(newRow)#write new row to file
#                                  nDstatefile.write('\n')#write carriage return
#            nDstatefile.close()#close file 
#            # Execute TableToTable 
#            outLocation = os.path.join(newfolder, states[x]+"_"+tdate+".gdb")#set outlocation for table
#            newTable=os.path.basename(newDaystatefile.replace('.csv',''))#set new Table name
#            if not os.path.exists(os.path.join(outLocation, newTable)):
#                arcpy.TableToTable_conversion(newDaystatefile, outLocation, newTable) #import csvfile to geodatabase
#            arcpy.AddMessage("Add new csv to gdb")
#            print("Add new csv to gdb")   
#            sdd=splitDatabyDay() 
#            pehsa = patternEHSA()
#            cpdf = combinePatternCount()
#            arcpy.AddMessage("Combine Pattern Count")
#            print("Combine Pattern Count")   
