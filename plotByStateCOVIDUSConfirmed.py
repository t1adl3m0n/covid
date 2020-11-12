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
x='Colorado'
#x = arcpy.GetParameterAsText(0)
#prjShapefile = arcpy.GetParameterAsText(1)
#arcpy.AddMessage(x+','+prjShapefile)
def read_from_url(COVIDUSConfirmed, timeout=0):
    try:
        ans = requests.get(COVIDUSConfirmed, proxies=urllib.request.getproxies())
        if ans.status_code == 200:
            return ans.text
    except Exception as e:
        print(e)
        return None
tdate=dt.datetime.strftime(dt.date.today(),'%Y%m%d')
fullDS = r"D:\data\covid\cases\\"+states[x]+"_All_series"+tdate+".csv"
stateDS = r"D:\data\covid\cases\\"+states[x]+"_time_series"+tdate+".csv"
currDaystatefile=os.path.join(r"D:\data\covid\cases",states[x]+"_time_series"+tdate+".csv")
if __name__ == '__main__':    
    #read URL 
    ans=read_from_url(COVIDUSConfirmed, timeout=0)
    test=ans.replace('\r','').replace('/','_')
    with open(fullDS,'w') as fileFull:
        fileFull.write(test) 
    fileFull.close() 
    df=pd.read_csv(fullDS) 
    stateDF=df[df['Province_State']==x] 
    currDay=stateDF.columns[-1]
    currDaystateDF=stateDF[stateDF[currDay]>0]  
    countMax =0
    newDF=pd.DataFrame(columns= ['COUNTY', 'STATE', 'FIPS', 'DATE', 'COUNT'])
    for col in range(currDaystateDF.columns.get_loc('Combined_Key')+1,len(currDaystateDF.columns)):
        if len(currDaystateDF[currDaystateDF.columns[col]].unique())>1: 
            firstCaseDay= currDaystateDF.columns[col]  
            break
        if currDaystateDF[currDaystateDF.columns[col]].unique().max() > countMax:
            countMax=currDaystateDF[currDaystateDF.columns[col]].unique().max() 
    with open(currDaystatefile,'w') as cDstatefile:
        cDstatefile.write("COUNTY,STATE,FIPS,DATE,COUNT\n")
        for row in range(0,len(currDaystateDF)): 
            for col in range(currDaystateDF.columns.get_loc(firstCaseDay),len(currDaystateDF.columns)):  
                newRow=currDaystateDF.Admin2.values[row]+','+str(currDaystateDF.Province_State.fillna(value='None').values[row])+','+"{}{}".format(10,str(int(currDaystateDF.FIPS.values[row])))+','+currDaystateDF.columns[col]+','+str(currDaystateDF.iloc[row,col])
                #(int(newRow[-1]) > 0) and 
                if (newRow.split(',')[0] != 'None') and (newRow.split(',')[0] != 'Unassigned') and (newRow.split(',')[0] != re.match('^Out of',newRow.split(',')[0])):
#                    print(newRow) 
#                    arcpy.AddMessage(newRow) 
                    newDF=newDF.append(pd.DataFrame([newRow])) 
                    cDstatefile.write(newRow)
                    cDstatefile.write('\n')
cDstatefile.close()
# Execute TableToTable
currTable = os.path.basename(currDaystatefile.replace('.csv',''))
outLocation = r'D:\data\covid\MyProject\MyProject.gdb'
arcpy.TableToTable_conversion(currDaystatefile, outLocation, currTable) 

#addTable
aprx = arcpy.mp.ArcGISProject("CURRENT")
addTab = arcpy.mp.Table(os.path.join(outLocation, currTable))
m = aprx.listMaps("Map*")[0]
m.addTable(addTab) 