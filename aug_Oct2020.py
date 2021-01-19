# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 12:55:48 2021

@author: me1vi
"""

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
def splitDatabyDay():
    try:
        newfolder = r"D:\data\covid\cases\aug_Oct2020"
        arcpy.env.workspace = r"D:\data\covid\cases\aug_Oct2020\aug_Oct2020.gdb"
        arcTables = arcpy.ListTables()# get list of tables
        coCounties = r"D:\data\covid\cases\aug_Oct2020\aug_Oct2020.gdb\ctyPrj" # variable for USA_Counties # variable for USA_Counties
        os.chdir(newfolder) # change the current working directory
        arcpy.AddMessage("arcTables "+str(arcTables))
        for tab in arcTables:
            field_names = [i.name for i in arcpy.ListFields(tab) if i.type != 'OID'] #Get field names
            cursor = arcpy.da.SearchCursor(tab, field_names)# Open a cursor to extract results from  table
            tdf = pd.DataFrame(data=[row for row in cursor],columns=field_names,dtype=int)# Create a pandas dataframe to display results
            for date in tdf.DATE.unique(): 
                tabtitle = os.path.join(newfolder,'cases'+date.strftime('%Y%m%d')+".csv")# Create title for daily csv
                tdf2 = tdf[tdf['DATE']<=date]   #create dataframe for daily data
                tdf2.to_csv(tabtitle,sep=',',index=None,header=1)  #Write daily data to daily csv
        arcpy.AddMessage("Create table for each day")
        print("Create table for each day")
        for root, dirs, files in os.walk(newfolder):
            fileGlob=glob.glob('*cases*.csv') #collect files with cases in title
            print(fileGlob)
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
                    arcpy.stpm.EmergingHotSpotAnalysis(netCDFTable, "COUNT_NONE_SPACE_TIME_NEIGHBORS", EHSA, "100 Kilometers", 7, None, "FIXED_DISTANCE", None, "ENTIRE_CUBE")
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
        arcpy.env.workspace = r"D:\data\covid\cases\aug_Oct2020\aug_Oct2020.gdb"
        newfolder = r"D:\data\covid\cases\aug_Oct2020"
        feature_classes = arcpy.ListFeatureClasses()
        df3= pd.DataFrame(columns=['GEONUM', 'CATEGORY', 'PATTERN','DATE'])
        for fc in feature_classes:
            if fc.title() !=('Ctyprj'):
                print(fc.title())
                fileDate=dt.datetime.strptime(fc[5:13],'%Y%m%d')
                field_names = [i.name for i in arcpy.ListFields(fc) if i.type != 'OID']
                # Open a cursor to extract results from stats table
                cursor = arcpy.da.SearchCursor(fc, field_names)
                # Create a pandas dataframe to display results
                df = pd.DataFrame(data=[row for row in cursor], columns=field_names,dtype=int) 
                df2=df[['GEONUM', 'CATEGORY', 'PATTERN']]
                df2['DATE'] = fileDate
                df3=df3.append(df2)
#        df3.rename(columns={"GEONUM": "FIPS"},inplace=True)
        patternCSV = os.path.join(newfolder,'patternEHSA'+tdate+".csv")
        df3.to_csv(patternCSV, sep = ',', index = None, header = 1)
        arcpy.TableToTable_conversion(patternCSV, arcpy.env.workspace, os.path.basename(patternCSV).replace('.csv','')) #Table To Table conversion
        return
    except:
        getTraceback()
#combinePatternCount 
def combinePatternCount():
    fileList = [];tsfileList = [];pdf2 = pd.DataFrame();tsdf2 = pd.DataFrame()   
    try:       
        tdate=dt.datetime.strftime(dt.date.today(),'%Y%m%d')
        newfolder = r"D:\data\covid\cases\aug_Oct2020"
        os.chdir(newfolder)
        for root, dirs, files in os.walk(newfolder):
            fileGlob = glob.glob('*pattern*.csv') #collect files with pattern in title
            for filename in fileGlob: # for file in fileGlob
                fileList.append(os.path.join(newfolder,filename) )
            break
        for root, dirs, files in os.walk(newfolder):
            tsfileGlob = glob.glob('*cases*.csv') #collect files with cases in title
            for tsfilename in tsfileGlob: # for file in fileGlob
                tsfileList.append(os.path.join(newfolder,tsfilename) )
            break
        print(fileList)
        for y in range(0,len(fileList)):
            pdf = pd.read_csv(fileList[y]) 
            pdf3=pdf[pdf['DATE']>=pdf.DATE.unique()[0]]
            pdf2 = pdf2.append(pdf3) 
        pdf2.to_csv(os.path.join(r"D:\data\covid\cases\aug_Oct2020","patternEHSA"+tdate+".csv"), sep = ',', index = None, header = 1)     
        
        print(tsfileList)
        for y in range(0,len(tsfileList)):
            tsdf = pd.read_csv(tsfileList[y]) 
            tsdf3=tsdf[tsdf.DATE>=pdf.DATE.unique()[0]]
            tsdf2 = tsdf2.append(tsdf3) 
        tsdf2.to_csv(os.path.join(r"D:\data\covid\cases\aug_Oct2020","time_series"+tdate+".csv"), sep = ',', index = None, header = 1)     
         
    except:
        getTraceback()
 
def setUpGlobalParameters(x,newfolder):
        arcpy.CreateFolder_management(r"D:\data\covid\\", "_"+tdate)#Create Folder 
        arcpy.CreateFileGDB_management(newfolder, "_"+tdate+".gdb")#Create FileGDB
        arcpy.AddMessage("Create Folder "+"Ugn"+tdate)
        arcpy.AddMessage("Create FileGDB "+"Ugn"+tdate)
        print("Create Folder "+"Ugn"+tdate)
        print("Create FileGDB "+"Ugn"+tdate)
fileList = [];tsfileList = [];pdf2 = pd.DataFrame();tsdf2 = pd.DataFrame()   
    
tdate=dt.datetime.strftime(dt.date.today(),'%Y%m%d')
fullDS = r"D:\data\covid\cases\aug_Oct2020\\"+"UgnAll_series"+tdate+".csv"
stateDS = r"D:\data\covid\cases\aug_Oct2020\\"+"Ugntime_series"+tdate+".csv"
currDaystatefile=os.path.join(r"D:\data\covid\cases\aug_Oct2020","_time_series"+tdate+".csv")
newgDf=pd.DataFrame(columns=['COUNTY','STATE','GEONUM','DATE','COUNT'])
newstateDF=pd.DataFrame(columns=['COUNTY','STATE','GEONUM','DATE','COUNT'])
fc=''
newtsdf=pd.DataFrame(columns=['STATE','COUNTY','GEONUM','DATE','PERDAY'])
if __name__ == '__main__':    
    try:
#        sdd=splitDatabyDay() 
#        pehsa = patternEHSA() 
#        cpdf = combinePatternCount()
        pdf = pd.read_csv(r'D:\data\covid\cases\aug_Oct2020\patternEHSA20210112.csv')
        tsdf = pd.read_csv(r'D:\data\covid\cases\aug_Oct2020\time_series20210112.csv')  
        newtsdf['DATE']=tsdf.DATE.str.replace(' 00:00:00','')
        newtsdf['STATE']=tsdf.STATE.to_frame()
        newtsdf['COUNTY' ]=tsdf.COUNTY.to_frame()
        newtsdf['PERDAY']=tsdf.PERDAY.to_frame()
        newtsdf['GEONUM']=tsdf.GEONUM.to_frame()
        newtsdf['DATE']=tsdf.DATE.str.replace(' 00:00:00','')
        newtsdf['PERDAY']=tsdf.PERDAY.to_frame()
        pdf=pdf.drop_duplicates() 
        newtsdf=tsdf.drop_duplicates() 
        new_df = pd.merge(newtsdf, pdf,  how='left', left_on=['GEONUM','DATE'], right_on=['GEONUM','DATE'])
        patternCount = os.path.join(r"D:\data\covid\cases\aug_Oct2020","patternCount.csv")
        new_df.to_csv(patternCount, sep = ',', index = None, header = 1)
        newtsdf.to_csv(os.path.join(r"D:\data\covid\cases\aug_Oct2020","time_series.csv"), sep = ',', index = None, header = 1)
        pdf.to_csv(os.path.join(r"D:\data\covid\cases\aug_Oct2020","patternEHSA.csv"), sep = ',', index = None, header = 1)
    except:
        getTraceback()
