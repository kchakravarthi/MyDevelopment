# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 16:44:03 2017

@author: Kalyan

dsm to dem generation
"""

from datetime import datetime
import gdal
import numpy as np
import math
import os
import scipy.interpolate as il
import scipy.ndimage as ni

#Slope calculation from DSM
def slope(ras_arr, rows, cols, x_size, y_size):
    slp_arr = []
    for i in range(rows - 1):
        slp = []
        for j in range(cols - 1):
            dir_x = ((ras_arr.item(i - 1, j + 1) + 2 * ras_arr.item(i, j + 1) + ras_arr.item(i + 1, j + 1)) - \
                     (ras_arr.item(i - 1, j - 1) + 2 * ras_arr.item(i, j - 1) + ras_arr.item(i + 1, j - 1))) / \
                    (8 * x_size)
            dir_y = ((ras_arr.item(i + 1, j - 1) + 2 * ras_arr.item(i + 1, j) + ras_arr.item(i + 1, j + 1)) - \
                     (ras_arr.item(i - 1, j - 1) + 2 * ras_arr.item(i - 1, j) + ras_arr.item(i - 1, j + 1))) / \
                    (8 * y_size)
            slope = math.degrees(math.atan(math.sqrt(math.pow(dir_x, 2) + math.pow(dir_y, 2))))
            slp.append(slope)
        slp_arr.append(slp)
    slp_arr = np.array(slp_arr)
    return slp_arr

#Adjacent pixel difference calculation from DSM in E-W and N-S direction
def dif(ras_arr, rows, cols):
    difx_arr = []
    # dify_arr = []
    for i in range(rows - 1):
        slp = []
        difx = []
        # dify = []
        for j in range(cols - 1):
            difx.append(ras_arr.item(i, j) - ras_arr.item(i, j + 1))
            # dify.append(ras_arr.item(i,j)-ras_arr.item(i+1,j))
        difx_arr.append(difx)
        # dify_arr.append(dify)
    difx_arr = np.array(difx_arr)
    # dify_arr = np.array(dify_arr)
    return difx_arr #, dify_arr

#Raster creation
def new_ras(ras_arr, ras, geotrans, proj, cols, rows, datatype):
    out_drv = gdal.GetDriverByName('GTiff')
    out_ras = out_drv.Create(ras, cols, rows, 1, datatype)
    out_ras.SetGeoTransform(geotrans)
    out_ras.SetProjection(proj)
    out_ras.GetRasterBand(1).WriteArray(ras_arr)

#Removing of objects from dsm
def xdirobj(slp_arr, difx_arr, dsm_arr, rows, cols):
    val_arr = []
    for i in range(rows-1):
        val = []
        slp = []
        slp_st = None
        min_ht = None
        max_ht = None
        for j in range(cols-1):
            slp.append(slp_arr.item(i,j))
        max_slp = np.nanmax(slp)
        if max_slp >= 80:
            slp_st = 1
        else:
            slp_st = 0
        for j in range(cols-1):
            if slp_st == 0:
                val.append(1)
            else:
                if slp_arr.item(i,j) >= 80:
                    if difx_arr.item(i,j) < -0.5:
                        val.append(0)
                        min_ht = dsm_arr.item(i,j)
                    elif difx_arr.item(i,j) > 0.5:
                        val.append(0)
                        max_ht = dsm_arr.item(i,j)
                    else:
                        val.append(0)
                elif slp_arr.item(i,j) < 80:
                    if min_ht == None:
                        val.append(1)
                    elif dsm_arr.item(i,j) > min_ht:
                        val.append(0)
                    elif dsm_arr.item(i,j) < max_ht:
                        val.append(1)
                    else:
                        val.append(0)
                else:
                    val.append(0)
        val_arr.append(val)
    val_arr = np.array(val_arr)
    return val_arr

def main():
    dsm = raw_input("DSM path: ")
    outdir = os.path.join(os.path.dirname(dsm), 'output')

    if not os.path.exists(outdir):
        os.makedirs(outdir)

    output_name = os.path.splitext(os.path.basename(dsm))[0]
    print 'Basename: {0}'.format(output_name)
    output_tif = os.path.join(outdir, output_name + '_objremoved.tif')

    print datetime.now().strftime("%Y-%m-%d %H:%M:%S")," 1 - Initiated processing"
    in_ras = gdal.Open(dsm)
    geotrans = in_ras.GetGeoTransform()
    proj = in_ras.GetProjection()
    x_size = geotrans[1]
    y_size = geotrans[5]
    cols = in_ras.RasterXSize
    rows = in_ras.RasterYSize
    band = in_ras.GetRasterBand(1)
    datatype = band.DataType
    ndv = band.GetNoDataValue()
    ras_arr = band.ReadAsArray()
    ras_arr[ras_arr == ndv] = np.nan

    print datetime.now().strftime("%Y-%m-%d %H:%M:%S"), " 2 - slope calculation processing"
    slp_arr = slope(ras_arr, rows, cols, x_size, y_size)
    print datetime.now().strftime("%Y-%m-%d %H:%M:%S"), " 3 - Adjacent pixel difference calculation processing"
    dif_arr = dif(ras_arr, rows, cols)
    print datetime.now().strftime("%Y-%m-%d %H:%M:%S"), " 3 - E-W diectional object removing processing"
    obj_arr = xdirobj(slp_arr, dif_arr, ras_arr, rows, cols)
    print datetime.now().strftime("%Y-%m-%d %H:%M:%S"), " 3 - slope raster generation"
    new_ras(obj_arr, output_tif, geotrans, proj, cols, rows, datatype)
    print datetime.now().strftime("%Y-%m-%d %H:%M:%S"), " 4 - Process completed"

if __name__ == '__main__':
    main()