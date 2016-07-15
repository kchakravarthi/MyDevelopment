# -*- coding: utf-8 -*-
"""
Created on Wed April 20 12:05:18 2016

@author: Kalyan

Creation of point and line shapefile from PH Telemetry
"""

import shapefile as shp
import csv
from osgeo import osr

# Location of telemetry file
in_file = 'E:/Python_Learning/Exercise/telemetry_1.dat'
# Location of output shapefile
out_point_file = 'E:/Python_Learning/Exercise/telemetry_point'
out_line_file = 'E:/Python_Learning/Exercise/telemetry_line'

name,lat,lon,alt = [],[],[],[]

# Reading telemetry file
with open(in_file, 'rb') as icsvfile:
    a = csv.reader(icsvfile, delimiter = '\t')
    for i, row in enumerate(a):
        if i > 1:
            name.append(row[0])
            lat.append(float(row[2]))
            lon.append(float(row[3]))
            alt.append(float(row[4]))

# Creating point shapefile
w = shp.Writer(shp.POINT)
w.field('Name')
w.field('LONG')
w.field('LAT')
w.field('ALT')

for j,k in enumerate(lon):
    w.point(k,lat[j])
    w.record(name[j],k,lat[j],alt[j])
 
w.save(out_point_file)

# Creating line shapefile
coords = []

for j,k in enumerate(lon):
    coords.append([k, lat[j]])

# Creating polyline shapefile            
w = shp.Writer(shp.POLYLINE)
w.field('Name')
w.line(parts = [coords])
w.record('FlightPath')
 
w.save(out_line_file)

#Assign projection to the shapefile
spatialRef = osr.SpatialReference()
spatialRef.ImportFromEPSG(4326)
spatialRef.MorphToESRI()
file1 = open(out_point_file + '.prj', 'w')
file2 = open(out_line_file + '.prj', 'w')
file1.write(spatialRef.ExportToWkt())
file2.write(spatialRef.ExportToWkt())
file1.close()
file2.close()
