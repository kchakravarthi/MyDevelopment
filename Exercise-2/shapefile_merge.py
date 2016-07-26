# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 12:17:32 2016

@author: Webonise Lab
"""

import glob, os
import shapefile
from osgeo import ogr, osr

def shapefileMerge(in_dir, out_dir, out_file):
    #remove outfile if exists    
    if os.path.exists(out_dir+out_file):
        os.remove(out_dir+out_file)
    #create out directory if not exists
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    #Split name and extension of out file
    (out_file_name, extension) = os.path.splitext(out_file)

    files = glob.glob(in_dir + "*.shp")
    fileEndsWith = '.shp'
    fileList = os.listdir(in_dir)
    
    for file in fileList:
        if file.endswith(fileEndsWith):
            ds = ogr.Open(in_dir+file)
            in_layer = ds.GetLayer()
            inSpatialRef = in_layer.GetSpatialRef() #input file spatial reference
    
    w = shapefile.Writer()
    for f in files:
        r = shapefile.Reader(f)
        w._shapes.extend(r.shapes())
        w.records.extend(r.records())
        w.fields = list(r.fields)
    #Save output sahpefile
    w.save(out_dir+out_file)
    #Creation of projection file
    spatialRef = osr.SpatialReference()
    spatialRef.MorphToESRI()
    file = open(out_dir + out_file_name + ".prj", 'w') 
    file.write(inSpatialRef.ExportToWkt())
    file.close()

#input shapefiles directory    
in_dir = 'E:/Python_Learning/Exercise/merge/'
#output shapefile name
out_file = 'merge.shp'
#output shapefile directory 
out_dir = "E:/Python_Learning/Exercise/merge/out/"

shapefileMerge(in_dir, out_dir, out_file)
