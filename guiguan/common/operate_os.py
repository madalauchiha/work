#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from common.parse_str import *
from common.comm_paras import *
from common.command import *
import pexpect
import time
import telnetlib
from datetime import datetime
from shutil import copyfile


def ls_ma_dir(dir):
    return g_ssh_master.ls_dir(dir)


def ls_sl_dir(dir):
    return g_ssh_slave.ls_dir(dir)


def rm_ma_dir(dir):
    try:
        g_ssh_master.rm_dir(dir)
    except FileNotFoundError:
        pass


def rm_sl_dir(dir):
    try:
        g_ssh_slave.rm_dir(dir)
    except FileNotFoundError:
        pass


def cp_pth_to_ma(src, dst):
    if not os.path.exists(src):
        assert False, '[%s] not exist!' % src

    if not g_ssh_master.upload(src, dst):
        assert False, 'version copy fail!'


def cp_pth_to_sl(src, dst):
    if not os.path.exists(src):
        assert False, '[%s] not exist!' % src

    if not g_ssh_slave.upload(src, dst):
        assert False, 'version copy fail!'


def burn_fpga_ver(verno):
    verpath = FPGA_VER_DIR + '/' + 'fpga-bitstream-cq-v' + verno + '.bin'
    cmd = BURN_FPGA + verpath

    proc = pexpect.spawn('ssh -X worker@' + SLAVE_IP)
    proc.expect("worker@" + SLAVE_IP + "'s password:", timeout=3)
    proc.sendline('uisee')
    proc.expect('worker@slave')

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

    # proc.expect(['TIMEOUT', 'picture!'])
    time.sleep(3)
    proc.expect(['TIMEOUT', 'interval time is'])
    res1 = bytes.decode(proc.before)

    proc.sendcontrol('c')
    proc.expect('worker@slave')

    proc.sendline('exit')

    return res+"\n"+res1


def apply_os_ver(ver_name):
    cmd = CD + TEST_DIR + '; ' + APPLY_OS + ver_name
    g_ssh_master.exec_cmd(cmd)

    reboot_os()


def set_prod_type(prod_type):
    g_ssh_master.exec_cmd(SET_PROD_TYPE + prod_type)

    reboot_os()


def get_list_ver():
    dict_ver = {}

    stdout = g_ssh_master.exec_cmd(LIST_VER)

    if isinstance(stdout, str):
        dict_ver['System Version'] = get_val_by_re(r'System Version:(.*)', stdout).strip().strip('","')
        dict_ver['Board Type'] = get_val_by_re(r'Board Type:(.*)', stdout).strip().strip('"",')
        dict_ver['FPGA Version'] = get_val_by_re(r'FPGA Version:(.*)', stdout).strip().strip('"".')
        dict_ver['FPGA Driver Version'] = get_val_by_re(r'FPGA Driver Version:(.*)', stdout).strip().strip('"",')
    else:
        dict_ver['System Version'] = bytes.decode(get_val_by_re(b'System Version:(.*)', stdout)).strip().strip('","')
        dict_ver['Board Type'] = bytes.decode(get_val_by_re(b'Board Type:(.*)', stdout)).strip().strip('"",')
        dict_ver['FPGA Version'] = bytes.decode(get_val_by_re(b'FPGA Version:(.*)', stdout)).strip().strip('"".')
        dict_ver['FPGA Driver Version'] = bytes.decode(get_val_by_re(b'FPGA Driver Version:(.*)', stdout)).strip().strip('"",')

    return dict_ver


def get_video_status():
    dict_status = {}

    stdout = g_ssh_master.exec_cmd(LIST_VER)

    if isinstance(stdout, str):
        dict_status['video0'] = get_val_by_re(r'video0\s*\|\s*(\S*)', stdout)
        dict_status['video1'] = get_val_by_re(r'video1\s*\|\s*(\S*)', stdout)
        dict_status['video2'] = get_val_by_re(r'video2\s*\|\s*(\S*)', stdout)
        dict_status['video3'] = get_val_by_re(r'video3\s*\|\s*(\S*)', stdout)
        dict_status['video4'] = get_val_by_re(r'video4\s*\|\s*(\S*)', stdout)
        dict_status['video5'] = get_val_by_re(r'video5\s*\|\s*(\S*)', stdout)
    else:
        dict_status['video0'] = bytes.decode(get_val_by_re(b'video0\\s*\\|\\s*(\\S*)', stdout))
        dict_status['video1'] = bytes.decode(get_val_by_re(b'video1\\s*\\|\\s*(\\S*)', stdout))
        dict_status['video2'] = bytes.decode(get_val_by_re(b'video2\\s*\\|\\s*(\\S*)', stdout))
        dict_status['video3'] = bytes.decode(get_val_by_re(b'video3\\s*\\|\\s*(\\S*)', stdout))
        dict_status['video4'] = bytes.decode(get_val_by_re(b'video4\\s*\\|\\s*(\\S*)', stdout))
        dict_status['video5'] = bytes.decode(get_val_by_re(b'video5\\s*\\|\\s*(\\S*)', stdout))

    return dict_status


