#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 16:21:43 2021

@author: mirazoki
"""
from _ast import Try
import datetime
import glob
import itertools
import logging
import os
import sys

import ecfas.cmems_datasets as dsets
import ecfas.fes.module_FES2014 as fes
import ecfas.swash_formulations as sf
import ecfas.utils as utils
import netCDF4 as nc
import numpy as np
import xarray as xr
import pandas as pd
from scipy.spatial import cKDTree as KDTree

log = logging.getLogger(__name__)


def split_by_chunks(dataset):
    chunk_slices = {}
    for dim, chunks in dataset.chunks.items():
        slices = []
        start = 0
        for chunk in chunks:
            if start >= dataset.sizes[dim]:
                break
            stop = start + chunk
            slices.append(slice(start, stop))
            start = stop
        chunk_slices[dim] = slices
    for slices in itertools.product(*chunk_slices.values()):
        selection = dict(zip(chunk_slices.keys(), slices))
        yield dataset[selection]
        
def get_MDT(region,maskdir,coords):
    if 'ARC' in region:
        data=xr.open_mfdataset(os.path.join(maskdir,'MDT_CNES_CLS18.nc'))
        longitude=data['longitude'].values
        mdtobsval=data['mdt'].isel(time=0).values
        
        left=longitude>180
        right=longitude<=180
        lonnew=np.hstack((longitude[left]-360,longitude[right]))
        # Xobs,Yobs=np.meshgrid(lonnew,data['latitude'])        
        mdtobsnew=np.hstack((mdtobsval[:,left],mdtobsval[:,right]))
        data=xr.Dataset(
            data_vars={'mdt':(['latitude','longitude'], mdtobsnew) ,
                    },
                    coords=dict(
                        longitude=lonnew,
                        latitude=data['latitude'].values,
                    ),
                    attrs=data.attrs,
                )        
    else:
        data=xr.open_mfdataset(os.path.join(maskdir,'%s_mdt.nc' %region))
    plotfield=data['mdt']#example field
    maskfield=np.isnan(plotfield.values)
    maskarr=np.ravel(maskfield)
    [LON,LAT]=np.meshgrid(data['longitude'],data['latitude'])
    lonarr=np.ravel(LON) #LONw and LATwl alwys in lo,lat coordinates
    latarr=np.ravel(LAT)
    # mdtarr=np.ravel(plotfield)[~maskarr]
    coordsmdt=np.column_stack((lonarr[~maskarr],latarr[~maskarr])) #either this, or I need to extrapolate the data first...
    kdwl=KDTree(coordsmdt)
    kdist, indxwl = kdwl.query(coords)
    # outmdt=mdtarr[indxwl]
    lon_xr = xr.DataArray(coordsmdt[indxwl,0], dims='stations')
    lat_xr = xr.DataArray(coordsmdt[indxwl,1], dims='stations')   

    outdata=plotfield.sel(longitude= lon_xr, latitude = lat_xr,method='nearest')
    
    return outdata


def coast_water_level_process(region, tsdir, outdir, label,maskdir, swashtype='cte', betatype='None', fes_tide=None):

    filename = glob.glob(os.path.join(tsdir, 'tseries_coastal_%s_*.nc' % (label)))[0]

    if len(filename) == 0:
        log.error('Error. Timeseries file %s is empty. Stopping analysis' % filename)
        os.system.exit(1)

    datamodel = xr.open_dataset(filename)
    if 'longitude' in datamodel.variables.keys():
             datamodel = datamodel.rename({'longitude':'lon', 'latitude':'lat'})
    for coordi in datamodel.coords:
        if coordi not in ['lon','lat','stations','time']:
            datamodel=datamodel.drop_vars([coordi])

    phy_var = dsets.datasets_hydro[region]['var'][0]
    # change PHYvar to standard 'zos' for all domains
    if phy_var in datamodel.variables.keys():
        datamodel = datamodel.rename({phy_var:'zos'})
    # make stnames the stations coordinate
    datamodel = datamodel.assign_coords(stations=datamodel['stnames'].values)

    encodingspec = dict()
    # check if other elements need loading up
    if fes_tide is not None:
        # include FES tide at closest point
        # build kdtree
        examplegrid = os.path.join(fes_tide['fesdir'], 'ocean_tide/m2.nc')
        fessample = xr.open_dataset(examplegrid)
        # plt.pcolormesh(fessample['lon'],fessample['lat'],fessample['amplitude'])
        Xfes, Yfes = np.meshgrid(fessample['lon'], fessample['lat'])
        # plt.pcolormesh(Xfes,Yfes,fessample['amplitude'])
        maskfes = np.isnan(fessample['amplitude'])
        xfesarr = Xfes[~maskfes].flatten()
        yfesarr = Yfes[~maskfes].flatten()
        coordsfes = np.column_stack((xfesarr, yfesarr))  # either this, or I need to extrapolate the data first...
        kdfes = KDTree(coordsfes)

        lonr = datamodel['lon'].values.copy()
        lonr[lonr < 0] = lonr[lonr < 0] + 360
        latr = datamodel['lat'].values.copy()

        kdist, indxfes = kdfes.query(np.hstack((np.reshape(lonr, (lonr.size, 1)), np.reshape(latr, (latr.size, 1)))))

        # initialize tide
        tideseries = np.ones(datamodel['zos'].values.shape) * np.nan
        for ipoint, ix in enumerate(indxfes):
            tideseries[ipoint,:] = fes.compute_geo_tide_FES_array(datamodel['time'].values, xfesarr[ix], yfesarr[ix], fes_tide['short_tide'], fes_tide['radial_tide'])

        tideseries_xr = xr.DataArray(
            data=tideseries,  # initialize to zero
            dims=datamodel.dims,
            coords=datamodel.coords,
            attrs={'standard_name': 'tide_FES',
                'long_name': 'tide retrieved from FES 2014 model',
                'units':'m'})

        xrtwl = datamodel['zos'] + tideseries_xr
        datamodel['zos'] = xrtwl

    if region == 'ARC':
        fileocean = filename.replace(region, 'ARC_ocean')
        if not os.path.exists(fileocean):
            log.error('Missing OCEAN file for t0 %s' % label)
            sys.exit(1)
        else:
            datamodel_ocean = xr.open_dataset(fileocean)
            ovar = dsets.datasets_hydro['ARC_ocean']['var'][0]
            # rename things
            if 'longitude' in datamodel_ocean.variables.keys():
                datamodel_ocean = datamodel_ocean.rename({'longitude':'lon', 'latitude':'lat'})
            for coordi in datamodel_ocean.coords:
                if coordi not in ['lon','lat','stations','time']:
                    datamodel_ocean=datamodel_ocean.drop_vars([coordi])
            if ovar in datamodel_ocean.variables.keys():
                datamodel_ocean = datamodel_ocean.rename({ovar:'zos'})

            coordswl = np.column_stack((datamodel['lon'].values, datamodel['lat'].values))  # either this, or I need to extrapolate the data first...
            coordswl_ocean = np.column_stack((datamodel_ocean['lon'].values, datamodel_ocean['lat'].values))  # either this, or I need to extrapolate the data first...

            kdwlocean = KDTree(coordswl_ocean)
            kdist, indxwl = kdwlocean.query(coordswl)

            toceaninterp = datamodel_ocean['zos'].isel(stations=indxwl)
            toceaninterp=toceaninterp.assign_coords(stations=datamodel['stnames'].values)
            _, index = np.unique(toceaninterp['time'], return_index=True)
            toceaninterp = toceaninterp.isel(time=index)
            _, index = np.unique(datamodel['time'], return_index=True)
            datamodel = datamodel.isel(time=index)

            xrtwl = datamodel['zos'] + toceaninterp.interp(time=datamodel['time'])  # maybe I need to interpolate to common times?
            datamodel['zos'] = xrtwl

    #make unique
    coords_coast=np.vstack((datamodel['lon'].values,datamodel['lat'].values)).T
    unlist,unidx=np.unique(coords_coast,axis=0,return_index=True)
    unidxs=np.sort(unidx)
    datamodel=datamodel.isel(stations=unidxs)
    
    #add MDT
    coords=np.vstack((datamodel['lon'].values,datamodel['lat'].values)).T
    mdt=get_MDT(region,maskdir,coords)
    if 'longitude' in mdt.coords:
        mdt=mdt.rename({'longitude':'lon', 'latitude':'lat'})
    mdt=mdt.assign_coords(lon=datamodel['lon'],lat=datamodel['lat'])
    datamodel['zos']=datamodel['zos']-mdt
    
    # add wave contributions
    # initialize
    datasetup_xr = xr.DataArray(
        data=np.zeros(datamodel['zos'].shape),  # initialize to zero
        dims=datamodel.dims,
        coords=datamodel.coords,
        attrs={'standard_name': 'wave_setup',
                'units':'m'}
        )

    datamodel = datamodel.assign(Vsetup=datasetup_xr.transpose("stations", "time"))
    if swashtype == 'cte':
        eta, _, _, R, irb = sf.Hsprop(datamodel['VHM0'].values)
        betatype = 'dissipative'
    elif swashtype == 'stockdon':
        if betatype is None:
            beta = np.zeros(datamodel[phy_var].shape)  # force the dissipative formulation of stockdon
            betatype = 'dissipative'
        elif betatype == 'Athanasios':
            beta = sf.slopes_athan(datamodel['lon'].values, datamodel['lat'].values)
        beta[np.isnan(beta)] = 0.0  # force it to be dissipative,beta independent
        eta, _, _, R, irb = sf.stockdon(datamodel['VHM0'].values,
                                           datamodel['VTPK'].values, beta=beta)

    datamodel['Vsetup'].values = eta
    datamodel['Vsetup'].attrs['long_name'] = 'wave setup calculated using %s parameterization and %s slope' % (swashtype, betatype)

    # add enconding
    encodingspec["Vsetup"] = {"dtype": 'int16',
                "scale_factor": float(0.001),
                "add_offset": float(0.0),
                "_FillValue":nc.default_fillvals['i2'],
                # 'chunksizes': []
                }
    datamodel.encoding['zlib'] = True  # Conserved

    datamodel.attrs['easting'] = 'lon'
    datamodel.attrs['northing'] = 'lat'

    if not os.path.exists(outdir):
        os.mkdir(outdir)
    # write out independent days
    dayarray = pd.date_range(start=datamodel.indexes['time'][0], end=datamodel.indexes['time'][-1], freq='1D', closed='left')
    bday = datetime.datetime.strptime(label, '%Y-%m-%d_%H-%M-%S').strftime('%Y%m%d%H%M%S')
    for iday in dayarray:
        tini = iday.to_pydatetime()
        tend = (iday.to_pydatetime() + datetime.timedelta(hours=23))
        dataday = datamodel.sel(time=slice(tini, tend))
        if dataday.dims['time'] > 0:
            fileout = 'TScoast_%s_b%s_%s_%s.nc' % (region, bday, tini.strftime('%Y%m%d'), (tend + datetime.timedelta(hours=1)).strftime('%Y%m%d'))
            dataday.to_netcdf(os.path.join(outdir, fileout), encoding=encodingspec)

    # // TODO: Check result of check and possibly stop?
    utils.check_timeseries_output_size(os.path.join(outdir, fileout), dsets.datasets_hydro[region]['tsdsize'], 0.25)

    log.info('=====Time series for %s: label %s  processed\n=====' % (region, label))

    return os.path.join(outdir, fileout)