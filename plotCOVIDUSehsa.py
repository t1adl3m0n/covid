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
    
COVIDUSConfirmed = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv"
COVIDUSDeaths = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv"

states={"Alabama":"AL","Alaska":"AK","American Samoa":"AS","Arizona":"AZ","Arkansas":"AR","California":"CA","Colorado":"CO","Connecticut":"CT","Delaware":"DE","District of Columbia":"DC","Federated States of Micronesia":"FM","Florida":"FL","Georgia":"GA","Guam":"GU","Hawaii":"HI","Idaho":"ID","Illinois":"IL","Indiana":"IN","Iowa":"IA","Kansas":"KS","Kentucky":"KY","Louisiana":"LA","Maine":"ME","Marshall Islands":"MH","Maryland":"MD","Massachusetts":"MA","Michigan":"MI","Minnesota":"MN","Mississippi":"MS","Missouri":"MO","Montana":"MT","Nebraska":"NE","Nevada":"NV","New Hampshire":"NH","New Jersey":"NJ","New Mexico":"NM","New York":"NY","North Carolina":"NC","North Dakota":"ND","Northern Mariana Islands":"MP","Ohio":"OH","Oklahoma":"OK","Oregon":"OR","Palau":"PW","Pennsylvania":"PA","Puerto Rico":"PR","Rhode Island":"RI","South Carolina":"SC","South Dakota":"SD","Tennessee":"TN","Texas":"TX","Utah":"UT","Vermont":"VT","Virgin Islands":"VI","Virginia":"VA","Washington":"WA","West Virginia":"WV","Wisconsin":"WI","Wyoming":"WY"}
capstoneStates={"Colorado":"CO"}#"Colorado":"CO","Kansas":"KS","Missouri":"MO","Nebraska":"NE","Oklahoma":"OK"
 
x=''
#x = arcpy.GetParameterAsText(0) 

def read_from_url(COVIDUSConfirmed, timeout=0):
    try:
        ans = requests.get(COVIDUSConfirmed, proxies=urllib.request.getproxies()) #Download data from URL
        if ans.status_code == 200:
            return ans.text
    except:
        getTraceback()
def splitDatabyDay():
    try:
        arcpy.env.workspace = os.path.join(newfolder, states[x]+"_"+tdate+".gdb")
        arcTables = arcpy.ListTables()# get list of tables
        coCounties = r"D:\data\covid\MyProject\counties.gdb\USA_Counties_LCC" # variable for USA_Counties
        os.chdir(newfolder) # change the current working directory
        arcpy.AddMessage("arcTables "+str(arcTables))
        print("arcTables "+str(arcTables))
        for tab in arcTables:
            field_names = [i.name for i in arcpy.ListFields(tab) if i.type != 'OID'] #Get field names
            cursor = arcpy.da.SearchCursor(tab, field_names)# Open a cursor to extract results from  table
            tdf = pd.DataFrame(data=[row for row in cursor],columns=field_names,dtype=int)# Create a pandas dataframe to display results
            for date in tdf.DATE.unique(): 
                tabtitle = os.path.join(newfolder,date.strftime('%Y%m%d')+".csv")# Create title for daily csv
                tdf2 = tdf[tdf['DATE']<=date]   #create dataframe for daily data
                tdf2.to_csv(tabtitle,sep=',',index=None,header=1)  #Write daily data to daily csv
        arcpy.AddMessage("Create table for each day")
        print("Create table for each day")
        for root, dirs, files in os.walk(newfolder):
            fileGlob=glob.glob('*.csv') #collect files with cases in title
            for filename in fileGlob: # for file in fileGlob
                if filename.find('xml'):pass # Pass on xml file
                #Set up variables
                inputTab = os.path.join(newfolder,filename)
                gdbTable = os.path.basename(filename.replace('.csv',''))
                outLocation = arcpy.env.workspace
                netCDFTable = os.path.join(newfolder,gdbTable+".nc")#r"D:\data\covid\netCDF"+gdbTable+".nc"
                EHSA = os.path.join(arcpy.env.workspace,"EHSA"+gdbTable) 
                arcpy.TableToTable_conversion(inputTab, outLocation, gdbTable) #Table To Table conversion
                try:
                    #Create Space Time Cube Defined Locations
                    arcpy.stpm.CreateSpaceTimeCubeDefinedLocations(coCounties, netCDFTable, "GEONUM", "NO_TEMPORAL_AGGREGATION", "DATE", "1 Days", "END_TIME", None, "COUNT SPACE_TIME_NEIGHBORS", None, os.path.join(outLocation, gdbTable), "GEONUM")
                    #Create Emerging Hot Spot Analysis
                    arcpy.stpm.EmergingHotSpotAnalysis(netCDFTable, "COUNT_NONE_SPACE_TIME_NEIGHBORS", EHSA, "100 Kilometers", 1, None, "FIXED_DISTANCE", None, "ENTIRE_CUBE")
                except:getTraceback()
                arcpy.AddMessage("Create Space Time Cube Defined Locations "+gdbTable )
                print("Create Space Time Cube Defined Locations "+gdbTable )
                arcpy.AddMessage("Create Emerging Hot Spot Analysis "+gdbTable)
                print("Create Emerging Hot Spot Analysis "+gdbTable)
            break
        return
    except:
        getTraceback()
