#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 14 13:25:18 2021
@author: mirazoki
"""

import argparse
import datetime
import glob
import os
import sys

import ecfas.cmems_datasets as dsets
import numpy as np
import xarray as xr
import pandas as pd


def run_checks(outdir, baselinedir, region, start_time):

    t0 = datetime.datetime.strptime(start_time, "%Y%m%d_%H%M%S")
    label = t0.strftime("%Y-%m-%d_%H-%M-%S")
    ts_datadir = os.path.join(outdir, region, 'data')
    tsproc_datadir = os.path.join(outdir, region, 'timeseries')

    pred_start = t0 - datetime.timedelta(days=2)
    pred_end = t0 + datetime.timedelta(days=5)

    print("====================QUALITY CHECK===============\n")
    print("==REGION:%s\n" % region)
    print("==BULLETIN DATE: %s\n" % t0.strftime("%Y%m%d_%H%M%S"))
    print("\n")
    print('Comparing EXTRACTED timeseries...\n')

    ok1 = True
    # find timeseries and compute differences for each variable
    ref_file = glob.glob(os.path.join(ts_datadir, 'tseries_coastal_%s*.nc' % label))[0]
    if not os.path.exists(ref_file):
        print(f'Cannot find reference timeseries file(s) {ref_file}')
        return False

    baseline_file = glob.glob(os.path.join(baselinedir, region, 'data', 'tseries_coastal_%s*.nc' % label))[0]
    if not os.path.exists(ref_file):
        print(f'Cannot find baseline file(s) {baseline_file}')
        return False

    refdata = xr.open_dataset(ref_file, decode_times=False)
    twindata = xr.open_dataset(baseline_file, decode_times=False)

    for vari in twindata.variables:
        # skip non-numeric data (e.g. station names, coordinates will tell us if this is ok)
        if refdata[vari].dtype in ['float32', 'int64']:
            checkdata = np.allclose(refdata[vari].values, twindata[vari].values, equal_nan=True, atol=0.01)
            if checkdata:
                print('Comparison of variable %s:%s\n' % (vari, 'succeded'))
            else:
                print('Comparison of variable %s:%s\n' % (vari, 'failed'))
                checkarr = np.zeros(refdata['stations'].shape, dtype='bool')
                maxdiff = np.zeros(refdata['stations'].shape)
                for istation in np.arange(refdata.dims['stations']):
                    checki = np.allclose(refdata[vari].isel(stations=istation).values, twindata[vari].isel(stations=istation).values, equal_nan=True)
                    checkarr[istation] = checki
                    maxdiff[istation] = np.max(np.abs(refdata[vari].isel(stations=istation).values - twindata[vari].isel(stations=istation).values))
                print('max diff %s: %f [%s] (%s)\n' % (vari, np.max(maxdiff[~np.isnan(maxdiff)]), refdata[vari].units, refdata['stnames'].isel(stations=np.where(maxdiff == np.max(maxdiff[~np.isnan(maxdiff)]))[0]).values))
                ok1 = False

    if ok1:
        print("Evaluation EXTRACTED timeseries: SUCCEDED\n")
    else:
        print("Evaluation EXTRACTED timeseries: FAILED\n")

    #=========================================================================================================
    print('Comparing PROCESSED timeseries...\n')
    ok2 = True
    if region != 'ARC_ocean':
        labelproc = ['b%s_%s_%s' % (t0.strftime('%Y%m%d%H%M%S'), tstarti.strftime('%Y%m%d'), (tstarti + datetime.timedelta(days=1)).strftime('%Y%m%d')) for tstarti in pd.date_range(start=pred_start, end=pred_end, freq='1D', closed='left')]

        for ilab in labelproc:
            print('Checking daily file %s\n' % ilab)
            ref_file = glob.glob(os.path.join(tsproc_datadir, 'TScoast_%s_%s.nc' % (region, ilab)))[0]
            if not os.path.exists(ref_file):
                print(f'Cannot find reference daily file(s) {ref_file}')
                return False

            baseline_file = glob.glob(os.path.join(baselinedir, region, 'timeseries', 'TScoast_%s_%s.nc' % (region, ilab)))[0]
            if not os.path.exists(baseline_file):
                print(f'Cannot find reference file(s) {baseline_file}')
                return False

            refdata = xr.open_dataset(ref_file, decode_times=False)
            twindata = xr.open_dataset(baseline_file, decode_times=False)

            for vari in twindata.variables:
                # skip non-numeric data (e.g. station names, coordinates will tell us if this is ok)
                if refdata[vari].dtype in ['float32', 'int64']:
                    checkdata = np.allclose(refdata[vari].values, twindata[vari].values, equal_nan=True, atol=0.01)
                    if not checkdata:
                        print('Comparison of variable %s:%s\n' % (vari, 'failed'))
                        checkarr = np.zeros(refdata['stations'].shape, dtype='bool')
                        maxdiff = np.zeros(refdata['stations'].shape)
                        for istation in np.arange(refdata.dims['stations']):
                            checki = np.allclose(refdata[vari].isel(stations=istation).values, twindata[vari].isel(stations=istation).values, equal_nan=True)
                            checkarr[istation] = checki
                            maxdiff[istation] = np.max(np.abs(refdata[vari].isel(stations=istation).values - twindata[vari].isel(stations=istation).values))
                        print('max diff %s: %f [%s] (%s)\n' % (vari, np.max(maxdiff[~np.isnan(maxdiff)]), refdata[vari].units, refdata['stnames'].isel(stations=np.where(maxdiff == np.max(maxdiff[~np.isnan(maxdiff)]))[0]).values))
                        ok2 = False
    if ok2:
        print("Evaluation PROCESSED timeseries: SUCCEDED\n")
    else:
        print("Evaluation PROCESSED timeseries: FAILED\n")

    print("====================END========================")
    if not ok1 or not ok2:
        return False
    else:
        return True


def main():
    parser = argparse.ArgumentParser("qual_checks")
    parser.add_argument('-o', '--outputs', metavar='<output_dir>', required=True, help='Absolute path to output data to be checked')
    parser.add_argument('-b', '--baselines', metavar='<baseline_dir>', required=True, help='Absolute path to baseline data to be checked against')
    parser.add_argument('-r', '--region', metavar='<region>', required=True, help='Region of interest, one of ARC, BAL, BS. IBI, MED, NWS, GLO. Defaults to all')
    parser.add_argument('-t', '--t0', metavar='<YYmmdd_HHMMSS>', required=True, help='Start time t0 in the format YYmmdd_HHMMSS')

    args = parser.parse_args()

    ok = run_checks(args.outputs, args.baselines, args.region, args.t0)
    # If any of the checks fail, exit with error flag, which will be picked up by test framework as a fail
    if not ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
