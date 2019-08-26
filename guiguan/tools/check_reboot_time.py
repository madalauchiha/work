#!/usr/local/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.extend(['/home/dingding/project/guiguan/venv/lib/python3.5/site-packages'])
sys.path.extend(['.'])

import serial.tools.list_ports
import modbus_tk.modbus_rtu
import modbus_tk.defines
import time
import pexpect
from host_visitor import HostVisitor

list_com_ports = serial.tools.list_ports.comports()
dict_com_ports = {}
list_str_ports = []
for item in list_com_ports:
    str_item = str(item)
    dict_com_ports[str_item] = item
    list_str_ports.append(str_item)

# print(dict_com_ports)


def power_off(com_port='/dev/ttyUSB0 - USB2.0-Serial'):
    ser = serial.Serial(dict_com_ports[com_port].device, 9600)

    try:
        master = modbus_tk.modbus_rtu.RtuMaster(ser)
        master.set_timeout(5)
        master.execute(1, modbus_tk.defines.WRITE_SINGLE_REGISTER, 1, 1, 0)
    except Exception as e:
        print(e)
        sys.exit(1)


def power_on(com_port='/dev/ttyUSB0 - USB2.0-Serial'):
    ser = serial.Serial(dict_com_ports[com_port].device, 9600)

    try:
        master = modbus_tk.modbus_rtu.RtuMaster(ser)
        master.set_timeout(5)
        master.execute(1, modbus_tk.defines.WRITE_SINGLE_REGISTER, 1, 1, 1)
    except Exception as e:
        print(e)
        sys.exit(1)


def check_ssh_pexpt(host_ip):
    ssh_cmd = 'ssh worker@' + host_ip
    proc = pexpect.spawn(ssh_cmd)

    idx = proc.expect(['password', 'worker', 'No route', pexpect.TIMEOUT, pexpect.EOF], timeout=2)

    if 0 == idx or 1 == idx:
        proc.sendcontrol('c')
        return proc, True
    else:
        proc.sendcontrol('c')
        return proc, False


def try_ssh_conn(hostip):
    ssh_try_cnt = 0
    while True:
        ssh_try_cnt += 1
        print('====== %d time ssh conn to %s start ======' % (ssh_try_cnt, hostip))
        proc, rst = check_ssh_pexpt(hostip)
        if proc.isalive():
            proc.kill(0)

        if not rst:
            print('ssh conn to %s fail, tried %d times!' % (hostip, ssh_try_cnt))
            time.sleep(3)
            continue
        else:
            print('ssh conn to %s success.' % hostip)
            break


def count_reboot_time():
    ip_master = '192.168.100.99'
    ip_slave = '192.168.100.98'

    start_time = time.time()
    print('waiting for os boot, cost 30s...')
    time.sleep(30)
    print('waiting for ssh connection resume...')
    try_ssh_conn(ip_master)
    try_ssh_conn(ip_slave)
    cost_time = time.time() - start_time

    return cost_time


if __name__ == '__main__':
    if list_str_ports:
        cnt_fail = 0

        log_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        log = open(log_time + '.log', 'a')

        for i in range(3):
            power_off(list_str_ports[0])
            time.sleep(5)
            power_on(list_str_ports[0])

            cost_time = count_reboot_time()

            total = i + 1
            if 50 < cost_time:
                master = HostVisitor(hostip='192.168.100.99')
                slave = HostVisitor(hostip='192.168.100.98')
                stdout_ma = master.exec_cmd('dmesg')
                stdout_sl = slave.exec_cmd('dmesg')

                cnt_fail += 1
                log_sep = '====== os boot cost %ds, total %d, fail %d ======\n' \
                          % (cost_time, total, cnt_fail)

                print(log_sep)
                log.write(log_sep)
                log.write('\n')
                log.write('====== dmesg master start ======\n')
                log.write(stdout_ma)
                log.write('====== dmesg master end ======\n')
                log.write('\n')
                log.write('====== dmesg slave start ======\n')
                log.write(stdout_sl)
                log.write('====== dmesg slave end ======\n')
                log.write('\n')
                print()
            else:
                log_sep = '====== os boot cost %ds, total %d, fail %d ======\n' \
                          % (cost_time, total, cnt_fail)
                print(log_sep)
                log.write(log_sep)
                log.write('\n')
                print()

            time.sleep(5)
    else:
        print('com port not exist!')
        sys.exit(1)
