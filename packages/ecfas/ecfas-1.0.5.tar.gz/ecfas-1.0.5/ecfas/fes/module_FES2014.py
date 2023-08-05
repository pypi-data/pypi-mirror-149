#!/usr/bin/env python
# coding: utf-8
'''
This module contains calls to the FES2014 tide model
'''

import os
import numpy as np
import datetime
import pyfes as fes
import argparse

from numpy import float64

import logging
log = logging.getLogger(__name__)


#------------------------------------------------------------------------------
def init_fes_h(fesdir, prodname='org'):
    file_FES_conf_ocean = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ocean_tide.ini')
    file_FES_conf_load = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'load_tide.ini')
    file_FES_conf_ocean_extrap = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ocean_tide_extrapolated.ini')

    if prodname == 'org':
        short_tide = fes.Handler("ocean", "memory", file_FES_conf_ocean)
    elif prodname == 'extrap':
        short_tide = fes.Handler("ocean", "memory", file_FES_conf_ocean_extrap)
    radial_tide = fes.Handler("radial", "memory", file_FES_conf_load)
    log.info('* init FES2014 tide model')
    return short_tide, radial_tide

#------------------------------------------------------------------------------
# def compute_uv_tide_FES(date, lon, lat, eastward_velocity, northward_velocity):

#     log.info('- compute tide currents for '+str(date))
#     lon=float64(lon); lat=float64(lat)
#     lons, lats = np.meshgrid(lon, lat)
#     npj,npi=lons.shape
#     dates = np.empty(lons.shape, dtype='datetime64[us]')
#     dates.fill(date)

#     u, lp   = eastward_velocity.vector(lats.ravel(), lons.ravel(), dates.ravel())
#     v, _    = northward_velocity.vector(lats.ravel(), lons.ravel(), dates.ravel())

#     # convert result in m/s
#     u=u*0.01 ; v=v*0.01
#     u = u.reshape((npj, npi))
#     v = v.reshape((npj, npi))
#     return u, v

# #-----------------------------------------------------------------------------
# def compute_uv_tide_FES(date, lon, lat, eastward_velocity, northward_velocity):
#     # test version to save time
#         log.info('- compute tide currents for '+str(date))
#         lon=float64(lon); lat=float64(lat)
#         lons, lats = np.meshgrid(lon, lat)
#         npj,npi=lons.shape
#         dates = np.empty(lons.shape, dtype='datetime64[us]')
#         dates.fill(date)

#         u, lp   = eastward_velocity.vector(lats.ravel(), lons.ravel(), dates.ravel())
#         v, _    = northward_velocity.vector(lats.ravel(), lons.ravel(), dates.ravel())

#         # convert result in m/s
#         u=u*0.01 ; v=v*0.01
#         u = u.reshape((npj, npi))
#         v = v.reshape((npj, npi))
#         return u, v


#------------------------------------------------------------------------------
def compute_geo_tide_FES(date, lon, lat, short_tide, radial_tide):  # compute FES tide for a grid. we normally have more locations than times, this could be smart to do...

    log.info('- compute tide elevation for ' + str(date))
    lon = float64(lon); lat = float64(lat)
    lons, lats = np.meshgrid(lon, lat)
    npj, npi = lons.shape
    dates = np.empty(lons.shape, dtype='datetime64[us]')
    dates.fill(date)

    tide, lp = short_tide.vector(lats.ravel(), lons.ravel(), dates.ravel())
    load, _ = radial_tide.vector(lats.ravel(), lons.ravel(), dates.ravel())

    # convert result in meters
    geo_tide = (tide + lp + load) * 0.01
    geo_tide = geo_tide.reshape((npj, npi))
    return geo_tide


def compute_geo_tide_FES_array(dates, lon, lat, short_tide, radial_tide):  # compute FES tide for one position, for a number of times
    lons = np.empty(len(dates), dtype=float64)
    lats = np.empty(len(dates), dtype=float64)
    lons.fill(lon)
    lats.fill(lat)
    tide, lp, _ = short_tide.calculate(lons, lats, dates.astype(dtype='datetime64[us]'))
    load, _, _ = radial_tide.calculate(lons, lats, dates.astype(dtype='datetime64[us]'))

    # convert result in meters
    geo_tide = (tide + lp + load) * 0.01

    # geo_tide = np.ma.masked_where(np.isnan(geo_tide), geo_tide)

    return geo_tide