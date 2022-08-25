#v2
import xarray as xr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import logging

def get_vertical_dim(da):
    if isinstance(da, xr.DataArray):
        vertical_names = ['level', 'pressure', 'pres', 'zt', 'height', 'lev']
        for ver_name in vertical_names:
            if ver_name in da.dims:
                logging.debug("get_vertical_dim: found name '%s'" % ver_name)
                return ver_name
        return None
    else: 
        raise ValueError("need an xarray for this")

def mean_without_this_axis(shape, excluding_dim):
    find_mean_axis = list(i for i in range(len(shape)))
    
    for i, shape_dim in enumerate(shape):
        if shape_dim == excluding_dim.shape[0]:
            find_mean_axis.remove(find_mean_axis[i])
            
    return tuple(find_mean_axis)
    
        
class Phase:
    
    phase_range=np.radians([-90., -67.5, -22.5, 22.5, 67.5, 90.])    
    ind_p=np.arange(0,7)
    
    min_A=0.5
    max_A=4.1
    
    def __init__(self, value, W1, W2):
        self.value=value
        self.W1=W1
        self.W2=W2
        self.phase_mean=xr.Dataset()
        
    def find_phase_id(self, ano=True):
        vertical = False
        A = np.sqrt(self.W1**2 + self.W2**2)
        phi = np.arctan(self.W2/self.W1)
        
        #if input is 3d, find a vertical dim
        if len(self.value.shape) == 3:
            vertical_dim = get_vertical_dim(self.value)
            dim_list = [e for e in self.value.dims]
            dim_list.remove(vertical_dim)
            
            new_dim =[ 'phase', vertical_dim ]
            new_coord = [ np.arange(1,9,1), self.value[vertical_dim].values ]
            new_arr = np.zeros( ( 8, self.value[vertical_dim].shape[0] ) )
            
            vertical = True

        elif len(self.value.shape) == 2:
            dim_list = [e for e in self.value.dims]
            
            new_dim = ['phase']
            new_coord = [ np.arange(1,9,1) ]
            new_arr = np.zeros( ( 8 ) )
            
        #to compute anomalies
        if ano:
            var_comp = self.value - self.value.mean(dim_list)
        else:
            var_comp = self.value.copy()
            
        var_comp = var_comp.where((A >= self.min_A) & (A <= self.max_A))
        
        var_p=var_comp.where(self.W1 > 0)
        var_n=var_comp.where(self.W1 < 0)

        for i in range(5):
            conditions=(phi >= self.phase_range[i]) & (phi < self.phase_range[i+1])
            
            cur_var_p=var_p.where(conditions)
            cur_var_n=var_n.where(conditions)
            
            if i == 0:
                phase_mean_6_p=cur_var_p
                phase_mean_2_n=cur_var_n
            if i == 4:
                phase_mean_2_p=cur_var_p
                phase_mean_6_n=cur_var_n
            else:
                new_arr[6-i,...]=cur_var_p.mean(dim_list).values
                new_arr[2-i,...]=cur_var_n.mean(dim_list).values
        
        phase_mean_6 = np.hstack([phase_mean_6_p, phase_mean_6_n])
        phase_mean_2 = np.hstack([phase_mean_2_p, phase_mean_2_n])
        
        if len(new_arr.shape) > 1:
            axis_for_mean = mean_without_this_axis(phase_mean_6.shape, self.value[vertical_dim])
            new_arr[6,...]=np.nanmean(phase_mean_6, axis=axis_for_mean)
            new_arr[2,...]=np.nanmean(phase_mean_2, axis=axis_for_mean)
            
        else:
            new_arr[6,...]=np.nanmean(phase_mean_6)
            new_arr[2,...]=np.nanmean(phase_mean_2)
        
        self.phase_mean['var'] = xr.DataArray(new_arr, coords = new_coord, dims = new_dim)
        self.phase_mean['var'].attrs = {'long_name': 'wave composite'}
        
        return self