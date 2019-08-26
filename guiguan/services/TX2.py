#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from common.manip_case_table import parse_cell_value
from common.check_result import *
from common.comm_paras import g_logger

g_case_input = None
g_case_expt = None


def check_version():
    # get list_version info
    dict_rst = get_list_ver()

    # check
    chk_dict_rst(g_case_expt, dict_rst)


def degrade_os_ver():
    # copy version to master host
    vername = g_case_input['version']
    verpath = os.path.join(OS_VER_DIR, vername)
    cp_pth_to_ma(verpath, TEST_DIR)

    list_old = get_sys_cfg_rec()

    # exec degrade cmd
    apply_os_ver(vername)

    # remove testdata dir
    rm_ma_dir(TEST_DIR)

    list_new = get_sys_cfg_rec()

    # check version
    dict_rst = get_list_ver()
    chk_dict_rst_with_key('System Version', g_case_expt, dict_rst)

    if set(list_old) - set(list_new):
        assert False, 'sys_cfg_rec not equal after os degrade!'


def upgrade_os_ver():
    # copy version to master host
    vername = g_case_input['version']
    verpath = os.path.join(OS_VER_DIR, vername)
    cp_pth_to_ma(verpath, TEST_DIR)

    list_old = get_sys_cfg_rec()

    # exec degrade cmd
    apply_os_ver(vername)

    # remove testdata dir
    rm_ma_dir(TEST_DIR)

    list_new = get_sys_cfg_rec()

    # check version
    dict_rst = get_list_ver()
    chk_dict_rst_with_key('System Version', g_case_expt, dict_rst)

    if set(list_old) - set(list_new):
        assert False, 'sys_cfg_rec not equal after os upgrade!'


def set_prod_type_cq():
    # exec cmd
    prod_type = 'cq'
    set_prod_type(prod_type)

    # check uisee_release
    dict_rst = get_ma_uisee_rel()
    chk_dict_rst_with_key('ProductType', g_case_expt, dict_rst)

    # check list_version
    dict_rst = get_list_ver()
    chk_dict_rst_with_key('Board Type', g_case_expt, dict_rst)

    # check master APU target version name
    chk_prod_type_in_apu(g_case_expt['ProductType'])

    # check slave FPGA version name
    chk_prod_type_in_fpga(g_case_expt['ProductType'])


def set_prod_type_gg():
    # exec cmd
    prod_type = 'gg'
    set_prod_type(prod_type)

    # check uisee_release
    dict_rst = get_ma_uisee_rel()
    chk_dict_rst_with_key('ProductType', g_case_expt, dict_rst)

    # check list_version
    dict_rst = get_list_ver()
    chk_dict_rst_with_key('Board Type', g_case_expt, dict_rst)

    # check master APU target version name
    chk_prod_type_in_apu(g_case_expt['ProductType'])

    # check slave FPGA version name
    chk_prod_type_in_fpga(g_case_expt['ProductType'])


def degrade_fpga_ver():
    # exec degrade
    verno = g_case_input['FPGA Version']
    burn_fpga_ver(verno)

    # need power off reset

    # check FPGA version
    dict_rst = get_list_ver()
    chk_dict_rst_with_key('FPGA Version', g_case_expt, dict_rst)


def upgrade_fpga_ver():
    # exec degrade
    verno = g_case_input['FPGA Version']
    burn_fpga_ver(verno)

    # need power off reset

    # check FPGA version
    dict_rst = get_list_ver()
    chk_dict_rst_with_key('FPGA Version', g_case_expt, dict_rst)


def check_video_stat():
    # get video status
    dict_rst = get_video_status()

    # check
    chk_dict_rst(g_case_expt, dict_rst)


def check_master_ip():
    # get master ip
    dict_ip = get_ma_ip()

    # check
    chk_dict_rst_with_key('IP', g_case_expt, dict_ip)


def check_ma_disk_size():
    # get master disk size
    dict_disk = get_ma_disk_info()

    # check
    chk_dict_rst(g_case_expt, dict_disk)


def check_ma_uisee_rel():
    dict_rel = get_ma_uisee_rel()
    chk_dict_rst(g_case_expt, dict_rel)


def check_ma_dev_info():
    # get lsmod info
    modinfo = get_ma_lsmod()

    chk_expt_words_exist(g_case_expt, modinfo)


