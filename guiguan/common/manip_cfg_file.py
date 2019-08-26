#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from configparser import ConfigParser
from collections import OrderedDict
import json


def get_host_cfg(cfgpath, host):
    conf = ConfigParser()
    conf.read(cfgpath, encoding="utf-8")

    tuple_host = conf.items(host)
    dict_host = OrderedDict(tuple_host)
    # print(tuple_host)
    # print(dict_host)

    return dict_host


def get_log_serv_cfg(cfgpath):
    conf = ConfigParser()
    conf.read(cfgpath, encoding="utf-8")

    tuple_host = conf.items('log ftp server')
    dict_host = OrderedDict(tuple_host)
    # print(tuple_host)
    # print(dict_host)

    return dict_host


def get_mod_cfg(modpath):
    mod = []
    with open(modpath) as f:
        for line in f:
            if not line.startswith("#"):
                mod.append(line.strip().lstrip('test_'))

    return mod


def get_mail_cfg(cfgpath):
    conf = ConfigParser()
    conf.read(cfgpath, encoding="utf-8")

    tuple_mail = conf.items('mail')
    dict_mail = OrderedDict(tuple_mail)
    # print(tuple_mail)
    # print(dict_mail)

    return dict_mail


def read_jason(fpath):
    with open(fpath, 'r') as f:
        dict_read = json.load(f, object_pairs_hook=OrderedDict)

    return dict_read


def write_jason(dict_write, fpath):
    with open(fpath, 'w') as f:
        json.dump(dict_write, f, indent=2)


def get_hardware_cfg(cfgpath):
    conf = ConfigParser()
    conf.read(cfgpath, encoding="utf-8")

    tuple_host = conf.items('hardware')
    dict_host = OrderedDict(tuple_host)
    # print(tuple_host)
    # print(dict_host)

    return dict_host
