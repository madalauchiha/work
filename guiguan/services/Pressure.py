#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from common.manip_case_table import parse_cell_value
from common.check_result import *
from common.comm_paras import g_logger

import pexpect
g_case_input = None
g_case_expt = None


def dpkg_arm(name, path):
    proc = pexpect.spawn('ssh -X worker@' + MASTER_IP)
    proc.expect("worker@" + MASTER_IP + "'s password:", timeout=3)
    proc.sendline('uisee')
    proc.expect('worker@master')
    time.sleep(8)
    proc.sendline("sudo dpkg -i /home/worker/{}/{}_arm64.deb".format(name, path))
    proc.expect(r"please choose project, \[1/2/3/4/5/6/7")
    proc.sendline("1")
    proc.expect(r"Would you like to update/create superuser now")
    proc.sendline("yes")
    proc.expect(r"Username \(leave blank to use \'root\'\):")
    proc.sendline("root")
    proc.expect("Password:")
    proc.sendline("root")
    proc.expect("Password \(again\):")
    proc.sendline("root")
    proc.expect("insert new vehicle")
    proc.sendline("y")
    proc.expect("vehicle name:")
    proc.sendline("e100")
    proc.expect("map id:")
    proc.sendline("1")
    proc.expect("installation path of uos:")
    proc.sendline("/home/worker/{}/run".format(name))
    proc.expect("worker@master")
    g_logger.info(bytes.decode(proc.before))
    print(bytes.decode(proc.before))
    proc.close()

def chk_service():
    stdout = g_ssh_master.exec_cmd("systemctl status uisee_io_dispatch.service")
    g_logger.info(stdout)
    if "Active: active (running)" not in stdout:
        assert False, "Service startup failed"


def hmi_uisee_io_dispatch():
    name = "prod_cq"
    path = "hmi"
    g_ssh_master.exec_cmd("cd /home/worker/{}/backend_deps/prepare_16.04_armhf/;sudo ./cleanhmi.sh".format(name))
    g_ssh_master.exec_cmd("cd /home/worker/{}/backend_deps/prepare_16.04_armhf/;sudo ./install.sh".format(name))
    dpkg_arm(name, path)

    reboot_os()

    chk_service()


def compass_uisee_io_dispatch():
    name = "arm"
    path = "compass"
    g_ssh_master.exec_cmd("cd /home/worker/{}/backend_deps/prepare_16.04_arm64/;sudo ./cleancompass.sh".format(name))
    g_ssh_master.exec_cmd("cd /home/worker/{}/backend_deps/prepare_16.04_arm64/;sudo ./install.sh".format(name))
    dpkg_arm(name, path)

    reboot_os()

    chk_service()


dict_func = {
    "hmi_uisee_io_dispatch": hmi_uisee_io_dispatch,
    "compass_uisee_io_dispatch": compass_uisee_io_dispatch
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
    dpkg_arm("prod_cq","hmi")
    # reboot_os()