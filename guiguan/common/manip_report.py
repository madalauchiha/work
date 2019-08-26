#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from py._xmlgen import html


def gen_table_style():
    dict_tbl = {
        'font-family': 'verdana,arial,sans-serif',
        'font-size': '11px',
        'color': '#333333',
        'border-width': '1px',
        'border-color': '#D8D8D8',
        'border-collapse': 'collapse'
    }

    dict_th = {
        'border-width': '1px',
        'padding': '8px',
        'border-style': 'solid',
        'border-color': '#D8D8D8',
        'background-color': '#EEEEEE',
    }

    dict_td = {
        'border-width': '1px',
        'padding': '8px',
        'border-style': 'solid',
        'border-color': '#D8D8D8',
        'background-color': '#FFFFFF',
    }

    list_tbl = [key + ': ' + value + ';' for key, value in dict_tbl.items()]
    str_tbl = 'table.gridtable {\n    ' + '\n    '.join(list_tbl) + '\n}'
    # print(str_tbl)

    list_th = [key + ': ' + value + ';' for key, value in dict_th.items()]
    str_th = 'table.gridtable th {\n    ' + '\n    '.join(list_th) + '\n}'
    # print(str_th)

    list_td = [key + ': ' + value + ';' for key, value in dict_td.items()]
    str_td = 'table.gridtable td {\n    ' + '\n    '.join(list_td) + '\n}'
    # print(str_td)

    str_style = '\n' + str_tbl + '\n' + str_th + '\n' + str_td + '\n'
    # print(str_style)

    return str_style


def gen_table_tag(statis):
    str_style = gen_table_style()

    tat_style = html.style(str_style, type='text/css')
    # print(tat_style)

    list_tag_row = list()
    list_head = ['Module', 'Total Tests', 'Passed', 'Failed', 'Pass Rate']
    list_tag_row.append(html.tr([html.th(item) for item in list_head]))

    for key, value in statis.items():
        list_stat = list()
        list_stat.append(key)
        list_stat.extend([v for v in value.values()])
        list_tag_col = list()
        for idx, item in enumerate(list_stat):
            if idx in [1, 2, 3]:
                list_tag_col.append(html.td(html.a(item, href="#results-table")))
            else:
                list_tag_col.append(html.td(item))

        list_tag_row.append(list_tag_col)
        # list_tag_row.append(html.tr([html.td(item) for item in list_stat]))

    tag_table = html.table([html.tr(item) for item in list_tag_row], class_='gridtable')

    return [tat_style, tag_table]