def patternEHSA():
    try:
        arcpy.env.workspace = os.path.join(newfolder, states[x]+"_"+tdate+".gdb")
        feature_classes = arcpy.ListFeatureClasses()
        df3= pd.DataFrame(columns=['GEONUM', 'CATEGORY', 'PATTERN','DATE'])
        for fc in feature_classes:
            fileDate=dt.datetime.strptime(fc[7:15],'%Y%m%d')
            field_names = [i.name for i in arcpy.ListFields(fc) if i.type != 'OID']
            # Open a cursor to extract results from stats table
            cursor = arcpy.da.SearchCursor(fc, field_names)
            # Create a pandas dataframe to display results
            df = pd.DataFrame(data=[row for row in cursor], columns=field_names,dtype=int) 
            print(df)
            df2=df[['GEONUM', 'CATEGORY', 'PATTERN']]
            print(fc,df2.PATTERN.unique())
            df2['DATE'] = fileDate
            print(df2)
            df3=df3.append(df2)
#        df3.rename(columns={"GEONUM": "FIPS"},inplace=True)
        patternCSV = os.path.join(newfolder,'patternEHSA'+tdate+".csv")
        df3.to_csv(patternCSV, sep = ',', index = None, header = 1)
        arcpy.TableToTable_conversion(patternCSV, arcpy.env.workspace, os.path.basename(patternCSV).replace('.csv','')) #Table To Table conversion
        return
    except:
        getTraceback()
# Create new state/date folder for each run of script
tdate=dt.datetime.strftime(dt.date.today(),'%Y%m%d')
#Set up global parameters 
def setUpGlobalParameters(x,newfolder):
        arcpy.CreateFolder_management(r"D:\data\covid\\", states[x]+"_"+tdate)#Create Folder 
        arcpy.CreateFileGDB_management(newfolder, states[x]+"_"+tdate+".gdb")#Create FileGDB
        arcpy.AddMessage("Create Folder "+states[x]+"_"+tdate)
        arcpy.AddMessage("Create FileGDB "+states[x]+"_"+tdate)
        print("Create Folder "+states[x]+"_"+tdate)
        print("Create FileGDB "+states[x]+"_"+tdate)
    
#    
#Set up global parameters    

