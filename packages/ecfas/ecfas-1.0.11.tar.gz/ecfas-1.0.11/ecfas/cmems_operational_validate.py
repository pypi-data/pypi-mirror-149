#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 17:20:10 2021

@author: mirazoki
"""

import argparse
import glob
import os
import sys
import logging

import datetime as dt
import ecfas.cmems_datasets as dsets
import ecfas.coast_water_level_validate as cv
import numpy as np

log = logging.getLogger(__name__)
def validate(outdir, region, t_start, t_end):

    if '15min' in region:
        regobs = region.replace('_15min', '')
    elif 'tsm' in region:
        regobs = region.replace('_tsm', '')
    else:
        regobs = region
    obsdir = os.path.join(outdir, regobs, 'observations')

    if t_start == 'None' and t_end == 'None':
        # validate the t0s of the last 5 days
        today = dt.datetime(dt.datetime.now().year, dt.datetime.now().month, dt.datetime.now().day)
        trangeval_start = today - dt.timedelta(days=5)
        trangeval_stop = trangeval_start + dt.timedelta(days=1)

    else:
        if t_start != 'None':
            # prescribing also the t0 list
            t0 = dt.datetime.strptime(t_start, "%Y-%m-%d %H-%M-%S")  # YYYYMMDD
            trangeval_start = t0
            if t_end == 'None':
                trangeval_stop = t0 + dt.timedelta(days=5)
            else:
                # prescribing also the t0 range
                trangeval_stop = dt.datetime.strptime(t_end, "%Y-%m-%d %H-%M-%S")  # YYYYMMDD

    trangeval = [trangeval_start, trangeval_stop]  # list of t0s

    obstype = 'latest'  # latest,monthly,history
    phy_var = dsets.datasets_hydro[region]['var'][0]

    listzos = glob.glob(os.path.join(outdir, region, 'timeseries', 'processed', 'tseries_coastal_*.nc'))

    listzos.sort()
    t0list = []
    for filei in listzos:
        parts = os.path.split(filei)[-1].split('_')
        t0list.append(dt.datetime.strptime(parts[-6] + '_' + parts[-5], "%Y-%m-%d_%H-%M-%S"))

    t0list, idxu = np.unique(t0list, return_index=True)
    listzos = np.array(listzos)[idxu]

    if len(trangeval) > 0:
        # clip the t0s to the given range
        boolsel = [t0i >= trangeval[0] and t0i < trangeval[1] for t0i in t0list]
    else:
        boolsel = np.ones(listzos.shape, dtype='bool')
    tsel = t0list[np.array(boolsel)]
    filesel = listzos[np.array(boolsel)]

    # TODO: how does this fail?
    for ifile, filename in enumerate(filesel):
        parts = os.path.split(filename)[-1].split('_')
        tini = dt.datetime.strptime(parts[-4] + '_' + parts[-3], "%Y-%m-%d_%H-%M-%S")
        tend = dt.datetime.strptime(parts[-2] + '_' + parts[-1].replace('.nc', ''), "%Y-%m-%d_%H-%M-%S")
        outdir = os.path.join(os.path.split(filename)[0], 'figures')
        cv.coast_water_level_validate(region, phy_var, outdir, filename, tini, tend, obstype, t0=tsel[ifile], obsdir=obsdir)

    return True


def main():
    parser = argparse.ArgumentParser("op_validate")
    parser.add_argument('-o', '--outputs', metavar='<output_dir>', required=True, help='Absolute path to output data to be checked')
    parser.add_argument('-r', '--region', metavar='<region>', required=True, help='Region of interest, one of ARC, BAL, BS. IBI, MED, NWS, GLO. Defaults to all')
    parser.add_argument('-s', '--t_start', metavar='<Y-m-d H-M-S>', default='None', help='Start time in the format Y-m-d H-M-S')
    parser.add_argument('-e', '--t_end', metavar='<Y-m-d H-M-S>', default='None', help='End time in the format Y-m-d H-M-S')

    args = parser.parse_args()

    ok = validate(args.outputs, args.region, args.t_start, args.t_end)
    # If any of the checks fail, exit with error flag, which will be picked up by test framework as a fail
    if not ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
