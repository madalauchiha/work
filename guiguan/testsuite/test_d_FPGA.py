#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
from common.manip_case_table import get_selected_case_param
from services.FPGA import run_case
from common.operate_os import write_file_data,reboot_os
from common.manip_case_table import CASE_XLS_PATH


def setup_module():
    write_file_data("s", "export DISPLAY=192.168.100.99:0.0", "#export DISPLAY=192.168.100.99:0.0", "/home/worker/.bashrc")
    reboot_os()


def teardown_module():
    write_file_data("s", "#export DISPLAY=192.168.100.99:0.0", "export DISPLAY=192.168.100.99:0.0", "/home/worker/.bashrc")
    reboot_os()


case_params = get_selected_case_param(CASE_XLS_PATH, 'FPGA')


@pytest.mark.parametrize(
    'case_name, case_input, case_expect',
    case_params,
    ids=[case_param[0] for case_param in case_params]
)
def test_FPGA(case_name, case_input, case_expect):
    assert run_case(case_name, case_input, case_expect)








