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
import sys
import traceback
def getTraceback():
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0] 
    pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
    print(pymsg)
states={"Alabama":"AL","Alaska":"AK","American Samoa":"AS","Arizona":"AZ","Arkansas":"AR","California":"CA","Colorado":"CO","Connecticut":"CT","Delaware":"DE","District of Columbia":"DC","Federated States of Micronesia":"FM","Florida":"FL","Georgia":"GA","Guam":"GU","Hawaii":"HI","Idaho":"ID","Illinois":"IL","Indiana":"IN","Iowa":"IA","Kansas":"KS","Kentucky":"KY","Louisiana":"LA","Maine":"ME","Marshall Islands":"MH","Maryland":"MD","Massachusetts":"MA","Michigan":"MI","Minnesota":"MN","Mississippi":"MS","Missouri":"MO","Montana":"MT","Nebraska":"NE","Nevada":"NV","New Hampshire":"NH","New Jersey":"NJ","New Mexico":"NM","New York":"NY","North Carolina":"NC","North Dakota":"ND","Northern Mariana Islands":"MP","Ohio":"OH","Oklahoma":"OK","Oregon":"OR","Palau":"PW","Pennsylvania":"PA","Puerto Rico":"PR","Rhode Island":"RI","South Carolina":"SC","South Dakota":"SD","Tennessee":"TN","Texas":"TX","Utah":"UT","Vermont":"VT","Virgin Islands":"VI","Virginia":"VA","Washington":"WA","West Virginia":"WV","Wisconsin":"WI","Wyoming":"WY"}
dataCol=['Confirmed', 'Deaths', 'Recovered', 'Active', 'Incident_Rate', 'People_Tested', 'People_Hospitalized','Mortality_Rate', 'Testing_Rate', 'Hospitalization_Rate']
df = pd.read_csv(r'C:\Users\me1vi\Documents\psds\dailyReports.csv', index_col="Day")
os.rename(r'C:\Users\me1vi\Documents\psds\dailyReports.csv',r'C:\Users\me1vi\Documents\psds\dailyReportsOld.csv')
fullDS = r'C:\Users\me1vi\Documents\psds\dailyReports.csv'# full dataset down load from raw.githubusercontent.com
if __name__ == '__main__':    
    try:
        newDF=pd.DataFrame()
        for state in states:
            print('State: ' + state)
            sdf=df[df['Province_State']==state]
            tdf=sdf.T
            tdfRows = tdf.index
            tdf2=pd.DataFrame(index=tdf.index,columns=tdf.columns)
            for row in dataCol:
                for col in range(0,len(tdf.columns)):
                    if (tdf.values[tdf.index.get_loc(row)][col] > tdf.values[tdf.index.get_loc(row)][col-1]):
                        newValue=tdf.values[tdf.index.get_loc(row)][col]-tdf.values[tdf.index.get_loc(row)][col-1]
                        tdf2.values[tdf2.index.get_loc(row)][col]=newValue
                    else:
                        tdf2.values[tdf2.index.get_loc(row)][col]=tdf.values[tdf.index.get_loc(row)][col]
            for name in tdf.index:
                for col in range(0,len(tdf.columns)):
                        if name not in dataCol:
                             tdf2.values[tdf.index.get_loc(name)][col]=tdf.values[tdf.index.get_loc(name)][col] 
            sdf2=tdf2.T 
            newDF = newDF.append(sdf2)
        newDF.to_csv(fullDS, sep=',',index="Day")
    except:
        getTraceback()
        
        