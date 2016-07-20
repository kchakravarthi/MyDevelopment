# -*- coding: utf-8 -*-
"""
Created on Wed Jul 20 10:35:39 2016

@author: Kalyan

Extraction of raster values to point vector shapefile
"""
from osgeo import gdal, ogr
import struct

#Input shapefile Location
in_shp = "E:/Python_Learning/Exercise/BGNIR_points.shp"
#Input raster file Location
in_raster = "E:/Python_Learning/Exercise/BGNIR.tif"


def ExtractPixelValue(in_shp, in_raster): 
    #Open Raster Layer    
    raster = gdal.Open(in_raster)
    raster_band = raster.GetRasterBand(1)
    geotransform = raster.GetGeoTransform()
    xmin = geotransform[0]
    ymax = geotransform[3]
    x_res = geotransform[1]
    y_res = geotransform[5]
    
    #Open Vector Layer
    shp=ogr.Open(in_shp,1)
    lyr=shp.GetLayer()
    new_field = ogr.FieldDefn('ras_val', ogr.OFTReal) # Add a field to store raster value
    lyr.CreateField(new_field)

    #Extracting pixel value of each point
    for feat in lyr:
        geom = feat.GetGeometryRef()
        x, y = geom.GetX(), geom.GetY()  #coordinates
        pixel_x = int((x - xmin) / x_res) #x pixel
        pixel_y = int((y - ymax) / y_res) #y pixel
        in_val = raster_band.ReadRaster(pixel_x, pixel_y, 1, 1, buf_type=gdal.GDT_Float32)
        pix_val = struct.unpack('f', in_val)
        val = pix_val[0]
        
        #Storing value to attribute table
        feat.SetField("ras_val", val)
        lyr.SetFeature(feat)
    
    #Closing of files
    shp = None
    raster = None
    
ExtractPixelValue(in_shp, in_raster)
