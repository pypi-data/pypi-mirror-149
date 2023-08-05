import argparse
import logging
import os
import sys

from motu_utils import motu_api, utils_log

import ecfas.cmems_datasets as dsets
import numpy as np
import pandas as pd

log = logging.getLogger(__name__)


def motu_download(usr, pwd, motu, t_start, t_end, out_dir, data_sets, dset_type, region=None, modtype='fcst', label='analysis'):
    """ Downloads hydro or wave data from CMEMS using motu API """
    log.info(f">> Downloading data for {dset_type}")

    max_time = 1
    tot_time = pd.Timestamp(t_end) - pd.Timestamp(t_start)
    if tot_time.total_seconds() < 0:
        log.error('The total time is negative, something is wrong with the dates')
        sys.exit(1)
    num_time_intervals = np.ceil(tot_time.days / max_time)

    times = []
    for tt in range(0, int(num_time_intervals)):
        times.append([pd.Timestamp(t_start) + pd.Timedelta(days=int(max_time * tt)), pd.Timestamp(t_start) + pd.Timedelta(days=int(max_time * (tt + 1)))])

    setsel = []
    if region is None:
        setsel.append(list(data_sets.keys()))
    elif region == 'ARC' and dset_type == 'PHY':
        setsel.append('ARC_ocean')
        setsel.append('ARC')
    else:
        setsel.append(region)

    for dseti in setsel:
        log.info(f">> Region {dseti}")
        out = os.path.join(out_dir, '%s' % dseti)
        out = os.path.join(out, 'data')

        if not os.path.exists(out):
            os.makedirs(out)

        if 'lon_min' in data_sets[dseti].keys() and 'lat_min' in data_sets[dseti].keys() and np.abs(data_sets[dseti]['lon_max'] - data_sets[dseti]['lon_min']) * np.abs(data_sets[dseti]['lat_max'] - data_sets[dseti]['lat_min']) > 858:
                log.info('WARNING: REQUESTED SPATIAL EXTENT MAY BE TOO BIG FOR SERVER. TRY REDUCING SPATIAL EXTENT')

        for tt in range(0, int(num_time_intervals)):
            query_args = get_query_args(usr, pwd, motu, times[tt][0], times[tt][1], out, data_sets[dseti], dset_type, label)
            if os.path.isfile(os.path.join(out, query_args.out_name)):
                log.info('File ' + query_args.out_name + ' already present')
                continue
            try:
                log.info('Downloading ' + query_args.out_name)
                motu_api.execute_request(query_args)
            except Exception as e:
                log.error('Download failed: ' + str(e))
                sys.exit(1)


def motu_download_satdata(usr, pwd, motu, t_start, t_end, out_dir, label='analysis'):
    """ Downloads satellite data from CMEMS using motu API """

    max_time = 1
    tot_time = pd.Timestamp(t_end) - pd.Timestamp(t_start)
    if tot_time.total_seconds() < 0:
        log.info('The total time is negative, something is wrong with the dates')
        sys.exit(1)
    num_time_intervals = np.ceil(tot_time.days / max_time)

    times = []
    for tt in range(0, int(num_time_intervals)):
        times.append([pd.Timestamp(t_start) + pd.Timedelta(days=int(max_time * tt)), pd.Timestamp(t_start) + pd.Timedelta(days=int(max_time * (tt + 1)))])

    for dseti in dsets.datasets_sat:
        out = os.path.join(out_dir, '%s' % dseti)
        out = os.path.join(out, 'data')

        if not os.path.exists(out):
            os.makedirs(out)

        for tt in range(0, int(num_time_intervals)):
            if type(dsets.datasets_sat[dseti]['product']) is list:
                dset = dsets.datasets_sat[dseti]
                for iprod in dsets.datasets_sat[dseti]['product']:
                    dset['product'] = iprod
                    query_args = get_query_args(usr, pwd, motu, times[tt][0], times[tt][1], out, dset, "", label)
                    if os.path.isfile(os.path.join(out, query_args.out_name)):
                        log.info('File ' + query_args.out_name + ' is already present')
                        continue
                    try:
                        log.info('Downloading ' + query_args.out_name)
                        motu_api.execute_request(query_args)
                    except Exception as e:
                        log.error('Download failed: ' + str(e))
                        sys.exit(1)

            else:
                query_args = get_query_args(usr, pwd, motu, times[tt][0], times[tt][1], out, dsets.datasets_sat[dseti], "", label)
                if os.path.isfile(os.path.join(out, query_args.out_name)):
                    log.info('File ' + query_args.out_name + ' is already present')
                    continue
                try:
                    motu_api.execute_request(query_args)
                except Exception as e:
                    log.error('Download failed: ' + str(e))
                    sys.exit(1)


def get_query_args(usr, pwd, motu, tmin, tmax, out_dir, dset, dset_type, label):
        """ Returns an argparse object with required query arguments and values """
        query_args = argparse.Namespace()
        # Required by API
        query_args.auth_mode = 'cas'
        query_args.size = False
        query_args.sync = False
        query_args.console_mode = False
        query_args.describe = False
        query_args.user_agent = None
        query_args.socket_timeout = None
        query_args.outputWritten = None
        query_args.block_size = 65536

        # Required by API, over written if present
        query_args.proxy_server = None
        query_args.proxy_user = None
        query_args.proxy_pwd = None
        query_args.depth_min = None
        query_args.depth_max = None
        query_args.longitude_min = None
        query_args.longitude_max = None
        query_args.latitude_min = None
        query_args.latitude_max = None

        query_args.motu = motu
        query_args.user = usr
        query_args.pwd = pwd
        query_args.service_id = dset['service']
        query_args.product_id = dset['product']

        if 'lon_min' in dset.keys() and 'lat_min' in dset.keys():
            query_args.longitude_min = str(dset['lon_min'])
            query_args.longitude_max = str(dset['lon_max'])
            query_args.latitude_min = str(dset['lat_min'])
            query_args.latitude_max = str(dset['lat_max'])

        if 'depth_min' in dset.keys():
            # append these attributes
            query_args.depth_min = str(dset['depth_min'])
            query_args.depth_max = str(dset['depth_max'])

        query_args.date_min = str(tmin)
        query_args.date_max = str(tmax)
        tmin_str = str(tmin).replace(':', '-').replace(' ', '_')
        tmax_str = str(tmax).replace(':', '-').replace(' ', '_')
        file_name = label + '_' + tmin_str + '_' + tmax_str + '.nc'

        query_args.variable = dset['var']
        ds_vars = dset['var']
        if ds_vars is None:
            file_name = 'all' + '_' + file_name
        elif isinstance(ds_vars, list):
            if isinstance(ds_vars[0], list):
                file_name = dset_type + 'subset' + '_' + file_name
            else:
                if ds_vars[0] != None:
                    file_name = ds_vars[0] + '_' + file_name
        else:
            file_name = ds_vars + '_' + file_name

        query_args.out_dir = out_dir
        query_args.out_name = file_name

        return query_args