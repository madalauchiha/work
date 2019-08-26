#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import pytest
import shutil
from common.comm_paras import g_mods, REPORT_DIR, ROOT_DIR
lib_path = os.path.join(ROOT_DIR, 'venv/lib/python3.5/site-packages')
if lib_path not in sys.path:
    sys.path.append(lib_path)

# init pytest
report_name = 'report.html'
report_path = os.path.join(REPORT_DIR, report_name)
suite_dir = os.path.join(ROOT_DIR, 'testsuite')

try:
    shutil.rmtree(os.path.join(ROOT_DIR, '__pycache__'))
    shutil.rmtree(os.path.join(ROOT_DIR, 'testsuite', '__pycache__'))
except FileNotFoundError:
    pass

if g_mods:
    keys = ' or '.join(g_mods)
    pytest.main([suite_dir, '-sq', '--tb=short', '-k', keys, '--html', report_path, '--self-contained-html'])
else:
    print('No module selected! Please select one.')

# # send mail
# rptpath = os.path.join(comm_paras.ROOT_DIR, 'report', report_name)
# mail_report(rptpath)
