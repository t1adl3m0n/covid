# -*- coding: utf-8 -*-
"""
Created on Wed May 13 14:09:00 2020

@author: me1vi
"""
import os 
import pandas as pd
import datetime as dt
import re
import traceback
import sys 
import matplotlib.pyplot as plt 
import random

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
    for color in range(0,len(df.COUNTY.unique())):
        for value in range(0,len(rgbColor)): 
            break
        nextColor=(random.randrange(0, 253, 1)/ 255., random.randrange(0, 253, 1)/ 255., random.randrange(0, 253, 1)/ 255.)
        colorlist.append(nextColor) 
    return colorlist 

def plotCasesCOUNT(df):  
    try: 
        df.DATE=pd.to_datetime(df.DATE, errors='raise', dayfirst=False, yearfirst=True, utc=None, format=None, exact=True, unit=None, infer_datetime_format=False, origin='unix', cache=True)

        plt.figure(figsize=(12, 14))    
        # Remove the plot frame lines. They are unnecessary chartjunk.    
        ax = plt.subplot(111)    
        ax.spines["top"].set_visible(False)    
        ax.spines["bottom"].set_visible(False)    
        ax.spines["right"].set_visible(False)    
        ax.spines["left"].set_visible(False)    
        
        # Ensure that the axis ticks only show up on the bottom and left of the plot.    
        # Ticks on the right and top of the plot are generally unnecessary chartjunk.    
        ax.get_xaxis().tick_bottom()    
        ax.get_yaxis().tick_left()    
          
        # Limit the range of the plot to only where the data is.    
        # Avoid unnecessary whitespace.    
        plt.ylim(0, df.COUNT.max())    
        plt.xlim(df.DATE.min(), df.DATE.max())    
          
        # Make sure your axis ticks are large enough to be easily read.    
        # You don't want your viewers squinting to read your plot.    
        plt.yticks(range(0, df.COUNT.max(), 50), [str(x)  for x in range(0, df.COUNT.max(), 50)], fontsize=14)    
        plt.xticks(fontsize=14)    
          
        # Provide tick lines across the plot to help your viewers trace along    
        # the axis ticks. Make sure that the lines are light and small so they    
        # don't obscure the primary data lines.    
        for y in range(10, 91, 10):    
            plt.plot(range(1968, 2012), [y] * len(range(1968, 2012)), "--", lw=0.5, color="black", alpha=0.3)    
          
        # Remove the tick marks; they are unnecessary with the tick lines we just plotted.    
        plt.tick_params(axis="both", which="both", bottom="off", top="off",    
                        labelbottom="on", left="off", right="off", labelleft="on")    
          
        # Now that the plot is prepared, it's time to actually plot the data!    
        # Note that I plotted the majors in order of the highest % in the final year.    
#        majors = df.COUNTY.unique()    
        for rank, column in enumerate(df.COUNTY.unique()):  
            # colorList[rank]=(random.randrange(0, 253, 1)/ 255., random.randrange(0, 253, 1)/ 255., random.randrange(0, 253, 1)/ 255.)
            # Plot each line separately with its own color, using the Tableau 20    
            # color set in order.    
            plt.scatter(df[df.COUNTY==column].DATE,    
                    df[df.COUNTY==column].COUNT,    
                    lw=2.5, color=colorList[rank])    
            # Add a text label to the right end of every line. Most of the code below    
            # is adding specific offsets y position because some labels overlapped.
            y_pos = df[df.COUNTY==column][-1:].COUNT - 0.5 
            x_pos = plt.xlim(df.DATE.min(), df.DATE.max())[1]
            # Again, make sure that all labels are large enough to be easily read    
            # by the viewer.     
            plt.text(x_pos,y_pos, column, fontsize=14, color=colorList[rank])    
           
        # matplotlib's title() call centers the title on the plot, but not the graph,    
        # so I used the text() call to customize where the title goes.    
          
        # Make the title big enough so it spans the entire plot, but don't make it    
        # so big that it requires two lines to show.    
          
        # Note that if the title is descriptive enough, it is unnecessary to include    
        # axis labels; they are self-evident, in this plot's case.    
        plt.text(df.DATE.mean(), df.COUNT.max(),cgn+ " New Confirmed COVID-19 cases "+str(df.DATE.min())[:10]+" to "+str(df.DATE.max())[:10], fontsize=17, ha="center")    

    except:
        getTraceback()        


