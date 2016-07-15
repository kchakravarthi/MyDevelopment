# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 10:04:13 2016

@author: Kalyan

Generation of vi image from PH BGNIR dataset (Band1: NIR, Band2: Green, Band3: Blue)
"""

from osgeo import gdal
import numpy as np

#Vegetation Index Type ENDVI/GDVI/GNDVI/GSAVI
veg_index = raw_input('VI Type(ENDVI/GDVI/GNDVI/GSAVI):')
#input file location 
infile = "E:/Python_Learning/Exercise/BGNIR.tif"
data = gdal.Open(infile)
#output file location
outfile = "E:/Python_Learning/Exercise/VI.tif"

band1 = data.GetRasterBand(1)
band2 = data.GetRasterBand(2)
band3 = data.GetRasterBand(3)

#Read as array
nir = band1.ReadAsArray()
green = band2.ReadAsArray()
blue = band3.ReadAsArray()
 
#Read array as float
nir = nir.astype(np.float32)
green = green.astype(np.float32)
blue = blue.astype(np.float32)

#Info for outfile creation
cols = data.RasterXSize
rows = data.RasterYSize
trans = data.GetGeoTransform()
proj = data.GetProjection()

#Vegetation Index Calculation
if veg_index == "ENDVI":
    vi = (((nir + green) - 2 * blue)/((nir + green) + 2 * blue))
    w = 1
    
elif veg_index == "GNDVI":
    vi = ((nir - green)/(nir + green))
    w = 1
    
elif veg_index == "GSAVI":
    vi = (((nir - green)/(nir + green + 0.5)) * 1.5)
    w = 1

elif veg_index == "GDVI":
    vi = (nir - green)
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
