# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 09:15:40 2020

@author: me1vi
"""
import os
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
    for color in range(0,len(df.COUNTY.unique())):
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
cff = pd.read_csv('D:/capstone/data/capstoneStates_CFF.csv')
esf = pd.read_csv('D:/capstone/data/capstoneStates_ESF.csv')
fbf = pd.read_csv('D:/capstone/data/capstoneStates_FBF.csv')
newfolder="D:/capstone/data/"
cfffile=os.path.join(newfolder,"cff.csv")# new cases by day for a state
esffile=os.path.join(newfolder,"esf.csv")# new cases by day for a state
fbffile=os.path.join(newfolder,"fbf.csv")# new cases by day for a state
if __name__ == '__main__':    
    try: 
        cff = cff.rename(columns={'FCAST_1':'2020-11-01','FCAST_2':'2020-11-02','FCAST_3':'2020-11-03','FCAST_4':'2020-11-04','FCAST_5':'2020-11-05','FCAST_6':'2020-11-06','FCAST_7':'2020-11-07','FCAST_8':'2020-11-08','FCAST_9':'2020-11-09','FCAST_10':'2020-11-10','FCAST_11':'2020-11-11','FCAST_12':'2020-11-12','FCAST_13':'2020-11-13','FCAST_14':'2020-11-14','FCAST_15':'2020-11-15','FCAST_16':'2020-11-16','FCAST_17':'2020-11-17','FCAST_18':'2020-11-18','FCAST_19':'2020-11-19','FCAST_20':'2020-11-20','FCAST_21':'2020-11-21','FCAST_22':'2020-11-22','FCAST_23':'2020-11-23','FCAST_24':'2020-11-24','FCAST_25':'2020-11-25','FCAST_26':'2020-11-26','FCAST_27':'2020-11-27','FCAST_28':'2020-11-28','FCAST_29':'2020-11-29','FCAST_30':'2020-11-30'}, errors="raise")
        esf = esf.rename(columns={'FCAST_1':'2020-11-01','FCAST_2':'2020-11-02','FCAST_3':'2020-11-03','FCAST_4':'2020-11-04','FCAST_5':'2020-11-05','FCAST_6':'2020-11-06','FCAST_7':'2020-11-07','FCAST_8':'2020-11-08','FCAST_9':'2020-11-09','FCAST_10':'2020-11-10','FCAST_11':'2020-11-11','FCAST_12':'2020-11-12','FCAST_13':'2020-11-13','FCAST_14':'2020-11-14','FCAST_15':'2020-11-15','FCAST_16':'2020-11-16','FCAST_17':'2020-11-17','FCAST_18':'2020-11-18','FCAST_19':'2020-11-19','FCAST_20':'2020-11-20','FCAST_21':'2020-11-21','FCAST_22':'2020-11-22','FCAST_23':'2020-11-23','FCAST_24':'2020-11-24','FCAST_25':'2020-11-25','FCAST_26':'2020-11-26','FCAST_27':'2020-11-27','FCAST_28':'2020-11-28','FCAST_29':'2020-11-29','FCAST_30':'2020-11-30'}, errors="raise")
        fbf = fbf.rename(columns={'FCAST_1':'2020-11-01','FCAST_2':'2020-11-02','FCAST_3':'2020-11-03','FCAST_4':'2020-11-04','FCAST_5':'2020-11-05','FCAST_6':'2020-11-06','FCAST_7':'2020-11-07','FCAST_8':'2020-11-08','FCAST_9':'2020-11-09','FCAST_10':'2020-11-10','FCAST_11':'2020-11-11','FCAST_12':'2020-11-12','FCAST_13':'2020-11-13','FCAST_14':'2020-11-14','FCAST_15':'2020-11-15','FCAST_16':'2020-11-16','FCAST_17':'2020-11-17','FCAST_18':'2020-11-18','FCAST_19':'2020-11-19','FCAST_20':'2020-11-20','FCAST_21':'2020-11-21','FCAST_22':'2020-11-22','FCAST_23':'2020-11-23','FCAST_24':'2020-11-24','FCAST_25':'2020-11-25','FCAST_26':'2020-11-26','FCAST_27':'2020-11-27','FCAST_28':'2020-11-28','FCAST_29':'2020-11-29','FCAST_30':'2020-11-30'}, errors="raise")
        fbf=fbf.drop(columns=['Shape_Leng', 'Shape_Area'])
        esf=esf.drop(columns=['LOCATION','Shape_Leng','Shape_Area', 'Field'])
        with open(cfffile,'w') as nDstatefile: #open new csv file to write data to
            nDstatefile.write("COUNTY,STATE,GEONUM,DATE,METHOD,COUNT\n")# write headers
            for row in range(0,len(cff)): 
                pcRow=pcn[pcn.GEONUM==cff.GEONUM.iloc[row]]
                for col in cff.columns[2:32]: 
                    pcCounty = pcRow.values[0,1:4].tolist()
                    jRow = (',').join([col,cff.iloc[row,len(cff.columns)-1],str(int(cff[col][row]))])
                    pcCounty.append(jRow.split(','))
                    print(pcCounty)
                    nDstatefile.write(str(pcCounty))#write new row to file
                    nDstatefile.write('\n')#write carriage return
        nDstatefile.close()#close file 
        with open(esffile,'w') as nDstatefile: #open new csv file to write data to
            nDstatefile.write("COUNTY,STATE,GEONUM,DATE,METHOD,COUNT\n")# write headers
            for row in range(0,len(esf)): 
                pcRow=pcn[pcn.GEONUM==esf.GEONUM.iloc[row]]
                for col in esf.columns[2:32]: 
                    pcCounty = pcRow.values[0,1:4].tolist()
                    jRow = (',').join([col,esf.iloc[row,len(esf.columns)-1],str(int(esf[col][row]))])
                    pcCounty.append(jRow)
                    print(pcCounty)
                    nDstatefile.write(str(pcCounty))#write new row to file
                    nDstatefile.write('\n')#write carriage return
        nDstatefile.close()#close file 
        with open(fbffile,'w') as nDstatefile: #open new csv file to write data to
            nDstatefile.write("COUNTY,STATE,GEONUM,DATE,METHOD,COUNT\n")# write headers
            for row in range(0,len(fbf)): 
                pcRow=pcn[pcn.GEONUM==fbf.GEONUM.iloc[row]]
                for col in fbf.columns[2:32]: 
                    pcCounty = pcRow.values[0,1:4].tolist()
                    jRow = (',').join([col,fbf.iloc[row,len(fbf.columns)-1].split(';')[0],str(int(fbf[col][row]))])
                    pcCounty.append(jRow)
                    print(pcCounty)
                    nDstatefile.write(str(pcCounty))#write new row to file
                    nDstatefile.write('\n')#write carriage return
        nDstatefile.close()#close file 
    except:
         getTraceback()