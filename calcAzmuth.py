# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 13:00:45 2020

@author: me1vi
"""

import arcpy
import pyproj
import pyproj
geodesic = pyproj.Geod(ellps='WGS84')
############ getAz ##############
def getAz(lons1,lats1,lats2,lons2):
    fwd_azimuth,back_azimuth,distance = geodesic.inv(lons1,lats1,lats2,lons2) 
    return fwd_azimuth
#D:\data\oats\oats\oats.gdb
#shipTracks
arcpy.env.workspace = r'D:\data\oats\oats\oats.gdb'
fc = r'D:\data\oats\oats\oats.gdb\shipTracks'
fields = ['minlat','minlon','maxlat','maxlon','Azimuth']
 
#expression = "geodesic.inv(!minlat!,!minlon!,!maxlat!,!maxlon!)"
# Create update cursor for feature class 

 
############ AddField ##############
with arcpy.da.UpdateCursor(fc, fields) as cursor:
    ############ Calculate Azimuth ##############
    for row in cursor:
         lons1 =row[0]
         lats1 =row[1]
         lats2 =row[2]
         lons2 =row[3]
         fwd_azimuth=getAz(lons1,lats1,lats2,lons2)
         if  fwd_azimuth < 0:
             fwd_azimuth=360+fwd_azimuth 
         print(int(fwd_azimuth)) 
         row[4] =int(fwd_azimuth)
         cursor.updateRow(row)