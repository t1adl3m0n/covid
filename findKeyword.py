# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import os, os.path,glob 
folder=r'D:\data\covid\MyProject'
for root, dirs, files in os.walk(folder):
    print(files)
    break
#        filenames =glob.glob(r'*.r')
#        for filename in filenames:
#            file=os.path.join(folder,filename)
#            with open(file, 'r', encoding="utf-8") as infile:
#                data= infile.readlines()
#                for line in data:
#                    if line.find('ggplot'):
#                        print(file,line)
#            break
 