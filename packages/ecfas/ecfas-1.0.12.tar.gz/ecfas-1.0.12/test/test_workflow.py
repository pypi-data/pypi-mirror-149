import os
import pytest
import argparse
import ecfas.cmems_operational_fullworkflow as wf


def setup_module():
    global test_dir
    test_dir = os.path.dirname(os.path.abspath(__file__))


def test_workflow_no_config_file():
    """ Test behavior when no config file is specified """
    cli_args = argparse.Namespace()
    cli_args.region = 'NWS'
    cli_args.reanal = False
    cli_args.t0 = None
    cli_args.debug = False
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        wf.execute_workflow(cli_args)
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1
