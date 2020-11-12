# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 08:53:13 2020

@author: me1vi
"""
import os
import datetime as dt
import pandas as pd
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
states={"Alabama":"AL","Alaska":"AK","American Samoa":"AS","Arizona":"AZ","Arkansas":"AR","California":"CA","Colorado":"CO","Connecticut":"CT","Delaware":"DE","District of Columbia":"DC","Federated States of Micronesia":"FM","Florida":"FL","Georgia":"GA","Guam":"GU","Hawaii":"HI","Idaho":"ID","Illinois":"IL","Indiana":"IN","Iowa":"IA","Kansas":"KS","Kentucky":"KY","Louisiana":"LA","Maine":"ME","Marshall Islands":"MH","Maryland":"MD","Massachusetts":"MA","Michigan":"MI","Minnesota":"MN","Mississippi":"MS","Missouri":"MO","Montana":"MT","Nebraska":"NE","Nevada":"NV","New Hampshire":"NH","New Jersey":"NJ","New Mexico":"NM","New York":"NY","North Carolina":"NC","North Dakota":"ND","Northern Mariana Islands":"MP","Ohio":"OH","Oklahoma":"OK","Oregon":"OR","Palau":"PW","Pennsylvania":"PA","Puerto Rico":"PR","Rhode Island":"RI","South Carolina":"SC","South Dakota":"SD","Tennessee":"TN","Texas":"TX","Utah":"UT","Vermont":"VT","Virgin Islands":"VI","Virginia":"VA","Washington":"WA","West Virginia":"WV","Wisconsin":"WI","Wyoming":"WY"}
capstoneStates={"Colorado":"CO","Kansas":"KS","Missouri":"MO","Nebraska":"NE","Oklahoma":"OK"}#"Colorado":"CO"
fileList = []
tsfileList = []
pdf2 = pd.DataFrame()
tsdf2 = pd.DataFrame()
tdate=dt.datetime.strftime(dt.date.today(),'%Y%m%d')
#df.DATE.unique()[len(df.DATE.unique())-90]
if __name__ == '__main__':    
    try:
        for x in capstoneStates:
            dfName=states[x]
            tdate=dt.datetime.strftime(dt.date.today(),'%Y%m%d')
            newfolder = os.path.join( r"D:\data\covid",states[x]+"_"+tdate)
            os.chdir(newfolder)
            df2 = pd.DataFrame()
            for root, dirs, files in os.walk(newfolder):
                fileGlob = glob.glob('*pattern*.csv') #collect files with cases in title
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
        pdf2.to_csv(os.path.join(r"D:\data\covid","EHSApattern"+tdate+".csv"), sep = ',', index = None, header = 1)     
        for y in range(0,len(tsfileList)):
            tsdf = pd.read_csv(tsfileList[y]) 
            tsdf3=tsdf[tsdf.DATE>=pdf.DATE.unique()[0]]
            tsdf2 = tsdf2.append(tsdf3)
        tsdf2.to_csv(os.path.join(r"D:\data\covid","time_series"+tdate+".csv"), sep = ',', index = None, header = 1)     
        new_df= pd.merge(tsdf2, pdf2,  how='left', on=['GEONUM','DATE'])
        new_df.dropna(inplace=True)
        new_df.to_csv(os.path.join(r"D:\data\covid","patternCount"+tdate+".csv"), sep = ',', index = None, header = 1)
        
    except:
        getTraceback()     
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        