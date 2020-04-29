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
import matplotlib.pyplot as plt 
import sys
import traceback

#url = 'https://github.KSm/CSSEGISandData/KSVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_KSnfirmed_US.csv'
#Set Johns Hopkins github data urls
#COVIDRecovered= "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"
#COVIDDeaths = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
#COVIDConfirmed = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
COVIDUSConfirmed = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv"
COVIDUSDeaths = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv"
ans=''
states={"Alabama":"AL","Alaska":"AK","American Samoa":"AS","Arizona":"AZ","Arkansas":"AR","California":"CA","Colorado":"CO","Connecticut":"CT","Delaware":"DE","District of Columbia":"DC","Federated States of Micronesia":"FM","Florida":"FL","Georgia":"GA","Guam":"GU","Hawaii":"HI","Idaho":"ID","Illinois":"IL","Indiana":"IN","Iowa":"IA","Kansas":"KS","Kentucky":"KY","Louisiana":"LA","Maine":"ME","Marshall Islands":"MH","Maryland":"MD","Massachusetts":"MA","Michigan":"MI","Minnesota":"MN","Mississippi":"MS","Missouri":"MO","Montana":"MT","Nebraska":"NE","Nevada":"NV","New Hampshire":"NH","New Jersey":"NJ","New Mexico":"NM","New York":"NY","North Carolina":"NC","North Dakota":"ND","Northern Mariana Islands":"MP","Ohio":"OH","Oklahoma":"OK","Oregon":"OR","Palau":"PW","Pennsylvania":"PA","Puerto Rico":"PR","Rhode Island":"RI","South Carolina":"SC","South Dakota":"SD","Tennessee":"TN","Texas":"TX","Utah":"UT","Vermont":"VT","Virgin Islands":"VI","Virginia":"VA","Washington":"WA","West Virginia":"WV","Wisconsin":"WI","Wyoming":"WY"}
#x = input('Enter your State:')
#print('State: ' + x)
def read_from_url(v, timeout=0):
    try:
        ans = requests.get(v, proxies=urllib.request.getproxies())
        if ans.status_code == 200:
            return ans.text
    except Exception as e:
        print(e)
        return None
def plotTest(test,title):
    fig = plt.figure() 
    test[:].plot(figsize=(16,12),ylim=(0,sdfTMax),xlim=(0,len(test)))
    plt.legend( loc='upper right', borderaxespad=0., ncol=5) 
    plt.ylabel("Case accumulation")
    plt.xlabel('first Case` Day'+ firstCaseDay)
    plt.title(title)
    plt.show() 
#    plt.savefig(fname='D:/data/covid/plots/'+v+"COVID19Cases"+test.index[len(test)-1]+'.png',
#            dpi=150,
#            facecolor='w',
#            edgecolor='w',
#            orientation='landscape',
#            format = 'png',
#            transparent=False
#    )    
tdate=dt.datetime.strftime(dt.date.today(),'%Y%m%d')
fullDS = r"D:\data\covid\cases\covid19_"+tdate+".csv"
# stateDS = r"D:\data\covid\cases\\"+states[x]+"_time_series"+tdate+".csv"
# currDaystatefile=r"D:\data\covid\cases\\\\"+states[x]+"_covid_"+tdate+".csv"
# create plot folder if it does not exist
if __name__ == '__main__':   
    try:
        ans=read_from_url(COVIDUSConfirmed, timeout=0)
        test=ans.replace('\r','').replace('/','_')
        with open(fullDS,'w') as fileFull:
            fileFull.write(test) 
        fileFull.close() 
        df=pd.read_csv(fullDS,header=0) 
        for k,v in states.items():
            x='Colorado'
            stateDS = r"D:\data\covid\cases\\"+states[x]+"_time_series"+tdate+".csv"
            currDaystatefile=r"D:\data\covid\cases\\\\"+states[x]+"_covid_"+tdate+".csv"
            sdf=df[df['Province_State']==x] 
            if len(sdf) > 1:
                for col in range(sdf.columns.get_loc('Combined_Key')+1,len(sdf.columns)): 
                    if len(sdf[sdf.columns[col]].unique())>1: 
                        firstCaseDay= sdf.columns[col-1] 
                        if k =='Washington':
                            firstCaseDay= sdf.columns[col] 
                        break
                sdfT=sdf.T
                sdfTMax=0
                for col in range(0,len(sdfT.columns)):
                    if sdfT[sdfT.columns[col]][firstCaseDay:].max() > sdfTMax:
                        sdfTMax=sdfT[sdfT.columns[col]][firstCaseDay:].max()
                test=sdfT[firstCaseDay:]
                test.columns=sdfT.values[5]
                allC = len(test.columns) 
                tcols=[]
                for tcol in test.columns:
                    if len(test[tcol].unique())==1:
#                        print(x,tcol,len(test[tcol].unique()),test[tcol].unique())
                        tcols.append(tcol) 
                test.drop(columns=tcols,inplace=True)
                finalC = len(test.columns) 
                title = x + " COVID-19 Cases in " + str(finalC) + " of " + str(allC)+" Counties "+ dt.datetime.strftime(dt.date.today(),'%m/%d/%Y')
                plotTest(test,title) 
            break
    except:
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        # Concatenate information together concerning the error into a message string
        pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
        # Print Python error messages for use in Python / Python window
        print(pymsg)
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            