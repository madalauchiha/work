#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from common.manip_case_table import parse_cell_value
from common.check_result import *
from common.comm_paras import g_logger

g_case_input = None
g_case_expt = None


def check_sl_ssd_exists():
    chk_ssd_exists('slave')


def check_sl_exter_disk_type():
    chk_exter_disk_type('slave')


def check_sl_ssd_size():
    chk_ssd_size('slave')


def sl_cp_file_to_disk():
    chk_cp_file_to_disk('slave')


def sl_dd_file_to_disk():
    chk_dd_file_to_disk('slave')


def sl_dd_file_to_disk_sync():
    chk_dd_file_to_disk_sync('slave')


def sl_dd_file_to_disk_fdsync():
    chk_dd_file_to_disk_fdsync('slave')


def sl_dd_file_to_disk_dsync():
    chk_dd_file_to_disk_dsync('slave')


def sl_cp_file_from_disk():
    chk_cp_file_from_disk('slave')


def sl_dd_file_from_disk():
    chk_dd_file_from_disk('slave')


def sl_dd_file_from_disk_sync():
    chk_dd_file_from_disk_sync('slave')


def sl_dd_file_from_disk_fdsync():
    chk_dd_file_from_disk_fdsync('slave')


def sl_dd_file_from_disk_dsync():
    chk_dd_file_from_disk_dsync('slave')


def check_ma_ssd_exists():
    chk_ssd_exists('master')


def check_ma_exter_disk_type():
    chk_exter_disk_type('master')


def check_ma_ssd_size():
    chk_ssd_size('master')


def ma_cp_file_to_disk():
    chk_cp_file_to_disk('master')


def ma_dd_file_to_disk():
    chk_dd_file_to_disk('master')


def ma_dd_file_to_disk_sync():
    chk_dd_file_to_disk_sync('master')


def ma_dd_file_to_disk_fdsync():
    chk_dd_file_to_disk_fdsync('master')


def ma_dd_file_to_disk_dsync():
    chk_dd_file_to_disk_dsync('master')


def ma_cp_file_from_disk():
    chk_cp_file_from_disk('master')


def ma_dd_file_from_disk():
    chk_dd_file_from_disk('master')


def ma_dd_file_from_disk_sync():
    chk_dd_file_from_disk_sync('master')


def ma_dd_file_from_disk_fdsync():
    chk_dd_file_from_disk_fdsync('master')


def ma_dd_file_from_disk_dsync():
    chk_dd_file_from_disk_dsync('master')


dict_func = {
    'slave check SSD exists': check_sl_ssd_exists,
    'slave check external disk type': check_sl_exter_disk_type,
    'slave check SSD size': check_sl_ssd_size,
    'slave cp file to disk': sl_cp_file_to_disk,
    'slave dd file to disk': sl_dd_file_to_disk,
    'slave dd file to disk sync': sl_dd_file_to_disk_sync,
    'slave dd file to disk fdatasync': sl_dd_file_to_disk_fdsync,
    'slave dd file to disk dsync': sl_dd_file_to_disk_dsync,
    'slave cp file from disk': sl_cp_file_from_disk,
    'slave dd file from disk': sl_dd_file_from_disk,
    'slave dd file from disk sync': sl_dd_file_from_disk_sync,
    'slave dd file from disk fdatasync': sl_dd_file_from_disk_fdsync,
    'slave dd file from disk dsync': sl_dd_file_from_disk_dsync,
    'master check SSD exists': check_ma_ssd_exists,
    'master check external disk type': check_ma_exter_disk_type,
    'master check SSD size': check_ma_ssd_size,
    'master cp file to disk': ma_cp_file_to_disk,
    'master dd file to disk': ma_dd_file_to_disk,
    'master dd file to disk sync': ma_dd_file_to_disk_sync,
    'master dd file to disk fdatasync': ma_dd_file_to_disk_fdsync,
    'master dd file to disk dsync': ma_dd_file_to_disk_dsync,
    'master cp file from disk': ma_cp_file_from_disk,
    'master dd file from disk': ma_dd_file_from_disk,
    'master dd file from disk sync': ma_dd_file_from_disk_sync,
    'master dd file from disk fdatasync': ma_dd_file_from_disk_fdsync,
    'master dd file from disk dsync': ma_dd_file_from_disk_dsync,
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
    pass
