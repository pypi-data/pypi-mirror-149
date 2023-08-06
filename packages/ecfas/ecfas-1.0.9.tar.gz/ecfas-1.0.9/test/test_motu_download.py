import os
import ecfas.cmems_datasets as ds
import ecfas.motu_download as md
import ecfas.utils as utils
import pytest


def setup_module():
    global out_dir
    out_dir = 'test_outputs'
    utils.clean_dir(out_dir)
    global motu
    motu = 'http://nrt.cmems-du.eu/motu-web/Motu'
    global user
    user = os.environ['CMEMS_USR']
    global password
    password = os.environ['CMEMS_PWD']


def test_fail_download_wrong_url():
    t_start = '2021-05-01 00:00:00'
    t_end = '2021-05-02 00:00:00'
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        md.motu_download(user, password, 'http://nrt.cmems-du.com/motu-web/Motu', t_start, t_end, out_dir, ds.datasets_hydro, "PHY", region='NWS')
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1


def test_download_hydroset():
    t_start = '2021-05-01 00:00:00'
    t_end = '2021-05-02 00:00:00'
    md.motu_download(user, password, motu, t_start, t_end, out_dir, ds.datasets_hydro, "PHY", region='NWS')


def test_download_waveset():
    t_start = '2021-05-01 00:00:00'
    t_end = '2021-05-02 00:00:00'
    md.motu_download(user, password, motu, t_start, t_end, out_dir, ds.datasets_wave, "WAV", region='NWS')


def test_download_satset():
    t_start = '2021-05-01 00:00:00'
    t_end = '2021-05-02 00:00:00'
    md.motu_download_satdata(user, password, motu, t_start, t_end, out_dir)