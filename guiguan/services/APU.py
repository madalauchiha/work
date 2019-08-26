#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from common.manip_case_table import *
from common.check_result import *
from common.record_time_log import *
import time

import pexpect
import re


g_case_input = None
g_case_expt = None


def get_apu_result(apu_path):

    stdout = g_ssh_master.exec_cmd(apu_path)
    list_key_val = []

    list_line = stdout.split('\n')
    list_line.remove('')
    for line in list_line:
        list_key_val.append((line.strip()))
    # if len(list_key_val) <= 8:
    #     get_apu_result(apu_path)
    return str(list_key_val[:])


def apu_firmware(num):
    apu_ver = g_case_input['burn_apu_e{}00'.format(num)]
    apupath = os.path.join(UOS_CQ_APU, apu_ver)
    return apupath


def apu_path_up(num):
    apu_ver = g_case_input['updata_apu_e{}00'.format(num)]
    apupath = os.path.join(UPDATA_APU, apu_ver)
    return apupath


def check_apu_number():
    proc = pexpect.spawn('ssh -X worker@' + MASTER_IP)
    proc.expect("worker@" + MASTER_IP + "'s password:", timeout=3)
    proc.sendline('uisee')
    proc.expect('worker@master:')

    cmd = "cd uos*/run/bin/apu/ ;python3 apu_conf.py uos_apu.json /dev/ttyTHS2"

    print('\n' + cmd + '\n')
    proc.sendline(cmd)
    proc.expect('waiting for enter key to exit')
    proc.sendline("")
    print(bytes.decode(proc.before).strip("\r").split("\n"))
    return bytes.decode(proc.before).strip("\r")


def check_apu_json_except():
    data = {}

    proc = pexpect.spawn('ssh -X worker@' + MASTER_IP)
    proc.expect("worker@" + MASTER_IP + "'s password:", timeout=3)
    proc.sendline('uisee')
    proc.expect('worker@master:')

    cmd = "cat uos/run/bin/apu/{}".format(g_case_expt["result"])

    print('\n' + cmd + '\n')
    proc.sendline(cmd)

    proc.expect('worker@master:')
    # json.load(bytes.decode(proc.before))

    dictdata = eval(bytes.decode(proc.before).strip("~$ cat uisee*/run/bin/apu/uos_apu.json"))
    for k, v in dictdata.items():
        if isinstance(v, list):
            for j in range(len(v)):
                data["brakes_array[%s]" % j] = str(v[j])
        else:
            data[k] = str(v)
    return data


def apu_conf_result(res):
    data = {}

    key = re.findall("request (.*) value\r", res)
    time.sleep(1)
    value = re.findall(">, value (.*)\r", res)

    for i in range(len(key)):
        data[key[i]] = value[i]

    return data


def timeout(num_time, comm):
    comm_timeout = "timeout {}".format(num_time) + comm
    return comm_timeout


def timeout_count_uos_cqe100_pro_srec(count):
    comm = apu_firmware(num=1)
    g_ssh_master.exec_cmd("timeout {} ".format(count)+BURN_APU+comm)

    time.sleep(10)
    apu_info = get_apu_result(BURN_APU+comm)

    return apu_info


# case


def burn_uos_cqe100_pro_srec():
    comm = apu_firmware(num=1)
    apu_info = get_apu_result(BURN_APU+comm)

    chk_expt_words_exist(g_case_expt, apu_info)

    # return chk_expt_apu(g_case_expt, apu_info)


def burn_uos_cqe200_pro_srec():
    comm = apu_firmware(num=2)
    apu_info = get_apu_result(BURN_APU+comm)

    chk_expt_words_exist(g_case_expt, apu_info)


def updata_uos_cqe100_pro_srec():
    comm = apu_path_up(num=1)
    apu_info = get_apu_result(comm)

    chk_expt_words_exist(g_case_expt, apu_info)


def updata_uos_cqe200_pro_srec():
    comm = apu_path_up(num=2)
    apu_info = get_apu_result(comm)

    chk_expt_words_exist(g_case_expt, apu_info)


def timeout_3_uos_upgrade_apu():
    apu_info = timeout_count_uos_cqe100_pro_srec(3)

    chk_expt_words_exist(g_case_expt, apu_info)


def timeout_5_uos_upgrade_apu():
    apu_info = timeout_count_uos_cqe100_pro_srec(5)

    chk_expt_words_exist(g_case_expt, apu_info)


def timeout_8_uos_upgrade_apu():
    apu_info = timeout_count_uos_cqe100_pro_srec(8)

    chk_expt_words_exist(g_case_expt, apu_info)


def reboot_uos_upgrade_apu():

    comm = apu_firmware(num=1)
    g_ssh_master.exec_cmd(BURN_APU+comm)
    reboot_os()

    apu_info = get_apu_result(BURN_APU+comm)

    chk_expt_words_exist(g_case_expt, apu_info)


def apu_vstream_test():
    apu_info = get_apu_result(BIN_VSTREAM_TEST)

    chk_expt_words_exist(g_case_expt, apu_info)


def apu_read_version():
    apu_script = g_case_input['script']
    apu_info = get_apu_result(PYTHON+APU_HOST_DIR+apu_script)

    chk_expt_words_exist(g_case_expt, apu_info)


def check_apu_conf():

    proc = check_apu_number()

    apu_info = apu_conf_result(proc)

    data = check_apu_json_except()

    chk_dict_rst(data, apu_info)


def updata_uos_e100_local():
    file = g_case_input['file']
    file_ext = os.path.splitext(file)[-1]
    if '.tar' == file_ext:
        filename = os.path.splitext(file)[0]
    elif '.gz' == file_ext:
        filename = file.replace('.tar.gz', '')
    else:
        assert False, 'expect apu ".tar" file in data/apu/, please check!'

    path_apu_local = os.path.join(APU_LOCAL_DIR, file)
    dir_apu_host = os.path.join(HOME_DIR, filename)

    upload_ma_tar_file(path_apu_local, HOME_DIR, filename, delflag=False)

    cmd = UPDATE_APU + os.path.join(dir_apu_host, g_case_input['version'])
    apu_info = get_apu_result(cmd)

    rm_ma_dir(dir_apu_host)

    chk_expt_words_exist(g_case_expt, apu_info)


dict_func = {
    'burn.sh_e100_upgrade_apu': burn_uos_cqe100_pro_srec,
    'burn.sh_e200_upgrade_apu': burn_uos_cqe200_pro_srec,
    'updata.sh_e100_upgrade_apu': updata_uos_cqe100_pro_srec,
    'updata.sh_e200_upgrade_apu': updata_uos_cqe200_pro_srec,
    'updata.sh_e100_upgrade_apu_local': updata_uos_e100_local,

    'timeout_3_e100_upgrade_apu': timeout_3_uos_upgrade_apu,
    'timeout_5_uos_upgrade_apu': timeout_5_uos_upgrade_apu,
    'timeout_8_uos_upgrade_apu': timeout_8_uos_upgrade_apu,

    'reboot_uos_upgrade_apu': reboot_uos_upgrade_apu,
    'apu_vstream_test': apu_vstream_test,
    'apu_read_version': apu_read_version,
    'check_apu_conf': check_apu_conf,
    }


def run_case(case_name, case_input, case_expt):
    global g_case_input
    global g_case_expt

    g_logger.info(case_name)

    g_case_input = parse_cell_value(case_input)

    g_case_expt = parse_cell_value(case_expt)

    dict_func[case_name]()

    return True


if __name__ == '__main__':
    updata_uos_e100_local()
