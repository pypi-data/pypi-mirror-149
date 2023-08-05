#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 16:10:11 2021

@author: mirazoki

combining forecasted fields at coastal locations

steps (special treatment for arctic, leave out for now)
in all other locations, we take the PHY coastal points and interpolate the wave quantities at those locations

1. retrieve WLs
2. retrieve waves at those same points. 
-ideally, we just save he weights of the regridding so that this is only done once
-because of nan values, it might be that we have to drop the idea of griddedinterpolant and just use Delaunay. For Delaunay, one can save weights.
-test for speed (interpolating every time between regular grids might give better performance than saving the delaunay interpolation, but Nan performance has to be checked)
-maybe interpolation in time is needed if wave params are outputted at a different time-stamp
"""

import datetime
from functools import partial
import logging
import os

import matplotlib
from scipy import interpolate
from scipy.interpolate import LinearNDInterpolator
from scipy.interpolate import NearestNDInterpolator
from scipy.spatial import Delaunay
from scipy.spatial import cKDTree as KDTree

import ecfas.cmems_datasets as dsets
import ecfas.utils as utils
import multiprocessing as mp
import netCDF4 as nc
import numpy as np
import pandas as pd
import xarray as xr

log = logging.getLogger(__name__)


def saveConcatenatedNC(datadir, PHYvar, label, fperiods, fperiode, filename):

    listfilesWL = np.array([os.path.join(datadir, 'data', '%s_%s_%s_%s.nc' % (PHYvar, label, fperiods[ii].strftime('%Y-%m-%d_%H-%M-%S'), fperiode[ii].strftime('%Y-%m-%d_%H-%M-%S'))) for ii in np.arange(len(fperiods))])

    ds = xr.open_mfdataset(listfilesWL)
    _, index = np.unique(ds['time'], return_index=True)
    ds = ds.isel(time=index)

    path = os.path.join(datadir, "data", filename)
    log.info("Temp file saved in: %s", path)
    ds.to_netcdf(path)


def calc_interp(itime, ncdataWAV, maskarr, coords_coast, tri):
    rav = np.ravel(ncdataWAV[itime])[~maskarr]
    interpolator = LinearNDInterpolator(tri, rav)
    interpolator_nearest = NearestNDInterpolator(tri, rav)
    dataint = interpolator(coords_coast)
    dataint[np.isnan(dataint)] = interpolator_nearest(coords_coast[np.isnan(dataint)])

    # if still nan values, it means it is ice - make it -9999
    dataint[np.isnan(dataint)] = -9999

    return dataint


def getLonLatData(data, sel, lon_xr="", lat_xr=""):
    datadim = data.dims

    if 'lat' in datadim:
        lon = data['lon']
        lat = data['lat']
        datawl = sel(lon=lon_xr, lat=lat_xr, method='nearest')

    elif 'latitude' in datadim:
        lon = data['longitude']
        lat = data['latitude']
        datawl = sel(longitude=lon_xr, latitude=lat_xr, method='nearest')

    elif 'x' in datadim:
        lon = data['x']
        lat = data['y']
        datawl = sel(x=lon_xr, y=lat_xr, method='nearest')

    if len(lon.shape) <= 1:
        lon, lat = np.meshgrid(lon, lat)

    return lon, lat, datawl

def getLonLatVars(data, sel):
    datadim = data.variables

    if 'lat' in datadim:
        lon = data['lon']
        lat = data['lat']

    elif 'latitude' in datadim:
        lon = data['longitude']
        lat = data['latitude']

    elif 'x' in datadim:
        lon = data['x']
        lat = data['y']

    if len(lon.shape) <= 1:
        lon, lat = np.meshgrid(lon, lat)

    return lon, lat


def coast_water_level_extract_multiple(datadir, outdir, maskdir, region, label, fstart, fend, addwave, dsettype='fcst'):

    if dsettype == 'fcst':
        dsethyd = dsets.datasets_hydro
        dsetwav = dsets.datasets_wave
    elif dsettype == 'reanal':
        dsethyd = dsets.datasets_hydro_reanal
        dsetwav = dsets.datasets_wave_reanal
    PHYvar = dsethyd[region]['var'][0]
    WAVvar = 'VHM0'

    fperiods = [fstart + datetime.timedelta(days=float(ii)) for ii in np.arange((fend - fstart).total_seconds() / 86400)]
    fperiode = [fperiodsi + datetime.timedelta(days=1) for fperiodsi in fperiods]

    saveConcatenatedNC(datadir, PHYvar, label, fperiods, fperiode, PHYvar + ".nc")
    if addwave:
        saveConcatenatedNC(datadir, "WAVsubset", label, fperiods, fperiode, "wav.nc")

    if not os.path.exists(outdir):
        os.mkdir(outdir)

    filepoints = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output_points/output_locs_%s.txt' % region)
    data = pd.read_csv(filepoints, sep='\t')
    lond = data.iloc[:, 0].values
    latd = data.iloc[:, 1].values
    names_coast = data.iloc[:, 2].values
    coords_coast = np.vstack((lond, latd))

    # PHY(alternative) colocate using coordinates. what is dangerous is that if grid changes slightly, then we might hit a land (masked) point
    lon_xr = xr.DataArray(lond, dims='stations')
    lat_xr = xr.DataArray(latd, dims='stations')

    ncdata = xr.open_dataset(datadir + '/data/' + PHYvar + ".nc")  # concatenated in time
    LONwl, LATwl = getLonLatVars(ncdata, ncdata.sel)
    datadim = ncdata.dims

    # check is any items fell on masked land
    # if (('rlon', 'x') in datadim) or datawl[PHYvar].isel(time=0).any():
        # use kdtree instead of the non-nan model points
    maskarr = np.ravel(ncdata[PHYvar].isel(time=0).isnull())

    # LONw and LATwl alwys in lo,lat coordinates
    lonarr = np.ravel(LONwl)
    latarr = np.ravel(LATwl)

    # either this, or I need to extrapolate the data first...
    coordswl = np.column_stack((lonarr[~maskarr], latarr[~maskarr]))
    kdwl = KDTree(coordswl)
    kdist, indxwl = kdwl.query(coords_coast.T)

    lon_xr = xr.DataArray(coordswl[indxwl, 0], dims='stations')
    lat_xr = xr.DataArray(coordswl[indxwl, 1], dims='stations')

    if 'lat' in datadim:
        datawl = ncdata.sel(lon=lon_xr, lat=lat_xr, method='nearest')
    elif 'latitude' in datadim:
        datawl = ncdata.sel(longitude=lon_xr, latitude=lat_xr, method='nearest')
    elif 'x' in datadim:
        # find equivalent rotated coords
        kdreg = KDTree(np.column_stack((lonarr, latarr)))
        _, indxr = kdreg.query(np.column_stack((lon_xr, lat_xr)))

        indxr_mat = np.unravel_index(indxr, (LONwl.shape))
        lati_xr_r = xr.DataArray(indxr_mat[0], dims='stations')
        loni_xr_r = xr.DataArray(indxr_mat[1], dims='stations')

        datawl = ncdata.isel(x=loni_xr_r, y=lati_xr_r)

    # make those too far away nan
    #toofar = np.arange(len(lond))[kdist > 20 / 110]
    #newarr = datawl[PHYvar].values
    #newarr[:, toofar] = np.nan * np.ones(newarr[:, toofar].shape)

    #datawl[PHYvar] = xr.DataArray(
    #        data=newarr.T,
    #        dims=datawl.dims,
    #        coords=datawl.coords,
    #        attrs=datawl[PHYvar].attrs,
    #        )
    #drop those too far away and make unique- can be changed in the future
    not_toofar = np.arange(len(lond))[kdist <= 20 / 110]
    # datawl=datawl.isel(stations=not_toofar)
    # coords_coast=coords_coast[:,not_toofar]

    datatotal = datawl.copy()
    encodingspec = dict()
    encodingspec[dsethyd[region]['var'][0]] = {
                            "dtype": 'int16',
                            "scale_factor": float(0.001),
                            "add_offset": float(0),
                            "_FillValue":nc.default_fillvals['i2'],
                            # 'chunksizes': []
                            }

    if addwave:
        log.info('Extract wave for each parameter in data set')
        wavevarlist = dsetwav[region]['var'][0]

        try:
            ncdata_wav = xr.open_dataset(datadir + '/data/wav.nc')  # concatenated in time
            _, index = np.unique(ncdata_wav['time'], return_index=True)
            ncdata_wav = ncdata_wav.isel(time=index)

            LON, LAT = getLonLatVars(ncdata_wav, ncdata.sel)

            # LON, LAT, _ = getLonLatData(ncdata_wav, lambda **kwargs: None)

            log.info('Interpolate wave params to phy locations')
            # first create the wave kdtree
            # get mask
            lonarr = np.ravel(LON)
            latarr = np.ravel(LAT)
            if 'summer_mask' in dsetwav[region].keys():
                # get mask from predefined field
                if isinstance(dsetwav[region]['summer_mask'], dict):
                    # check for which mask to use
                    for item in dsetwav[region]['summer_mask']:
                        if fstart >= datetime.datetime.strptime(item, '%Y%m%d'):
                            refdata = xr.open_dataset(os.path.join(maskdir, dsetwav[region]['summer_mask'][item]['filename']))
                            refdata = refdata[dsetwav[region]['summer_mask'][item]['var']]
                else:
                    refdata = xr.open_dataset(os.path.join(maskdir, dsetwav[region]['summer_mask']))
                    refdata = refdata['VHM0']

                plotfield = refdata.isel(time=0)  # example field
                tempmask = np.isnan(plotfield.values)  # #WARNING! Wave fields showing time-dependent mask fields (or at least, some invalid points sometimes)
                maskfieldW = tempmask.copy()

                vhmot0 = ncdata_wav['VHM0'].isel(time=0)
                if not tempmask.shape == vhmot0.shape:
                    # if just one row difference, gind nearest neighbor
                    if np.abs(tempmask.shape[0] - vhmot0.shape[0]) <= 1 and np.abs(tempmask.shape[1] - vhmot0.shape[1]) <= 1:
                        # just find nearest
                        [LONmsk, LATmsk] = np.meshgrid(refdata['lon'].values, refdata['lat'].values)
                        lonarrmask = np.ravel(LONmsk)
                        latarrmask = np.ravel(LATmsk)
                        kdmskorg = KDTree(np.vstack((lonarrmask, latarrmask)).T)
                        kdist, indxmsk = kdmskorg.query(np.vstack((lonarr, latarr)).T)
                        maskfieldW = np.ravel(tempmask)[indxmsk]
                        maskfieldW = maskfieldW.reshape(LON.shape)
                    else:
                        raise  RuntimeError('Mask does not fit wave grid. Stop\n')
            else:
                # get mask from this dataset
                plotfield = ncdata_wav['VHM0'].isel(time=0)  # example field
                maskfieldW = np.isnan(plotfield.values)  # #WARNING! Wave fields showing time-dependent mask fields (or at least, some invalid points sometimes)

            maskarr = np.ravel(maskfieldW)
            coords = np.vstack((lonarr[~maskarr], latarr[~maskarr]))  # either this, or I need to extrapolate the data first...

            tri = Delaunay(coords.T)  # Compute the triangulation, so we can reuse it
            dateswa = matplotlib.dates.date2num(ncdata_wav['time'].values)
            dateswl = matplotlib.dates.date2num(ncdata['time'].values)

            transp = coords_coast.T

            pool = mp.Pool()
            for varw in wavevarlist:
                dataWAVfield = np.ones((len(lond), ncdata_wav.dims['time'])) * np.nan

              # colocate in space
                vals = ncdata_wav[varw].values
                result = pool.map(partial(calc_interp, ncdataWAV=vals, maskarr=maskarr, coords_coast=transp, tri=tri), range(len(ncdata_wav['time'])))
                for idx, val in enumerate(result):
                    dataWAVfield[:, idx] = val

                # colocate in time.
                # could interpolate in time in one go by using interp2d (numpoints*time=field)
                f = interpolate.interp2d(dateswa, np.arange(coords_coast.shape[1]), dataWAVfield)
                # no idea what happens if the wave datasets spans less time (i.e. extrapolation). we could always take a day before and after for overlap
                data_wavfield_int = f(dateswl, np.arange(coords_coast.shape[1]))

                # remask
                data_wavfield_int[data_wavfield_int < 0] = np.nan

                data_wavfield_xr = xr.DataArray(
                    data=data_wavfield_int,
                    dims=datawl.dims,
                    coords=datawl.coords,
                    attrs=ncdata_wav[varw].attrs
                )

                datatotal = datatotal.assign({varw:data_wavfield_xr})
                if varw in ['VMDR', 'VPED']:
                    scf = float(0.1)
                else:
                    scf = float(0.01)
                encodingspec[varw] = { "dtype": 'int16',
                                    "scale_factor": scf,
                                    "add_offset": float(0),
                                    "_FillValue": nc.default_fillvals['i2'],
                                    # 'chunksizes': []
                                    }
        except Exception as e:
            log.error(e)
            log.info("Creating an empty dataset")
            for varw in wavevarlist:
                # create empty field, so that file size remains the same always
                data_wavfield_xr = xr.DataArray(
                    data=np.ones(datawl[PHYvar].shape) * np.nan,
                    dims=datawl.dims,
                    coords=datawl.coords
                )
                datatotal = datatotal.assign({varw:data_wavfield_xr})
                scf = float(0.01)
                encodingspec[varw] = { "dtype": 'int16',
                                    "scale_factor": scf,
                                    "add_offset":float(0),
                                    "_FillValue":nc.default_fillvals['i2'],
                                    # 'chunksizes': []
                                    }

    obsnames = xr.DataArray(
        data=np.array(names_coast, dtype='S50'),
        dims=datawl.stations.dims,
        coords=datawl.stations.coords,
        attrs={'standard_name': 'station_name',
                'long_name': 'station_name'}
    )

    datatotal = datatotal.assign(stnames=obsnames)
    datatotal[PHYvar]=datatotal[PHYvar].transpose("stations", "time")
    datatotal=datatotal.isel(stations=not_toofar)
    # rename coordinates to longitude and latitude
    # if 'lon' in datatotal.variables.keys():
    #     datatotal = datatotal.rename({'lon':'longitude', 'lat':'latitude'})

    fileout = 'tseries_coastal_%s_%s_%s.nc' % (label, fperiods[0].strftime('%Y-%m-%d_%H-%M-%S'), fperiode[-1].strftime('%Y-%m-%d_%H-%M-%S'))
    datatotal.encoding['zlib'] = True  # Conserved
    datatotal.to_netcdf(os.path.join(outdir, fileout), encoding=encodingspec)
    # // TODO: Check result of check and possibly stop?
    utils.check_timeseries_output_size(os.path.join(outdir, fileout), dsethyd[region]['tssize'], 0.2)

    log.info('=====Time series for %s: %s /%s generated\n=====' % (region, fperiods[0].strftime('%Y-%m-%d_%H-%M-%S'), fperiode[-1].strftime('%Y-%m-%d_%H-%M-%S')))

    # else:
    #     log.info('=====Files for %s: %s /%s not there yet, will try again next day\n=====' % (region, fperiods[0].strftime('%Y-%m-%d_%H-%M-%S'), fperiode[-1].strftime('%Y-%m-%d_%H-%M-%S')))
