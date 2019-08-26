#!usr/bin/env python3
# -*- coding: utf-8 -*-

import re


def get_val_by_re(str_pat, text):
    obj_pat = re.compile(str_pat)
    rsts = obj_pat.findall(text)

    rst = ''
    if rsts:
        rst = rsts[0]

    return rst


def get_list_by_re_groups(str_pat, text):
    obj_pat = re.compile(str_pat)
    rsts = obj_pat.search(text).groups()

    return rsts


def get_list_by_re_findall(str_pat, text):
    obj_pat = re.compile(str_pat)
    rsts = obj_pat.findall(text)

    return rsts


if __name__ == '__main__':
    text = '<<<<<<<<<<<<<<<<<<<<<<<<<< 25.00 fps\
     <<<<<<<<<<<<<<<<<<<<<<<<< 25.00 fps <<<<<<<<<<<<<<<<<<<<<<<<< 25.00 fps <<<<<<<<<<<<<<<<<<<<<<<<'

    pat = r'(\S*?) fps'
    print(get_list_by_re_findall(pat, text))
