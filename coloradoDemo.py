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
  
if __name__ == '__main__':   
    df=pd.read_csv('D:/data/covid/countyDemographics.csv',header=0) 
    for x in df[['Diabetes', 'Flu_Vax', 'Health_Ins', 'Heart_Dise', 'Obesity_Co', 'No_Physica', 'Frequent_P']]:
        df[x.upper()]=df.pop1418/df[x]
    