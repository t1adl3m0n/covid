# -*- coding: utf-8 -*-
"""
Created on Fri Jan  8 09:17:16 2021

@author: me1vi
"""
import os
import requests
import urllib.request
import pandas as pd
import datetime as dt
import re
import arcpy
import sys
import glob 

pdf = pd.read_csv(r'D:\data\covid\cases\aug_Oct2020\patternEHSA20210108.csv')
tsdf = pd.read_csv(r'D:\data\covid\cases\aug_Oct2020\cases20201031.csv')  
pdf=pdf.drop_duplicates() 
tsdf=tsdf.drop_duplicates() 
new_df = pd.merge(tsdf, pdf,  how='left', left_on=['GEONUM','DATE'], right_on=['GEONUM','DATE'])
patternCount = os.path.join(r"D:\data\covid\cases\aug_Oct2020","patternCount.csv")
new_df.to_csv(patternCount, sep = ',', index = None, header = 1)
tsdf.to_csv(os.path.join(r"D:\data\covid\cases\aug_Oct2020","time_series.csv"), sep = ',', index = None, header = 1)
pdf.to_csv(os.path.join(r"D:\data\covid\cases\aug_Oct2020","patternEHSA.csv"), sep = ',', index = None, header = 1)