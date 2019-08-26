#!usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
from py._xmlgen import html
from common.comm_paras import g_ssh_master, g_ssh_slave, g_mods
from common.comm_paras import CASE_XLS_PATH
from common.manip_case_table import write_rst_to_xls
from common.manip_report import gen_table_tag
from collections import OrderedDict


def pytest_sessionstart(session):
    session.results = dict()


dict_rst = dict()
for mod in g_mods:
    dict_rst[mod] = dict()


def get_modname_casename(item_name):
    modname, casename = item_name.split('[')
    modname = modname.lstrip('test_')
    casename = casename.rstrip(']')

    return modname, casename


caseno = 0


@pytest.mark.hookwrapper
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    # extra = getattr(report, 'extra', [])

    if report.when == 'call':
        global caseno
        caseno += 1
        print('====== case[%d] end ======' % caseno)

        # always add url to report
        # extra.append(pytest_html.extras.url('http://www.example.com/'))
        # report.extra = extra

        # parse modname and case name
        modname, casename = get_modname_casename(item.name)

        # save test result to dict
        # item.session.results[item.name] = report.outcome
        global dict_rst
        dict_rst[modname][casename] = report.outcome

        # write test result to excel
        test_rst = report.outcome.rstrip('ed').upper()
        # write_rst_to_xls(CASE_XLS_PATH, modname, casename, test_rst)
        write_rst_to_xls(CASE_XLS_PATH, modname, caseno, test_rst)


def get_rst_statis():
    global dict_rst

    statis = OrderedDict()
    heads = ['Total Tests', 'Passed', 'Failed', 'Pass Rate']
    for mod in g_mods:
        statis[mod] = OrderedDict()
        for head in heads:
            statis[mod][head] = 0

    statis['Count'] = OrderedDict()
    for head in heads:
        statis['Count'][head] = 0

    cnt_tests = 0
    cnt_passed = 0
    cnt_failed = 0
    for mod in dict_rst:
        passed_amount = sum(1 for result in dict_rst[mod].values() if result == 'passed')
        failed_amount = sum(1 for result in dict_rst[mod].values() if result == 'failed')
        total = passed_amount + failed_amount

        cnt_tests += total
        cnt_passed += passed_amount
        cnt_failed += failed_amount

        try:
            pass_rate = round(passed_amount / total * 100)
        except ZeroDivisionError:
            pass_rate = 0

        statis[mod]['Total Tests'] = str(total)
        statis[mod]['Passed'] = str(passed_amount)
        statis[mod]['Failed'] = str(failed_amount)
        statis[mod]['Pass Rate'] = str(pass_rate) + '%'

    try:
        cnt_pass_rate = round(cnt_passed / cnt_tests * 100)
    except ZeroDivisionError:
        cnt_pass_rate = 0

    statis['Count']['Total Tests'] = str(cnt_tests)
    statis['Count']['Passed'] = str(cnt_passed)
    statis['Count']['Failed'] = str(cnt_failed)
    statis['Count']['Pass Rate'] = str(cnt_pass_rate) + '%'

    return statis


def pytest_sessionfinish(session, exitstatus):
    g_ssh_master.close_conn()
    g_ssh_slave.close_conn()

    # print('run status code:', exitstatus)
    # print(session.results)


# @pytest.fixture(scope='session', autouse=True)
# def setup_and_teardown():
#     yield
#     g_ssh_master.close_conn()
#     g_ssh_slave.close_conn()


@pytest.mark.optionalhook
def pytest_html_results_summary(prefix, summary, postfix):
    for idx, item in enumerate(summary):
        if 'skipped' in str(item):
            del summary[idx:idx+3]
    for idx, item in enumerate(summary):
        if 'xfailed' in str(item):
            del summary[idx:idx+3]
    for idx, item in enumerate(summary):
        if 'xpassed' in str(item):
            del summary[idx:idx+2]

    global statis
    postfix.extend([html.br('')])
    postfix.extend(gen_table_tag(get_rst_statis()))


@pytest.mark.optionalhook
def pytest_html_results_table_html(report, data):
    if report.passed:
        del data[:]


@pytest.mark.optionalhook
def pytest_html_results_table_header(cells):
    del cells[-1]


@pytest.mark.optionalhook
def pytest_html_results_table_row(report, cells):
    del cells[-1]


# def pytest_configure(config):
#     del config._metadata
