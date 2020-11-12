# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 13:39:45 2020

@author: me1vi
"""
# importing all the required modules
import PyPDF2
import pandas as pd
import numpy as np
# creating an object 
df = pd.read_csv("D:/data/covid/pivotColorado_COVID19.csv")
df.head()
pd.pivot(df,index=["COUNTY"],values=['18-Mar', '19-Mar', '20-Mar', '21-Mar', '22-Mar', '23-Mar',
       '24-Mar', '25-Mar', '26-Mar', '27-Mar', '28-Mar', '29-Mar'])