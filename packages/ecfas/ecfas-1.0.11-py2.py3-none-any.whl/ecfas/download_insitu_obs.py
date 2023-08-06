#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 16:45:04 2021

@author: mirazoki
test to download NRT Insitu obs
"""
import datetime
import logging
import os
import urllib.request

import numpy as np
import pandas as pd

log = logging.getLogger(__name__)


def download_insitu_obs(region, dateini, dateend, obstype='latest', chosen=['TG'], outdir='.'):

	datasets = {'TG':['SLEV'],
						'MO':['SWHT', 'VSPEC1D'],
						'ARC':{'strname':'arc', 'folder':'INSITU_ARC_NRT_OBSERVATIONS_013_031'},
						# 'ARC_tsm':{'strname':'arc','folder':'INSITU_ARC_NRT_OBSERVATIONS_013_031'},
						'BAL':{'strname':'bal', 'folder':'INSITU_BAL_NRT_OBSERVATIONS_013_032'},
						'BS':{'strname':'bs', 'folder':'INSITU_BS_NRT_OBSERVATIONS_013_034'},
						'MED':{'strname':'med', 'folder':'INSITU_MED_NRT_OBSERVATIONS_013_035'},
						'IBI':{'strname':'ibi', 'folder':'INSITU_IBI_NRT_OBSERVATIONS_013_033'},
						# 'IBI_15min':{'strname':'ibi','folder':'INSITU_IBI_NRT_OBSERVATIONS_013_033'},
						'NWS':{'strname':'nws', 'folder':'INSITU_NWS_NRT_OBSERVATIONS_013_036'}
						# 'NWS_15min':{'strname':'nws','folder':'INSITU_NWS_NRT_OBSERVATIONS_013_036'}
						}
	if region in datasets.keys():
			if not os.path.exists(outdir):
					os.mkdir(outdir)

			# outdirdata=os.path.join(outdir,obstype)
			# if not os.path.exists(outdirdata):
			# 		  os.mkdir(outdirdata)
			colidx = ['product_id', 'file_name', 'geospatial_lat_min', 'geospatial_lat_max', 'geospatial_lon_min', 'geospatial_lon_max', 'time_coverage_start', 'time_coverage_end', 'institution', 'date_update', 'data_mode', 'parameters']
			# obs_sets=['history']#,'monthly','latest']
			# chosen=['MO','TG']

			indexfile = r'/Core/%s/%s_multiparameter_nrt/index_%s.txt' % (datasets[region]['folder'], datasets[region]['strname'], obstype)
			# ftp_add=r'/Core/%s/%s_multiparameter_nrt/%s' %(datasets[region],region.lower(),obstype)
			# dateini=datetime.datetime(2021,2,22)
			# dateend=datetime.datetime(2021,2,21)
			# urllib.urlretrieve('ftp://username:password@server/path/to/file', 'file')

			# download index file
			urllib.request.urlretrieve('ftp://mirazoquiapecec:MaialenCMEMS2017@nrt.cmems-du.eu%s' % indexfile, os.path.join(outdir, 'index_%s.txt' % obstype))

			id_data = pd.read_csv(os.path.join(outdir, 'index_%s.txt' % obstype), sep=',', delimiter=None, header=None, skiprows=6, names=colidx, index_col=None)

			for obsi in chosen:
					searchvars = datasets[obsi]
					boolvar = [np.any([vari in row['parameters'] for vari in searchvars]) for ii, row in id_data.iterrows()]

					if obstype == 'latest':
							# filter to the dates we need
							datestrlist = [datetime.datetime.strftime(dateini + datetime.timedelta(days=i), "%Y%m%d") for i in np.arange((dateend - dateini).total_seconds() / 86400.0)]
							# datestr=dateini.strftime("%Y%m%d")
							# filter those for the chosen times
							boolvar_un = [np.any([datestr in row['file_name'] for datestr in datestrlist]) for ii, row in id_data.iterrows()]

							boolvar = np.array(boolvar) & np.array(boolvar_un)

							# listncs=[pathlib.Path(filei).parts[-1].replace('.nc','') for filei in id_data['file_name'].loc[boolvar]]
							listncfull = id_data['file_name'].loc[boolvar]
							# listobs=['_'.join(nci.split('_')[0:-1]) for nci in listncs]

					# download list
					for ii, inc in enumerate(listncfull):
							outfile = os.path.join(outdir, inc[inc.find(obstype):])
							outdiri = os.path.split(outfile)[0]

							if not os.path.exists(os.path.split(outdiri)[0]):  # parent directory
									os.mkdir(os.path.split(outdiri)[0])
							if not os.path.exists(outdiri):
									os.mkdir(outdiri)

							address = inc.replace('ftp://', '')
							if not os.path.isfile(outfile):
									try:
											urllib.request.urlretrieve('ftp://mirazoquiapecec:MaialenCMEMS2017@%s' % address, filename=outfile)
									except:
											log.error("Failed to retrieve observation %s: %s - %s\n" % (inc, dateini.strftime("%Y%m%d"), dateend.strftime("%Y%m%d")))
