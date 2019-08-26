#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import sys
sys.path.extend(['/home/dingding/project/guiguan/venv/lib/python3.5/site-packages'])

import serial.tools.list_ports
import modbus_tk.modbus_rtu
import modbus_tk.defines
import time

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


if __name__ == '__main__':
    if list_str_ports:
        power_off(list_str_ports[0])
        time.sleep(5)
        power_on(list_str_ports[0])
    else:
        print('com port not exist!')
        sys.exit(1)