def get_video_status_gg30():
    dict_status = {}

    stdout = g_ssh_master.exec_cmd(LIST_VER)

    half_idx = stdout.find('video1')
    str_video0 = stdout[:half_idx]
    str_video1 = stdout[half_idx:]

    if isinstance(stdout, str):
        dict_status['video0_port0'] = get_val_by_re(r'Port0\s*\|\s*(\S*)', str_video0)
        dict_status['video0_port1'] = get_val_by_re(r'Port1\s*\|\s*(\S*)', str_video0)
        dict_status['video0_port2'] = get_val_by_re(r'Port2\s*\|\s*(\S*)', str_video0)
        dict_status['video0_port3'] = get_val_by_re(r'Port3\s*\|\s*(\S*)', str_video0)

        dict_status['video1_port0'] = get_val_by_re(r'Port0\s*\|\s*(\S*)', str_video1)
        dict_status['video1_port1'] = get_val_by_re(r'Port1\s*\|\s*(\S*)', str_video1)
        dict_status['video1_port2'] = get_val_by_re(r'Port2\s*\|\s*(\S*)', str_video1)
        dict_status['video1_port3'] = get_val_by_re(r'Port3\s*\|\s*(\S*)', str_video1)
    else:
        dict_status['video0_port0'] = bytes.decode(get_val_by_re(b'Port0\\s*\\|\\s*(\\S*)', str_video0))
        dict_status['video0_port1'] = bytes.decode(get_val_by_re(b'Port1\\s*\\|\\s*(\\S*)', str_video0))
        dict_status['video0_port2'] = bytes.decode(get_val_by_re(b'Port2\\s*\\|\\s*(\\S*)', str_video0))
        dict_status['video0_port3'] = bytes.decode(get_val_by_re(b'Port3\\s*\\|\\s*(\\S*)', str_video0))

        dict_status['video1_port0'] = bytes.decode(get_val_by_re(b'Port0\\s*\\|\\s*(\\S*)', str_video1))
        dict_status['video1_port1'] = bytes.decode(get_val_by_re(b'Port1\\s*\\|\\s*(\\S*)', str_video1))
        dict_status['video1_port2'] = bytes.decode(get_val_by_re(b'Port2\\s*\\|\\s*(\\S*)', str_video1))
        dict_status['video1_port3'] = bytes.decode(get_val_by_re(b'Port3\\s*\\|\\s*(\\S*)', str_video1))

    return dict_status


def get_ma_ip():
    dict_ip = {}

    stdout = g_ssh_master.exec_cmd(IFCONFIG)

    dict_ip['IP'] = get_val_by_re(r'inet addr:(\S*)  Bcast', stdout)

    return dict_ip


def get_sl_ip():
    dict_ip = {}

    stdout = g_ssh_slave.exec_cmd(IFCONFIG)

    dict_ip['IP'] = get_val_by_re(r'inet addr:(\S*)  Bcast', stdout)

    return dict_ip


def get_ma_disk_info():
    stdout = g_ssh_master.exec_cmd(DF)

    if '/dev/mmcblk' not in stdout:
        raise Exception('/dev/mmcblk not found!')

    str_pat = r'(/dev/mmcblk\S*)' + r'\s*(\S*)' * 5
    values_disk = get_list_by_re_groups(str_pat, stdout)
    keys_disk = ['Filesystem', 'Size', 'Used', 'Avail', 'Use%', 'Mounted on']
    dict_disk = dict(zip(keys_disk, values_disk))

    return dict_disk


def get_sl_disk_info():
    stdout = g_ssh_slave.exec_cmd(DF)

    if '/dev/mmcblk' not in stdout:
        raise Exception('/dev/mmcblk not found!')

    str_pat = r'(/dev/mmcblk\S*)' + r'\s*(\S*)' * 5
    values_disk = get_list_by_re_groups(str_pat, stdout)
    keys_disk = ['Filesystem', 'Size', 'Used', 'Avail', 'Use%', 'Mounted on']
    dict_disk = dict(zip(keys_disk, values_disk))

    return dict_disk


def get_ma_uisee_rel():
    dict_rel = {}

    stdout = g_ssh_master.exec_cmd(CAT_REL)
    # dict_rel['Name'] = get_val_by_re(r'"Name":\s*(.*),', stdout).strip('"')
    # dict_rel['Date'] = get_val_by_re(r'"Date":\s*(.*),', stdout).strip('"')
    # dict_rel['Release'] = get_val_by_re(r'"Release":\s*(.*),', stdout).strip('"')
    dict_rel['version'] = get_val_by_re(r'"version":\s*(.*)', stdout).strip('"').strip('",')
    dict_rel['apu'] = get_val_by_re(r'"apu":\s*(.*)', stdout).strip('"').strip('",')
    dict_rel['bootloader'] = get_val_by_re(r'"bootloader":\s*(.*)', stdout).strip('"').strip('",')
    dict_rel['fpga'] = get_val_by_re(r'"fpga":\s*(.*)', stdout).strip('"').strip('",')
    dict_rel['fpga_drv'] = get_val_by_re(r'"fpga_drv":\s*(.*)', stdout).strip('"')
    dict_rel['ProductType'] = get_val_by_re(r'"ProductType":\s*(.*)', stdout).strip('"')

    return dict_rel


