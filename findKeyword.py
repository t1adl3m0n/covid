# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import os, os.path,glob 
folder=r'D:\data'
os.chdir(folder)
for root, dirs, files in os.walk(folder): 
    filenames =glob.glob(r'*.py')
    for filename in filenames:
        file=os.path.join(folder,filename)
        with open(file, 'r', encoding="utf-8") as infile:
            data= infile.readlines()
            for line in data:
                if line.find('fillna')==0:
                    print(file,line)
         
 