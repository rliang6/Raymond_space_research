# -*- coding: utf-8 -*-
"""
Created on Fri Sep 21 14:13:06 2018

@author: Raymond
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Aug 21 16:01:51 2018
@author: Raymond Liang
"""
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
from os import path
import argparse
from datetime import date
from datetime import time
from datetime import datetime, timedelta
from typing import List

PC = ccrs.PlateCarree()
ST = ccrs.Stereographic()
MR = ccrs.Mercator()
def datetimerange(start: datetime, stop: datetime, step: timedelta) -> List[datetime]:
    """
    generates range of datetime start,stop,step just like range() for datetime
    """
    return [start + i*step for i in range((stop-start) // step)]
def themisasi(dat, ax): #function used to save plots 
        
    imgs = dat['imgs'].squeeze()
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
    
    
    firstnan=np.nonzero(mask.any(axis=1))[0]
    ax.pcolormesh(lon[firstnan[0]:firstnan[-1], :], lat[firstnan[0]:firstnan[-1], :], 
              imgs[firstnan[0]:firstnan[-1], :], transform=PC)
    
     #filename
#     
caldir = Path("c:\code") / 'themisasi' / 'asf_folder_with_calibration'
datadir = Path('C:\code') / 'themisasi' / 'testfolderforgraphicalthemis'

p=argparse.ArgumentParser('the container used for storing the name of sites')
p.add_argument('sites', nargs='+', help='names of sites')
p.add_argument('-t','--time', nargs='+', required=True)
p.add_argument('-i', '--interval', help='time interval (seconds)', type=float, default=1.)
p=p.parse_args()  
datas=[]
sites=p.sites
start=parse(p.time[0])
stop=parse(p.time[1])
timedelta=timedelta(seconds = p.interval)
rangedate=datetimerange(start,stop,timedelta)
for site in sites:
    ta.download('2008-03-26T07', site , 'C:\code\data')
f=plt.figure()
ax=f.gca(projection=MR)
ax.set_extent((-180,-35,25,75))
ax.gridlines()
ax.coastlines()
datadir='C:\code\data'
for t in rangedate:
    for site in sites:#loading the sites which return xarrays
        try:
            loadit=tio.load(datadir,site,'2008-03-26T07')
        except ValueError:
            continue
        except FileNotFoundError:
            continue
        
        themisasi(loadit, ax) 
    plt.savefig('C:/alltheplotsforgraphicthemis/multiplethemis%s%s%s.png' %(t.hour,t.minute,t.second))
