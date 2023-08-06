#!/usr/bin/env python3
"""
Created on Thu Feb  4 14:53:13 2021

@author: mirazoki

wave setup and runup parameterizations
"""
import logging

import cartopy
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from matplotlib.gridspec import GridSpec
from mpl_toolkits.axes_grid1 import make_axes_locatable
from scipy.spatial import cKDTree as KDTree

import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

log = logging.getLogger(__name__)


def shoal_K(T0, h):
    L0 = (9.81 * T0 ** 2) / 2 / np.pi
    a = h / L0
    # obtain the deep water equivalent wave height through linear wave theory.
    Ks = 1 / np.sqrt(np.tanh(2 * np.pi * a) * (1 + 4 * np.pi * a / np.sinh(4 * np.pi * a)))
    return Ks


def shoal_K_GL(a):
    # obtain the deep water equivalent wave height through linear wave theory.Green's law for shallow waters
    Ks = 1 / np.sqrt(np.sqrt(a * 2 * np.pi) * (1 + 4 * np.pi * a / np.sinh(4 * np.pi * a)))
    return Ks


def stockdon(H0, T0, beta=0.01):  # most common slope for sandy beaches, comparable to EU median in Athanasios
    L0 = (9.81 * T0 ** 2) / 2 / np.pi
    wsteep = H0 / L0
    irb = beta / (wsteep ** 0.5)
    diss = irb < 0.3
    # initialize
    eta = np.zeros(H0.shape)
    S_ig = np.zeros(H0.shape)
    S_inc = np.zeros(H0.shape)
    R2 = np.zeros(H0.shape)

    # general formulation
    eta = 0.35 * beta * (H0 * L0) ** 0.5
    S_ig = 0.06 * (H0 * L0) ** 0.5
    S_inc = 0.75 * beta * (H0 * L0) ** 0.5

    # substitue where dissipative
    eta[diss] = 0.016 * (H0[diss] * L0[diss]) ** 0.5
    S_ig[diss] = 0.046 * (H0[diss] * L0[diss]) ** 0.5
    S_inc[diss] = 0.0

    # runup
    R2 = 1.1 * (eta + 0.5 * (S_ig + S_inc))
    return eta, S_ig, S_inc, R2, irb


def Hsprop(H0, cte=0.2):
    eta = cte * H0
    S_ig = np.zeros(H0.shape)
    S_inc = np.zeros(H0.shape)
    R2 = np.zeros(H0.shape)
    irb = np.zeros(H0.shape)

    return eta, S_ig, S_inc, R2, irb


def slopes_athan(lonarray, latarray):
    # read slopes from Athanasios dataset
    filename = r'/homelocal2/mirazoki/ECFAS/data/Slopes/nearshore_slopes_lo.csv'
    dataslopes = pd.read_csv(filename, sep=',', delimiter=None, index_col=None)

    # find the closest non-nan given certain distance. also discard other dodgy values (only pick 0 and 6)
#   			0: No errors or warnings
# 				1: Error- Number of cross-shore underwater points not enough for analysis
# 				2: Warning - DoC deeper that most deep offshore point (used that one as DoC)
# 				3: Error - Shoreline point not found
# 				4: Error - DoC point not found
# 				5: Warning - Negative calculated  slope
# 				6: Warning - Really steep slope (step) close to MSL
# 				7: Error - No DoC estimation available
# 				8: Warning 1 and 6

    dataslopes = dataslopes.loc[dataslopes['error_code'].isin([0, 6])]
    coords = np.column_stack((dataslopes['X'].values, dataslopes['Y'].values))  # either this, or I need to extrapolate the data first...
    kdslope = KDTree(coords)
    coordsreq = np.hstack((lonarray.reshape(lonarray.size, 1), (latarray.reshape(latarray.size, 1))))
    dist, i = kdslope(coordsreq)
    reqslopes = dataslopes['slope'].iloc[i]
    return reqslopes

    # #plot to check
    # bbox=[-32,35,25,80]
    # figid=plt.figure(figsize=(12,12))
    # axloc = plt.gca(projection=ccrs.PlateCarree())
    # axloc.add_feature(cartopy.feature.LAND.with_scale('10m'),facecolor='gray',zorder=-1,alpha=1, edgecolor='black')
    # axloc.set_extent(bbox)
    # im=axloc.scatter(dataslopes['X'],dataslopes['Y'],10,dataslopes['slope'],cmap='jet',vmin=0,vmax=1,transform=ccrs.PlateCarree())
    # im2=axloc.scatter(lonarray,latarray,10,transform=ccrs.PlateCarree())

    # figid.colorbar(im,orientation='vertical')

    # bbox=[-32,35,25,80]
    # figid=plt.figure(figsize=(12,12))
    # axloc = plt.gca(projection=ccrs.PlateCarree())
    # axloc.add_feature(cartopy.feature.LAND.with_scale('10m'),facecolor='gray',zorder=-1,alpha=1, edgecolor='black')
    # axloc.set_extent(bbox)
    # im=axloc.scatter(lonarray,latarray,10,transform=ccrs.PlateCarree())
    # figid.colorbar(im,orientation='vertical')

    # request model locations
    kdist, indx = kdslope.query(np.vstack((lonarray, latarray)).T)
    kdist, indx = kdslope.query(np.vstack((lonarray[0], latarray[0])).T)

    beta = dataslopes['slope'].iloc[indx].values

    beta[kdist >= 0.1] = np.nan

    return beta

# T0=10
# h=np.arange(1,300)

# L0=(9.81*T0**2)/2/np.pi
# a=h/L0

# Kslist=np.array([shoal_K(ai) for ai in a])
# Kslist_GL=np.array([shoal_K_GL(ai) for ai in a])

# fig=plt.figure(1)
# plt.plot(a,Kslist,'-r')
# ax.plot(a,Kslist_GL,'-g')
# ax=plt.gca()
# ax.semilogx()

# fig=plt.figure(2)
# plt.plot(a,Kslist_GL)
# ax=plt.gca()
# ax.semilogx()
