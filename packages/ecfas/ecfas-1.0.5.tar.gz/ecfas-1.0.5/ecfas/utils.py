import glob
import logging
import os
from pathlib import Path
import shutil

from configobj import ConfigObj

import datetime as dt
import ecfas.cmems_datasets as dsets
import numpy as np

log = logging.getLogger(__name__)


def clean_dir(dir_path):
    try:
        shutil.rmtree(dir_path)
    except Exception as e:
        log.error('Failed to delete %s. Reason: %s' % (dir, e))


def read_config(config_file):
    """ Reads a standard key=value config file """

    try:
        return ConfigObj(config_file, raise_errors=True, file_error=True)
    except:
        log.error("Error: " + config_file + " not found or unreadable")
        raise


def validate_date(self, s, date_format="%Y%m%d"):
    """ Validates a string representation of a date against the given format """

    try:
        return dt.datetime.strptime(s, date_format).date()
    except ValueError:
        log.error("Not a valid date: '{0}'.".format(s))
        raise


def check_downloads(outdir, region, t_start, t_end, label):

    log.info("Check all necessary CMEMS files have been downloaded")

    datadir = os.path.join(outdir, region, 'data')
    expected_dates = [t_start + dt.timedelta(days=i) for i in np.arange(np.ceil((t_end - t_start).total_seconds() / (86400)))]

    varshyd = []
    varswav = []

    if region in dsets.datasets_hydro.keys():
        varshyd = dsets.datasets_hydro[region]['var']
    if region in dsets.datasets_wave.keys():
        varswav = dsets.datasets_wave[region]['var']

    for vari in varshyd:
        files = glob.glob(os.path.join(datadir, vari + '*' + label + '*.nc'))
        files.sort()
        dateini_list = get_existing_files_start_dates(files)
        missing = [datei for datei in expected_dates if datei not in dateini_list]
        missing.sort()
        if len(missing) > 0:
            for imiss in missing:
                log.error("Missing PHY field data for date %s\n" % imiss.strftime("%Y-%m-%d_%H-%M-%S"))
            return False

        # only check WAV fields for the PHY fields available
        for varj in varswav:
            if isinstance(varj, list):
                files = glob.glob(os.path.join(datadir, 'WAVsubset_' + label + '*.nc'))
            else:
                files = glob.glob(os.path.join(datadir, varj + '_' + label + '*.nc'))
            files.sort()
            dateini_list_wav = get_existing_files_start_dates(files)

            missing = [datei for datei in dateini_list if datei not in dateini_list_wav]
            missing.sort()

            if len(missing) > 0:
                for imiss in missing:
                    log.error("Missing WAV field data for date %s\n" % imiss.strftime("%Y-%m-%d_%H-%M-%S"))
                return False

    return True


def get_existing_files_start_dates(files):

    start_dates = []
    for f in files:
        pathi, fnameext = os.path.split(f)
        fname = os.path.splitext(fnameext)[0]
        _, _, _, dateinia, dateinib, _, _ = fname.split("_")
        start_dates.append(dt.datetime.strptime((dateinia + ' ' + dateinib), '%Y-%m-%d %H-%M-%S'))

    return start_dates


def check_timeseries_output_size(file, exp_size, tolerance):

    log.info("Check timeseries output size")

    if len(file) == 0:
        log.error("File %s is empty!" % file)
        return False
    else:
        filesize = Path(file).stat().st_size
        if not np.isclose(filesize, exp_size, rtol=tolerance):
            log.warning("File %s size %x differs from expected %x" % (file, filesize, exp_size))
            return False
    return True
