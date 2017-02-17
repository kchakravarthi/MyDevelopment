# -*- coding: utf-8 -*-
"""
Created on Wed Mar 02 17:07:13 2016

@author: Kalyan

Creation of flightpath pdf file from PH Telemetry 
"""

import csv
from pylab import *
import matplotlib.pyplot as plt
import numpy as np

#Location of telemetry file
in_file = 'E:/Python_Learning/Exercise/telemetry_1.dat'
#Location of output file
out_file = 'E:/Python_Learning/Exercise/flightpath.pdf'

name,lat,lon,alt = [],[],[],[]

#Reading telemetry file
with open(in_file, 'rb') as icsvfile:
    a = csv.reader(icsvfile, delimiter = '\t')
    for i, row in enumerate(a):
        if i > 1:
            name.append(row[0])
            lat.append(float(row[2]))
            lon.append(float(row[3]))
            alt.append(float(row[4]))

x, y = [], []
x = lon
y = lat

#Plotting of telemetry cordinates as points and line
fig = plt.figure()    
#Plotting of points and line
plt.scatter(x,y,color="red", s=8)
plt.plot(x,y,color="blue", linewidth=1.0, linestyle="-")
#Rounding to 3 decimal
rxmin = round(min(x),3)
rxmax = round(max(x),3)
rymin = round(min(y),3)
rymax = round(max(y),3)
#Scale
plt.xlim(rxmin - 0.001, rxmax + 0.001)
plt.ylim(rymin - 0.001, rymax + 0.001)
#Lables
xnums = np.arange(rxmin, rxmax, round((rxmax - rxmin)/5,3))
ynums = np.arange(rymin, rymax, round((rymax - rymin)/5,3))
plt.ticklabel_format(useOffset=False, style='plain')
xlbls = [ str(i) for i in xnums ]
xticks(xnums, xlbls, rotation=0)
ylbls = [ str(i) for i in ynums ]
yticks(ynums, ylbls, rotation=0)
xlabel('LONGITUDE') ; ylabel('LATITUDE')
title('Flight Path')
#Saving of plot to pdf
savefig(out_file, fmt='pdf', dpi=100, bbox_inches='tight')
plt.show()