def get_sl_uisee_rel():
    dict_rel = {}

    stdout = g_ssh_slave.exec_cmd(CAT_REL)
    # dict_rel['Name'] = get_val_by_re(r'"Name":\s*(.*),', stdout).strip('"')
    # dict_rel['Date'] = get_val_by_re(r'"Date":\s*(.*),', stdout).strip('"')
    # dict_rel['Release'] = get_val_by_re(r'"Release":\s*(.*),', stdout).strip('"')
    dict_rel['version'] = get_val_by_re(r'"version":\s*(.*)', stdout).strip('"').strip('",')
    dict_rel['apu'] = get_val_by_re(r'"apu":\s*(.*)', stdout).strip('"').strip('",')
    dict_rel['bootloader'] = get_val_by_re(r'"bootloader":\s*(.*)', stdout).strip('"').strip('",')
    dict_rel['fpga'] = get_val_by_re(r'"fpga":\s*(.*)', stdout).strip('"').strip('",')
    dict_rel['fpga_drv'] = get_val_by_re(r'"fpga_drv":\s*(.*)', stdout).strip('"')
    dict_rel['ProductType'] = get_val_by_re(r'"ProductType":\s*(.*)', stdout).strip('"')

    return dict_rel


def get_ma_lsmod():
    stdout = g_ssh_master.exec_cmd(LSMOD)

    return stdout


def get_sl_lsmod():
    stdout = g_ssh_slave.exec_cmd(LSMOD)

    return stdout


def get_ma_modinfo(fpath):
    stdout = g_ssh_master.exec_cmd(MODINFO + fpath)
    list_key_val = []

    list_line = stdout.split('\n')
    list_line.remove('')

    for line in list_line:
        tmp = line.split(':')
        list_key_val.append((tmp[0], tmp[1].strip()))

    return dict(list_key_val)


def get_sl_modinfo(fpath):
    stdout = g_ssh_slave.exec_cmd(MODINFO + fpath)
    list_key_val = []

    list_line = stdout.split('\n')
    list_line.remove('')

    for line in list_line:
        tmp = line.split(':')
        list_key_val.append((tmp[0], tmp[1].strip()))

    return dict(list_key_val)


def get_ma_video_dev():
    cmd = CD + DEV_DIR + '; ' + LS + 'video*'
    stdout = g_ssh_master.exec_cmd(cmd)

    return stdout


def get_sl_video_dev():
    cmd = CD + DEV_DIR + '; ' + LS + 'video*'
    stdout = g_ssh_slave.exec_cmd(cmd)

    return stdout


def ma_ping(des, pkt_num=1):
    cmd = 'ping -c {} -w {} {}'.format(str(pkt_num), str(pkt_num), des)
    stdout = g_ssh_master.exec_cmd(cmd)

    if str(pkt_num) != get_val_by_re(r'(\d) received', stdout):
        assert False, 'master ping [{}] fail'.format(des)

    return True


def sl_ping(des, pkt_num=1):
    cmd = 'ping -c {} -w {} {}'.format(str(pkt_num), str(pkt_num), des)
    stdout = g_ssh_slave.exec_cmd(cmd)

    if str(pkt_num) != get_val_by_re(r'(\d) received', stdout):
        assert False, 'slave ping [{}] fail'.format(des)

    return True


def check_ssh_pexpt(host_ip):
    ssh_cmd = 'ssh worker@' + host_ip
    proc = pexpect.spawn(ssh_cmd)

    idx = proc.expect(['password', 'No route', pexpect.TIMEOUT, pexpect.EOF], timeout=2)

    if 0 == idx:
        proc.sendcontrol('c')
        return proc, True
    else:
        proc.sendcontrol('c')
        return proc, False


def try_ssh_conn(hostip):
    ssh_try_cnt = 0
    while True:
        proc, rst = check_ssh_pexpt(hostip)
        if proc.isalive():
            proc.kill(0)

        if not rst:
            ssh_try_cnt += 1
            logger.error('ssh conn to %s fail, tried %d times!' % (hostip, ssh_try_cnt))

            if 100 == ssh_try_cnt:
                logger.error('ssh conn to %s fail, tried 5 minutes, still can not resume!' % hostip)
                os._exit(1)

            time.sleep(3)
            continue
        else:
            print('ssh conn to %s success.' % hostip)
            break

    return ssh_try_cnt


def reboot_os():
    g_ssh_master.exec_cmd(REBOOT)

    print('waiting for os reboot, cost 30s...')
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
            os._exit(1)

    fail_cnt = 0
    while True:
        if g_ssh_master.reconnect():
            print('master ssh connection resume success.')
            break

        print('master ssh connection resume fail, try again!')
        fail_cnt += 1
        if 10 == fail_cnt:
            logger.error('try [{}] times, master ssh conn resume fail!'.format(fail_cnt))
            os._exit(1)

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
            os._exit(1)

        time.sleep(10)

        ssh_ma_cnt += try_ssh_conn(MASTER_IP)
        ssh_sl_cnt += try_ssh_conn(SLAVE_IP)

    print('reboot completed.')

    time.sleep(1)

    dmesg_master = g_ssh_master.exec_cmd('dmesg')
    dmesg_slave = g_ssh_slave.exec_cmd('dmesg')

    if 40 < time_cost:
        assert False, 'ssh resume cost > %.2fs, expect < 40s!' % time_cost

    return dmesg_master, dmesg_slave


