# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 11:04:57 2020

@author: me1vi
"""


import requests
import urllib.request
import os, time
import datetime as dt
import glob
import traceback
import pandas as pd
import matplotlib.pyplot as plt 
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import random
import sys
from sklearn.cluster import KMeans
def getTraceback():
    # Get the traceback object
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0] 
    # Concatenate information together concerning the error into a message string
    pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
#    msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n" 
    # Return python error messages for use in script tool or Python window
#    arcpy.AddError(pymsg)
#    arcpy.AddError(msgs) 
    # Print Python error messages for use in Python / Python window
    print(pymsg)
#    print(msgs)    
def getColorMap(df): 
    colorlist=[]
    rgbColor=[(1,1,1)] 
    for color in range(0,len(df.state.unique())):
        for value in range(0,len(rgbColor)): 
            break
        nextColor=(random.randrange(0, 253, 1)/ 255., random.randrange(0, 253, 1)/ 255., random.randrange(0, 253, 1)/ 255.)
        colorlist.append(nextColor) 
    return colorlist 
def read_from_url(COVIDUSConfirmed, timeout=0):
    try:
        ans = requests.get(COVIDUSConfirmed, proxies=urllib.request.getproxies()) #Download data from URL
        if ans.status_code == 200:
            return ans.text
    except:
        getTraceback()
import os
import platform

def creation_date(path_to_file):
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    """
    if platform.system() == 'Windows':
        return os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return stat.st_mtime
def plotIncrease(df):  
    try:    
        plt.figure(figsize=(12, 14))    
        # Remove the plot frame lines. They are unnecessary chartjunk.   
        ax = plt.subplot(111)    
        ax.spines["top"].set_visible(False)    
        ax.spines["bottom"].set_visible(True)    
        ax.spines["right"].set_visible(False)    
        ax.spines["left"].set_visible(True)    
        
        # Ensure that the axis ticks only show up on the bottom and left of the plot.    
        # Ticks on the right and top of the plot are generally unnecessary chartjunk.    
        ax.get_xaxis().tick_bottom()    
        ax.get_yaxis().tick_left()    
          
        # Limit the range of the plot to only where the data is.    
        # Avoid unnecessary whitespace.    
        plt.ylim(0, df.deathIncrease.max())    
        plt.xlim(ndf.hospitalizedIncrease.min(), ndf.hospitalizedIncrease.max())    
          
        # Make sure your axis ticks are large enough to be easily read.    
        # You don't want your viewers squinting to read your plot.    
        plt.yticks(fontsize=14)    
        plt.xticks(fontsize=14)    
        # Remove the tick marks; they are unnecessary with the tick lines we just plotted.    
        plt.tick_params(axis="both", which="both", bottom="off", top="off",    
                        labelbottom="on", left="off", right="off", labelleft="on")    
          
        # Now that the plot is prepared, it's time to actually plot the data!    
        # Note that I plotted the majors in order of the highest % in the final year.    
        #majors = df.CATEGORY.unique()    
        # colorList[rank]=(random.randrange(0, 253, 1)/ 255., random.randrange(0, 253, 1)/ 255., random.randrange(0, 253, 1)/ 255.)
        # Plot each line separately with its own color, using the Tableau 20    
        # color set in order.    
        plt.scatter(df.date,df.positive,label=ndf.date, lw=2.5)    
        # Add a text label to the right end of every line. Most of the code below    
        # is adding specific offsets y position because some labels overlapped.
        y_pos = ndf.hospitalizedIncrease- 0.5 
        x_pos = ndf.deathIncrease- 0.5 
        # Again, make sure that all labels are large enough to be easily read    
        # by the viewer.     
        plt.text(x_pos,y_pos, ndf.date, fontsize=14)#  
        
        # matplotlib's title() call centers the title on the plot, but not the graph,    
        # so I used the text() call to customize where the title goes.    
              
        plt.title( file.split('history')[0].upper()+" Hospitalizations vs Deaths ".upper(), fontsize=17, ha="center")    
    except:
        getTraceback()     
def getDailyReports():  
    try:      
        capstoneStates=["Colorado","Kansas","Missouri","Nebraska","Oklahoma"]#
        for state in capstoneStates:
            stHist="https://covidtracking.com/data/download/"+state.lower()+"-history.csv"
            ans = requests.get(stHist, proxies=urllib.request.getproxies()) #Download data from URL
            if ans.status_code == 200:
                stateDS = os.path.join(r'D:/data/covid/',os.path.basename(stHist).replace('-h','h'))
                with open(stateDS,'w') as fileFull: #Save text string  to csv file
                    fileFull.write(ans.text)         
    except:
        getTraceback()  
    
os.chdir(r'D:\data\covid')
fileGlob = glob.glob('*history.csv') 
df=pd.DataFrame()
if __name__ == '__main__':  
    try: 
        if len(fileGlob) == 0:
            getDailyReports()
        for file in fileGlob:     
            hfile=os.path.join(r'D:\data\covid',file)  
            rc = pd.read_csv(hfile)
            df=df.append(rc,ignore_index=True)
        print(file,df.state.unique())
        colorList=getColorMap(df)
        df.date=pd.to_datetime(df.date, errors='raise', dayfirst=False, yearfirst=True, utc=None, format=None, exact=True, unit=None, infer_datetime_format=False, origin='unix', cache=True)
        df[['date','deathIncrease', 'hospitalizedIncrease']]=df[['date','deathIncrease', 'hospitalizedIncrease']].fillna(value=0)
        df[['positiveIncrease']]=df[['positiveIncrease']].astype('int')

        sdf=df.sort_values(by='date')
        d = dt.datetime.today() - dt.timedelta(days=90)
        ndf=sdf[(sdf.date>d ) & (sdf.positiveIncrease >0)]
        plt.figure(figsize=(12, 14))    
        # Remove the plot frame lines. They are unnecessary chartjunk.   
        ax = plt.subplot(111)    
        ax.spines["top"].set_visible(False)    
        ax.spines["bottom"].set_visible(True)    
        ax.spines["right"].set_visible(False)    
        ax.spines["left"].set_visible(True)    
        for rank, column in enumerate(df.state.unique()):  
            # colorList[rank]=(random.randrange(0, 253, 1)/ 255., random.randrange(0, 253, 1)/ 255., random.randrange(0, 253, 1)/ 255.)
            # Plot each line separately with its own color, using the Tableau 20    
            # color set in order.    
            plt.scatter(ndf[ndf.state==column].date,    
                    ndf[ndf.state==column].positiveIncrease,    
                    lw=2.5, color=colorList[rank])    
            # Add a text label to the right end of every line. Most of the code below    
            # is adding specific offsets y position because some labels overlapped.
            y_pos = ndf[ndf.state==column][-1:].positiveIncrease - 0.5 
            x_pos = plt.xlim(ndf.date.min(), ndf.date.max())[1]
            # Again, make sure that all labels are large enough to be easily read    
            # by the viewer.     
            plt.text(x_pos,y_pos, column, fontsize=14, color=colorList[rank])    
            x=enumerate(ndf.date)
            y=ndf.positiveIncrease
            kdf={'x':enumerate(ndf.date),'y':ndf.positiveIncrease}
            c
            centroids = kmeans.cluster_centers_
            print(centroids)
            
            plt.scatter(df['x'], df['y'], c= kmeans.labels_.astype(float), s=50, alpha=0.5)
            plt.scatter(centroids[:, 0], centroids[:, 1], c='red', s=50)
            plt.show()
    except:
        getTraceback()   