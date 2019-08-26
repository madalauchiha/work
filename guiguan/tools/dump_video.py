#!/usr/local/bin/env python
# -*- coding: utf-8 -*-

from tools.power_ctrl import power_off, power_on
import time
from common.operate_os import try_ssh_conn
from common.comm_paras import MASTER_IP, SLAVE_IP, g_ssh_master, g_ssh_slave
from common.record_time_log import logger
import sys
from common.command import *


def check_ssh():
    print('waiting for os boot, cost 30s...')
    time.sleep(30)
    print('waiting for ssh connection resume...')

    time_start = time.time()
    print('====== test ssh conn start ======')
    ssh_ma_cnt = try_ssh_conn(MASTER_IP)
    ssh_sl_cnt = try_ssh_conn(SLAVE_IP)
    time.sleep(3)
    print('====== test ssh conn again ======')
    ssh_ma_cnt += try_ssh_conn(MASTER_IP)
    ssh_sl_cnt += try_ssh_conn(SLAVE_IP)
    time.sleep(3)
    print('====== test ssh conn again ======')
    ssh_ma_cnt += try_ssh_conn(MASTER_IP)
    ssh_sl_cnt += try_ssh_conn(SLAVE_IP)
    print('====== test ssh conn end ======')
    time_end = time.time()
    time_cost = time_end - time_start
    if 40 < time_cost:
        logger.error('ssh resume cost time %.2fs, os reboot problem, wait 5 mins to confirm!' % time_cost)
        time.sleep(300)

        time_start2 = time.time()
        print('====== test ssh conn start ======')
        ssh_ma_cnt = try_ssh_conn(MASTER_IP)
        ssh_sl_cnt = try_ssh_conn(SLAVE_IP)
        time.sleep(3)
        print('====== test ssh conn again ======')
        ssh_ma_cnt += try_ssh_conn(MASTER_IP)
        ssh_sl_cnt += try_ssh_conn(SLAVE_IP)
        time.sleep(3)
        print('====== test ssh conn again ======')
        ssh_ma_cnt += try_ssh_conn(MASTER_IP)
        ssh_sl_cnt += try_ssh_conn(SLAVE_IP)
        print('====== test ssh conn end ======')
        time_end2 = time.time()
        time_cost2 = time_end2 - time_start2
        if 40 < time_cost2:
            logger.error('os reboot problem, ssh can not resume!')
            sys.exit(1)

    fail_cnt = 0
    while True:
        if g_ssh_master.reconnect():
            print('master ssh connection resume success.')
            break

        print('master ssh connection resume fail, try again!')
        fail_cnt += 1
        if 10 == fail_cnt:
            logger.error('try [{}] times, master ssh conn resume fail!'.format(fail_cnt))
            sys.exit(1)

        time.sleep(10)

        ssh_ma_cnt += try_ssh_conn(MASTER_IP)
        ssh_sl_cnt += try_ssh_conn(SLAVE_IP)

    fail_cnt = 0
    while True:
        if g_ssh_slave.reconnect():
            print('slave ssh connection resume success.')
            break

        print('slave ssh connection resume fail, try again!')
        fail_cnt += 1
        if 10 == fail_cnt:
            logger.error('try [{}] times, slave ssh conn resume fail!'.format(fail_cnt))
            sys.exit(1)

        time.sleep(10)

        ssh_ma_cnt += try_ssh_conn(MASTER_IP)
        ssh_sl_cnt += try_ssh_conn(SLAVE_IP)

    print('reboot completed.')

    time.sleep(1)

    dmesg_master = g_ssh_master.exec_cmd('dmesg')
    dmesg_slave = g_ssh_slave.exec_cmd('dmesg')

    # if 40 < time_cost:
    #     assert False, 'ssh resume cost > %.2fs, expect < 40s!' % time_cost

    return dmesg_master, dmesg_slave


def power_switch_and_dump_video():
    cnt = 0
    while True:
        cnt += 1

        logger.info('======= round %d power off start =======' % cnt)

        power_off()
        print('sleep 15s...')
        time.sleep(15)
        power_on()

        logger.info('======= round %d power on end =======' % cnt)

        check_ssh()

        try:
            g_ssh_master.exec_cmd(CONFIG_UB964)
            g_ssh_master.exec_cmd(DUMP_VIDEO0 + '4')
            g_ssh_master.exec_cmd(DUMP_VIDEO1 + '4')
            g_ssh_slave.exec_cmd(DUMP_VIDEO0 + '4')
            g_ssh_slave.exec_cmd(DUMP_VIDEO1 + '4')
        except Exception as e:
            print(e)
            sys.exit(1)


if __name__ == '__main__':
    power_switch_and_dump_video()