def check_ma_apu_host_dir():
    list_rst = ls_ma_dir(APU_HOST_DIR)

    chk_expt_words_exist(g_case_expt, list_rst)


def check_ma_apu_target_dir():
    list_rst = ls_ma_dir(APU_VER_DIR)

    chk_expt_words_exist(g_case_expt, list_rst)


def check_ma_uisee_ko_info():
    dict_rst = get_ma_modinfo(UISEE_KO_PATH)

    chk_expt_words_exist(g_case_expt, dict_rst.keys())


def check_slave_ip():
    # get slave ip
    dict_ip = get_sl_ip()

    # check
    chk_dict_rst_with_key('IP', g_case_expt, dict_ip)


def check_sl_disk_size():
    # get slave disk size
    dict_disk = get_sl_disk_info()

    # check
    chk_dict_rst(g_case_expt, dict_disk)


def check_sl_uisee_rel():
    dict_rel = get_sl_uisee_rel()
    chk_dict_rst(g_case_expt, dict_rel)


def check_sl_dev_info():
    # get lsmod info
    modinfo = get_sl_lsmod()

    chk_expt_words_exist(g_case_expt, modinfo)


def check_sl_apu_host_dir():
    list_rst = ls_sl_dir(APU_HOST_DIR)

    chk_expt_words_exist(g_case_expt, list_rst)


def check_sl_apu_target_dir():
    list_rst = ls_sl_dir(APU_VER_DIR)

    chk_expt_words_exist(g_case_expt, list_rst)


def check_sl_uisee_ko_info():
    dict_rst = get_sl_modinfo(UISEE_KO_PATH)

    chk_expt_words_exist(g_case_expt, dict_rst.keys())


def check_sl_video_dev():
    str_rst = get_sl_video_dev()

    chk_expt_words_exist(g_case_expt, str_rst)


def check_ma_video_dev():
    str_rst = get_ma_video_dev()

    chk_expt_words_exist(g_case_expt, str_rst)


def ma_ssh_sl_with_name():

    chk_ma_ssh_sl('slave')


def ma_ssh_sl_with_ip():

    chk_ma_ssh_sl(SLAVE_IP)


def ma_ping_sl_with_name():

    ma_ping('slave')


def ma_ping_sl_with_ip():

    ma_ping(SLAVE_IP)


def sl_ssh_ma_with_name():

    chk_sl_ssh_ma('master')


def sl_ssh_ma_with_ip():

    chk_sl_ssh_ma(MASTER_IP)


def sl_ping_ma_with_name():

    sl_ping('master')


def sl_ping_ma_with_ip():

    sl_ping(MASTER_IP)


def check_time_consist():

    chk_ma_sl_time()


def mod_ma_time():

    mod_and_chk_ma_time()


def mod_sl_time():

    mod_and_chk_sl_time()


def check_time_correct():
    chk_ma_loc_time()
    chk_sl_loc_time()


def local_uos_prepare():
    prepare_local_uos(g_case_input)


def launch_stop_uos():
    chk_uos_launch(g_case_input['uosdir'])


def switch_ftp_enable():
    enable_ftp()

    cmd = SWITCH_FTP + 'enable'

    if cmd != get_sys_cfg_rec()[-1]:
        assert False, 'enable ftp fail!'

    chk_ftp_open()


def switch_ftp_disable():
    disable_ftp()

    cmd = SWITCH_FTP + 'disable'

    if cmd != get_sys_cfg_rec()[-1]:
        assert False, 'disable ftp fail!'

    chk_ftp_closed()


def connect_ftp():
    proc = open_ma_ftp()

    close_ftp(proc)


def ftp_add_file():
    fname = 'test.log'
    fpath = os.path.join(UOS_LOG_DIR, fname)

    rm_ma_file(fpath)
    touch_ma_file(fpath)

    chk_ftp_file_exist(fname)

    rm_ma_file(fpath)


def ftp_mod_and_down_file():
    text = 'test'
    fname = 'test.log'
    fpath_ma = os.path.join(UOS_LOG_DIR, fname)
    fpath_loc = os.path.join(os.getcwd(), fname)

    rm_ma_file(fpath_ma)
    rm_loc_file(fpath_loc)

    add_text_to_ma_file(fpath_ma, text)

    chk_ftp_file_content(fname, text)

    rm_ma_file(fpath_ma)
    rm_loc_file(fpath_loc)


