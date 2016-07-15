# -*- coding: utf-8 -*-
"""
Created on Wed Mar 02 15:31:42 2016

@author: Kalyan

Creation of Flight Plan shapefile from PH mission.dat
"""

import shapefile as shp
import csv
from osgeo import osr

# Location of mission file
in_file = 'E:/Python_Learning/Exercise/mission.dat'
# Location of output shapefile
out_file = 'E:/Python_Learning/Exercise/FlightPlan'

name,lat,lon = [],[],[]

# Reading mission file
with open(in_file, 'rb') as icsvfile:
    a = csv.reader(icsvfile, delimiter = ' ')
    for i, row in enumerate(a):
        if i > 206:
            lat.append(float(row[2]))
            lon.append(float(row[1]))

coords = []
for j,k in enumerate(lon):
    coords.append([k, lat[j]])
    
# Creating polygon shapefile            
w = shp.Writer(shp.POLYGON)
w.field('Name')
w.poly(parts=[coords])
w.record('FlightPlan')
w.save(out_file)

#Assign projection to the shapefile
spatialRef = osr.SpatialReference()
spatialRef.ImportFromEPSG(4326)
spatialRef.MorphToESRI()
file = open(out_file + '.prj', 'w')
file.write(spatialRef.ExportToWkt())
file.close()
