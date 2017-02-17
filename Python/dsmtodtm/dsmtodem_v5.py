# -*- coding: utf-8 -*-
"""
Created on Tue Jan 05 11:18:57 2017

@author: Kalyan

dsm to dem generation

"""

from datetime import datetime
import gdal
import numpy as np
import math
import scipy.interpolate as il

def dsm_to_dem(dsm, dem1, dem2, dem3, dem, ndsm):
    print datetime.now().strftime("%Y-%m-%d %H:%M:%S"), \
          " ", "Start"
    in_dsm = gdal.Open(dsm)
    geotrans = in_dsm.GetGeoTransform()
    proj = in_dsm.GetProjection()
    x_size = geotrans[1]
    y_size = geotrans[5]
    cols = in_dsm.RasterXSize
    rows = in_dsm.RasterYSize
    band = in_dsm.GetRasterBand(1)
    datatype = band.DataType
    dsm_arr = band.ReadAsArray()
    ndv = band.GetNoDataValue()  
    dsm_arr[dsm_arr==ndv] = np.nan
    print dsm_arr.shape
    print datetime.now().strftime("%Y-%m-%d %H:%M:%S"), \
          " ", "1 - Initiated processing"
#--------------------------------------------------------- 
    slp_arr = []
    difx_arr = []
    #dify_arr = []
    for i in range(rows-1):       
        slp = []
        difx = []
        #dify = []
        for j in range(cols-1):
            dir_x = ((dsm_arr.item(i-1,j+1)+ 2*dsm_arr.item(i,j+1)+dsm_arr.item(i+1,j+1)) - \
                     (dsm_arr.item(i-1,j-1)+ 2*dsm_arr.item(i,j-1)+dsm_arr.item(i+1,j-1))) / \
                     (8 * x_size)
            dir_y = ((dsm_arr.item(i+1,j-1)+ 2*dsm_arr.item(i+1,j)+dsm_arr.item(i+1,j+1)) - \
                     (dsm_arr.item(i-1,j-1)+ 2*dsm_arr.item(i-1,j)+dsm_arr.item(i-1,j+1))) / \
                     (8 * y_size)
            slope = math.degrees(math.atan(math.sqrt(math.pow(dir_x,2)+math.pow(dir_y,2))))
            slp.append(slope)
            difx.append(dsm_arr.item(i,j)-dsm_arr.item(i,j+1))
            #dify.append(dsm_arr.item(i,j)-dsm_arr.item(i+1,j))
        slp_arr.append(slp)
        difx_arr.append(difx)
        #dify_arr.append(dify)
    slp_arr1 = np.array(slp_arr)
    difx_arr1 = np.array(difx_arr)
    #dify_arr1 = np.array(dify_arr)
    slp_arr = None
    difx_arr = None
    #dify_arr = None
    print slp_arr1.shape
    print difx_arr1.shape
    #print dify_arr1.shape
    
    out_drv = gdal.GetDriverByName('GTiff')    
    out_dem1 = out_drv.Create(dem1, cols, rows, 3, datatype)
    out_dem1.SetGeoTransform(geotrans)
    out_dem1.SetProjection(proj)
    out_dem1.GetRasterBand(1).WriteArray(slp_arr1)
    out_dem1.GetRasterBand(2).WriteArray(difx_arr1)
    #out_dem1.GetRasterBand(3).WriteArray(dify_arr1)
    out_dem1 =None
    dem1 = None
    print datetime.now().strftime("%Y-%m-%d %H:%M:%S"), \
          " ", "2 - Slope and adjacent pixel difference calculation completed" 
#------------------------------------------------------------
    val_arr = []
    for i in range(rows-1):
        val = []
        slp = []
        slp_st = None
        min_ht = None
        max_ht = None
        for j in range(cols-1):
            slp.append(slp_arr1.item(i,j))
        max_slp = np.nanmax(slp)
        if max_slp >= 80:
            slp_st = 1
        else:
            slp_st = 0
        for j in range(cols-1):
            if slp_st == 0:
                val.append(1)
            else:
                if slp_arr1.item(i,j) >= 80:
                    if difx_arr1.item(i,j) < -0.5:
                        val.append(0)
                        min_ht = dsm_arr.item(i,j)
                    elif difx_arr1.item(i,j) > 0.5:
                        val.append(0)
                        max_ht = dsm_arr.item(i,j)
                    else:
                        val.append(0)
                elif slp_arr1.item(i,j) < 80:
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
    val_arr1 = np.array(val_arr)
    #val_arr1[val_arr1==ndv] = np.nan
    val_arr = None
    print val_arr1.shape
#------------------------------------------------------------
    '''val_arr = []
    for i in range(cols-1):
        val = []
        slp = []
        slp_st = None
        min_ht = None
        max_ht = None
        for j in range(rows-1):
            slp.append(slp_arr1.item(j,i))
        max_slp = np.nanmax(slp)
        if max_slp >= 80:
            slp_st = 1
        else:
            slp_st = 0
        for j in range(rows-1):
            if slp_st == 0:
                val.append(dsm_arr.item(j,i))
            else:
                if slp_arr1.item(j,i) >= 80:
                    if dify_arr1.item(j,i) < -0.5:
                        val.append(ndv)
                        min_ht = dsm_arr.item(j,i)
                    elif dify_arr1.item(j,i) > 0.5:
                        val.append(ndv)
                        max_ht = dsm_arr.item(j,i)
                    else:
                        val.append(ndv)
                elif slp_arr1.item(j,i) < 80:
                    if min_ht == None:
                        val.append(dsm_arr.item(j,i))
                    elif dsm_arr.item(j,i) > min_ht:
                        val.append(ndv)
                    elif dsm_arr.item(j,i) < max_ht:
                        val.append(dsm_arr.item(j,i))
                    else:
                        val.append(ndv)
                else:
                    val.append(ndv)
        val_arr.append(val)
    val_arr2 = np.array(val_arr)
    val_arr2 = val_arr2.transpose()
    val_arr2[val_arr2==ndv] = np.nan
    val_arr = None'''
    
    out_drv = gdal.GetDriverByName('GTiff')    
    out_dem2 = out_drv.Create(dem2, cols, rows, 1, datatype)
    out_dem2.SetGeoTransform(geotrans)
    out_dem2.SetProjection(proj)
    out_dem2.GetRasterBand(1).WriteArray(val_arr1)
    #out_dem2.GetRasterBand(2).WriteArray(val_arr2)
    out_dem2 =None
    dem2 = None
    print datetime.now().strftime("%Y-%m-%d %H:%M:%S"), \
          " ", "3 - Elevated data/Ground identification completed  "             
