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
def splitDatabyDay():
    try:
        arcpy.env.workspace = os.path.join(newfolder, states[x]+"_"+tdate+".gdb")
        arcTables = arcpy.ListTables()# get list of tables
        coCounties = os.path.join("D:\data\covid\MyProject\counties.gdb\\"+x) # variable for USA_Counties
        os.chdir(newfolder) # change the current working directory
        arcpy.AddMessage("arcTables "+str(arcTables))
        for tab in arcTables:
            field_names = [i.name for i in arcpy.ListFields(tab) if i.type != 'OID'] #Get field names
            cursor = arcpy.da.SearchCursor(tab, field_names)# Open a cursor to extract results from  table
            tdf = pd.DataFrame(data=[row for row in cursor],columns=field_names,dtype=int)# Create a pandas dataframe to display results
            for date in tdf.DATE.unique(): 
                tabtitle = os.path.join(newfolder,states[x]+'cases'+date.strftime('%Y%m%d')+".csv")# Create title for daily csv
                tdf2 = tdf[tdf['DATE']<=date]   #create dataframe for daily data
                tdf2.to_csv(tabtitle,sep=',',index=None,header=1)  #Write daily data to daily csv
        arcpy.AddMessage("Create table for each day")
        print("Create table for each day")
        for root, dirs, files in os.walk(newfolder):
            fileGlob=glob.glob('*cases*.csv') #collect files with cases in title
            for filename in fileGlob: # for file in fileGlob
                if filename.find('xml'):pass # Pass on xml file
                #Set up variables
                inputTab = os.path.join(newfolder,filename)
                gdbTable = os.path.basename(filename.replace('.csv',''))
                outLocation = arcpy.env.workspace
                netCDFTable = os.path.join(newfolder,gdbTable+".nc")#r"D:\data\covid\netCDF"+gdbTable+".nc"
                relTable = os.path.join(outLocation, gdbTable)
                EHSA = os.path.join(arcpy.env.workspace,gdbTable+"EHSA") 
                arcpy.TableToTable_conversion(inputTab, outLocation, gdbTable) #Table To Table conversion
                try:
                    #Create Space Time Cube Defined Locations
                    arcpy.stpm.CreateSpaceTimeCubeDefinedLocations(coCounties, netCDFTable, "GEONUM", "NO_TEMPORAL_AGGREGATION", "DATE", "1 Days", "END_TIME", None, "COUNT SPACE_TIME_NEIGHBORS", None, relTable, "GEONUM")
                    arcpy.AddMessage("Create Space Time Cube Defined Locations "+gdbTable )
                    print("Create Space Time Cube Defined Locations "+gdbTable )
                    #Create Emerging Hot Spot Analysis
                    arcpy.stpm.EmergingHotSpotAnalysis(netCDFTable, "COUNT_NONE_SPACE_TIME_NEIGHBORS", EHSA, "100 Kilometers", 1, None, "FIXED_DISTANCE", None, "ENTIRE_CUBE")
                    arcpy.AddMessage("Create Emerging Hot Spot Analysis "+gdbTable)
                    print("Create Emerging Hot Spot Analysis "+gdbTable)
                except: 
                    getTraceback()
            break
        return
    except:
        getTraceback()
#pattern EHSA 
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
            df2=df[['GEONUM', 'CATEGORY', 'PATTERN']]
            df2['DATE'] = fileDate
            df3=df3.append(df2)
#        df3.rename(columns={"GEONUM": "FIPS"},inplace=True)
        patternCSV = os.path.join(newfolder,states[x]+'patternEHSA'+tdate+".csv")
        df3.to_csv(patternCSV, sep = ',', index = None, header = 1)
        arcpy.TableToTable_conversion(patternCSV, arcpy.env.workspace, os.path.basename(patternCSV).replace('.csv','')) #Table To Table conversion
        return
    except:
        getTraceback()
