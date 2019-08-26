#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from common.manip_cfg_file import *
from common.host_visitor import HostVisitor
from common.record_time_log import logger

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
CFG_DIR = os.path.join(ROOT_DIR, 'configs')
CASE_DIR = os.path.join(ROOT_DIR, 'testcases')
REPORT_DIR = os.path.join(ROOT_DIR, 'report')
DATA_DIR = os.path.join(ROOT_DIR, 'data')
OS_VER_DIR = os.path.join(DATA_DIR, 'os_version')
UOS_VER_DIR = os.path.join(DATA_DIR, 'uos_version')
OTA_DATA_DIR = os.path.join(DATA_DIR, 'ota')
SHELL_DIR = os.path.join(DATA_DIR, 'shell')
DGPS_DIR = os.path.join(DATA_DIR, 'dgps')
APU_LOCAL_DIR = os.path.join(DATA_DIR, 'apu')

CFG_FILE_PATH = os.path.join(CFG_DIR, 'config.ini')
MOD_FILE_PATH = os.path.join(CFG_DIR, 'module.ini')
CASE_XLS_PATH = os.path.join(CASE_DIR, 'case_cq.xlsx')
board_type = get_hardware_cfg(CFG_FILE_PATH)['board_type']
if 'gg' == board_type:
    CASE_XLS_PATH = os.path.join(CASE_DIR, 'case_gg.xlsx')

MASTER_IP = get_host_cfg(CFG_FILE_PATH, 'host')['masterip']
SLAVE_IP = get_host_cfg(CFG_FILE_PATH, 'host')['slaveip']

# MASTER_IP_1 = get_host_cfg(CFG_FILE_PATH, 'host_1')['masterip']
# SLAVE_IP_1 = get_host_cfg(CFG_FILE_PATH, 'host_1')['slaveip']
#
# MASTER_IP_2 = get_host_cfg(CFG_FILE_PATH, 'host_2')['masterip']
# SLAVE_IP_2 = get_host_cfg(CFG_FILE_PATH, 'host_2')['slaveip']
#
# MASTER_IP_3 = get_host_cfg(CFG_FILE_PATH, 'host_3')['masterip']
# SLAVE_IP_3 = get_host_cfg(CFG_FILE_PATH, 'host_3')['slaveip']
#
# MASTER_IP_4 = get_host_cfg(CFG_FILE_PATH, 'host_4')['masterip']
# SLAVE_IP_4 = get_host_cfg(CFG_FILE_PATH, 'host_4')['slaveip']
#
# MASTER_IP_5 = get_host_cfg(CFG_FILE_PATH, 'host_5')['masterip']
# SLAVE_IP_5 = get_host_cfg(CFG_FILE_PATH, 'host_5')['slaveip']
#
# MASTER_IP_6 = get_host_cfg(CFG_FILE_PATH, 'host_6')['masterip']
# SLAVE_IP_6 = get_host_cfg(CFG_FILE_PATH, 'host_6')['slaveip']
LOG_FTP_IP = get_log_serv_cfg(CFG_FILE_PATH)['ip']

HOME_DIR = '/home/worker'
TEST_DIR = '/home/worker/testdata'
APU_HOST_DIR = '/home/worker/firmware/APU/host/'
APU_VER_DIR = '/home/worker/firmware/APU/target/'
FPGA_VER_DIR = '/home/worker/firmware/FPGA'
UISEE_KO_PATH = '/opt/pcie_v4l2_mono6/app/uisee.ko'
DEV_DIR = '/dev'
UOS_LOG_DIR = '/home/worker/UISEE_LOGS'
SYS_CFG_REC_PATH = '/etc/sys_cfg_rec'
NETWORK_CFG_PATH = '/etc/network/interfaces'
UOS_CFG_DIR = '/home/worker/config'
OTA_UOS_DIR = '/home/worker/uos'
OTA_UOS_DATA_DIR = '/home/worker/uos/data'

FTP_LOG_DIR_FS = '/uisee_log_fs'

UOS_CQ_APU = '/home/worker/firmware/APU/target/'
UPDATA_APU = "cd firmware/APU/host ; ./updata_apu.sh /dev/ttyTHS2 ../target/"
BIN_VSTREAM_TEST = "cd uos/run/ ; source set_env.sh ; timeout 10 ./bin/vstream-test   -c   /dev/ttyTHS2"

g_ssh_master = HostVisitor(hostip=MASTER_IP)
g_ssh_slave = HostVisitor(hostip=SLAVE_IP)

# g_ssh_master_1 = HostVisitor(hostip=MASTER_IP_1)
# g_ssh_slave_1 = HostVisitor(hostip=SLAVE_IP_1, port=10022)
#
# g_ssh_master_2 = HostVisitor(hostip=MASTER_IP_2)
# g_ssh_slave_2 = HostVisitor(hostip=SLAVE_IP_2, port=10022)
#
# g_ssh_master_3 = HostVisitor(hostip=MASTER_IP_3)
# g_ssh_slave_3 = HostVisitor(hostip=SLAVE_IP_3, port=10022)
#
# g_ssh_master_4 = HostVisitor(hostip=MASTER_IP_4)
# g_ssh_slave_4 = HostVisitor(hostip=SLAVE_IP_4, port=10022)
#
# g_ssh_master_5 = HostVisitor(hostip=MASTER_IP_5)
# g_ssh_slave_5 = HostVisitor(hostip=SLAVE_IP_5, port=10022)
#
# g_ssh_master_6 = HostVisitor(hostip=MASTER_IP_6)
# g_ssh_slave_6 = HostVisitor(hostip=SLAVE_IP_6, port=10022)

g_logger = logger
g_mods = get_mod_cfg(MOD_FILE_PATH)
g_rst_xy = dict()

if __name__ == '__main__':
    print(MASTER_IP)