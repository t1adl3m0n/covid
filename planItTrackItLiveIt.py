# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
import pandas as pd
import csv
dbFile = r'C:\Users\me1vi\Documents\planIttrackItLiveIt\BFPD_csv_07132018\Nutrients.csv'
with open(dbFile, mode='r') as csvfile:
    dbreader = pd.read_csv(csvfile, delimiter = ',')
    for line in dbreader:
        print(line)
        break
    