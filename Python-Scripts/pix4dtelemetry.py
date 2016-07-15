# -*- coding: utf-8 -*-
"""
Created on Wed April 02 17:07:13 2016

@author: Kalyan

Creation Pix4Dtelemetry from PH Telemetry
"""

import csv
import numpy

# Location of telemetry file
in_file = 'E:/Python_Learning/Exercise/telemetry.dat'
# Location of output telemetry file
out_telem = 'E:/Python_Learning/Exercise/Pix4DTelemetry.dat'

name,lat,lon,alt,yaw,pitch,roll = [],[],[],[],[],[],[]

# Reading telemetry file
with open(in_file, 'rb') as icsvfile:
    a = csv.reader(icsvfile, delimiter = '\t')
    for i, row in enumerate(a):
        if i > 1:
            name.append(row[0])
            lat.append(float(row[2]))
            lon.append(float(row[3]))
            alt.append(float(row[4]))
            yaw.append((numpy.pi/2)-float(row[12]))
            pitch.append(float(row[6]))
            roll.append(float(row[5]))

# Creating Pix4D Telemetry file
with open(out_telem, 'wb') as ocsvfile:
    a = csv.writer(ocsvfile)
    for j,k in enumerate(lon):
        a.writerow([name[j], lat[j], k, alt[j], yaw[j], pitch[j], roll[j]])
