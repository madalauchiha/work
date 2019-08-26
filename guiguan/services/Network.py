#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from common.manip_case_table import parse_cell_value
from common.check_result import *
from common.comm_paras import g_logger
from time import sleep

g_case_input = None
g_case_expt = None


def switch_internal():
    switch_net_internal()

    sleep(40)

    chk_ping_ip()


def switch_external():

    switch_net_external()


def switch_wifi():

    switch_net_wifi()


def check_4g_mod():
    usbids = get_ma_lsusb()

    chk_expt_words_exist(g_case_expt, usbids)


def check_4g_usb_dev():
    usbdevs = get_ma_usb_dev()
    chk_expt_words_exist(g_case_expt, usbdevs)


def check_wvdial_info():
    info = get_wvdial_info()

    chk_wvdial_info(info)


def check_ppp0_exists():
    chk_ppp0_exists()


def ping_ip():
    get_sys_cfg_rec()

    chk_ping_ip()


def ping_url():
    get_sys_cfg_rec()

    chk_ping_url()


def check_uploaded_log():
    get_sys_cfg_rec()

    log_date = get_latest_uos_log()

    chk_ftp_fs_log_size(log_date)


def download_data():
    get_sys_cfg_rec()

    chk_download()


def check_ppp0_not_exist():
    chk_ppp0_not_exist()


def check_wvdial_not_exist():
    chk_wvdial_not_exist()


def check_external_ip():
    chk_exter_gateway()


def connect_wifi():
    uname = g_case_input['username']
    pwd = g_case_input['password']
    set_wifi(uname, pwd)

    chk_wifi_cfg(uname, pwd)


def check_wlan0_exists():
    chk_wlan0_exists()


def ota_full():
    get_sys_cfg_rec()

    do_ota_full(g_case_input)

    chk_uos_launch(OTA_UOS_DIR)

    chk_ota_version(g_case_input['version'])


def ota_delta():
    get_sys_cfg_rec()

    do_ota_delta()

    chk_uos_launch(OTA_UOS_DIR)

    chk_ota_version(g_case_input['version'])


def wifi_upload_data():
    get_sys_cfg_rec()

    ip_wifi = get_wifi_ip()

    scp_file_ma_to_lo(ip_wifi)


def wifi_download_data():
    get_sys_cfg_rec()

    ip_wifi = get_wifi_ip()

    scp_file_lo_to_ma(ip_wifi)


dict_func = {
    'switch to internal': switch_internal,
    'switch to external': switch_external,
    'switch to wifi': switch_wifi,
    'switch internal to external': switch_external,
    'switch external to wifi': switch_wifi,
    'switch wifi to internal': switch_internal,
    'switch internal to wifi': switch_wifi,
    'switch wifi to external': switch_external,
    'switch external to internal': switch_internal,
    'check 4g module': check_4g_mod,
    'check 4g usb dev': check_4g_usb_dev,
    'check wvdial info': check_wvdial_info,
    'check ppp0 exists': check_ppp0_exists,
    'ping IP': ping_ip,
    'ping URL': ping_url,
    'check uploaded log': check_uploaded_log,
    'download data': download_data,
    'check ppp0 not exist': check_ppp0_not_exist,
    'check wvdial not exist': check_wvdial_not_exist,
    'check external IP': check_external_ip,
    'set wifi': connect_wifi,
    'check wifi config': connect_wifi,
    'check wlan0 exists': check_wlan0_exists,
    'OTA full': ota_full,
    'OTA delta': ota_delta,
    'wifi upload data': wifi_upload_data,
    'wifi download data': wifi_download_data,
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
