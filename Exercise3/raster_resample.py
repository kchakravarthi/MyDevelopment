# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 11:52:31 2016

@author: Kalyan

Raster resample
"""

from osgeo import gdal
from gdalconst import *


def RasterResample(in_file, out_file, pixel_size):
    
    in_data = gdal.Open(in_file, GA_ReadOnly) #Read input raster file
    in_band = in_data.GetRasterBand(1) #Read first band
    data_type = in_band.DataType #Data type of input raster
    bands = in_data.RasterCount #no. of Raster bands
    geotrans = in_data.GetGeoTransform() #Geotransformation of input raster
    proj = in_data.GetProjection() #Projection information of input raster
    in_cols = in_data.RasterXSize #input raster columns
    in_rows = in_data.RasterYSize #input raster rows
    in_xsize = geotrans[1] #x pixel size
    in_ysize = geotrans[5] #y pixel size
    xmin = geotrans[0] #Upper Left x
    ymax = geotrans[3] #Upper left y
    
    out_cols = int((in_cols * in_xsize)/pixel_size) #output raster cols
    out_rows = int((in_rows * abs(in_ysize)/pixel_size)) #output raster rows
        
    out_geotrans=(xmin, pixel_size, 0, ymax, 0, -pixel_size) #output geotransformation
    
    out_drv = gdal.GetDriverByName('GTiff') #Output driver
    out_data = out_drv.Create(out_file, out_cols, out_rows, bands , data_type) #output raster creation
    out_data.SetGeoTransform(out_geotrans) #Assigning geotransformation to output raster
    out_data.SetProjection(proj) #Assigning projection to output raster
    gdal.ReprojectImage(in_data, out_data, None, None, gdal.GRA_NearestNeighbour) #Resampling
    
    #Closing of data
    in_data = None   
    out_data = None

#input raster location
in_file = "E:/Python_Learning/Exercise/VI.tif"
#output raster location
out_file = "E:/Python_Learning/Exercise/VI_resample.tif"
#Resampling pixel size
pixel_size = 2

RasterResample(in_file, out_file, pixel_size)
