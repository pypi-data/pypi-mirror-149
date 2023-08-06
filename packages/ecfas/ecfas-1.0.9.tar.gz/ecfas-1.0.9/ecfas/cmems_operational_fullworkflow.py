"""
@author: mirazoki, gturek
operational download of CMEMS data
"""
import argparse
from distutils.log import debug
import logging
import os
import shutil
import sys
import time

import datetime as dt
import ecfas.cmems_datasets as dsets
import ecfas.coast_water_level_extract_multiple as cem
import ecfas.coast_water_level_process as cp
import ecfas.fes.module_FES2014 as fes
import ecfas.motu_download as md
import ecfas.utils as utils
import logging.handlers as handlers


def init_logger(log_dir):
    """ Initialize logging """

    log_level = logging.INFO
    if debug:
        log_level = logging.DEBUG
    logging.basicConfig(format='%(asctime)s:%(name)s:%(levelname)-4s:%(message)s', level=log_level, datefmt='%Y-%m-%d %H:%M:%S')

    global log
    log = logging.getLogger('ecflow')
    log.addHandler(logging.StreamHandler())

    if log_dir != "":
        os.makedirs(log_dir, exist_ok=True)
        log_dir = os.path.join(log_dir, 'ecflow.log')
        # Rotate log daily into a new file up to a maximum number of 2 backups
        log.info(f'Logging to file {log_dir}')
        file_handler = handlers.TimedRotatingFileHandler(log_dir, when='midnight', interval=1, backupCount=3)
        file_handler.setFormatter(logging.Formatter("%(asctime)s:%(name)s:%(levelname)-4s:%(message)s", "%Y-%m-%d %H:%M:%S"))
        file_handler.setLevel(log_level)
        log.addHandler(file_handler)


def clean_working_dirs(data_sets, out_dir, region):
    """ Re-initializes all 'data' directories at the beginning of each run """
    setsel = []

    if region is None:
        setsel.append(list(data_sets.keys()))
    elif region == 'ARC':
        setsel.append('ARC_ocean')
        setsel.append('ARC')
    else:
        setsel.append(region)

    for dseti in setsel:
        out = os.path.join(out_dir, '%s' % dseti)
        out = os.path.join(out, 'data')

        # Clean any pre-existing data files
        if os.path.exists(out):
            shutil.rmtree(out)

        os.makedirs(out)


def get_datasets(dset_type, mod_type):
    if mod_type == 'fcst':
        if dset_type == 'PHY':
            data_sets = dsets.datasets_hydro
        elif dset_type == 'WAV':
            data_sets = dsets.datasets_wave
    elif mod_type == 'reanal':
        if dset_type == 'PHY':
            data_sets = dsets.datasets_hydro_reanal
        elif dset_type == 'WAV':
            data_sets = dsets.datasets_wave_reanal
    return data_sets


