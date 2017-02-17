# -*- coding: utf-8 -*-
"""
Created on Fri Apr 25 14:21:13 2016

@author: Kalyan

Generation of VI image from RGNIR dataset (Band1: NIR, Band2: Red, Band3: Green)
"""

from osgeo import gdal
import numpy as np

#Vegetation Index Type NDVI/DVI/SAVI/OSAVI
veg_index = raw_input('VI Type(NDVI/DVI/SAVI/OSAVI):')
#input file location 
infile = "E:/Python_Learning/Exercise/RGNIR.tif"
data = gdal.Open(infile)
#output file location
outfile = "E:/Python_Learning/Exercise/VI.tif"

band1 = data.GetRasterBand(1)
band2 = data.GetRasterBand(2)
band3 = data.GetRasterBand(3)

#Read as array
nir = band1.ReadAsArray()
red = band2.ReadAsArray()
green = band3.ReadAsArray()
 
#Read array as float
nir = nir.astype(np.float32)
red = red.astype(np.float32)
green = green.astype(np.float32)

#Info for outfile creation
cols = data.RasterXSize
rows = data.RasterYSize
trans = data.GetGeoTransform()
proj = data.GetProjection()

#Vegetation Index Calculation
if veg_index == "NDVI":
    vi = ((nir - red)/(nir + red))
    w = 1
    
elif veg_index == "SAVI":
    vi = (((nir - red)/(nir + red + 0.5)) * 1.5)
    w = 1
    
elif veg_index == "OSAVI":
    vi = ((nir - red)/(nir + red + 0.16))
    w = 1

elif veg_index == "DVI":
    vi = (nir - red)
    w = 1

else:
    w = 0

#Creation of outfile
if w == 1:
    outdriver = gdal.GetDriverByName('GTiff')
    outdata = outdriver.Create(outfile, cols, rows, 1, gdal.GDT_Float32)
    outband = outdata.GetRasterBand(1)
    outband.WriteArray(vi)
    outdata.SetGeoTransform(trans)
    outdata.SetProjection(proj)
else:
    print 'Not available'


#close dataset
data = None
band1 = None
band2 = None
band3 = None
outdriver = None
outdata = None
outband = None
