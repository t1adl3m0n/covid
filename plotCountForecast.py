# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 09:15:40 2020

@author: me1vi
"""
import matplotlib.pyplot as plt 
import sys 
import pandas as pd
import traceback
import random
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
def getTraceback():
    # Get the traceback object
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0] 
    # Concatenate information together concerning the error into a message string
    pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
    print(pymsg)
 
def getColorMap(df): 
    colorlist=[]
    rgbColor=[(1,1,1)] 
    for color in range(0,len(df.METHOD.unique())):
        for value in range(0,len(rgbColor)): 
            break
        nextColor=(random.randrange(0, 253, 1)/ 255., random.randrange(0, 253, 1)/ 255., random.randrange(0, 253, 1)/ 255.)
        colorlist.append(nextColor) 
    return colorlist 
 
colorList=[]
newCols = ['OBJECTID', 'GEONUM','2020-11-01','2020-11-02','2020-11-03','2020-11-04','2020-11-05','2020-11-06','2020-11-07','2020-11-08','2020-11-09','2020-11-10','2020-11-11','2020-11-12','2020-11-13','2020-11-14','2020-11-15','2020-11-16','2020-11-17','2020-11-18','2020-11-19','2020-11-20','2020-11-21','2020-11-22','2020-11-23','2020-11-24','2020-11-25','2020-11-26','2020-11-27','2020-11-28','2020-11-29','2020-11-30', 'METHOD']

pco = pd.read_csv('D:/data/covid/patternCount20201031.csv')
pcn = pd.read_csv('D:/data/covid/patternCount20201130.csv')
tso = pd.read_csv('D:/capstone/data/time_series20201031.csv')
tsn = pd.read_csv('D:/capstone/data/time_series20201130.csv')
cff = pd.read_csv('D:/capstone/data/cff.csv')
esf = pd.read_csv('D:/capstone/data/esf.csv')
fbf = pd.read_csv('D:/capstone/data/fbf.csv')
newfolder="D:/capstone/data/"
if __name__ == '__main__':    
    try: 
        fc=cff.append(esf)
        fc=fc.append(fbf)
        fc.DATE=pd.to_datetime(fc.DATE, errors='raise', dayfirst=False, yearfirst=True, utc=None, format=None, exact=True, unit=None, infer_datetime_format=False, origin='unix', cache=True)
 
        pc=pco.append(pcn)
        pc.DATE=pd.to_datetime(pc.DATE, errors='raise', dayfirst=False, yearfirst=True, utc=None, format=None, exact=True, unit=None, infer_datetime_format=False, origin='unix', cache=True)
        cff.DATE=pd.to_datetime(cff.DATE, errors='raise', dayfirst=False, yearfirst=True, utc=None, format=None, exact=True, unit=None, infer_datetime_format=False, origin='unix', cache=True)
        esf.DATE=pd.to_datetime(esf.DATE, errors='raise', dayfirst=False, yearfirst=True, utc=None, format=None, exact=True, unit=None, infer_datetime_format=False, origin='unix', cache=True)
        fbf.DATE=pd.to_datetime(fbf.DATE, errors='raise', dayfirst=False, yearfirst=True, utc=None, format=None, exact=True, unit=None, infer_datetime_format=False, origin='unix', cache=True)
        colorList=getColorMap(fc)# Get color for each METHOD to be displayed in plot
        plt.figure(figsize=(12, 14)) 
        ax = plt.subplot(111)     
        for GEONUM in pltPC.GEONUM.unique():  
            pltFC=fc[fc['GEONUM']==GEONUM]
            cffFC=cff[cff['GEONUM']==GEONUM]
            esfFC=esf[esf['GEONUM']==GEONUM]
            fbfFC=fbf[fbf['GEONUM']==GEONUM]
            pltPC=pc[pc['GEONUM']==GEONUM]
            print(GEONUM)
            plt.plot(pltPC[pltPC.GEONUM==GEONUM].DATE,    
                    pltPC[pltPC.GEONUM==GEONUM].COUNT,    
                    lw=2.5, color="Black")
            ax.plot(cffFC.DATE, cffFC.COUNT, color='tab:purple')
            ax.plot(esfFC.DATE, esfFC.COUNT, color='tab:orange')
            ax.plot(fbfFC.DATE, fbfFC.COUNT, color='tab:green')
            ## Add a text label to the right end of every line. Most of the code below    
            # is adding specific offsets y position because some labels overlapped.
            cffFCpos = cffFC[cffFC.GEONUM==GEONUM][-1:].COUNT - 0.5 
            esfFCpos = esfFC[esfFC.GEONUM==GEONUM][-1:].COUNT - 0.5 
            fbfFCpos = fbfFC[fbfFC.GEONUM==GEONUM][-1:].COUNT - 0.5 
            y_pos = pc[pc.GEONUM==GEONUM][-1:].COUNT - 0.5 
            x_pos = plt.xlim(pc.DATE.min(), pc.DATE.max())[1]
            # Again, make sure that all labels are large enough to be easily read    
            # by the viewer.     
            plt.text(x_pos,cffFCpos, cffFC.METHOD.values[0], fontsize=14, color="purple")  
            plt.text(x_pos,esfFCpos, esfFC.METHOD.values[0], fontsize=14, color="orange")  
            plt.text(x_pos,fbfFCpos, fbfFC.METHOD.values[0], fontsize=14, color="green")  
            plt.text(x_pos,y_pos, 'True Count', fontsize=14, color="Black")    
            plt.show()
            break
#        # matplotlib's title() call centers the title on the plot, but not the graph,    
#        # so I used the text() call to customize where the title goes.    
#          
#        # Make the title big enough so it spans the entire plot, but don't make it    
#        # so big that it requires two lines to show.    
#          
#        # Note that if the title is descriptive enough, it is unnecessary to include    
#        # axis labels; they are self-evident, in this plot's case.    
#        plt.text(pltPC.DATE.mean(), pltPC.COUNT.max(), "New Confirmed COVID-19 cases "+str(pltPC.DATE.min())[:10]+" to "+str(pltPC.DATE.max())[:10], fontsize=17, ha="center")    

    except:
         getTraceback()