#combinePatternCount 
def combinePatternCount():
    fileList = [];tsfileList = [];pdf2 = pd.DataFrame();tsdf2 = pd.DataFrame()   
    try:       
        for x in capstoneStates:
            tdate=dt.datetime.strftime(dt.date.today(),'%Y%m%d')
            newfolder = os.path.join( r"D:\data\covid",states[x]+"_"+tdate)
            os.chdir(newfolder)
            for root, dirs, files in os.walk(newfolder):
                fileGlob = glob.glob('*pattern*.csv') #collect files with pattern in title
                for filename in fileGlob: # for file in fileGlob
                    fileList.append(os.path.join(newfolder,filename) )
                break
            for root, dirs, files in os.walk(newfolder):
                tsfileGlob = glob.glob('*time_series*.csv') #collect files with cases in title
                for tsfilename in tsfileGlob: # for file in fileGlob
                    tsfileList.append(os.path.join(newfolder,tsfilename) )
                break
        for y in range(0,len(fileList)):
            pdf = pd.read_csv(fileList[y]) 
            pdf3=pdf[pdf['DATE']>=pdf.DATE.unique()[0]]
            pdf2 = pdf2.append(pdf3)
        print(pdf2)
        pdf2.to_csv(os.path.join(r"D:\data\covid","patternEHSA"+tdate+".csv"), sep = ',', index = None, header = 1)     
        for y in range(0,len(tsfileList)):
            tsdf = pd.read_csv(tsfileList[y]) 
            tsdf3=tsdf[tsdf.DATE>=pdf.DATE.unique()[0]]
            tsdf2 = tsdf2.append(tsdf3)
        print(tsdf2)
        tsdf2.to_csv(os.path.join(r"D:\data\covid","time_series"+tdate+".csv"), sep = ',', index = None, header = 1)     
        new_df = pd.merge(tsdf2, pdf2,  how='left', on=['GEONUM','DATE'])
        new_df.dropna(inplace=True)
        patternCount = os.path.join(r"D:\data\covid","patternCount"+tdate+".csv")
        new_df.to_csv(patternCount, sep = ',', index = None, header = 1)
        arcpy.TableToTable_conversion(patternCount, r"D:\data\covid\capstoneStates.gdb","patternCount"+tdate) #Table To Table conversion
        return new_df
    except:
        getTraceback()
def mergeFeatureClasses():#arcpy.management.Merge(mfileList, r"D:\data\covid\MyProject.gdb\capstoneStates", '', "NO_SOURCE_INFO")
    
    #r"D:\data\covid\CO_20201103\\"+states[x]+"_"+tdate+".gdb\\"+states[x]+"_"+tdate+"EHSA
    try:       
        for x in capstoneStates:
            mfileList.append(r"D:\data\covid\\"+states[x]+"_"+tdate+"\\"+states[x]+"_"+tdate+".gdb\\"+states[x]+"cases"+str(int(tdate)-1)+"EHSA" )           
        for file in mfileList:
            print(file)
        if arcpy.Exists(r"D:\data\covid\capstoneStates.gdb\capstoneStates"):
            arcpy.Delete_management(r"D:\data\covid\capstoneStates.gdb\capStates")
            print("Exists D:\data\covid\capstoneStates.gdb\capstoneStates",arcpy.Exists(r"D:\data\covid\capstoneStates.gdb\capstoneStates"))
        arcpy.management.Merge(mfileList, r"D:\data\covid\capstoneStates.gdb\capstoneStates", '', "NO_SOURCE_INFO")
        arcpy.management.AddIndex(r"D:\data\covid\capstoneStates.gdb\capstoneStates", "GEONUM", "GEONUM", "NON_UNIQUE", "NON_ASCENDING")
        patternCount = os.path.join(r"D:\data\covid","patternCount"+tdate+".csv")
        arcpy.TableToTable_conversion(patternCount, r"D:\data\covid\capstoneStates.gdb","patternCount"+tdate) #Table To Table conversion
        
    except:
        getTraceback()
#Set up global parameters 
def setUpGlobalParameters(x,newfolder):
        arcpy.CreateFolder_management(r"D:\data\covid\\", states[x]+"_"+tdate)#Create Folder 
        arcpy.CreateFileGDB_management(newfolder, states[x]+"_"+tdate+".gdb")#Create FileGDB
        arcpy.AddMessage("Create Folder "+states[x]+"_"+tdate)
        arcpy.AddMessage("Create FileGDB "+states[x]+"_"+tdate)
        print("Create Folder "+states[x]+"_"+tdate)
        print("Create FileGDB "+states[x]+"_"+tdate)
def CountFrequency(countyValues):  
    try:
        # Creating an empty dictionary  
        freq = {} 
        lastValue=0
        for item in countyValues: 
            if (item in freq): 
                freq[item] += 1
            else: 
                freq[item] = 1 
        for k, v in freq.items(): 
            if (k-lastValue) > v:
                freq[k]=int((k-lastValue)/v)
                lastValue =k
    #        print ("% d : % d"%(k, v)) 
        return freq
    except:
        getTraceback()

