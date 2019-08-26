#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from common.manip_case_table import parse_cell_value
from common.check_result import *
from common.comm_paras import g_logger

g_case_input = None
g_case_expt = None


def master_udisk_exists():
    chk_ma_udisk_exists()


def master_ehd_exists():
    chk_ma_ehd_exists()


def mv_file_between_ma_udisk():
    chk_ma_file_io_exter('udisk')


def mv_file_between_ma_ehd():
    chk_ma_file_io_exter('ehd')


def slave_udisk_exists():
    chk_sl_udisk_exists()


def slave_ehd_exists():
    chk_sl_ehd_exists()


def mv_file_between_sl_udisk():
    chk_sl_file_io_exter('udisk')


def mv_file_between_sl_ehd():
    chk_sl_file_io_exter('ehd')


dict_func = {
    'master udisk exists': master_udisk_exists,
    'copy file master to udisk': mv_file_between_ma_udisk,
    'copy file udisk to master': mv_file_between_ma_udisk,
    'slave udisk exists': slave_udisk_exists,
    'copy file slave to udisk': mv_file_between_sl_udisk,
    'copy file udisk to slave': mv_file_between_sl_udisk,
    'master EHD exists': master_ehd_exists,
    'copy file master to EHD': mv_file_between_ma_ehd,
    'copy file EHD to master': mv_file_between_ma_ehd,
    'slave EHD exists': slave_ehd_exists,
    'copy file slave to EHD': mv_file_between_sl_ehd,
    'copy file EHD to slave': mv_file_between_sl_ehd,
}


def run_case(case_name, case_input, case_expt):
    global g_case_input
    global g_case_expt

    g_logger.info(case_name)

    g_case_input = parse_cell_value(case_input)
    g_case_expt = parse_cell_value(case_expt)

    dict_func[case_name]()

    return True


if '__main__' == __name__:
    switch_internal()