if __name__ == '__main__':    
    try:
        for x in capstoneStates:
            arcpy.AddMessage('State: ' + x)
            print('State: ' + x)
            newfolder =os.path.join( r"D:\data\covid",states[x]+"_"+tdate) 
            if not os.path.exists(newfolder):
                setUpGlobalParameters(x,newfolder)
            arcpy.env.workspace = os.path.join(newfolder, states[x]+"_"+tdate+".gdb")
            newDaystatefile=os.path.join(newfolder,states[x]+"time_series"+tdate+".csv")# new cases by day for a state
            fullDS = os.path.join(newfolder,"All_series.csv")# full dataset down load from raw.githubusercontent.com
            stateDS = os.path.join(newfolder,"time_series.csv")# subset state dataset from raw.githubusercontent.com
            cumulativeDaystatefile=os.path.join(newfolder,"cumtime_series.csv")# cumulative confirmed cases for a state
            newTable=os.path.join(newfolder,"new.csv")
            ans=''
            #read URL 
            arcpy.AddMessage("read URL")
            ans=read_from_url(COVIDUSConfirmed, timeout=0)#Sownload data from raw.githubusercontent.com
            test=ans.replace('\r','').replace('/','_')#Set up text string to save to csv file
            with open(fullDS,'w') as fileFull: #Save text string  to csv file
                fileFull.write(test) 
            fileFull.close() # Close csv file after recieving test string
            df=pd.read_csv(fullDS) #Open csv file into pandas Data Frame
            stateDF=df[df['Province_State']==x] #Create new data frame with state specific data
            currDay=len(stateDF.columns)# identify  current day column in dataset
            startDay = len(stateDF.columns)-89# find start day today -90 days in state dataframe
            newCdf=pd.DataFrame(columns=stateDF.columns)# create new cases per day dataframe 
            newDF=pd.DataFrame()# create new dataframe for transformed dataframe
            with open(newDaystatefile,'w') as nDstatefile: #open new csv file to write data to
                  nDstatefile.write("UID,COUNTY,STATE,GEONUM,DATE,COUNT\n")# write headers
                  for row in range(0,len(stateDF)): #for row in cumulative data set
                      for col in range(0,startDay): #for column in cumulative data set
                          newCdf[newCdf.columns[col]]=stateDF[stateDF.columns[col]]# populate first 11 columns of  new cases dataframe
                      for col in range(startDay,currDay):#  for column in cumulative data set
                          newCdf[newCdf.columns[col]]=stateDF[stateDF.columns[col]]-stateDF[stateDF.columns[col-1]]# calculate new cases for each day column
                  for row in range(0,len(newCdf)): #transformed dataframe from column to rows
                      for col in range(startDay,len(newCdf.columns)): # 
                          newRow=str(newCdf.UID.values[row])+','+str(newCdf.Admin2.values[row])+','+str(newCdf.Province_State.fillna(value='None').values[row])+','+str(int(newCdf.FIPS.fillna(value='0').values[row]))+','+ str(dt.datetime.strptime(newCdf.columns[col],'%m_%d_%y'))[:10]+','+str(newCdf.iloc[row,col])#format new row for transformed dataframe
                          if (newRow.split(',')[0] != 'None') and (newRow.split(',')[0] != 'Unassigned') and (newRow.split(',')[0] != re.match('^Out of',newRow.split(',')[0])):# data carpentry before writing to file
                              nDstatefile.write(newRow)#write new row to file
                              nDstatefile.write('\n')#write carriage return
            nDstatefile.close()#close file
            arcpy.AddMessage("create new cases per day dataframe")
            print("Create new cases per day dataframe ")
            nDstatefile.close()#close file
            # Execute TableToTable 
            outLocation = os.path.join(newfolder, states[x]+"_"+tdate+".gdb")#set outlocation for table
            newTable=os.path.basename(newDaystatefile.replace('.csv',''))#set new Table name
            if not os.path.exists(os.path.join(outLocation, newTable)):
                arcpy.TableToTable_conversion(newDaystatefile, outLocation, newTable) #import csvfile to geodatabase
            arcpy.AddMessage("Add new csv to gdb")
            print("Add new csv to gdb")   
            sdd=splitDatabyDay()
            pehsa = patternEHSA()
    except:
        getTraceback()