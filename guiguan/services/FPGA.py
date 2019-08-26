#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from common.manip_case_table import parse_cell_value
from common.check_result import *
from common.operate_os import *


g_case_input = None
g_case_expt = None


def open_bashrc():
    write_file_data("s", "export DISPLAY=192.168.100.99:0.0", "#export DISPLAY=192.168.100.99:0.0", "/home/worker/.bashrc")
    reboot_os()


def pexcept_rsult():
    proc = pexpect.spawn('ssh -X worker@' + SLAVE_IP)
    proc.expect("worker@" + SLAVE_IP + "'s password:", timeout=3)
    proc.sendline('uisee')
    proc.expect('worker@slave')
    return proc



def fun_run():
    cmd = UPDATA_FPGA.rstrip("util/ ; ./uisee-test /dev/video0 30 0 2 ") + str("; ./")+ str("run_test.sh")

    proc = pexcept_rsult()
    g_logger.info(cmd)

    print('\n' + cmd + '\n')
    proc.sendline(cmd)
    time.sleep(10)
    ps_ef_grep("s", "ps -ef|grep -v grep |grep video")
    g_ssh_slave.exec_cmd(KILLALL + " uisee-test")


def get_video_info(num):
    cmd = UPDATA_FPGA.replace("./", "timeout 5 ./").strip("0 30 0 2 ")+num
    g_logger.info(cmd)
    proc = pexcept_rsult()

    print('\n' + cmd + '\n')
    proc.sendline(cmd)
    proc.expect("dev_name /dev/video{} already close fd 0xffffffff".format(num))
    res = bytes.decode(proc.before)
    res_num = [len(i) for i in res.split("\n")[-30:-3]]
    g_logger.info(res)
    g_logger.info(res_num)
    return res_num, res


def get_video_type(command):

    stdout = g_ssh_slave.exec_cmd(command)
    if not stdout:
        stdout = g_ssh_master.exec_cmd(command)
    list_key_val = []

    list_line = stdout.split('\n')
    list_line.remove('')

    for line in list_line:
        list_key_val.append((line.strip()))

    return str(list_key_val[:])


def updata_fpga_ver(verno):
    verpath = FPGA_VER_DIR + '/' + 'fpga-bitstream-cq-v' + verno + '.bin'
    cmd = UPDATA_FPGA + verpath

    proc = pexcept_rsult()
    print('\n' + cmd + '\n')
    proc.sendline(cmd)
    # print(bytes.decode(proc.before))

    proc.expect('Please press any key for next step!')
    # print(bytes.decode(proc.before))

    proc.sendline('')
    proc.expect('Please press any key for next step!')
    # print(bytes.decode(proc.before))

    proc.sendline('')
    proc.expect('Please press any key for next step!')
    # print(bytes.decode(proc.before))

    proc.sendline('')
    proc.expect('Please press any key for view the picture!', timeout=60)

    proc.sendline('')
    res = bytes.decode(proc.before)
    time.sleep(1)
    proc.expect(['TIMEOUT', 'interval time is'])

    res1 = bytes.decode(proc.before)

    proc.sendcontrol('c')
    proc.expect('worker@slave')
    # print(bytes.decode(proc.before))
    proc.sendline('exit')
    g_logger.info(res)
    g_logger.info(res1)
    return res+"\n"+res1

# case


def updata_fpga_0():

    filename = g_case_input["fpga"]

    fpga_res = updata_fpga_ver(filename)

    chk_expt_words_exist(g_case_expt, fpga_res)

    # Power_outages()
    #
    # dict_ver = get_list_ver()
    # return chk_dict_rst_with_key('FPGA Version', g_case_expt, dict_ver)


def upgrade_fpga_1():
    filename = g_case_input["fpga"]

    fpga_res = burn_fpga_ver(filename)

    chk_expt_words_exist(g_case_expt, fpga_res)

    # Power_outages()
    #
    # dict_ver = get_list_ver()
    # return chk_dict_rst_with_key('FPGA Version', g_case_expt, dict_ver)


def upgrade_fpga_2():
    filename = g_case_input["fpga"]

    fpga_res = burn_fpga_ver(filename)

    chk_expt_words_exist(g_case_expt, fpga_res)

    # Power_outages()
    #
    # dict_ver = get_list_ver()
    # return chk_dict_rst_with_key('FPGA Version', g_case_expt, dict_ver)


def updata_fpga_3():
    filename = g_case_input["fpga"]

    fpga_res = updata_fpga_ver(filename)

    chk_expt_words_exist(g_case_expt, fpga_res)

    # Power_outages()
    #
    # dict_ver = get_list_ver()
    # return chk_dict_rst_with_key('FPGA Version', g_case_expt, dict_ver)


def upgrade_fpga_4():
    filename = g_case_input["fpga"]

    fpga_res = burn_fpga_ver(filename)

    chk_expt_words_exist(g_case_expt, fpga_res)

    # Power_outages()
    #
    # dict_ver = get_list_ver()
    # return chk_dict_rst_with_key('FPGA Version', g_case_expt, dict_ver)


