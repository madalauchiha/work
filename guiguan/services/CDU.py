#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from common.manip_case_table import parse_cell_value
from common.check_result import *
from common.comm_paras import g_logger

g_case_input = None
g_case_expt = None


def check_video_stat():
    stats = get_video_status_gg30()

    chk_dict_rst(g_case_expt, stats)


def dump_video0_num_4():
    chk_dump_video0('master', 4)
    chk_dump_video0('slave', 4)


def dump_video1_num_4():
    chk_dump_video1('master', 4)
    chk_dump_video1('slave', 4)


dict_func = {
    'check video status': check_video_stat,
    'dump video0 num 4': dump_video0_num_4,
    'dump video1 num 4': dump_video1_num_4,
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
    def video_dump_loop():
        while True:
            try:
                dump_video0_num_4()

                time.sleep(1)

                dump_video1_num_4()
            except Exception:
                import sys
                sys.exit(1)

    video_dump_loop()