def power_outages(board):

    CRLF = b'\r'
    stateon = "State        : ON"
    stateoff = "State        : OFF"
    host = "192.168.100.248"
    username = "apc"
    password = "apc"

    tn = telnetlib.Telnet(host)
    # tn.set_debuglevel(2)

    # login
    tn.read_until(b"User Name : ")
    tn.write(username.encode("ascii") + CRLF)
    if password:
        tn.read_until(b"Password  : ")
        tn.write(password.encode("ascii") + CRLF)

    tn.read_until(b"\r\n> ")
    # ------- Control Console -------
    # 1- Device Manager
    # 2- Network
    # 3- System
    # 4- Logout

    tn.write(b"1" + CRLF)
    tn.read_until(b"\r\n> ")
    # ------- Device Manager ----------
    # 1- Phase Management
    # 2- Outlet Management
    # 3- Power Supply Status

    tn.write(b"2" + CRLF)
    tn.read_until(b"\r\n> ")
    # ------- Outlet Management ----------
    #  1- Outlet Control/Configuration
    #  2- Outlet Restriction

    tn.write(b"1" + CRLF)
    tn.read_until(b"\r\n> ")
    # ------- Outlet Control/Configuration -----
    #  1- Outlet 1                 OFF
    #  2- Zedboard-1               ON
    #  3- Outlet 3                 OFF
    #  4- Zedboard-2               OFF
    #  5- Outlet 5                 OFF
    #  6- Outlet 6                 OFF
    #  7- Outlet 7                 OFF
    #  8- Outlet 8                 OFF
    #  9- Master Control/Configuration

    if board == 1:
        tn.write(b"1" + CRLF)
    elif board == 2:
        tn.write(b"2" + CRLF)
    elif board == 3:
        tn.write(b"3" + CRLF)
    elif board == 4:
        tn.write(b"4" + CRLF)
    elif board == 5:
        tn.write(b"5" + CRLF)
    elif board == 6:
        tn.write(b"6" + CRLF)
    elif board == 7:
        tn.write(b"7" + CRLF)
    elif board == 8:
        tn.write(b"8" + CRLF)
    else:
        print("the board does not exist !! ")
        tn.close()
        return 100

    tn.read_until(b"\r\n> ")
    # ------- Zedboard-1 -----------
    #    Name         : Zedboard-1
    #    Outlet       : 2
    #    State        : ON
    #    1- Control Outlet
    #    2- Configure Outlet

    tn.write(b"1" + CRLF)
    controloutlet = tn.read_until(b"\r\n> ")
    # ------- Control Outlet --------
    #     Name         : Zedboard-1
    #     Outlet       : 2
    #     State        : ON
    #  1- Immediate On
    #  2- Immediate Off
    #  3- Immediate Reboot
    #  4- Delayed On
    #  5- Delayed Off
    #  6- Delayed Reboot
    #  7- Cancel

    poweron = controloutlet.find(stateon)
    poweroff = controloutlet.find(stateoff)
    if (poweron > 20) and (poweroff == -1):
        tn.write(b"3" + CRLF)
        print("shutdown and delay for 5 seconds, reboot")
    else:
        tn.write(b"1" + CRLF)
        print("immediately turn on")

    tn.read_until(b"to cancel : ")
    # ----------------------------------
    #    Immediate Reboot
    #    This command will immediately shutdown
    #    outlet 2 named 'Zedboard-1', delay for 5 seconds,
    #    and then restart.
    #    Enter 'YES' to continue or <ENTER> to cancel : yes

    tn.write(b"YES" + CRLF)
    tn.read_until(b"to continue...")
    # Command successfully issued.
    # Press <ENTER> to continue...

    tn.write(CRLF)
    tn.read_until(b"\r\n> ")
    # ------- Control Outlet ------
    # ?- Help, <ESC>- Back, <ENTER>- Refresh, <CTRL-L>- Event Log

    tn.write(b"\x1b" + CRLF)
    tn.read_until(b"\r\n> ")
    # ------- Zedboard-1 -------
    # ?- Help, <ESC>- Back, <ENTER>- Refresh, <CTRL-L>- Event Log

    tn.write(b"\x1b" + CRLF)
    tn.read_until(b"\r\n> ")
    # ------- Outlet Control/Configuration -------
    #     <ESC>- Back, <ENTER>- Refresh, <CTRL-L>- Event Log

    tn.write(b"\x1b" + CRLF)
    tn.read_until(b"\r\n> ")
    # ------- Outlet Management ----------
    # <ESC>- Back, <ENTER>- Refresh, <CTRL-L>- Event Log

    tn.write(b"\x1b" + CRLF)
    tn.read_until(b"\r\n> ")
    # ------- Device Manager ------
    # <ESC>- Back, <ENTER>- Refresh, <CTRL-L>- Event Log

    tn.write(b"\x1b" + CRLF)
    tn.read_until(b"\r\n> ")
    # ------- Control Console -------
    # 1- Device Manager
    # 2- Network
    # 3- System
    # 4- Logout
    # <ESC>- Main Menu, <ENTER>- Refresh, <CTRL-L>- Event Log

    tn.write(b"4" + CRLF)
    # print tn.read_all()
    tn.close()