if __name__ == '__main__':    
    try:
        for x in capstoneStates:
            arcpy.AddMessage('State: ' + x)
            print('State: ' + x)
            newfolder =os.path.join( r"D:\data\covid",states[x]+"_"+tdate)
            if not os.path.exists(newfolder):
                setUpGlobalParameters(x,newfolder)
            fullDS = os.path.join(newfolder,"All_series"+tdate+".csv")# full dataset down load from raw.githubusercontent.com
            stateDS = os.path.join(newfolder,states[x]+"_time_series"+tdate+".csv")# subset state dataset from raw.githubusercontent.com
            newDaystatefile=os.path.join(newfolder,states[x]+"time_series"+tdate+".csv")# new cases by day for a state
            arcpy.env.workspace = os.path.join(newfolder, states[x]+"_"+tdate+".gdb")
            #read URL 
            arcpy.AddMessage("read URL")
            ans=read_from_url(COVIDUSConfirmed, timeout=0)#Sownload data from raw.githubusercontent.com
            test=ans.replace('\r','').replace('/','_')#Set up text string to save to csv file
            with open(fullDS,'w') as fileFull: #Save text string  to csv file
                fileFull.write(test) 
            fileFull.close() # Close csv file after recieving test string
            df=pd.read_csv(fullDS) #Open csv file into pandas Data Frame
            df=pd.read_csv(fullDS) #Open csv file into pandas Data Frame
            # drop columns from '1-22-20' to today - 90 days 
            startdf = len(df.columns)-95 # find start day today -90 days
            for col in range(startdf-1,10,-1):
                df.drop(df.columns[col],axis=1,inplace=True)# drop columns from '1-22-20' to today - 90 days 
            countyPop= pd.read_csv(r'D:\data\covid\countyPop.csv')
            cpop=countyPop[['POPULATION','GEONUM']]
            df = cpop.merge(df,left_on='GEONUM',right_on='FIPS')
            stateDF=df[df['Province_State']==x] #Create new data frame with state specific data
            currDay=len(stateDF.columns)# identify  current day column in dataset
            startDay = 14# find start day today -90 days in state dataframe
            newCdf=pd.DataFrame(columns=stateDF.columns)# create new cases per day dataframe 
            with open(newDaystatefile,'w') as nDstatefile: #open new csv file to write data to
                  nDstatefile.write("UID,COUNTY,STATE,POP,GEONUM,DATE,COUNT\n")# write headers
                  for row in stateDF.index: #for row in cumulative data set
                      county=stateDF['Admin2'][row]
                      cdf=stateDF[stateDF['Admin2']==county]
                      cdf[cdf.columns[13:]].diff(axis=1)
                      countyValues = cdf.T[13:].values.flatten()
                      freqL=CountFrequency(countyValues)
                      for col in range(0,startDay): #for column in cumulative data set
                          newCdf[newCdf.columns[col]]=stateDF[stateDF.columns[col]]# populate first 11 columns of  new cases dataframe
                      for col in range(startDay,currDay):#  for column in cumulative data set
                          cVal = int(cdf[cdf.columns[col]])
                          newCdf[newCdf.columns[col]]=freqL[cVal]# calculate new cases for each day column
                  for row in range(0,len(newCdf)): #transformed dataframe from column to rows
                      for col in range(startDay,len(newCdf.columns)): # 
                           newRow=str(newCdf.UID.values[row])+','+str(newCdf.Admin2.values[row])+','+str(newCdf.Province_State.fillna(value='None').values[row])+','+str(newCdf.POPULATION.fillna(value='0').values[row]) +','+str(int(newCdf.FIPS.fillna(value='0').values[row]))+','+ str(dt.datetime.strptime(newCdf.columns[col],'%m_%d_%y'))[:10]+','+str(newCdf.iloc[row,col])#format new row for transformed dataframe
                           if (newRow.split(',')[0] != 'None') and (newRow.split(',')[0] != 'Unassigned') and (newRow.split(',')[0] != re.match('^Out of',newRow.split(',')[0])):# data carpentry before writing to file
                              nDstatefile.write(newRow)#write new row to file
                              nDstatefile.write('\n')#write carriage return
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
            cpdf = combinePatternCount()
            arcpy.AddMessage("Combine Pattern Count")
            print("Combine Pattern Count")  
    except:
        getTraceback()
