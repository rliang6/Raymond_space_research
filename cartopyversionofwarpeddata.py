#!/usr/bin/env python
"""
Created on Thu Aug 16 10:43:42 2018

@author: Raymond
"""
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import dascutils.io as dio
import pymap3d as pm
from pathlib import Path

PC = ccrs.PlateCarree()
ST = ccrs.Stereographic()
MR = ccrs.Mercator()
R = Path('~/code/dascutils/').expanduser()

dat = dio.load(R/'tests', R/'cal/PKR_DASC_20110112')
img = dat[428].isel(time=1).values
# %% coord conv.
alt = 100000
srange = alt/np.sin(np.radians(dat.el.values))
lat, lon, alt = pm.aer2geodetic(dat.az.values, dat.el.values, srange,
                                dat.lat, dat.lon, 0)

mask = np.isfinite(lat)
top = None
for i, m in enumerate(mask):
    good = m.nonzero()[0]

    if good.size == 0:
        continue
    elif top is None:
        top = i

    lat[i, good[-1]:] = lat[i, good[-1]]
    lat[i, :good[0]] = lat[i, good[0]]

    lon[i, good[-1]:] = lon[i, good[-1]]
    lon[i, :good[0]] = lon[i, good[0]]

lat[:top, :] = lat[top, 256]
lon[:top, :] = lon[top, 256]

print('plotting', dat.filename)


ax = plt.axes(projection=MR)
ax.set_extent((-180, -120, 50, 75))
ax.gridlines()
ax.coastlines()
ax.pcolormesh(lon[:400, :], lat[:400, :], img[:400, :], transform=PC)
plt.show()
