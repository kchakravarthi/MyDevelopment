# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 10:54:11 2016

@author: Kalyan

Extraction of Raster Information to txt file
"""
import gdal

#input file location 
in_file = "E:/Python_Learning/Exercise/BGNIR.tif"
#output file location
out_file = "E:/Python_Learning/Exercise/Rater_info.txt"
data = gdal.Open(in_file)

#Reading data
band = data.GetRasterBand(1)
bandtype = gdal.GetDataTypeName(band.DataType)
metadata = data.GetMetadata()
cols = data.RasterXSize
rows = data.RasterYSize
trans = data.GetGeoTransform()
proj = data.GetProjection()
bands = data.RasterCount
resol = trans[1], trans[5]
ulcoord = (trans[0], trans[3])
urcoord = ((trans[0] + trans[1] * cols), trans[3])
lrcoord = ((trans[0] + trans[1] * cols), (trans[3] + trans[5] * rows))
llcoord = (trans[0], (trans[3] + trans[5] * rows))
ext = ulcoord, urcoord, lrcoord, llcoord

#Write Raster Info to Text file
textfile = open(out_file, "w")
textfile.write("Metadata= %r \nBand Type= %r \nColumns= %r \nRows= %r \
                \nPixel Size= %r \nNo.of Bands= %r \nBounding Coordinates: %r \
                \nProjection Information: %r \n"\
                %(metadata, bandtype, cols, rows, resol, bands, ext, proj)) 

#Read Each Band and Extract Statistics
for band in range( data.RasterCount ):
    band += 1
    textfile.write("Band: %r \n" %band)
    srcband = data.GetRasterBand(band)
    if srcband is None:
        continue

    stats = srcband.GetStatistics( True, True )
    ndv = srcband.GetNoDataValue()
    if stats is None:
        continue
    
    textfile.write("Stats: Min= %r, Max= %r, Mean= %r, StdDev= %r \n" %(stats[0],\
    stats[1], stats[2], stats[3]))

textfile.close
data = None
