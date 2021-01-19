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
bdCsv = r'D:\capstone\baseData.csv'
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
        arcpy.env.workspace = os.path.join(newfolder, states[x]+"_20201031"+".gdb")
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
        arcpy.env.workspace = os.path.join(newfolder, states[x]+"_20201031"+".gdb")
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
        patternCSV = os.path.join(newfolder,states[x]+'patternEHSA'+"20201031"+".csv")
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
            newfolder = os.path.join( r"D:\data\covid",states[x]+"_20201031")
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
        pdf2.to_csv(os.path.join(r"D:\data\covid","patternEHSA"+"20201031"+".csv"), sep = ',', index = None, header = 1)     
        for y in range(0,len(tsfileList)):
            tsdf = pd.read_csv(tsfileList[y]) 
            tsdf3=tsdf[tsdf.DATE>=pdf.DATE.unique()[0]]
            tsdf2 = tsdf2.append(tsdf3)
        print(tsdf2)
        tsdf2.to_csv(os.path.join(r"D:\data\covid","time_series"+"20201031"+".csv"), sep = ',', index = None, header = 1)     
        new_df = pd.merge(tsdf2, pdf2,  how='left', on=['GEONUM','DATE'])
        new_df.dropna(inplace=True)
        patternCount = os.path.join(r"D:\data\covid","patternCount"+"20201031"+".csv")
        new_df.to_csv(patternCount, sep = ',', index = None, header = 1)
        arcpy.TableToTable_conversion(patternCount, r"D:\data\covid\capstoneStates.gdb","patternCount"+"20201031") #Table To Table conversion
        return new_df
    except:
        getTraceback()
def mergeFeatureClasses():#arcpy.management.Merge(mfileList, r"D:\data\covid\MyProject.gdb\capstoneStates", '', "NO_SOURCE_INFO")
    
    #r"D:\data\covid\CO_20201103\\"+states[x]+"_20201031"+".gdb\\"+states[x]+"_20201031"+"EHSA
    try:
        for x in capstoneStates:
            newfolder =os.path.join( r"D:\data\covid",states[x]+"_20201031")
            arcpy.env.workspace = os.path.join(newfolder, states[x]+"_20201031"+".gdb")
            EHSA = os.path.join(arcpy.env.workspace,states[x]+'cases'+"20201031"+"EHSA") 
            print(x,EHSA)
            mfileList.append(EHSA)
        if arcpy.Exists(r"D:\data\covid\capstoneStates.gdb\capstoneStates"):
            arcpy.Delete_management(r"D:\data\covid\capstoneStates.gdb\capstoneStates")
            print("Exists D:\data\covid\capstoneStates.gdb\capstoneStates20201031",arcpy.Exists(r"D:\data\covid\capstoneStates.gdb\capstoneStates20201031"))
        arcpy.management.Merge(mfileList, r"D:\data\covid\capstoneStates.gdb\capstoneStates", '', "NO_SOURCE_INFO")
        arcpy.management.AddIndex(r"D:\data\covid\capstoneStates.gdb\capstoneStates", "GEONUM", "GEONUM", "NON_UNIQUE", "NON_ASCENDING")
        patternCount = os.path.join(r"D:\data\covid","patternCount"+"20201031"+".csv")
        arcpy.TableToTable_conversion(patternCount, r"D:\data\covid\capstoneStates.gdb","patternCount"+"20201031") #Table To Table conversion
        arcpy.management.AddIndex(r"D:\data\covid\capstoneStates.gdb\capstoneStates", "GEONUM", "GEONUM", "NON_UNIQUE", "NON_ASCENDING")
    except:
        getTraceback()

#Create Final FC        
def createFinalFC():#arcpy.management.Merge(mfileList, r"D:\data\covid\MyProject.gdb\capstoneStates", '', "NO_SOURCE_INFO")
    try:
        patternCount = os.path.join(r"D:\data\covid","patternCount"+"20201031"+".csv")
        capstoneStates = r"D:\data\covid\capstoneStates.gdb\capstoneStates"
        arcpy.management.AddJoin(capstoneStates, "GEONUM", patternCount, "GEONUM", "KEEP_ALL")
        arcpy.conversion.FeatureClassToFeatureClass("capstoneStates", r"D:\data\covid\cases\Default.gdb", "capstoneStates", '', 'GEONUM "GEONUM" true true false 4 Long 0 0,First,#,capstoneStates,capstoneStates.GEONUM,-1,-1;Shape_Length "Shape_Length" false true true 8 Double 0 0,First,#,capstoneStates,capstoneStates.Shape_Length,-1,-1;Shape_Area "Shape_Area" false true true 8 Double 0 0,First,#,capstoneStates,capstoneStates.Shape_Area,-1,-1;UID "UID" true true false 4 Long 0 0,First,#,capstoneStates,patternCount20201031.UID,-1,-1;STATE "STATE" true true false 8000 Text 0 0,First,#,capstoneStates,patternCount20201031.STATE,0,8000;GEONUM_1 "GEONUM" true true false 4 Long 0 0,First,#,capstoneStates,patternCount20201031.GEONUM,-1,-1;DATE "DATE" true true false 8 Date 0 0,First,#,capstoneStates,patternCount20201031.DATE,-1,-1;COUNT "COUNT" true true false 8 Double 0 0,First,#,capstoneStates,patternCount20201031.COUNT,-1,-1;CATEGORY "CATEGORY" true true false 4 Long 0 0,First,#,capstoneStates,patternCount20201031.CATEGORY,-1,-1;PATTERN "PATTERN" true true false 8000 Text 0 0,First,#,capstoneStates,patternCount20201031.PATTERN,0,8000', '')
        #Create Space Time Cube Defined Locations
        arcpy.stpm.CreateSpaceTimeCubeDefinedLocations(coCounties, netCDFTable, "GEONUM", "NO_TEMPORAL_AGGREGATION", "DATE", "1 Days", "END_TIME", None, "COUNT SPACE_TIME_NEIGHBORS", None, relTable, "GEONUM")
        arcpy.AddMessage("Create Space Time Cube Defined Locations "+gdbTable )
        print("Create Space Time Cube Defined Locations "+gdbTable )
    except:
        getTraceback()
