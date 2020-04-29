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
import re
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import scipy.stats as stats
import sys

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
def read_from_url(v, timeout=0):
    try:
        ans = requests.get(v, proxies=urllib.request.getproxies())
        if ans.status_code == 200:
            return ans.text
    except Exception as e:
        print(e)
        return None
def transpose(df):
    sdf=df[df['Province_State']==x] 
    for col in range(sdf.columns.get_loc('Combined_Key')+1,len(sdf.columns)): 
        if len(sdf[sdf.columns[col]].unique())>1: 
            firstCaseDay= sdf.columns[col]  
            break
    sdfT=sdf.T
    sdfTMax=0
    for col in range(0,len(sdfT.columns)):
        if sdfT[sdfT.columns[col]][firstCaseDay:].max() > sdfTMax:
            sdfTMax=sdfT[sdfT.columns[col]][firstCaseDay:].max()
    test=sdfT[firstCaseDay:].astype('int')
    test.columns=sdfT.values[5]
    return test
def pmf(test):#Probability Mass Function
    n,bins,patches = plt.hist(test[test.columns[col]], bins='auto', density=False, facecolor='red', alpha=.5, edgecolor="k")
    plt.title(str(test.columns[col])+' Probability Mass Function')
    plt.show()  
def pdf(test):#Probability Density Functions
    mu = test[test.columns[col]].mean()
    sigma = test[test.columns[col]].std()
    
    # In pixels on a computer screen, continuous rendering is in the
    # eye of the beholder -- below we are just computing and then plotting higher resolution curve points
    
    # Generate the x-axis data for fine-grained rendering (0.1 x-axis step size) over acceleration values from 5 to 25
    x = np.arange(test[test.columns[col]].min(),test[test.columns[col]].max(),test[test.columns[col]].std())
    
    # Calculate and plot a normal distribution Probability Density Function or PDF
    y = stats.norm.pdf(x, mu, sigma)  # Alternate: y = stats.norm.pdf(x, mu, sigma)
    
    n2,bins2,patches2 = plt.hist(test[test.columns[col]], bins='auto', density=True, facecolor='blue', alpha=.5, edgecolor="blue")
    plt.plot(x,y,'y-')
    plt.title(str(test.columns[col])+' Normal Probability Density Function')
    plt.xlabel(str(test.columns[col])+" Confirmed Cases")
    plt.show()    
def cdf(test):#cumulative Density Functions
    plt.figure(figsize=(10, 5)) 
    
    # Subplot (m,n,X) below sets up an m = 1 row x n = 2 column grid of plots
    # and then X is used to select the plot number 
    
    plt.subplot(1,2,1)  # Select plot #1 
    plt.hist(test[test.columns[col]], bins='auto', density=True, facecolor='blue', label='PMF', edgecolor="k")
    
    plt.title(str(test.columns[col])+' Normal Probability Density Function')
    plt.xlabel("Horsepower")
    plt.ylabel("Probability")
    plt.legend(loc='upper left')
    
    plt.subplot(1,2,2) # Select plot #2
    n, bins, patches = plt.hist(test[test.columns[col]], bins='auto', density=True, 
                                facecolor='blue', edgecolor="k",
                                cumulative=True,  # NOTE we are specifying cumulative = True to 
                                                  # accumulate the counts in the histogram bins
                                label='Discrete CDF')
    
    plt.title(str(test.columns[col])+' Discrete CDF')
    plt.xlabel("Horsepower")
    plt.ylabel("Probability")
    plt.legend(loc='upper left')
    
    plt.show()
    
def Continuouscdf(test):#cumulative Density Functions
    plt.figure(figsize=(15, 5)) 
    # The next two lines use NumPy to compute a simple mean and 
    # standard deviation from the data column for acceleration
    mu = test[test.columns[col]].mean()
    sigma = test[test.columns[col]].std()
    # Subplot (m,n,X) below sets up an m = 1 row x n = 2 column grid of plots
    # and then X is used to select the plot number 
    plt.subplot(1,2,1) # Select plot #1
    plt.hist(test[test.columns[col]], bins='auto', density=True, facecolor='blue', label='Probability Mass Function', alpha=.25, edgecolor="k")
    # In pixels on a computer screen, continuous rendering is in the
    # eye of the beholder -- below we are just computing and then plotting higher resolution curve points
    # Generate the x-axis data for fine-grained rendering over acceleration values from 5 to 25
    x = np.arange(test[test.columns[col]].min(),test[test.columns[col]].max(),0.1)   # Notice this a 0.1 x-axis step size!  Look for a '/10' normalizer later
    # Plot a normal distribution: "Probability Density Function"
    apdf = stats.norm.pdf(x, mu, sigma)
    # Use the mlab library to generate a plot from the descriptive statistics
             # the Y-value will be the curve values generated 
             # from bin edges and the decsriptive statistics
            
    plt.plot(x, apdf,'r-',label='Estimated Normal Curve')  # \n is a line feed; see effect in plot legend below
    plt.xlabel(test.columns[col])
    plt.ylabel("Probability Mass Function Probability")
    plt.legend(loc='upper left')
    plt.title('Estimated Normal Curve from Descriptive Statistics')
    plt.subplot(1,2,2)  # Select plot #2
    n, bins, patches = plt.hist(test[test.columns[col]], bins='auto', density=True, alpha=.25, edgecolor="k",
                                facecolor='blue', 
                                cumulative=True,  # NOTE, we are specifying cumulative = True to 
                                                  # accumulate the counts in the bins
                                label='Discrete CDF')
    x = np.arange(test[test.columns[col]].min(),test[test.columns[col]].max(),0.1)   # Notice this a 0.1 x-axis step size!  Look for a '/10' normalizer later
    
    # Plot a Cumulative Distribution Function at 10X resolution
                                      # cumsum() converts a series of values to a cumulative sum
                                      # which is what a CDF is
                                               
    acdf = stats.norm.pdf(x, mu, sigma).cumsum()/10  # The '/10' normalizes the 0.1 x-axis step size of the bins
    plt.plot(x, acdf,'r-',label='Continuous CDF')
    plt.xlabel(test.columns[col])
    plt.ylabel("CDF Probability")
    plt.legend(loc='upper left')
    plt.title('Continuous CDF Generated from Descriptive Statistics')
    plt.show()
    
    
    
tdate=dt.datetime.strftime(dt.date.today(),'%Y%m%d')
fullDS = r"D:\data\covid\cases\covid19_"+tdate+".csv"
stateDS = r"D:\data\covid\cases\\"+states[x]+"_time_series"+tdate+".csv"
currDaystatefile=r"D:\data\covid\cases\\\\"+states[x]+"_covid_"+tdate+".csv"
if __name__ == '__main__':   
#    ans=read_from_url(COVIDUSConfirmed, timeout=0)
#    test=ans.replace('\r','').replace('/','_')
#    with open(fullDS,'w') as fileFull:
#        fileFull.write(test) 
#    fileFull.close() 
    df=pd.read_csv(fullDS,header=0) 
    test=transpose(df)
#    for col in range(0,len(test.columns)):
##        try:
#            if test[test.columns[col]].max()>0:
#                print(test.columns[col])
##                pmf(test)#Probability Mass Function
##                pdf(test)#Probability Density Functions
#                Continuouscdf(test)
##        except:  
##            e = sys.exc_info()[1]
##            print(e.args[0])  
##        break        
                
                
                
                