def plotCasesCATEGORY(df):  
    try:    
        df.DATE=pd.to_datetime(df.DATE, errors='raise', dayfirst=False, yearfirst=True, utc=None, format=None, exact=True, unit=None, infer_datetime_format=False, origin='unix', cache=True)

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
        plt.ylim(0, df.CATEGORY.max())    
        plt.xlim(df.DATE.min(), df.DATE.max())    
          
        # Make sure your axis ticks are large enough to be easily read.    
        # You don't want your viewers squinting to read your plot.    
        plt.yticks(range(0, df.CATEGORY.max(), 1), [str(x)  for x in range(0, df.CATEGORY.max(), 1)], fontsize=14)    
        plt.xticks(fontsize=14)    
          
       
        # Remove the tick marks; they are unnecessary with the tick lines we just plotted.    
        plt.tick_params(axis="both", which="both", bottom="off", top="off",    
                        labelbottom="on", left="off", right="off", labelleft="on")    
          
        # Now that the plot is prepared, it's time to actually plot the data!    
        # Note that I plotted the majors in order of the highest % in the final year.    
        #majors = df.CATEGORY.unique()    
        for rank, column in enumerate(df.COUNTY.unique()):  
            # colorList[rank]=(random.randrange(0, 253, 1)/ 255., random.randrange(0, 253, 1)/ 255., random.randrange(0, 253, 1)/ 255.)
            # Plot each line separately with its own color, using the Tableau 20    
            # color set in order.    
            plt.scatter(df.DATE,    
                    df.CATEGORY,    
                    lw=2.5, color=colorList[rank])    
            # Add a text label to the right end of every line. Most of the code below    
            # is adding specific offsets y position because some labels overlapped.
            y_pos = df[df.COUNTY==column][-1:].CATEGORY - 0.5 
            x_pos = plt.xlim(df.DATE.min(), df.DATE.max())[1]
            # Again, make sure that all labels are large enough to be easily read    
            # by the viewer.     
            plt.text(x_pos,y_pos, column, fontsize=14, color=colorList[rank])#  
           
        # matplotlib's title() call centers the title on the plot, but not the graph,    
        # so I used the text() call to customize where the title goes.    
          
        # Make the title big enough so it spans the entire plot, but don't make it    
        # so big that it requires two lines to show.    
          
        # Note that if the title is descriptive enough, it is unnecessary to include    
        # axis labels; they are self-evident, in this plot's case.    
        plt.text( cgn+" New Confirmed COVID-19 cases "+str(df.DATE.min())[:10]+" to "+str(df.DATE.max())[:10], fontsize=17, ha="center")    

    except:
        getTraceback()        
        
cdf = pd.read_csv('D:/data/covid/patternCount20200929.csv')
adf= pd.read_csv(r'D:\data\covid\CO_20200929\CO_All_series20200929.csv')
sdf=adf[['FIPS','Province_State','Lat','Long_']]
colorList=getColorMap(cdf)# Get color for each county to be displayed in plot
capstoneStates=["Colorado","Kansas","Missouri","Nebraska","Oklahoma"]#
             
if __name__ == '__main__':    
    try: 
#        lldf=sdf[sdf["Province_State"].isin(capstoneStates)]#get lat long for each county from source data
#        mdf=cdf.merge(lldf,left_on='GEONUM', right_on='FIPS')#merge source data lat long with dataset
#        mdf.drop(columns=['FIPS','Province_State'],inplace=True)#drop duplicate columns
#        mdf.loc[mdf['COUNT']<0, ['COUNT']]=0
#        mdf.to_csv(r'D:\data\covid\casesLLAll20200929.csv')
        for cgn in cdf.STATE.unique():
            print(cgn)#
            df=cdf[cdf['STATE']==cgn] 
            tdf=df[df.DATE>'2020-07-01']
            plotCasesCOUNT(tdf)
            plotCasesCATEGORY(tdf)
#            break
    except:  
        getTraceback()        
        
        
        