#------------------------------------------------------------

    val_array = []
    for i in range(rows-1):
        val = []
        #ht_row = []
        for j in range(cols-1):
            if val_arr1.item(i,j) == 0:
                dsm_val = ndv
            else:
                dsm_val = dsm_arr.item(i,j)
            val.append(dsm_val)
        val_array.append(val)
    val_arr3 = np.array(val_array)    
    val_arr1 = None
    val_array = None
    #dsm_array = None
    
    out_dem3 = out_drv.Create(dem3, cols, rows, 1, datatype)
    out_dem3.SetGeoTransform(geotrans)
    out_dem3.SetProjection(proj)
    out_dem3.GetRasterBand(1).WriteArray(val_arr3)
    out_dem3 = None
    dem3 = None
    print datetime.now().strftime("%Y-%m-%d %H:%M:%S"), \
          " ", "4- Elevated data removed from dsm"
#------------------------------------------------------------
    x_pt_arr=[]
    y_pt_arr=[]
    z_pt_arr=[]
    
    for i in range(rows-1):
        x_pt=[]
        y_pt=[]
        z_pt=[]
        for j in range(cols-1):
            dem_val = val_arr3.item(i,j)
            if (dem_val == ndv):
                pass
            else:
                x_pt.append(j)
                y_pt.append(i)
                z_pt.append(dem_val)

        x_pt_arr.extend(x_pt)
        y_pt_arr.extend(y_pt)
        z_pt_arr.extend(z_pt)
    
    val_arr3 = None
    
    x1 = np.array(x_pt_arr)
    y1 = np.array(y_pt_arr)
    z1 = np.array(z_pt_arr)
    x_pt_arr = None
    y_pt_arr = None
    z_pt_arr = None
    
    print datetime.now().strftime("%Y-%m-%d %H:%M:%S"), \
          " ", "5 - Interpolation initiated"
    
    xi = np.linspace(0, cols, cols)
    yi = np.linspace(0, rows, rows)
    xi, yi = np.meshgrid(xi, yi)
    
    #zi = ml.griddata(x1,y1,z1,xi,yi,interp='linear')
    
    zi = il.griddata((x1, y1), z1, (xi, yi),method='nearest')

    print datetime.now().strftime("%Y-%m-%d %H:%M:%S"), \
          " ", "6 - Interpolation completed"
    
    x1 = None
    y1 = None
    z1 = None
 
    out_dem = out_drv.Create(dem, cols, rows, 1, datatype)
    out_dem.SetGeoTransform(geotrans)
    out_dem.SetProjection(proj)
    out_dem.GetRasterBand(1).WriteArray(zi)
    out_dem =None
    dem = None
    print datetime.now().strftime("%Y-%m-%d %H:%M:%S"), \
          " ", "7 - Dem tif created"
#------------------------------------------------------------       
    dem_arr = np.array(zi)
    
    dsm_arr = dsm_arr.astype(np.float32)
    dem_arr = dem_arr.astype(np.float32)
    zi = None
    
    ndsm_arr = dsm_arr - dem_arr
    
    out_ndsm = out_drv.Create(ndsm, cols, rows, 1, datatype)
    out_ndsm.SetGeoTransform(geotrans)
    out_ndsm.SetProjection(proj)
    out_ndsm.GetRasterBand(1).WriteArray(ndsm_arr)
    out_ndsm = None
    ndsm = None
    print datetime.now().strftime("%Y-%m-%d %H:%M:%S"), \
          " ", "8 - ndsm tif created"
    
    dsm_arr = None    
    dem_arr = None
    in_dsm = None
    out_ndsm =None
    dsm = None
    dem = None      
    print datetime.now().strftime("%Y-%m-%d %H:%M:%S"), \
          " ", "Processing successful"
     
dsm = "E:/PH-Algo/DSMtoDEM/Tullavo/Tullavo_dsm_clip.tif"
dem1 = "E:/PH-Algo/DSMtoDEM/Tullavo/Tullavo_dsm_clip_slp_dif.tif"
dem2 = "E:/PH-Algo/DSMtoDEM/Tullavo/Tullavo_dsm_clip_obj.tif"
dem3 = "E:/PH-Algo/DSMtoDEM/Tullavo/Tullavo_dsm_clip_dem_obj.tif"
dem = "E:/PH-Algo/DSMtoDEM/Tullavo/Tullavo_dsm_clip_dem.tif"
ndsm = "E:/PH-Algo/DSMtoDEM/Tullavo/Tullavo_dsm_clip_ndsm.tif"

dsm_to_dem(dsm, dem1, dem2, dem3, dem, ndsm)