def stop_uos(uosdir):
    rundir = os.path.join(uosdir, 'run')
    cmd = CD + rundir + ';' + STOP_UOS
    g_ssh_master.exec_cmd(cmd)

    list_proc = ['uos_daemon',
                 'uos_display',
                 'uos_log_daemon',
                 'uos_diag_daemon',
                 'uos_planner',
                 'uos_speedctrl-main',
                 'uos_lateralctrl-main',
                 'uos_ap_planner',
                 'uos_ideal_vehicle']
    uosprocs = g_ssh_master.exec_cmd('ps -ef|grep uos')
    for proc in list_proc:
        if proc in uosprocs:
            assert False, 'process [{}] stop fail!'.format(proc)


def launch_uos_pexpt(uosdir):
    promp = 'worker@master'
    proc = pexpect.spawn('ssh -X worker@' + MASTER_IP)
    proc.expect("worker@" + MASTER_IP + "'s password:", timeout=3)
    proc.sendline('uisee')
    proc.expect(promp)

    rundir = os.path.join(uosdir, 'run')
    cmd = CD + rundir + ';./launch_uos.sh'
    print('\n' + cmd + '\n')
    print('uos is launching, cost 15s...\n')

    proc.sendline(cmd)

    idx = proc.expect(['back to normal', pexpect.TIMEOUT], timeout=15)

    if 0 == idx:
        proc.sendline('exit')
    else:
        proc.kill(0)

    list_proc = ['uos_daemon',
                 'uos_display',
                 'uos_log_daemon',
                 'uos_diag_daemon',
                 'uos_planner',
                 'uos_speedctrl-main',
                 'uos_lateralctrl-main',
                 'uos_ap_planner',
                 'uos_ideal_vehicle']
    uosprocs = g_ssh_master.exec_cmd('ps -ef|grep uos')
    for proc in list_proc:
        if proc not in uosprocs:
            stop_uos(uosdir)
            assert False, 'process [{}] launch fail!'.format(proc)


def launch_uos(uosdir):
    rundir = os.path.join(uosdir, 'run')
    cmd = CD + rundir + ';' + LAUNCH_UOS
    g_ssh_master.exec_cmd(cmd)

    print('uos is launching, cost 15s...')
    time.sleep(15)

    list_proc = ['uos_daemon',
                 # 'uos_display',
                 'uos_log_daemon',
                 'uos_diag_daemon',
                 'uos_planner',
                 'uos_speedctrl-main',
                 'uos_lateralctrl-main',
                 'uos_ap_planner',
                 'uos_ideal_vehicle']
    uosprocs = g_ssh_master.exec_cmd('ps -ef|grep uos')
    for proc in list_proc:
        if proc not in uosprocs:
            stop_uos(uosdir)
            assert False, 'process [{}] launch fail!'.format(proc)


def get_ma_time():
    tm_ma = g_ssh_master.exec_cmd(DATE).strip()

    return tm_ma


def get_uos_logdir():
    tm_ma = get_ma_time()
    tm_ma = datetime.strptime(tm_ma, '%a %b %d %H:%M:%S CST %Y')

    log_date = tm_ma.strftime('%Y-%m-%d')

    return os.path.join(UOS_LOG_DIR, log_date)


def get_ma_fsize(fpath):
    return g_ssh_master.get_stat(fpath).st_size


def get_sl_fsize(fpath):
    return g_ssh_slave.get_stat(fpath).st_size


def enable_ftp():
    cmd = SWITCH_FTP + 'enable'
    g_ssh_master.exec_cmd(cmd)

    reboot_os()


def disable_ftp():
    cmd = SWITCH_FTP + 'disable'
    g_ssh_master.exec_cmd(cmd)

    reboot_os()


def get_sys_cfg_rec():
    return g_ssh_master.exec_cmd(CAT + SYS_CFG_REC_PATH).splitlines()


def open_ma_ftp():
    proc = pexpect.spawn('ftp -p ' + MASTER_IP)
    idx = proc.expect(['Name \(192.168.100.99', pexpect.TIMEOUT], timeout=3)

    if 1 == idx:
        proc.kill(0)
        assert False, 'ftp master connect fail!'

    proc.sendline('turtle')
    proc.expect('Password:')
    proc.sendline('turtle')
    idx = proc.expect(['Login successful', pexpect.TIMEOUT], timeout=3)

    if 0 == idx:
        return proc

    if 1 == idx:
        proc.kill(0)
        assert False, 'ftp master login fail!'


def close_ftp(proc):
    proc.sendline('by')
    idx = proc.expect(['Goodbye', pexpect.EOF, pexpect.TIMEOUT], timeout=3)

    if 2 == idx:
        proc.kill(0)