def ftp_rm_file():
    fname = 'test.log'
    fpath = os.path.join(UOS_LOG_DIR, fname)

    rm_ma_file(fpath)
    touch_ma_file(fpath)

    chk_ftp_file_exist(fname)

    rm_ma_file(fpath)

    chk_ftp_file_not_exist(fname)


def ftp_get_big_file():
    fname = g_case_input['file']
    big_file_path = os.path.join(OS_VER_DIR, fname)
    fpath_ma = os.path.join(UOS_LOG_DIR, fname)
    down_file_path = os.path.join(os.getcwd(), fname)

    rm_ma_file(fpath_ma)
    rm_loc_file(down_file_path)

    cp_pth_to_ma(big_file_path, UOS_LOG_DIR)

    ftp_get(fname)

    if os.path.getsize(down_file_path) != os.path.getsize(big_file_path):
        rm_ma_file(fpath_ma)
        rm_loc_file(down_file_path)
        assert False, 'size of downloaded file [{}] is wrong!'

    rm_ma_file(fpath_ma)
    rm_loc_file(down_file_path)


def check_ftp_closed():
    disable_ftp()

    chk_ftp_closed()

    enable_ftp()


def check_os_reboot():
    rst_dmesg = reboot_os()

    chk_dmesg_info('master', rst_dmesg[0])
    chk_dmesg_info('slave', rst_dmesg[1])


dict_func = {
    'check os reboot': check_os_reboot,
    'check version': check_version,
    'degrade os verision': degrade_os_ver,
    'upgrade os verision': upgrade_os_ver,
    'set product type cq': set_prod_type_cq,
    'set product type gg': set_prod_type_gg,

    'degrade fpga verision': degrade_fpga_ver,
    'upgrade fpga verision': upgrade_fpga_ver,
    'check video status': check_video_stat,
    'check master IP': check_master_ip,
    'check master disk size': check_ma_disk_size,
    'check master uisee release info': check_ma_uisee_rel,
    'check master dev info': check_ma_dev_info,
    'check master APU host dir': check_ma_apu_host_dir,
    'check master APU target dir': check_ma_apu_target_dir,
    'check master uisee.ko info': check_ma_uisee_ko_info,
    'check master video dev': check_ma_video_dev,
    'check slave IP': check_slave_ip,
    'check slave disk size': check_sl_disk_size,
    'check slave uisee release info': check_sl_uisee_rel,
    'check slave device info': check_sl_dev_info,
    'check slave APU host dir': check_sl_apu_host_dir,
    'check slave APU target dir': check_sl_apu_target_dir,
    'check slave uisee.ko info': check_sl_uisee_ko_info,
    'check slave video dev': check_sl_video_dev,

    'master ssh slave with name': ma_ssh_sl_with_name,
    'master ssh slave with IP': ma_ssh_sl_with_ip,
    'master ping slave with name': ma_ping_sl_with_name,
    'master ping slave with IP': ma_ping_sl_with_ip,
    'slave ssh master with name': sl_ssh_ma_with_name,
    'slave ssh master with IP': sl_ssh_ma_with_ip,
    'slave ping master with name': sl_ping_ma_with_name,
    'slave ping master with IP': sl_ping_ma_with_ip,
    'check time consistency': check_time_consist,
    'modify master time': mod_ma_time,
    'modify slave time': mod_sl_time,
    'check time correctness': check_time_correct,

    'launch and stop uos': launch_stop_uos,
    'switch ftp enable': switch_ftp_enable,
    'switch ftp disable': switch_ftp_disable,
    'ftp master': connect_ftp,
    'ftp add file': ftp_add_file,
    'ftp modify file': ftp_mod_and_down_file,
    'ftp get file': ftp_mod_and_down_file,
    'ftp remove file': ftp_rm_file,
    'ftp_get_big_file': ftp_get_big_file,
    'get file when ftp closed': check_ftp_closed,
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
    # ftp_add_file()
    # check_os_reboot()

    cnt = 0
    while True:
        ma_ssh_sl_with_name()
        cnt += 1
        print('===%d===' % cnt)
