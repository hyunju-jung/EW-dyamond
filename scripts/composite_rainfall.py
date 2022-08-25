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
from matplotlib import cm
from matplotlib.colors import ListedColormap

plt.rcParams.update({'font.size': 15})
HOME=os.path.expanduser("~")
opath='%s/B6/Hyunju/prepare-dyamond/' % HOME

waves = ['Kelvin', 'WMRG','R1','WG1']
wv_name = ['KW','MRG','ER', 'WIG1']

titles=['ecmwf','ICON-2.5km','ICON-5km','ICON-10km','ICON-20km','ICON-40km',
        'ICON-80km','ICON-20km-conv','ICON-40km-conv','ICON-80km-conv']

names = ['obs', '2.5km', '20km','80km','20km-conv','80km-conv']

#plt.style.use('dark_background')
sel_lat = {'Kelvin': 0.,'WG1': 0.,'WG2': 7.,
           'WMRG':10, 'EMRG':0, 'R1': 0.,'R2': 13., 'EG1':7.}
wv_wind = {'Kelvin': 'u_wave','WG1':'u_wave','WG2':'u_wave',
           'WMRG':'u_wave','EMRG': 'v_wave','R1':'u_wave','R2':'v_wave', 'EG1':'v_wave'}

wv_pair = {'WG1':'v_wave','WG2':'v_wave', 'WMRG':'v_wave',
           'EMRG': 'v_wave','R1':'v_wave','R2':'u_wave', 'EG1':'u_wave'}
lat_pair = {'WG1': 10. ,'WG2':13., 'WMRG': 0.,
           'EMRG': 8.,'R1': 8.,'R2':8., 'EG1': 13.}

fig, axs = plt.subplots(2,4,figsize=(13,6.5))
fig.subplots_adjust(left=0.07, wspace=0.15, right=0.98, bottom=0.2, top =0.92, hspace=0.25)
#colors = ['black', '#D33F6A', '#E07B91','#E5C9CE', '#4A6FE3','#B5BBE3']
#lss = ['dotted', 'solid', 'solid', 'solid','dashed', 'dashed']
colors = ['black', '#D33F6A', '#DA5F7D','#E07B91','#E495A5','#E6AFB9','#E5C9CE',
         '#4A6FE3','#8595E1','#B5BBE3']
lss = ['dotted', 'solid', 'solid', 'solid', 'solid', 'solid', 'solid',
      'dashed', 'dashed', 'dashed']
label_phase=['(a)', '(b)', '(c)', '(d)']
label_ex=['(e)', '(f)', '(g)', '(h)']
sel_time=[slice(np.datetime64('2016-08-25T06'),np.datetime64('2016-08-31T00')),
          slice(np.datetime64('2016-08-05T06'),np.datetime64('2016-08-10T00')),
          slice(np.datetime64('2016-08-01T06'),np.datetime64('2016-08-07T00')),
    slice(np.datetime64('2016-09-01T06'),np.datetime64('2016-09-03T00'))]
#comp_lon = [-100,-130,-50,0]
comp_lon = [-130,-100,-50,0]

newcmp = cm.get_cmap('tab20b', 20)
cmp_first = True