def ftp_get(fname):
    proc = open_ma_ftp()
    prompt = 'ftp>'

    proc.sendline(CD + os.path.basename(UOS_LOG_DIR))
    proc.expect(prompt)

    proc.sendline(GET + fname)
    idx = proc.expect(['Transfer complete', pexpect.TIMEOUT], timeout=30)

    if 1 == idx:
        proc.kill(0)
        assert False, 'ftp get file [{}] fail!'.format(fname)

    close_ftp(proc)


def touch_ma_file(fpath):
    g_ssh_master.exec_cmd(TOUCH + fpath)


def rm_ma_file(fpath):
    g_ssh_master.rm_file(fpath)


def rm_sl_file(fpath):
    g_ssh_slave.rm_file(fpath)


def get_ma_file_size(fpath):
    return g_ssh_master.get_stat(fpath).st_size


def get_sl_file_size(fpath):
    return g_ssh_slave.get_stat(fpath).st_size


def rm_loc_file(fpath_loc):
    try:
        os.remove(fpath_loc)
    except FileNotFoundError:
        pass


def add_text_to_ma_file(fpath, text):
    g_ssh_master.exec_cmd(ECHO + text + ' > ' + fpath)


def chk_sys_cfg_rec(cmd):
    if cmd != get_sys_cfg_rec()[-1]:
        assert False, "command [{}] isn't the last line of sys_cfg_rec!"

    return True


def switch_net_internal():
    cmd = SWITCH_NET + 'internal'
    g_ssh_master.exec_cmd(cmd)

    reboot_os()

    return chk_sys_cfg_rec(cmd)


def switch_net_external():
    cmd = SWITCH_NET + 'external'
    g_ssh_master.exec_cmd(cmd)

    reboot_os()

    return chk_sys_cfg_rec(cmd)


def switch_net_wifi():
    cmd = SWITCH_NET + 'wifi'
    g_ssh_master.exec_cmd(cmd)

    reboot_os()

    return chk_sys_cfg_rec(cmd)


def get_ma_lsusb():
    return g_ssh_master.exec_cmd(LSUSB)


def get_ma_usb_dev():
    return g_ssh_master.exec_cmd(LS + '/dev/ttyUSB*')


def get_wvdial_info():
    fname = 'wvdial.log'

    try:
        g_ssh_master.get_stat(os.path.join(HOME_DIR, fname))
    except FileNotFoundError:
        assert False, '[{}] does not exist!'.format(fname)

    return g_ssh_master.exec_cmd(CAT + fname)


def get_latest_uos_log():
    list_date = g_ssh_master.ls_dir(UOS_LOG_DIR)

    list_tmp = [item.replace('-', '') for item in list_date]
    idx = list_tmp.index(max(list_tmp))

    return list_date[idx]


def set_wifi(uname, pwd):
    g_ssh_master.exec_cmd(SET_WIFI + uname + ' ' + pwd)


def prepare_local_uos():
    uos_ver = 'UOS-arm64-deploy-2019-04-15-15-31-daily-stable_Beijing_e100.car15.sh'
    uos_src_path = os.path.join(UOS_VER_DIR, uos_ver)
    uos_dst_path = os.path.join(TEST_DIR, uos_ver)
    g_ssh_master.upload(uos_src_path, TEST_DIR)
    g_ssh_master.exec_cmd('chmod u+x ' + uos_dst_path)


def prepare_ota_full(dict_cfg):
    # modify vid.json
    vid_path_tmp_loc = os.path.join(OTA_DATA_DIR, 'vid.json.template')
    vid_path_tmp_host = os.path.join(UOS_CFG_DIR, 'vid.json.template')
    vid_path_loc = os.path.join(OTA_DATA_DIR, 'vid.json')

    try:
        os.remove(vid_path_loc)
    except FileNotFoundError:
        pass

    g_ssh_master.download(vid_path_tmp_host, vid_path_loc)

    try:
        dict_json = read_jason(vid_path_loc)
    except json.decoder.JSONDecodeError:
        copyfile(vid_path_tmp_loc, vid_path_loc)
        dict_json = read_jason(vid_path_loc)
        # assert False, 'vid.json.template not exist in master ~/config!'

    dict_json['MOD_uos']['version'] = dict_cfg['version']
    for key in dict_cfg.keys():
        if 'version' != key:
            dict_json[key] = dict_cfg[key]

    write_jason(dict_json, vid_path_loc)

    g_ssh_master.upload(vid_path_loc, UOS_CFG_DIR)

    os.remove(vid_path_loc)

    # copy common json and map
    cfg_path_loc = os.path.join(OTA_DATA_DIR, 'uos_common.json')
    data_path_loc = os.path.join(OTA_DATA_DIR, 'data.tar.gz')
    g_ssh_master.upload(cfg_path_loc, UOS_CFG_DIR)
    upload_ma_tar_file(data_path_loc, OTA_UOS_DIR, 'data', delflag=False)


