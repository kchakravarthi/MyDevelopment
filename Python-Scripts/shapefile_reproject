# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 17:02:45 2016

@author: Kalyan

Reprojecting of a point shapefile
"""

from osgeo import ogr, osr
import os, sys

#input file location  
infile = 'E:/Python_Learning/Exercise/telemetry_point.shp'
#output file location  
outfile = 'E:/Python_Learning/Exercise/telemetry_point_UTM.shp' 

#get path and filename seperately 
(outfilepath, outfilename) = os.path.split(outfile)
#get file name without extension  
(outfileshortname, extension) = os.path.splitext(outfilename)

# input SpatialReference
driver = ogr.GetDriverByName('ESRI Shapefile')
inDataset = driver.Open(infile, 0)
inLayer = inDataset.GetLayer()
inSpatialRef = inLayer.GetSpatialRef()

# output SpatialReference
outSpatialRef = osr.SpatialReference()
outSpatialRef.ImportFromEPSG(32613)

# create the CoordinateTransformation
coordTrans = osr.CoordinateTransformation(inSpatialRef, outSpatialRef)

# Open the input shapefile and get the layer   
if inDataset is None:   
    print ' Could not open file'   
    sys.exit(1)   
   
# Create the output shapefile  
if os.path.exists(outfile):   
    driver.DeleteDataSource(outfile)   
   
outDataset = driver.CreateDataSource(outfile)   
   
if outfile is None:   
    print ' Could not create file'   
    sys.exit(1)   
outLayer = outDataset.CreateLayer(outfileshortname, geom_type=ogr.wkbPoint)


# add fields
inLayerDefn = inLayer.GetLayerDefn()
for i in range(0, inLayerDefn.GetFieldCount()):
    fieldDefn = inLayerDefn.GetFieldDefn(i)
    outLayer.CreateField(fieldDefn)

# get the output layer's feature definition
outLayerDefn = outLayer.GetLayerDefn()

# loop through the input features
inFeature = inLayer.GetNextFeature()
while inFeature:
    geom = inFeature.GetGeometryRef()
    geom.Transform(coordTrans)
    outFeature = ogr.Feature(outLayerDefn)
    outFeature.SetGeometry(geom)
    
    for i in range(0, outLayerDefn.GetFieldCount()):
        outFeature.SetField(outLayerDefn.GetFieldDefn(i).GetNameRef(), inFeature.GetField(i))
    
    outLayer.CreateFeature(outFeature)

    outFeature.Destroy()
    inFeature.Destroy()
    inFeature = inLayer.GetNextFeature()

# close the shapefiles
inDataset.Destroy()
outDataset.Destroy()

#create the prj projection file  
outSpatialRef.MorphToESRI()
file = open(outfilepath + '\\'+ outfileshortname + '.prj', 'w') 
file.write(outSpatialRef.ExportToWkt())
file.close()
