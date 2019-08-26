#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
from common.manip_case_table import get_selected_case_param
from services.IO_Internal import run_case
from common.comm_paras import CASE_XLS_PATH


case_params = get_selected_case_param(CASE_XLS_PATH, 'IO_Internal')


@pytest.mark.parametrize(
    'case_name, case_input, case_expect',
    case_params,
    ids=[case_param[0] for case_param in case_params]
)
def test_IO_Internal(case_name, case_input, case_expect):
    assert run_case(case_name, case_input, case_expect)