def copy_map():
    cfg_path_loc = os.path.join(OTA_DATA_DIR, 'uos_common.json')
    data_path_loc = os.path.join(OTA_DATA_DIR, 'data.tar.gz')
    g_ssh_master.upload(cfg_path_loc, UOS_CFG_DIR)
    upload_ma_tar_file(data_path_loc, OTA_UOS_DIR, 'data', delflag=False)


def do_ota_full(dict_cfg):
    prepare_ota_full(dict_cfg)

    g_ssh_master.exec_cmd(OTA + '-f')
    # g_ssh_master.exec_cmd(OTA + '-f > /dev/null')


def do_ota_delta():
    g_ssh_master.exec_cmd(OTA)
    # g_ssh_master.exec_cmd(OTA + '> /dev/null')


def get_apu_info():
    stdout = g_ssh_master.exec_cmd(APU_INFO)

    dict_rst = dict()
    list_re = get_list_by_re_findall(r'is:\s*(\S*)', stdout)
    if list_re:
        dict_rst['apu compile time'] = list_re[0]
        dict_rst['hardware version'] = list_re[1]
        dict_rst['software version'] = list_re[2]

    str_re = get_val_by_re(r'is\s+(\w*)', stdout)
    dict_rst['hardware'] = str_re

    return dict_rst


def write_file_data(termanil, old_str, new_str, filename):
    if termanil == "m":
        g_ssh_master.exec_cmd("perl -pi -e 's|{}|{}|g' {}".format(old_str, new_str, filename))
    elif termanil == "s":
        g_ssh_slave.exec_cmd("perl -pi -e 's|{}|{}|g' {}".format(old_str, new_str, filename))
    else:
        print(termanil + "error")


def get_ma_udisk_paths():
    stdout = g_ssh_master.exec_cmd(DF + '|grep /dev/sd')

    list_udisk_paths = []
    if '' == stdout:
        return list_udisk_paths

    for item in stdout.splitlines():
        list_info = item.split()
        if 400 > eval(list_info[1].rstrip('G')):
            list_udisk_paths.append(list_info[-1])

    return list_udisk_paths


def get_ma_ehd_paths():
    stdout = g_ssh_master.exec_cmd(DF + '|grep /dev/sd')

    list_ehd_paths = []
    if '' == stdout:
        return list_ehd_paths

    for item in stdout.splitlines():
        list_info = item.split()
        if 400 < eval(list_info[1].rstrip('G')):
            list_ehd_paths.append(list_info[-1])

    return list_ehd_paths


def get_sl_udisk_paths():
    stdout = g_ssh_slave.exec_cmd(DF + '|grep /dev/sd')

    list_udisk_paths = []
    if '' == stdout:
        return list_udisk_paths

    for item in stdout.splitlines():
        list_info = item.split()
        if 400 > eval(list_info[1].rstrip('G')):
            list_udisk_paths.append(list_info[-1])

    return list_udisk_paths


def get_sl_ehd_paths():
    stdout = g_ssh_slave.exec_cmd(DF + '|grep /dev/sd')

    list_ehd_paths = []
    if '' == stdout:
        return list_ehd_paths

    for item in stdout.splitlines():
        list_info = item.split()
        if 400 < eval(list_info[1].rstrip('G')):
            list_ehd_paths.append(list_info[-1])

    return list_ehd_paths


def upload_ma_tar_file(fpath_src, dir_dst, dirname, delflag=True):
    fname = os.path.basename(fpath_src)
    fpath_host = os.path.join(dir_dst, fname)

    if delflag:
        dir_untar = os.path.join(dir_dst, dirname)
        rm_ma_dir(dir_untar)

    if not os.path.exists(fpath_src):
        assert False, '%s not exist!' % fpath_src

    g_ssh_master.upload(fpath_src, dir_dst)

    ext = os.path.splitext(fname)[-1]
    if '.gz' == ext:
        g_ssh_master.exec_cmd(CD + dir_dst + ';' + UNTAR + fname)
    if '.tar' == ext:
        g_ssh_master.exec_cmd(CD + dir_dst + ';' + UNTAR2 + fname)

    rm_ma_file(fpath_host)


def upload_sl_tar_file(fpath_src, dir_dst, dirname, delflag=True):
    fname = os.path.basename(fpath_src)
    fpath_host = os.path.join(dir_dst, fname)

    if delflag:
        dir_untar = os.path.join(dir_dst, dirname)
        rm_sl_dir(dir_untar)

    if not os.path.exists(fpath_src):
        assert False, '%s not exist!' % fpath_src

    g_ssh_slave.upload(fpath_src, dir_dst)

    g_ssh_slave.exec_cmd(CD + dir_dst + ';' + UNTAR + fname)

    rm_sl_file(fpath_host)


def prepare_gg30_dgps_test():
    fpath_loc = os.path.join(DGPS_DIR, 'test_dgps.tar.gz')
    upload_ma_tar_file(fpath_loc, HOME_DIR, 'install')


def prepare_gg30_cam_test():
    fpath_loc = os.path.join(UOS_VER_DIR, 'mipi_test.tar.gz')
    data_loc_path = os.path.join(UOS_VER_DIR, 'testdata.tar.gz')

    upload_ma_tar_file(fpath_loc, HOME_DIR, 'install')
    upload_ma_tar_file(data_loc_path, HOME_DIR, 'testdata')

    upload_sl_tar_file(fpath_loc, HOME_DIR, 'install')
    upload_sl_tar_file(data_loc_path, HOME_DIR, 'testdata')