#Set up global parameters 
def setUpGlobalParameters(x,newfolder):
        arcpy.CreateFolder_management(r"D:\data\covid\\", states[x]+"_20201031")#Create Folder 
        arcpy.CreateFileGDB_management(newfolder, states[x]+"_20201031"+".gdb")#Create FileGDB
        arcpy.AddMessage("Create Folder "+states[x]+"_20201031")
        arcpy.AddMessage("Create FileGDB "+states[x]+"_20201031")
        print("Create Folder "+states[x]+"_20201031")
        print("Create FileGDB "+states[x]+"_20201031")
if __name__ == '__main__':    
    try:
#        for x in capstoneStates:
#            arcpy.AddMessage('State: ' + x)
#            print('State: ' + x)
#            newfolder =os.path.join( r"D:\data\covid",states[x]+"_20201031")
#            if not os.path.exists(newfolder):
#                setUpGlobalParameters(x,newfolder)
#            newDaystatefile=os.path.join(newfolder,states[x]+"time_series"+"20201031"+".csv")# new cases by day for a state
#            df=pd.read_csv(bdCsv) #Open csv file into pandas Data Frame
#            countyPop= pd.read_csv(r'D:\data\covid\countyPop.csv')
#            cpop=countyPop[['POPULATION','GEONUM']]
#            df = df.merge(cpop,left_on='FIPS',right_on='GEONUM')
#            # drop columns from '1-22-20' to today - 90 days 
#            stateDF=df[df['Province_State']==x] #Create new data frame with state specific data
#            currDay=len(stateDF.columns)-2# identify  current day column in dataset
#            startDay = 12 # find start day today -90 days in state dataframe
#            newCdf=pd.DataFrame(columns=stateDF.columns)# create new cases per day dataframe 
#            with open(newDaystatefile,'w') as nDstatefile: #open new csv file to write data to
#                  nDstatefile.write("UID,COUNTY,STATE,GEONUM,DATE,COUNT\n")# write headers
#                  for row in range(0,len(stateDF)): #for row in cumulative data set
#                      for col in range(0,startDay): #for column in cumulative data set
#                          newCdf[newCdf.columns[col]]=stateDF[stateDF.columns[col]]# populate first 11 columns of  new cases dataframe
#                      for col in range(startDay,currDay):#  for column in cumulative data set
#                          newCdf[newCdf.columns[col]] = ((stateDF[stateDF.columns[col]]-stateDF[stateDF.columns[col-1]])/stateDF.POPULATION)*100000# calculate new cases for each day column
#                  for row in range(0,len(newCdf)): #transformed dataframe from column to rows
#                      for col in range(startDay,len(newCdf.columns)-2): # 
#                          newRow=str(newCdf.UID.values[row])+','+str(newCdf.Admin2.values[row])+','+str(newCdf.Province_State.fillna(value='None').values[row])+','+str(int(newCdf.FIPS.fillna(value='0').values[row]))+','+ str(dt.datetime.strptime(newCdf.columns[col],'%m_%d_%y'))[:10]+','+str(newCdf.iloc[row,col])#format new row for transformed dataframe
#                          if (newRow.split(',')[0] != 'None') and (newRow.split(',')[0] != 'Unassigned') and (newRow.split(',')[0] != re.match('^Out of',newRow.split(',')[0])):# data carpentry before writing to file
#                              nDstatefile.write(newRow)#write new row to file
#                              nDstatefile.write('\n')#write carriage return
#            nDstatefile.close()#close file 
#            # Execute TableToTable 
#            outLocation = os.path.join(newfolder, states[x]+"_20201031"+".gdb")#set outlocation for table
#            newTable=os.path.basename(newDaystatefile.replace('.csv',''))#set new Table name
#            if not os.path.exists(os.path.join(outLocation, newTable)):
#                arcpy.TableToTable_conversion(newDaystatefile, outLocation, newTable) #import csvfile to geodatabase
#            arcpy.AddMessage("Add new csv to gdb")
#            print("Add new csv to gdb")   
#            sdd=splitDatabyDay() 
#            pehsa = patternEHSA()
#            cpdf = combinePatternCount()
        
        mergefc=mergeFeatureClasses()
        arcpy.AddMessage("Combine Pattern Count")
        print("Combine Pattern Count") 
        createFinalFC
#            nDstatefile.close()#close file   
    except:
        getTraceback()
