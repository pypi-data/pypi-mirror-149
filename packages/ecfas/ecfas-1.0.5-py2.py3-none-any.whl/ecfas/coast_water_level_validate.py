#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 12:35:23 2021

@author: mirazoki
validation of forecasted WLs
"""
import datetime
import glob
import os
import pathlib
import sys
import urllib
import logging

import cartopy
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib
from matplotlib.gridspec import GridSpec
from mpl_toolkits.axes_grid1 import make_axes_locatable
from scipy import interpolate
from scipy.interpolate import LinearNDInterpolator
from scipy.interpolate import RegularGridInterpolator
from scipy.spatial import Delaunay
from scipy.spatial import cKDTree as KDTree
from scipy.spatial import cKDTree as KDTree

import cartopy.crs as ccrs
import ecfas.cmems_datasets as dsets
import ecfas.download_insitu_obs as dio
import ecfas.swash_formulations
import matplotlib.pyplot as plt
import netCDF4 as nc
import numpy as np
import pandas as pd
import xarray as xr

log = logging.getLogger(__name__)

# import dask
def coast_water_level_validate(reg, PHYvar, outdir, filename, tini, tend, obstype, getobs=True, t0=None, obsdir=None):
            # coast_water_level_validate(region,PHYvar,datadir,outdir,filename,tini,tend,obstype,t0=tsel[ifile])

    zoom = 2  # deg

    if '15min' in reg:
        regobs = reg.replace('_15min', '')
    elif 'tsm' in reg:
        regobs = reg.replace('_tsm', '')
    else:
        regobs = reg

    if obsdir is None:
        obsdir = os.path.join(r'/homelocal2/mirazoki/ECFAS/data/CMEMS/observations/insitu', regobs)

    if not os.path.exists(outdir):
        os.mkdir(outdir)
    #==========================MODEL============================================
    datamodel = xr.open_dataset(filename)

    if 'lon' in datamodel.variables.keys():
        datamodel = datamodel.rename({'lon':'longitude', 'lat':'latitude'})

    kdmodel = KDTree(np.column_stack((datamodel['longitude'].values, datamodel['latitude'].values)))

    # loop over observations and retrieve closest point, and plot!

    #==========================OBS============================================

    searchvars = [['SWHT', 'VSPEC1D'],
                ['SLEV']]
    # outdirobs=os.path.join(obsdir,reg)
    outdirobs = obsdir
    if getobs:
        dio.download_insitu_obs(regobs, tini, tend, obstype='latest', chosen=['TG'], outdir=outdirobs)

    # read observation list from the index files
    colidx = ['product_id', 'file_name', 'geospatial_lat_min', 'geospatial_lat_max', 'geospatial_lon_min', 'geospatial_lon_max', 'time_coverage_start', 'time_coverage_end', 'institution', 'date_update', 'data_mode', 'parameters']
    id_data = pd.read_csv(os.path.join(obsdir, 'index_%s.txt' % (obstype)), sep=',', delimiter=None, header=None, skiprows=6, names=colidx, index_col=None)
    boolvar_PHY = [np.any([vari in row['parameters'] for vari in searchvars[1]]) for ii, row in id_data.iterrows()]

    # if obstype=='monthly' or obstype=='latest':
    #     #just take the unique station names. take first date array for example
    #     # datestr=pathlib.Path(id_data['file_name'].iloc[0]).parts[-2]
    #     datestr=tini.strftime("%Y%m%d")
    #     #filter those for the chosen times
    #     boolvar_un=[datestr in row['file_name'] for ii,row in id_data.iterrows()]
    #     boolvar_PHY=np.array(boolvar_PHY) & np.array(boolvar_un)

    #     listncs=[pathlib.Path(filei).parts[-1].replace('.nc','') for filei in id_data['file_name'].loc[boolvar_PHY]]
    #     listobs=['_'.join(nci.split('_')[0:-1]) for nci in listncs]
    # else:
    #     listobs=[pathlib.Path(filei).parts[-1].replace('.nc','') for filei in id_data['file_name'].loc[boolvar_PHY]]

    if obstype == 'monthly' or obstype == 'latest':
        # just take the unique station names. take first date array for example
        # datestr=pathlib.Path(id_data['file_name'].iloc[0]).parts[-2]
        datestr = tini.strftime("%Y%m%d")
        # filter those for the chosen times
        boolvar_un = [datestr in row['file_name'] for ii, row in id_data.iterrows()]
        if sum(boolvar_un) == 0:  # we are using a id file that doesn't match what we are looking for'
            # take the first date available, use that as ref
            datestr = datetime.datetime.strptime(id_data['time_coverage_start'].iloc[int(id_data.index.size / 2)], '%Y-%m-%dT%H:%M:%SZ')
            datestr = datetime.datetime(datestr.year, datestr.month, datestr.day).strftime("%Y%m%d")
            boolvar_un = [datestr in row['file_name'] for ii, row in id_data.iterrows()]
        boolvar_PHY = np.array(boolvar_PHY) & np.array(boolvar_un)

        listncs = [pathlib.Path(filei).parts[-1].replace('.nc', '') for filei in id_data['file_name'].loc[boolvar_PHY]]
        listobs = ['_'.join(nci.split('_')[0:-1]) for nci in listncs]
    else:
        listobs = [pathlib.Path(filei).parts[-1].replace('.nc', '') for filei in id_data['file_name'].loc[boolvar_PHY]]

    # listobs=glob.glob(os.path.join(obsdir,obstype,'*TG*.nc')) #these are directories

    for ii, iobs in enumerate(listobs):
        # ncobs=glob.glob(os.path.join(iobs,'*SLEV*.nc'))
        # if len(iobs)>0:
        if obstype == 'latest':
            # concatenate by day
            listfiles = glob.glob(os.path.join(obsdir, obstype, '**', iobs + '*.nc'))
            # listfiles=glob.glob(os.path.join(obsdir,obstype,iobs + '*.nc'), recursive=True)
            listfiles.sort()

            if len(listfiles) > 0:
                # do it manually, not mf dataset
                listxr = []
                for i, filei in enumerate(listfiles):
                    datai = xr.open_dataset(filei, drop_variables=['POSITION', 'POSITION_QC'])
                    datai = datai.isel(LONGITUDE=0, LATITUDE=0, DEPTH=0)
                    listxr.append(datai)
                try:
                    dataobs = xr.concat(listxr, dim='TIME')
                except:
                    log.warning(' Could not manage to concatenate observations. Skip station\n')
                    continue  # go to next station
            else:
                continue  # go to next station

            # dataobs=xr.open_mfdataset(listfiles,concat_dim='TIME',data_vars=['SLEV'],coords='all',compat="override")
        # elif obstype=='monthly':
        #     dataobs=xr.open_dataset(os.path.joiniobs)
        # elif obstype=='history':
        #     dataobs=xr.open_dataset(os.path.joiniobs)
        # CLIP to given timeframe

        # make unique in time
        _, index = np.unique(dataobs['TIME'], return_index=True)
        dataobs = dataobs.isel(TIME=index)
        datasel = dataobs.sel(TIME=slice(tini.strftime("%Y-%m-%d"), tend.strftime("%Y-%m-%d")))
        if datasel.dims['TIME'] > 0:
            log.debug(iobs)

            try:
                # some data found. interpolate model values to the available observed times and geo location
                # dist,i=kdmodel.query(np.array([np.squeeze(datasel.LONGITUDE[0].values),np.squeeze(datasel.LATITUDE[1].values)]),distance_upper_bound=0.25)
                dist, i = kdmodel.query(np.array([np.squeeze(datasel.LONGITUDE.values), np.squeeze(datasel.LATITUDE.values)]), distance_upper_bound=0.25)

                if not np.isinf(dist):
                    datamodeli = datamodel.isel(stations=i)
                    # plot!
                    datesmod = matplotlib.dates.date2num(datamodeli['time'].values)
                    datesobs = matplotlib.dates.date2num(datasel['TIME'].values)

                    # #stats

                    # errarray=mdata_intp[~nanobs]-obsdata.values[~nanobs]
                    # stats=dict()
                    # stats['bias']=np.mean(errarray)
                    # stats['std']=np.std(errarray)
                    # stats['stdobs']=np.std(obsdata.values[~nanobs])
                    # stats['stdmod']=np.std(mdata_intp[~nanobs])
                    # stats['rmse']=np.sqrt(np.square(stats['std'])+np.square(stats['bias']))
                    # rpears=np.corrcoef(obsdata.values[~nanobs],mdata_intp[~nanobs])
                    # stats['rpears']=rpears[0,1]

                    figid = plt.figure(figsize=(12, 12))
                    gs = GridSpec(3, 2, width_ratios=[3, 1])
                    axloc = plt.subplot(gs[:, 1], projection=ccrs.PlateCarree())
                    axloc.add_feature(cartopy.feature.LAND.with_scale('10m'), facecolor='gray', zorder=-1, alpha=1, edgecolor='black')
                    axloc.set_extent([datamodeli.longitude.values - zoom, datamodeli.longitude.values + zoom, datamodeli.latitude.values - zoom, datamodeli.latitude.values + zoom], ccrs.PlateCarree())
                    axloc.plot(datamodeli.longitude.values, datamodeli.latitude.values, color='blue', linewidth=2, marker='o', transform=ccrs.PlateCarree(), label='mod')
                    # axloc.plot(datasel.LONGITUDE[0].values,datasel.LATITUDE[0].values,color='red', linewidth=2, marker='*',transform=ccrs.PlateCarree(),label='obs')
                    axloc.plot(datasel.LONGITUDE.values, datasel.LATITUDE.values, color='red', linewidth=2, marker='*', transform=ccrs.PlateCarree(), label='obs')

                    axloc.legend()

                    # for now, bias correct
                    ax1 = plt.subplot(gs[0, 0])
                    ax1.plot_date(datesobs, datasel['SLEV'].values - np.nanmean(datasel['SLEV'].values), linestyle='--', color='k', marker=None, label='obs', zorder=10)
                    ax1.plot_date(datesmod, datamodeli[PHYvar].values - np.nanmean(datamodeli[PHYvar].values), linestyle='-', color='b', marker=None, label='model', zorder=0)
                    # ax1.plot_date(datesmod,datamodeli['zos'].values-np.mean(datamodeli['zos'].values)+datamodeli['Vsetup'].values,linestyle='-',color='c',marker=None,label='model+setup')
                    # ax1.plot_date(datesmod,datamodeli['zos'].values-np.mean(datamodeli['zos'].values)+datamodeli['VHM0'].values*0.2,linestyle='-',color='g',marker=None,label='model+0.2Hs')
                    # ax1.plot_date(dateswl,datamodeli['zos'].values-np.mean(datamodeli['zos'].values)+datamodeli['Vsetup'].values+datamodeli['VS_ig'].values+datamodeli['VS_inc'].values,linestyle='-')
                    try:
                        ax1.set_ylim([np.floor(np.nanmin(datasel['SLEV'].values - np.nanmean(datasel['SLEV'].values))), np.ceil(np.nanmax(datasel['SLEV'].values - np.nanmean(datasel['SLEV'].values)))])
                    except:
                        try:
                            ax1.set_ylim([np.floor(np.nanmin(datamodeli[PHYvar].values - np.nanmean(datamodeli[PHYvar].values))), np.ceil(np.nanmax(datamodeli[PHYvar].values - np.nanmean(datamodeli[PHYvar].values)))])
                        except:
                            ax1.set_ylim([-1, 1])
                    ax1.xaxis.set_tick_params(rotation=45)
                    ax1.legend(loc='lower right')
                    ax1.set_ylabel('TWL[m]')

                    if 'VHM0' in datamodeli.variables.keys():
                        # for now, bias correct
                        ax2 = plt.subplot(gs[1, 0])
                        ax2.plot_date(datesmod, datamodeli['VHM0'].values, linestyle='-', color='c', marker=None, label='Hs')
                        # ax2.plot_date([matplotlib.dates.date2num(t0),matplotlib.dates.date2num(t0)],[-10,10],'--r')
                        try:
                            ax2.set_ylim([np.floor(np.nanmin(datamodeli['VHM0'].values)), np.ceil(np.nanmax(datamodeli['VHM0'].values))])
                        except:
                            ax2.set_ylim([0, 1])

                        ax2.legend(loc='lower right')
                        ax2.set_ylabel('Hs[m]')
                        ax2.xaxis.set_tick_params(rotation=45)

                        # for now, bias correct
                        ax3 = plt.subplot(gs[2, 0])
                        ax3.plot_date(datesmod, datamodeli['VTPK'].values, linestyle='-', color='g', marker=None, label='Tp')
                        # ax3.plot_date([matplotlib.dates.date2num(t0),matplotlib.dates.date2num(t0)],[-100,100],'--r')
                        try:
                            ax3.set_ylim([np.floor(np.nanmin(datamodeli['VTPK'].values)), np.ceil(np.nanmax(datamodeli['VTPK'].values))])
                        except:
                            ax3.set_ylim([0, 1])
                        ax3.legend(loc='lower right')
                        ax3.set_ylabel('Tp[s]')
                        ax3.set_xlabel('time')
                        ax3.xaxis.set_tick_params(rotation=45)

                    if t0 is not None:
                        ax_list = figid.axes
                        for axi in ax_list:
                            axi.plot_date([matplotlib.dates.date2num(t0), matplotlib.dates.date2num(t0)], [-10, 10], '--r', label='t0')
                            axi.legend(loc='lower right')

                    figid.suptitle(os.path.basename(iobs).split('.')[0])
                    outname = os.path.join(outdir, 'WL_%s_t0%s_%s_%s.png' % (os.path.basename(iobs).split('.')[0], t0.strftime("%Y-%m-%d"), tini.strftime("%Y-%m-%d"), tend.strftime("%Y-%m-%d")))
                    plt.savefig(outname, dpi=100, bbox_inches='tight')
                    plt.close('all')
            except:
                log.warning("=====Something failed in the observation data extraction. Continue\n====")


if __name__ == "__main__":

    trangeval = [datetime.datetime(2021, 3, 1), datetime.datetime(2021, 3, 2)]  # list of t0s
    # trangeval=[]
    listreg = list(dsets.datasets_hydro.keys())
    listreg = ['BAL']

    if len(sys.argv) > 1:
        listreg = [str(sys.argv[1])]
        tstart = datetime.datetime.strptime(sys.argv[2], "%Y%m%d")
        tend = datetime.datetime.strptime(sys.argv[3], "%Y%m%d")
        trangeval = [tstart, tend]  # list of t0s

    datadir = r'/homelocal2/mirazoki/ECFAS/data/CMEMS'  # '/IBI/timeseries/'
    obstype = 'latest'  # latest,monthly,history
    for region in listreg:
        PHYvar = dsets.datasets_hydro[region]['var'][0]

        # identify all t0 that haven't been made into timeseries
        listzos = glob.glob(os.path.join(datadir, region, 'timeseries', 'tseries_coastal_*.nc'))
        listzos.sort()
        t0list = []
        for filei in listzos:
            parts = os.path.split(filei)[-1].split('_')
            t0list.append(datetime.datetime.strptime(parts[2] + '_' + parts[3], "%Y-%m-%d_%H-%M-%S"))
        t0list, idxu = np.unique(t0list, return_index=True)
        listzos = np.array(listzos)[idxu]
        if len(trangeval) > 0:
            # clip the t0s to the given range
            boolsel = [t0i > trangeval[0] and t0i < trangeval[1] for t0i in t0list]
        else:
            boolsel = np.ones(listzos.shape, dtype='bool')

        tsel = t0list[np.array(boolsel)]
        filesel = listzos[np.array(boolsel)]
        for ifile, filename in enumerate(filesel):
            parts = os.path.split(filename)[-1].split('_')
            tini = datetime.datetime.strptime(parts[4] + '_' + parts[5], "%Y-%m-%d_%H-%M-%S")
            tend = datetime.datetime.strptime(parts[6] + '_' + parts[7].replace('.nc', ''), "%Y-%m-%d_%H-%M-%S")
            outdir = os.path.join(os.path.split(filename)[0], 'figures')
            coast_water_level_validate(region, PHYvar, outdir, filename, tini, tend, obstype, t0=tsel[ifile])