plev = 0
xt = np.arange(1,9,1)
for i, od in enumerate(titles):
    prec=xr.open_dataset('%s%s/prec_1x1.nc' % (opath, od))['prec']
    prec=prec.sel(lat = slice(5,15)).mean('lat')*4/24.
    print("%s : %.2f mm/h" %(od, prec.mean().values))
    
    if od == titles[0]:
        names = 'obs'
    else:
        names = od[5:]
    
    for j, wv in enumerate(waves):
        ds = xr.open_dataset('%s%s/yang_%s.nc' % (opath, od, wv))
        var = ds[wv_wind[wv]].sel(lat = sel_lat[wv]).isel(plev=plev)[0,...]
        
        if wv == 'Kelvin':
            W2 = var / var.std()
            W1 = var.diff('lon')
            W1 = W1/ W1.std()
            
            prec_wv = Phase(value=prec[:,1:].copy(), W1=W1, W2=W2[:,1:])
            
        else:
            W1 = ds[wv_pair[wv]].sel(lat=lat_pair[wv]).isel(plev=plev)[0,...]
            W1 = W1 / W1.std()
            W2 = var / var.std()
            
            if wv == 'WMRG':
                W1 = -W1
                print(wv)
            
            prec_wv = Phase(value=prec[:,1:].copy(), W1=W1[:,1:], W2=W2)
            
        prec_wv = prec_wv.find_phase_id(ano=False)

        axs[0,j].plot(xt, prec_wv.phase_mean['var'], 'o', label = names, lw=2, color=colors[i], ls=lss[i])
        axs[0,j].set_title(wv_name[j])
        axs[0,j].text(1.3, 0.46, label_phase[j])
        #axs[1,j].set_title(sublabels[j])
        
        if i == 0:
            t=W1.time.sel(time=sel_time[j])
            print(wv, od, sel_time[j])

            xx=W1.sel(lon=comp_lon[j]).where(W1.time == t, drop=True)
            yy=W2.sel(lon=comp_lon[j]).where(W2.time == t, drop=True)

            
            x8=np.linspace(-5,5,61)
            
            for theta in range(4):
                slope=np.tan(np.radians(theta*45.+22.5))
                axs[1,j].plot(x8, x8*slope, linestyle='--',color='lightgray', zorder=4)
                
                
                axs[1,j].text(-3,0,'1', color='lightgray', fontweight='bold')
                axs[1,j].text(-2.5,2.5,'2', color='lightgray', fontweight='bold')
                axs[1,j].text(0,3,'3', color='lightgray', fontweight='bold')
                axs[1,j].text(2.5,2.5,'4', color='lightgray', fontweight='bold')
                axs[1,j].text(3,0,'5', color='lightgray', fontweight='bold')
                axs[1,j].text(2.5,-2.5,'6', color='lightgray', fontweight='bold')
                axs[1,j].text(0,-3,'7', color='lightgray', fontweight='bold')
                axs[1,j].text(-2.5,-2.5,'8', color='lightgray', fontweight='bold')
                
            if wv == 'Kelvin':
                axs[1,j].set_xlabel('du/dx at 0\u00b0' )
                axs[1,j].set_ylabel('u at 0\u00b0')
                
            elif wv == 'WMRG':
                axs[1,j].set_xlabel('-%s at %d\u00b0' % (wv_pair[wv][:1], lat_pair[wv]))
                axs[1,j].set_ylabel('%s at %d\u00b0' % (wv_wind[wv][:1], sel_lat[wv]))

            else:
                axs[1,j].set_xlabel('%s at %d\u00b0' % (wv_pair[wv][:1], lat_pair[wv]))
                axs[1,j].set_ylabel('%s at %d\u00b0' % (wv_wind[wv][:1], sel_lat[wv]))
                
            if cmp_first:
                newcolors = newcmp(np.linspace(0,1,len(t.time)))
                newcmp = ListedColormap(newcolors)
                im = axs[1,j].scatter(xx, yy,c=t,cmap=newcmp)
                print(wv, od, sel_time[j])
                cmp_first = False
            else:
                newcmp = ListedColormap(newcolors[:len(t.time),:])
                print(wv, od, sel_time[j])
                axs[1,j].scatter(xx, yy,c=t,cmap=newcmp)
                
            axs[1,j].text(-4, 3.3, label_ex[j])
            
cbaxes = fig.add_axes([0.72, 0.06, 0.2, 0.01])
cb=fig.colorbar(im,cax = cbaxes, orientation='horizontal', ticks=[])

for i in range(4):
    axs[0,i].set_xlim(1,8)
    axs[0,i].set_xticks(xt)
    axs[0,i].set_ylim(0.2,0.5)
    #axs[0,i].set_ylim(0.05,0.25)
    
    axs[1,i].set_ylim(-4.2,4.2)
    axs[1,i].set_xlim(-4.2,4.2)
    axs[1,i].set_xticks([-4,-2,0,2,4])
    axs[1,i].set_yticks([-4,-2,0,2,4])
    axs[1,i].set_aspect(aspect=1)
    #ax.xaxis.set_minor_locator(MultipleLocator(1))
    #ax.set_xticklabels(phase_str)
    
for i in range(1,4):
    axs[0,i].set_yticklabels([])
    axs[1,i].set_yticklabels([])
#axs[0].set_title('u wind')
axs[0,0].set_ylabel('precip [mm/h]')

axs[0,0].legend(loc='upper left', bbox_to_anchor=(0.2, -1.45), ncol=4,frameon=False, fontsize=13)
plt.savefig('wave_composite.pdf')