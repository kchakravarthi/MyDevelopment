# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 11:15:04 2016

@author: Kalyan

extraction of raster statistics to polygon vector (zonal statistics)
"""


from osgeo import gdal, ogr
#from osgeo.gdalconst import *
import numpy as np
#import sys
gdal.PushErrorHandler('CPLQuietErrorHandler')


def bbox_to_pixel_offsets(gt, bbox):
    originX = gt[0]
    originY = gt[3]
    pixel_width = gt[1]
    pixel_height = gt[5]
    x1 = int((bbox[0] - originX) / pixel_width)
    x2 = int((bbox[1] - originX) / pixel_width)

    y1 = int((bbox[3] - originY) / pixel_height)
    y2 = int((bbox[2] - originY) / pixel_height)

    xsize = x2 - x1
    ysize = y2 - y1
    return (x1, y1, xsize, ysize)

def zonal_stats(shapefile, raster, nodata_value=None, global_src_extent=False):
    in_ras = gdal.Open(raster)
    assert(in_ras)
    in_band = in_ras.GetRasterBand(1)
    ras_geo = in_ras.GetGeoTransform()

    if nodata_value:
        nodata_value = float(nodata_value)
        in_band.SetNoDataValue(nodata_value)

    in_shp = ogr.Open(shapefile, 1)  # TODO maybe open update if we want to write stats
    assert(in_shp)
    in_layer = in_shp.GetLayer(0)
    field1, field2, field3, field4, field5, field6 = "MIN", "MAX", "MEAN", "STD", "SUM", "COUNT"
    fd1 = ogr.FieldDefn(field1)
    in_layer.CreateField(fd1)
    fd2 = ogr.FieldDefn(field2)
    in_layer.CreateField(fd2)
    fd3 = ogr.FieldDefn(field3)
    in_layer.CreateField(fd3)
    fd4 = ogr.FieldDefn(field4)
    in_layer.CreateField(fd4)
    fd5 = ogr.FieldDefn(field5)
    in_layer.CreateField(fd5)
    fd6 = ogr.FieldDefn(field6)
    in_layer.CreateField(fd6)

    # create an in-memory numpy array of the source raster data
    # covering the whole extent of the vector layer
    if global_src_extent:
        # use global source extent
        src_offset = bbox_to_pixel_offsets(ras_geo, in_layer.GetExtent())
        src_array = in_band.ReadAsArray(*src_offset)

        # calculate new geotransform of the layer subset
        new_gt = ((ras_geo[0] + (src_offset[0] * ras_geo[1])), ras_geo[1], 0.0,(ras_geo[3] + (src_offset[1] * ras_geo[5])), 0.0, ras_geo[5])

    mem_drv = ogr.GetDriverByName('Memory')
    driver = gdal.GetDriverByName('MEM')

    # Loop through vectors
#    stats = []
    feat = in_layer.GetNextFeature()
    while feat is not None:

        if not global_src_extent:
            # use local source extent
            src_offset = bbox_to_pixel_offsets(ras_geo, feat.geometry().GetEnvelope())
            src_array = in_band.ReadAsArray(*src_offset)

            # calculate new geotransform of the feature subset
            new_gt = ((ras_geo[0] + (src_offset[0] * ras_geo[1])),ras_geo[1], 0.0, (ras_geo[3] + (src_offset[1] * ras_geo[5])),0.0, ras_geo[5])

        # Create a temporary vector layer in memory
        temp_shp = mem_drv.CreateDataSource('out')
        temp_layer = temp_shp.CreateLayer('poly', None, ogr.wkbPolygon)
        temp_layer.CreateFeature(feat.Clone())

        # Rasterize it
        temp_data = driver.Create('', src_offset[2], src_offset[3], 1, gdal.GDT_Float32)
        temp_data.SetGeoTransform(new_gt)
        gdal.RasterizeLayer(temp_data, [1], temp_layer, burn_values=[1])
        rv_array = temp_data.ReadAsArray()

        # Mask the source data array with our current feature
        # we take the logical_not to flip 0<->1 to get the correct mask effect
        # we also mask out nodata values explictly
        masked = np.ma.MaskedArray(src_array, mask=np.logical_or(src_array == nodata_value, np.logical_not(rv_array)))        
        val1 = float(masked.min())
        val2 = float(masked.max())
        val3 = float(masked.mean())
        val4 = float(masked.std())
        val5 = float(masked.sum())
        val6 = float(masked.count())
#   print val1, val2, val3, val4
        feat.SetField(field1, val1)
        feat.SetField(field2, val2)
        feat.SetField(field3, val3)
        feat.SetField(field4, val4)
        feat.SetField(field5, val5)
        feat.SetField(field6, val6)
        in_layer.SetFeature(feat)

        temp_data = None
        temp_shp = None
        feat = in_layer.GetNextFeature()


    in_shp = None
    in_ras = None
#    return stats
    
shapefile = "E:/Python_Learning/Exercise/Zonalstats/BGNIR_resample_clip.shp"
raster = "E:/Python_Learning/Exercise/VI.tif"

zonal_stats(shapefile, raster, nodata_value=None, global_src_extent=False)