def upgrade_fpga_5():
    filename = g_case_input["fpga"]

    fpga_res = burn_fpga_ver(filename)

    chk_expt_words_exist(g_case_expt, fpga_res)

    # Power_outages()
    #
    # dict_ver = get_list_ver()
    # return chk_dict_rst_with_key('FPGA Version', g_case_expt, dict_ver)


def upgrade_fpga_6():
    filename = g_case_input["fpga"]

    fpga_res = burn_fpga_ver(filename)

    chk_expt_words_exist(g_case_expt, fpga_res)

    # Power_outages()
    #
    # dict_ver = get_list_ver()
    # return chk_dict_rst_with_key('FPGA Version', g_case_expt, dict_ver)


def updata_fpga_7():
    filename = g_case_input["fpga"]

    fpga_res = updata_fpga_ver(filename)

    chk_expt_words_exist(g_case_expt, fpga_res)

    # Power_outages()
    #
    # dict_ver = get_list_ver()
    # return chk_dict_rst_with_key('FPGA Version', g_case_expt, dict_ver)


def video_type_state():

    video_state = get_video_type(UPDATA_FPGA.strip("0 30 0 2 ").replace(";", "; timeout 5")+str(g_case_input["video"]))

    chk_expt_words_exist(g_case_expt, video_state)


def check_video_status_no():
    dict_data = {}
    version = get_list_ver()
    video = get_video_status()

    dict_data.update(video)
    dict_data.update(version)

    chk_dict_rst(g_case_expt, dict_data)

    # dict_rst = get_video_status()

    # check
    # chk_dict_rst(g_case_expt, dict_rst)


def check_fun_state0():

    len_video, video_info = get_video_info(str(g_case_input["video"]))

    chk_keyword_exists(g_case_expt["result"], video_info)
    chk_len_str(g_case_expt["str_len"], len_video)


def check_fun_state1():

    len_video, video_info = get_video_info(str(g_case_input["video"]))

    chk_keyword_exists(g_case_expt["result"], video_info)
    chk_len_str(g_case_expt["str_len"], len_video)


def check_fun_state2():

    len_video, video_info = get_video_info(str(g_case_input["video"]))

    chk_keyword_exists(g_case_expt["result"], video_info)
    chk_len_str(g_case_expt["str_len"], len_video)


def check_fun_state3():

    len_video, video_info = get_video_info(str(g_case_input["video"]))

    chk_keyword_exists(g_case_expt["result"], video_info)
    chk_len_str(g_case_expt["str_len"], len_video)


def check_fun_state4():

    len_video, video_info = get_video_info(str(g_case_input["video"]))

    chk_keyword_exists(g_case_expt["result"], video_info)
    chk_len_str(g_case_expt["str_len"], len_video)


def check_fun_state5():

    len_video, video_info = get_video_info(str(g_case_input["video"]))

    chk_keyword_exists(g_case_expt["result"], video_info)
    chk_len_str(g_case_expt["str_len"], len_video)


def check_fun_run_state():
    fun_run()


def uos_cv_framework():

    g_ssh_slave.exec_cmd(CV_MAIN)

    time.sleep(5)
    ps_ef_grep("s", g_case_expt["result"])


def uos_camera():
    g_ssh_slave.exec_cmd(CAMERA_MAIN)

    time.sleep(5)
    ps_ef_grep("s", g_case_expt["result"])


def check_video_status_yes():
    dict_data = {}
    video = get_video_status()
    version = get_list_ver()

    dict_data.update(video)
    dict_data.update(version)

    chk_dict_rst(g_case_expt, dict_data)


def shutdown_bashrc():
    write_file_data("s", "#export DISPLAY=192.168.100.99:0.0", "export DISPLAY=192.168.100.99:0.0", "/home/worker/.bashrc")
    reboot_os()


dict_func = {
    # "open_bashrc": open_bashrc(),
    "updata_fpga_0": updata_fpga_0,
    "upgrade_fpga_1": upgrade_fpga_1,
    "upgrade_fpga_2": upgrade_fpga_2,
    "updata_fpga_3": updata_fpga_3,
    "upgrade_fpga_4": upgrade_fpga_4,
    "upgrade_fpga_5": upgrade_fpga_5,
    "upgrade_fpga_6": upgrade_fpga_6,
    "updata_fpga_7": updata_fpga_7,
    "video_type_state": video_type_state,
    "check_video_status_no": check_video_status_no,
    "check_fun_state0": check_fun_state0,
    "check_fun_state1": check_fun_state1,
    "check_fun_state2": check_fun_state2,
    "check_fun_state3": check_fun_state3,
    "check_fun_state4": check_fun_state4,
    "check_fun_state5": check_fun_state5,
    "check_funrun_state": check_fun_run_state,
    "uos_cv_framework-main": uos_cv_framework,
    "uos_camera-main": uos_camera,
    "check_video_status_yes": check_video_status_yes,
    # "shutdown_bashrc": shutdown_bashrc()
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
    fun_run()