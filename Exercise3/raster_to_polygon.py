# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 21:45:32 2016

@author: Kalyan

Raster to polygon vector
"""

from osgeo import gdal, ogr, osr
import os

def RastertoPolygon(in_file, out_file):
    in_data = gdal.Open(in_file) #open input raster
    in_band = in_data.GetRasterBand(1) #get raster band
    proj = in_data.GetProjection() #get projection
    
    # create output shape file
    out_driver = ogr.GetDriverByName('ESRI Shapefile') 
    if os.path.exists(out_file):
        out_driver.DeleteDataSource(out_file)
    out_srs = osr.SpatialReference(wkt=proj)

    out_ds = out_driver.CreateDataSource(out_file)
    out_layer = out_ds.CreateLayer(out_file, out_srs, ogr.wkbPolygon)
    newField = ogr.FieldDefn('Value') #Define new field for data values
    out_layer.CreateField(newField) #create field
    gdal.Polygonize(in_band, None, out_layer, 0, [], callback=None) #gdal polygonize to write vector
    
    #closing of files    
    out_ds.Destroy()
    in_data = None

#input raster file
in_file = 'E:/Python_Learning/Exercise/BGNIR_resample.tif'
#output shape file
out_file = 'E:/Python_Learning/Exercise/BGNIR_resample.shp'

RastertoPolygon(in_file, out_file)
