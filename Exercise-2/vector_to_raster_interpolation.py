# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 10:28:41 2016

@author: Kalyan

To interpolate point vector data to raster
"""

from osgeo import gdal, ogr
import numpy as np
import matplotlib.mlab as ml
import scipy.interpolate as il #for method2, in case the matplotlib griddata method fails

#Input file Location
in_file = "E:/Python_Learning/Exercise/Sample_point_UTM.shp"
#Output file Location
out_raster = "E:/Python_Learning/Exercise/Raster.tif"
#Resolution of cell
pixel_size = float(raw_input("Resolution:"))
#Values attribute name
attribute = raw_input("Attribute Name:")
#open shapefile
in_shp = ogr.Open(in_file)
in_layer = in_shp.GetLayer()
xmin, xmax, ymin, ymax = in_layer.GetExtent()
inSpatialRef = in_layer.GetSpatialRef()
feature_count = in_layer.GetFeatureCount()
lon, lat, val = [], [], []
for feature in in_layer:
    geom =feature.GetGeometryRef()
    xy = geom.GetPoint()
    lon.append(float(xy[0]))
    lat.append(float(xy[1]))
for i in range(feature_count):
    feature = in_layer.GetFeature(i)
    values = feature.GetField(attribute)
    val.append(values)  
x, y, z = lon, lat, val

#size of 2 m grid
cols = int((xmax - xmin)/pixel_size)
rows = int((ymax - ymin)/pixel_size)

# Generate a regular grid to interpolate the data.
xi = np.linspace(xmin, xmax, cols)
yi = np.linspace(ymin, ymax, rows)
xi, yi = np.meshgrid(xi, yi) 

# Interpolate the values of z for all points in the rectangular grid
# Method 1 - Interpolate by matplotlib
zi = ml.griddata(x,y,z,xi,yi,interp='linear')

# Otherwise, try Method 2 - Interpolate  using scipy interpolate griddata
#zi = il.griddata((x, y), z, (xi, yi),method='linear')
 
#---------------  Write to GeoTIFF ------------------------
geotransform=(xmin, pixel_size, 0, ymin, 0, pixel_size) 

output_raster = gdal.GetDriverByName('GTiff').Create(out_raster,cols, rows, 1 ,gdal.GDT_Float32,['TFW=YES', 'COMPRESS=PACKBITS'])
output_raster.SetGeoTransform(geotransform)
output_raster.SetProjection(inSpatialRef.ExportToWkt())
output_raster.GetRasterBand(1).WriteArray(zi)

output_raster=None
