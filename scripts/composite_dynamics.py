#Compoiste on basis of wave phases of WK-filtered rainfall
import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import sys
import os
import pandas as pd
from enstools.misc import swapaxis
from matplotlib.ticker import MultipleLocator
sys.path.append('../scripts')
from phase8 import Phase
import pickle

wv='WIG1'
xt=np.arange(1,9)
titles = ['ecmwf' ,'ICON-2.5km','ICON-5km','ICON-10km','ICON-20km','ICON-40km',
         'ICON-80km','ICON-20km-conv','ICON-40km-conv','ICON-80km-conv']

HOME=os.path.expanduser("~")
opath='%s/B6/Hyunju/prepare-dyamond/' % HOME

def wave_composition(W1, W2, var, zt, xt=xt):
    
    new_ds = xr.Dataset()
    new_ds['W1'] = xr.DataArray(W1.values, coords=[W1.time, W1.lon], dims=['time','lon'])
    new_ds['W2'] = xr.DataArray(W2.values, coords=[W1.time, W1.lon], dims=['time','lon'])
    new_ds['var'] = xr.DataArray(var.values, coords=[zt, W1.time, W1.lon], dims = ['level','time','lon'])

    comp_3d = Phase(new_ds['var'], new_ds['W1'], new_ds['W2'])
    comp_3d = comp_3d.find_phase_id()
    
    return comp_3d
    
for od in titles:
    #---wave
    ds = xr.open_dataset('%s%s/WK_filtered_precip_5_15N_with_anomaly.nc' % (opath, od))
    ds = ds.sel(time=slice(np.datetime64('2016-08-01T00'), np.datetime64('2016-09-09T18')))
    var = ds[wv]
    
    norm_var1 = var / var.std()
    
    norm_var2 = var.diff('time')
    norm_var2 = norm_var2 / norm_var2.std()
    var_wv = Phase(value=var[1:,:], W1=norm_var1[1:,:], W2=norm_var2)
      
    var_wv = var_wv.find_phase_id(ano=False)
    pickle.dump(var_wv.phase_mean['var'], open('pickle/WK_wind_%s_%s.pkl' % (od,wv), 'wb'))
    
    W1=norm_var1[1:,:].copy()
    W2=norm_var2.copy()

    if od == 'ecmwf':
        ofile_q = '%s%s/era5_specific_humidity_3d.nc' % (opath, od)
        ofile_t = '%s%s/era5_temperature_ml.nc' % (opath, od)
        ofile_u = '%s%s/era5_u_ml.nc' % (opath, od)
        ofile_v = '%s%s/era5_v_ml.nc' % (opath, od)
        lat_range= slice(15,5)
    else:
        ofile_q = '%s%s/nwp_R2B10_lkm1007_atm_3d_qv_ml_6hr_mergetime.nc' % (opath, od)
        ofile_t = '%s%s/nwp_R2B10_lkm1007_atm_3d_t_ml_6hr_mergetime.nc' % (opath, od)
        ofile_u = '%s%s/nwp_R2B10_lkm1007_atm_3d_u_ml_6hr_mergetime.nc' % (opath, od)
        ofile_v = '%s%s/nwp_R2B10_lkm1007_atm_3d_v_ml_6hr_mergetime.nc' % (opath, od)
        lat_range= slice(5,15)
        zt = xr.open_dataset('%sICON-2.5km/mean_pres.nc' % opath)['pres']

    var = xr.open_dataset(ofile_q)['q']
    var = var.where(var.time < np.datetime64('2016-09-10T00'), drop=True)
    if 'latitude' in var.dims:
        var = var.rename({'latitude':'lat'})
        var = var.rename({'longitude':'lon'})
    var = var.sel(lat=lat_range).mean('lat')
    var = swapaxis(var, 1, 0)
    
    if od == 'ecmwf':
        #zt = var.level.values
        df=pd.read_csv("%stable.csv" % opath)
        zt = [float(i) for i in df['pf [hPa]'][1:]]

    #comp_q = wave_composition(W1[:,1:], W2, var[:,:,1:], zt)
    #comp_q = wave_composition(W1, W2, var[:,1:,:], zt)
    #pickle.dump(comp_q, open('pickle/WK_q_%s_%s.pkl' % (od,wv), 'wb'))

    #------temp----
    var = xr.open_dataset(ofile_t)['t']
    var = var.where(var.time < np.datetime64('2016-09-10T00'), drop=True)
    if 'latitude' in var.dims:
        var = var.rename({'latitude':'lat'})
        var = var.rename({'longitude':'lon'})
    var = var.sel(lat=lat_range).mean('lat')
    var = swapaxis(var, 1, 0)
            
    comp_t = wave_composition(W1, W2, var[:,1:,:], zt)
    comp_t = comp_t.phase_mean['var']
    pickle.dump(comp_t, open('pickle/WK_t_%s_%s_ml.pkl' % (od,wv), 'wb'))
    
    #------u------
    var = xr.open_dataset(ofile_u)['u']
    var = var.where(var.time < np.datetime64('2016-09-10T00'), drop=True)
    if 'latitude' in var.dims:
        var = var.rename({'latitude':'lat'})
        var = var.rename({'longitude':'lon'})
    var = var.sel(lat=lat_range).mean('lat')
    var = swapaxis(var, 1, 0)

    comp_3d = wave_composition(W1, W2, var[:,1:,:], zt)
    comp_3d = comp_3d.phase_mean['var']
    pickle.dump(comp_3d, open('pickle/WK_u_%s_%s_ml.pkl' % (od,wv), 'wb'))
    
    #-----v-------
    var = xr.open_dataset(ofile_v)['v']
    var = var.where(var.time < np.datetime64('2016-09-10T00'), drop=True)
    if 'latitude' in var.dims:
        var = var.rename({'latitude':'lat'})
        var = var.rename({'longitude':'lon'})
    var = var.sel(lat=lat_range).mean('lat')
    var = swapaxis(var, 1, 0)

    comp_3d = wave_composition(W1, W2, var[:,1:,:], zt)
    comp_3d = comp_3d.phase_mean['var']
    pickle.dump(comp_3d, open('pickle/WK_v_%s_%s_ml.pkl' % (od,wv), 'wb'))