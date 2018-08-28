# -*- coding: utf-8 -*-
"""
Created on Tue Aug 21 16:01:51 2018

@author: Raymond Liang

"""
from datetime import datetime
from dateutil.parser import parse
from pathlib import Path
import cartopy.crs as ccrs
import themisasi.io as tio
import numpy as np
import matplotlib.pyplot as plt
import pymap3d.aer as pm
import themisasi as ta
import themisasi.io as tio
import os
import argparse

PC = ccrs.PlateCarree()
ST = ccrs.Stereographic()
MR = ccrs.Mercator()
    
def themisasi(dat, ax): #function used to save plots 
        
    imgs = dat['imgs'].isel(time=800)
    #gets rid of the negative values and replaces them with nans
    el = dat['el'].values
    el.setflags(write=True)
    bad = el < 15 
    el[bad] = np.nan
    az = dat.az.values
    az.setflags(write=True)
    az[bad] = np.nan
     

    
    alt=100000
    srange=alt/np.sin(np.radians(el))
    lat,lon,alt=pm.aer2geodetic(az,el,srange,(dat.attrs['lat']),(dat.attrs['lon']),0)
    
    mask = np.isfinite(lat)
    top = None
    for i, m in enumerate(mask):
        good = m.nonzero()[0]
    
        if good.size == 0:
            continue
        elif top is None:#only focusing on non n
            top = i
    
        lat[i, good[-1]:] = lat[i, good[-1]]
        lat[i, :good[0]] = lat[i, good[0]]
    
        lon[i, good[-1]:] = lon[i, good[-1]]
        lon[i, :good[0]] = lon[i, good[0]]
    
    
    lat[:top, :] = np.nanmax(lat[top, :])
    lon[:top, :] = np.nanmax(lon[top, :])
    firstnan=np.nonzero(np.isnan(lat).any(axis=1))[0][0]
    lat[:top, :] = lat[top, firstnan]
    lon[:top, :] = lon[top, firstnan]
    
    ax.pcolormesh(lon[:firstnan, :], lat[:firstnan, :], imgs[:firstnan, :], transform=PC)
     #filename
#     
caldir = Path("c:\code") / 'themisasi' / 'asf_folder_with_calibration'
datadir = Path('C:\code') / 'themisasi' / 'testfolderforgraphicalthemis'

p=argparse.ArgumentParser('the container used for storing the name of sites')
p.add_argument('sites', nargs='+', help='names of sites')
p.add_argument('time', help='time')
p=p.parse_args()
   
    
t = parse(p.time)
datas=[]
# thefile1=ta.download('2012-03-12T12','fykn','/code/themisasi/testfolderforgraphicalthemis' )
# thefile2=ta.download('2012-03-12T08','gako','/code/themisasi/testfolderforgraphicalthemis' )
f=plt.figure()
ax=f.gca(projection=MR)
ax.set_extent((-180, -120, 50, 75))
ax.gridlines()
ax.coastlines()
    
for site in p.sites:#loading the sites which return xarrays
    datafn = datadir / f'thg_l1_asf_{site}_{t.year:4d}{t.month:02d}{t.day:02d}{t.hour:02d}_v01.cdf'
    califn = sorted(caldir.glob(f'themis_skymap_{site}_200*.sav'))[0]
    loadit=tio.load(fn=datafn,calfn=califn)
#    datas.append(loadit)  
#for i in datas:
    themisasi(loadit, ax)
#pathofplots='C:/code/themisasi/alltheplotsforgraphicthemis'
#for i in range(pathofplots.glob()):#save as png
#    fig.savefig('plot{i}.png')  
plt.savefig('C:/code/themisasi/alltheplotsforgraphicthemis')#change the format to png needc to include site name and time 
