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
 
x=''
#x = arcpy.GetParameterAsText(0) 
#arcpy.AddMessage('State: ' + x)
#print('State: ' + x)

def splitDatabyDay():
    try:
        
        newfolder =os.path.join( r"D:\data\covid","ctyPrj_"+tdate)
        arcpy.env.workspace = r'D:\data\covid\ctyPrj_20210101\ctyPrj_20210101.gdb'
        arcTables = arcpy.ListTables()# get list of tables
        coCounties = r"D:\data\covid\MyProject.gdb\ctyPrj" # variable for USA_Counties
        os.chdir(newfolder) # change the current working directory
        arcpy.AddMessage("arcTables "+str(arcTables))
        print("arcTables "+str(arcTables))
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
                    arcpy.stpm.CreateSpaceTimeCubeDefinedLocations(coCounties, netCDFTable, "GEONUM", "NO_TEMPORAL_AGGREGATION", "DATE", "1 Days", "END_TIME", None, "PERDAY ZEROS", None, relTable, "GEONUM")
#                    arcpy.stpm.CreateSpaceTimeCubeDefinedLocations("ctyPrj", r"D:\data\covid\ctyPrj_20210101\cases20200601.nc", "GEONUM", "NO_TEMPORAL_AGGREGATION", "DATE", "1 Days", "END_TIME", None, "PERDAY ZEROS", None, r"D:\data\covid\ctyPrj_20210101\ctyPrj_20210101.gdb\Jun_Dec_perDay", "GEONUM")
                    
                    arcpy.AddMessage("Create Space Time Cube Defined Locations "+gdbTable )
                    print("Create Space Time Cube Defined Locations "+gdbTable )
                    #Create Emerging Hot Spot Analysis
                    #arcpy.stpm.EmergingHotSpotAnalysis(r"D:\data\covid\USA_Counties_WM_Project.nc", "PERDAY_NONE_ZEROS", r"D:\data\MyProject.gdb\USA_Counties_WM_Project_EmergingHotSpotAnalysis", "100 Kilometers", 1, None, "FIXED_DISTANCE", None, "ENTIRE_CUBE")
                    arcpy.stpm.EmergingHotSpotAnalysis(netCDFTable, "PERDAY_NONE_ZEROS", EHSA, "100 Kilometers", 1, None, "FIXED_DISTANCE", None, "ENTIRE_CUBE")
                    arcpy.AddMessage("Create Emerging Hot Spot Analysis "+gdbTable)
                    print("Create Emerging Hot Spot Analysis "+gdbTable)
                except: 
                    print(netCDFTable)
                    getTraceback()
        return
    except:
        getTraceback()
def patternEHSA():
    try:
        arcpy.env.workspace = r'D:\data\covid\ctyPrj_20210101\ctyPrj_20210101.gdb'
        feature_classes = arcpy.ListFeatureClasses()
        df3= pd.DataFrame(columns=['GEONUM', 'CATEGORY', 'PATTERN','DATE'])
        for fc in feature_classes:
            fileDate=dt.datetime.strptime(fc[5:13],'%Y%m%d')
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
def combinePatternCount():
    fileList = [];tsfileList = [];pdf2 = pd.DataFrame();tsdf2 = pd.DataFrame()   
    try:       
        tdate=dt.datetime.strftime(dt.date.today(),'%Y%m%d')
        newfolder =os.path.join( r"D:\data\covid","ctyPrj_"+tdate)
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


# Create  date 
tdate=dt.datetime.strftime(dt.date.today(),'%Y%m%d')
ans=''
gdbTable=''
if __name__ == '__main__':    
    try:
        newfolder =os.path.join( r"D:\data\covid","ctyPrj_"+tdate)
        if not os.path.exists(newfolder):
            arcpy.CreateFolder_management(r"D:\data\covid","ctyPrj_"+tdate)#Create Folder 
            arcpy.CreateFileGDB_management(newfolder,"ctyPrj_"+tdate+".gdb")#Create FileGDB
        fullDS = r"D:\data\covid\Jun_Dec_perDay.csv" # full dataset down load from raw.githubusercontent.com
        outLocation = os.path.join(newfolder, "ctyPrj_"+tdate+".gdb")#set outlocation for table
        newTable=os.path.basename(fullDS.replace('.csv',''))#set new Table name
        if not os.path.exists(os.path.join(outLocation, newTable)):
            arcpy.TableToTable_conversion(fullDS, outLocation, newTable) #import csvfile to geodatabase
        arcpy.AddMessage("Add "+newTable+" to gdb")
        print("Add "+newTable+"  to gdb")   
        sdd=splitDatabyDay() 
        pehsa = patternEHSA()
#        cpdf = combinePatternCount()
#        mergefc=mergeFeatureClasses()
    except:
        getTraceback()