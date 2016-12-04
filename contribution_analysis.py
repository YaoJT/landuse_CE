import arcpy
import pandas as pd
import numpy as np

class raster_map:
    def __init__(self,in_raster,get_array = True):
        self.path = in_raster
        self.none = arcpy.Raster(in_raster).noDataValue
        self.left = float(arcpy.GetRasterProperties_management(in_raster,'LEFT').getOutput(0))
        self.right = float(arcpy.GetRasterProperties_management(in_raster,'Right').getOutput(0))
        self.top = float(arcpy.GetRasterProperties_management(in_raster,'TOP').getOutput(0))
        self.bottom = float(arcpy.GetRasterProperties_management(in_raster,'BOTTOM').getOutput(0))
        self.cellsize_x = float(arcpy.GetRasterProperties_management(in_raster,'CELLSIZEX').getOutput(0))
        self.cellsize_y = float(arcpy.GetRasterProperties_management(in_raster,'CELLSIZEY').getOutput(0))
        if get_array:
            self.array = arcpy.RasterToNumPyArray(in_raster)
    def value_list(self):
        array = arcpy.RasterToNumPyArray(self.path)
        array1 = list(np.unique(array))
        array1.remove(self.none)
        return array1
##    def get_value(self,(row,col)):
##        array = arcpy.RasterToNumPyArray(self.path)
##def contribution_analysis(or_map,fi_map,zonal):
if True:
    or_map = 'h:/CE2010f/CEH.tif'
    fi_map = 'h:/CE2015f/CEH.tif'
    zonal = 'g:/GHG_Landuse/Beijing_city/driving_factors/function_zone_f.tif'
    Z_map = raster_map(zonal)
    O_map = raster_map(or_map)
    F_map = raster_map(fi_map)
    index = Z_map.value_list()
    columns = ['count_or','sum_or','count_fi','sum_fi','sum_net','count+','sum+','count-','sum-','change','contribution']
    init_data = np.zeros((len(index),len(columns)))
    out_res = pd.DataFrame(init_data,index,columns)
    for i in range(len(O_map.array)):
        for j in range(len(O_map.array[i])):
            x,y = O_map.left + O_map.cellsize_x*j,O_map.top-O_map.cellsize_y*i
            row_F,col_F = int((F_map.top-y)/F_map.cellsize_y),int((x-F_map.left)/F_map.cellsize_x)
            row_Z,col_Z = int((Z_map.top-y)/Z_map.cellsize_y),int((x-Z_map.left)/Z_map.cellsize_x)
            try:
                value_or,value_fi,value_zone = O_map.array[i,j],F_map.array[row_F,col_F],Z_map.array[row_Z,col_Z]
##                print value_or,value_fi,value_zone
                if value_zone != Z_map.none:
                    if value_or != O_map.none:
                        out_res['count_or'][value_zone] += 1
                        out_res['sum_or'][value_zone] += value_or
                        if value_fi != F_map.none:
                            out_res['count_fi'][value_zone] += 1
                            out_res['sum_fi'][value_zone] += value_fi
                        else:
                            out_res['count-'][value_zone] += 1
                            out_res['sum-'][value_zone] += value_or
                    else:
                        if value_fi != F_map.none:
                            out_res['count_fi'][value_zone] += 1
                            out_res['sum_fi'][value_zone] += value_fi
                            out_res['count+'][value_zone] += 1
                            out_res['sum+'][value_zone] += value_fi
            except:
                None
    out_res['sum_net'] = out_res['sum_fi']-out_res['sum_or']
    out_res['change'] = out_res ['sum+'] - out_res['sum-']
    out_res['contribution'] = out_res['change']/out_res['sum_net']
    
    
    
