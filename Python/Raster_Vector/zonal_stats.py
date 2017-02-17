# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 11:15:04 2016

@author: Kalyan

extraction of raster statistics to polygon vector (zonal statistics)
"""

from osgeo import gdal, ogr
import numpy as np


def extent_to_pixel_offsets(geotrans, extent):
    originX = geotrans[0]
    originY = geotrans[3]
    pixel_width = geotrans[1]
    pixel_height = geotrans[5]
    x1 = int((extent[0] - originX) / pixel_width)
    x2 = int((extent[1] - originX) / pixel_width) + 1

    y1 = int((extent[3] - originY) / pixel_height)
    y2 = int((extent[2] - originY) / pixel_height) + 1

    xsize = x2 - x1
    ysize = y2 - y1
    return (x1, y1, xsize, ysize)


def zonal_stats(shapefile, raster):
    in_ras = gdal.Open(raster) #Open raster
    in_band = in_ras.GetRasterBand(1) #Open raster band1
    ras_geotrans = in_ras.GetGeoTransform() #Get geotransform

    '''if nodata_value:
        nodata_value = float(nodata_value)
        in_band.SetNoDataValue(nodata_value)'''

    in_shp = ogr.Open(shapefile, 1)  #open to write stats
    assert(in_shp)
    in_lyr = in_shp.GetLayer(0) #Get layer of shapefile
    #Define fileds and create fields to write stats    
    field1, field2, field3, field4, field5, field6 = "MIN", "MAX", "MEAN", "STD", "SUM", "COUNT"
    fd1 = ogr.FieldDefn(field1)
    in_lyr.CreateField(fd1)
    fd2 = ogr.FieldDefn(field2)
    in_lyr.CreateField(fd2)
    fd3 = ogr.FieldDefn(field3)
    in_lyr.CreateField(fd3)
    fd4 = ogr.FieldDefn(field4)
    in_lyr.CreateField(fd4)
    fd5 = ogr.FieldDefn(field5)
    in_lyr.CreateField(fd5)
    fd6 = ogr.FieldDefn(field6)
    in_lyr.CreateField(fd6)

    mem_drv = ogr.GetDriverByName('Memory')
    driver = gdal.GetDriverByName('MEM')

    # Loop through vectors
    feat = in_lyr.GetNextFeature()
    while feat is not None:
        ras_offset = extent_to_pixel_offsets(ras_geotrans, feat.geometry().GetEnvelope())
        ras_array = in_band.ReadAsArray(*ras_offset)

        # calculate new geotransform of the feature subset
        new_geotrans = ((ras_geotrans[0] + (ras_offset[0] * ras_geotrans[1])),ras_geotrans[1],0.0,(ras_geotrans[3] + (ras_offset[1] * ras_geotrans[5])),0.0,ras_geotrans[5])          

        # Create a temporary vector layer in memory
        temp_shp = mem_drv.CreateDataSource('out')
        temp_layer = temp_shp.CreateLayer('poly', None, ogr.wkbPolygon)
        temp_layer.CreateFeature(feat.Clone())

        # Rasterize it
        temp_ras = driver.Create('', ras_offset[2], ras_offset[3], 1, gdal.GDT_Float32)
        temp_ras.SetGeoTransform(new_geotrans)
        gdal.RasterizeLayer(temp_ras, [1], temp_layer, burn_values=[1])
        rasterize_array = temp_ras.ReadAsArray()

        # Mask the source data array with our current feature
        masked = np.ma.MaskedArray(ras_array,mask=np.logical_not(rasterize_array))
        #Extract stats and write into shapefile
        val1 = float(masked.min())
        val2 = float(masked.max())
        val3 = float(masked.mean())
        val4 = float(masked.std())
        val5 = float(masked.sum())
        val6 = float(masked.count())

        feat.SetField(field1, val1)
        feat.SetField(field2, val2)
        feat.SetField(field3, val3)
        feat.SetField(field4, val4)
        feat.SetField(field5, val5)
        feat.SetField(field6, val6)
        in_lyr.SetFeature(feat)
        
        temp_ras = None
        temp_shp = None
        feat = in_lyr.GetNextFeature()
    
    #Close data
    in_shp = None
    in_ras = None

#in put shapefile
shapefile = "E:/Python_Learning/Exercise/Zonalstats/BGNIR_resample_clip.shp"
#input vector
raster = "E:/Python_Learning/Exercise/VI.tif"

zonal_stats(shapefile, raster)