def get_wifi_ip():
    stdout = g_ssh_master.exec_cmd(IFCONFIG)

    keyword = 'wlan0'

    if keyword not in stdout:
        assert False, 'wlan0 node not exist!'

    key_idx = stdout.find(keyword)
    ip_wifi = get_val_by_re(r'inet addr:(\S*)\s', stdout[key_idx:key_idx+100])

    if not ip_wifi:
        assert False, 'wlan0 ip not exist!'

    # print(ip_wifi)
    return ip_wifi


def scp_file_ma_to_lo(ip_net):
    g_ssh_master.exec_cmd(DD_FILE_100M)

    cmd = 'scp worker@%s:~/iofile %s' % (ip_net, DATA_DIR)
    logger.info(cmd)
    proc = pexpect.spawn(cmd)
    idx = proc.expect(['yes/no', 'password', pexpect.TIMEOUT], timeout=3)

    if 0 == idx:
        proc.sendline('yes')
        proc.expect('password')
        proc.sendline('uisee')
        idx2 = proc.expect([pexpect.EOF, pexpect.TIMEOUT], timeout=30)
        if 0 == idx2:
            proc.kill(0)
        if 1 == idx2:
            proc.kill(0)
            assert False, 'wifi upload 100M file timeout!'

    if 1 == idx:
        proc.sendline('uisee')
        idx2 = proc.expect([pexpect.EOF, pexpect.TIMEOUT], timeout=30)
        if 0 == idx2:
            proc.kill(0)
        if 1 == idx2:
            proc.kill(0)
            assert False, 'wifi upload 100M file timeout!'

    if 2 == idx:
        proc.kill(0)
        assert False, 'can not connect to wifi ip [%s]!' % ip_net

    fpath_src = os.path.join(HOME_DIR,'iofile')
    fpath_dst = os.path.join(DATA_DIR, 'iofile')
    fsize_src = get_ma_fsize(fpath_src)
    fsize_dst = os.path.getsize(fpath_dst)

    rm_ma_file(fpath_src)
    try:
        os.remove(fpath_dst)
    except FileNotFoundError:
        pass

    if fsize_dst != fsize_src:
        assert False, 'wifi upload file size wrong, expect[%d], get[%d]' % (fsize_src, fsize_dst)


def scp_file_lo_to_ma(ip_net):
    fpath_src = os.path.join(DATA_DIR,'iofile')
    dd_cmd = 'dd if=/dev/zero of=%s bs=1M count=100' % fpath_src
    os.system(dd_cmd)

    cmd = 'scp %s worker@%s:~/' % (fpath_src, ip_net)
    logger.info(cmd)
    proc = pexpect.spawn(cmd)
    idx = proc.expect(['yes/no', 'password', pexpect.TIMEOUT], timeout=3)

    if 0 == idx:
        proc.sendline('yes')
        proc.expect('password')
        proc.sendline('uisee')
        idx2 = proc.expect([pexpect.EOF, pexpect.TIMEOUT], timeout=30)
        if 0 == idx2:
            proc.kill(0)
        if 1 == idx2:
            proc.kill(0)
            assert False, 'wifi download 100M file timeout!'

    if 1 == idx:
        proc.sendline('uisee')
        idx2 = proc.expect([pexpect.EOF, pexpect.TIMEOUT], timeout=30)
        if 0 == idx2:
            proc.kill(0)
        if 1 == idx2:
            proc.kill(0)
            assert False, 'wifi download 100M file timeout!'

    if 2 == idx:
        proc.kill(0)
        assert False, 'can not connect to wifi ip [%s]!' % ip_net

    fpath_dst = os.path.join(HOME_DIR,'iofile')
    fsize_src = os.path.getsize(fpath_src)
    fsize_dst = get_ma_fsize(fpath_dst)

    try:
        os.remove(fpath_src)
    except FileNotFoundError:
        pass
    rm_ma_file(fpath_dst)

    if fsize_dst != fsize_src:
        assert False, 'wifi download file size wrong, expect[%d], get[%d]' % (fsize_src, fsize_dst)


def home_df_size(terminal):
    if "s" == terminal:
        stdout = g_ssh_slave.exec_cmd(DF_SPACE)
    elif "m" == terminal:
        stdout = g_ssh_master.exec_cmd(DF_SPACE)
    else:
        print("Parameter error")
    return stdout


def fallocate_file(terminal, file_size, size):
    diff = int(size) - int(file_size)
    if "m" == terminal:
        g_ssh_master.exec_cmd(FALLOCATE.format(diff))
    elif "s" == terminal:
        g_ssh_slave.exec_cmd(FALLOCATE.format(diff))
    else:
        print("parameter error")


if '__main__' == __name__:
    # prepare_local_uos()
    # prepare_gg30_dgps_test()
    # prepare_gg30_cam_test()
    print(get_ma_disk_info())