def execute_workflow(args):

    region = args.region
    mod_type = 'fcst'
    if args.reanal:
        mod_type = 'reanal'
    global debug
    debug = args.debug

    # Read config file
    try:
        config = utils.read_config(args.config)
    except Exception as e:
        print('Failed to read config file: ' + str(e))
        sys.exit(1)

    outdir = config['outdir']
    maskdir = config['maskdir']
    logdir = config['logdir']
    fesdir = config['fesdir']
    # FES code will read env variable $FES_DATA to find where the data lives
    os.environ['FES_DATA'] = fesdir
    user = config['usr']
    pwd = config['pwd']
    motu = config['url']

    init_logger(config['logdir'])

    if args.t0 == None:
        uptime = dsets.datasets_hydro[region]["uptime"]
        now = dt.datetime.now()
        next_start = dt.datetime(now.year, now.month, now.day, int(uptime), int((uptime * 60) % 60), int((uptime * 3600) % 3600))
    else:
        next_start = dt.datetime.strptime(args.t0, "%Y%m%d_%H%M%S")

    #1. DOWNLOAD THE FIELDS ==========================================================================================================
    log.info(">> Downloading data from CMEMS")
    pred_start = next_start - dt.timedelta(days=2)
    pred_end = next_start + dt.timedelta(days=5)

    # call function
    t_start = pred_start.strftime("%Y-%m-%d %H:%M:%S")
    t_end = pred_end.strftime("%Y-%m-%d %H:%M:%S")
    label = next_start.strftime("%Y-%m-%d_%H-%M-%S")

    tic_download = time.time()
    datadir = os.path.join(outdir, '%s' % region)

    data_sets_phy = get_datasets('PHY', mod_type)
    if not debug:
        clean_working_dirs(data_sets_phy, outdir, region)
    data_sets_wav = get_datasets('WAV', mod_type)
    tries = 1
    while tries <= 2:
        md.motu_download(user, pwd, motu, t_start, t_end, outdir, data_sets_phy, 'PHY', region=region, modtype=mod_type, label=label)
        md.motu_download(user, pwd, motu, t_start, t_end, outdir, data_sets_wav, 'WAV', region=region, modtype=mod_type, label=label)
        ok = utils.check_downloads(outdir, region, pred_start, pred_end, label)
        if ok:
            break
        else:
            tries += 1
            if tries > 2:
                log.error("Problems downloading CMEMS data, please check server status")
                sys.exit(1)
            log.warning("Retrying download, some files were found to be missing")

    toc_download = time.time()

    #2. CLIP TO COASTAL LEVELS ========================================================================================================
    log.info(">> Clipping to coastal levels")
    tic_clip = time.time()

    outdirts = os.path.join(datadir, 'data')
    if region not in dsets.datasets_wave:
        add_wave = False
    else:
        add_wave = True
    # clip to coastal points
    if region == 'ARC':
        cem.coast_water_level_extract_multiple(datadir.replace(region, 'ARC_ocean'), outdirts.replace(region, 'ARC_ocean'), maskdir, 'ARC_ocean', next_start.strftime("%Y-%m-%d_%H-%M-%S"), pred_start, pred_end, False)
    cem.coast_water_level_extract_multiple(datadir, outdirts, maskdir, region, next_start.strftime("%Y-%m-%d_%H-%M-%S"), pred_start, pred_end, add_wave)
    toc_clip = time.time()

    #3. COMBINE DATASETS AND CALCULATE SETUP ===========================================================================================
    log.info(">> Combining datasets and calculating setup")
    tic_process = time.time()
    tide = None

    outdirproc = os.path.join(datadir, 'timeseries')
    if region in ['BS']:
        # initialize FES
        short_tide, radial_tide = fes.init_fes_h(fesdir)
        tide = dict()
        tide['short_tide'] = short_tide
        tide['radial_tide'] = radial_tide
        tide['fesdir'] = fesdir
    cp.coast_water_level_process(region, outdirts, outdirproc, label,maskdir, swashtype='cte', betatype='None', fes_tide=tide)
    toc_process = time.time()

    outfile = os.path.join(datadir, 'time_diagnostics.txt')
    file = open(outfile, 'w')
    file.write('Time download CMEMS: %s\n' % (toc_download - tic_download))
    file.write('Time snip CMEMS: %s\n' % (toc_clip - tic_clip))
    file.write('Time process CMEMS: %s\n' % (toc_process - tic_process))
    file.close()


def main():
    #0. READ ARGS AND CONFIG ==========================================================================================================
    parser = argparse.ArgumentParser("op_workflow")
    parser.add_argument('-c', '--config', metavar='<config_file>', default='ecfas.cfg', required=True, help='Absolute path to config file')
    parser.add_argument('-r', '--region', metavar='<region>', default=None, help='Region of interest, one of ARC, BAL, BS. IBI, MED, NWS, GLO. Defaults to all')
    parser.add_argument('-t', '--t0', metavar='<YYmmdd_HHMMSS>', default=None, help='Start time t0 in the format YYmmdd_HHMMSS')
    parser.add_argument('--reanal', action='store_true', help='reanal mode')
    parser.add_argument('--debug', action='store_true', help='Debug mode')

    execute_workflow(parser.parse_args())


if __name__ == "__main__":
    main()
