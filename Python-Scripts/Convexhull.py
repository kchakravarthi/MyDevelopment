# -*- coding: utf-8 -*-
"""
Created on Thu May 05 15:12:38 2016

@author: Kalyan

Creation of convexhull shapefile from a point shapefile
"""

from osgeo import ogr, osr
import os

#Input shape file 
inShapefile = 'E:/Python_Learning/Exercise/telemetry_point.shp'
#Output shapefile
outShapefile = 'E:/Python_Learning/Exercise/telemetry_convex.shp'

#get path and filename seperately 
(outfilepath, outfilename) = os.path.split(outShapefile)
#get file name without extension  
(outfileshortname, extension) = os.path.splitext(outfilename)

# input SpatialReference
driver = ogr.GetDriverByName("ESRI Shapefile")
inDataSource = driver.Open(inShapefile, 0)
inLayer = inDataSource.GetLayer()
inSpatialRef = inLayer.GetSpatialRef()

# Collect all Geometry
geomcol = ogr.Geometry(ogr.wkbGeometryCollection)
for feature in inLayer:
    geomcol.AddGeometry(feature.GetGeometryRef())

# Calculate convex hull
convexhull = geomcol.ConvexHull()

# Remove output shapefile if it already exists
if os.path.exists(outShapefile):
    driver.DeleteDataSource(outShapefile)

# Create the output shapefile
outDataSource = driver.CreateDataSource(outShapefile)
outLayer = outDataSource.CreateLayer(outfileshortname, geom_type=ogr.wkbPolygon)
idField = ogr.FieldDefn("id", ogr.OFTInteger)
outLayer.CreateField(idField)

# Create the feature and set values
featureDefn = outLayer.GetLayerDefn()
feature = ogr.Feature(featureDefn)
feature.SetGeometry(convexhull)
feature.SetField("id", 1)
outLayer.CreateFeature(feature)

# Close DataSource
inDataSource.Destroy()
outDataSource.Destroy()

#Add Spatial Reference
spatialRef = osr.SpatialReference()
spatialRef.MorphToESRI()
file = open(outfilepath + '\\'+ outfileshortname + '.prj', 'w') 
file.write(spatialRef.ExportToWkt())
file.close()
