# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 17:07:13 2016

@author: Kalyan

Generation of NDVI image from PH BGNIR dataset (Band1: NIR, Band2: Green, Band3: Blue)
"""

from osgeo import gdal
import numpy as np

#input file location 
infile = "E:/Python_Learning/Exercise/BGNIR.tif"
#Open input file
data = gdal.Open(infile)
#output file location
outfile = "E:/Python_Learning/Exercise/GNDVI.tif"

band1 = data.GetRasterBand(1)
band2 = data.GetRasterBand(2)
band3 = data.GetRasterBand(3)

#Read as array
b1 = band1.ReadAsArray()
b2 = band2.ReadAsArray()
b3 = band3.ReadAsArray()
 
#Read array as float
b1 = b1.astype(np.float32)
b2 = b2.astype(np.float32)
b3 = b3.astype(np.float32)

#Calculate GNDVI
GNDVI = (b1-b2)/(b1+b2)

#Info for outfile creation
cols = data.RasterXSize
rows = data.RasterYSize
trans = data.GetGeoTransform()
proj = data.GetProjection()

#Creation of outfile
outdriver = gdal.GetDriverByName('GTiff')
outdata = outdriver.Create(outfile, cols, rows, 1, gdal.GDT_Float32)
outband = outdata.GetRasterBand(1)
outband.WriteArray(GNDVI)
outdata.SetGeoTransform(trans)
outdata.SetProjection(proj)


#close dataset
data = None
band1 = None
band2 = None
band3 = None
outdriver = None
outdata = None
outband = None
