#!usr/bin/env python3
# -*- coding: utf-8 -*-

from common.operate_os import *
from common.comm_paras import *
import pexpect
from datetime import datetime, timedelta
from common.host_visitor import FtpHandler
import math
from multiprocessing import Process, Pipe
from common.parallel_proc import exec_cmd_subproc


def chk_prod_type_in_apu(prod_type):
    rst = True
    prod_type = prod_type.lower()

    list_files = ls_ma_dir(APU_VER_DIR)
    print(list_files)
    for item in list_files:
        if item.startswith('uos'):
            if prod_type not in item:
                rst &= False
                assert rst, 'expect [{}], get [{}]'.format(prod_type, item)

    return rst


def chk_prod_type_in_fpga(prod_type):
    rst = True
    prod_type = prod_type.lower()
    ref_file = 'fpga-bitstream-card-v00.bin'
    len_ref_file = len(ref_file)

    list_files = ls_sl_dir(FPGA_VER_DIR)
    print(list_files)
    for item in list_files:
        if item.startswith('fpga') and len(item) < len_ref_file:
            if prod_type not in item:
                rst &= False
                assert rst, 'expect [{}], get [{}]'.format(prod_type, item)

    return rst


def chk_dict_rst_with_key(key, dict_expt, dict_rst):
    rst = True
    rsts = {}

    if dict_expt[key] != dict_rst[key]:
        rst &= False
        rsts[key] = '[{}] check fail: expect [{}], get [{}]'.format(key, dict_expt[key], dict_rst[key])

    assert rst, str(rsts)
    return rst


def chk_dict_rst(dict_expt, dict_rst):
    rst = True
    rsts = {}

    for key in dict_expt:
        if dict_expt[key] != dict_rst[key]:
            rst &= False
            rsts[key] = '[{}] check fail: expect [{}], get [{}]'.format(key, dict_expt[key], dict_rst[key])

    assert rst, str(rsts)
    return rst


def chk_keyword_not_exist(keyword, str_or_list_rst):
    if keyword in str_or_list_rst:
        assert False, 'result expect not include [{}]'.format(keyword)


def chk_keyword_exists(keyword, str_or_list_rst):
    # check error in str_or_list_rst
    list_error = ['error', 'Error', 'ERROR']
    for item in list_error:
        chk_keyword_not_exist(item, str_or_list_rst)

    if keyword not in str_or_list_rst:
        assert False, 'result expect including [{}]'.format(keyword)


def chk_expt_words_exist(dict_expt, str_or_list_rst):
    rst = True

    # check error in str_or_list_rst
    list_error = ['error', 'Error', 'ERROR']
    for item in list_error:
        chk_keyword_not_exist(item, str_or_list_rst)

    for key, value in dict_expt.items():
        for item in value.split('/'):
            if item not in str_or_list_rst:
                rst &= False
                assert rst, 'result expect including [{}]'.format(item)

    return rst


def chk_ma_ssh_sl(str_sl):
    proc = pexpect.spawn(SSH + 'worker@' + MASTER_IP)
    proc.expect("password:", timeout=3)
    proc.sendline('uisee')
    proc.expect('worker@master')
    proc.sendline(SSH + str_sl)
    idx = proc.expect(['worker@slave', pexpect.TIMEOUT], timeout=3)
    if 0 == idx:
        print('master ssh ' + str_sl + ' OK.')
        proc.sendline('exit')
        proc.expect('worker@master')
        proc.sendline('exit')
        return True
    if 1 == idx:
        proc.kill(0)
        assert False, 'master ssh [{}] fail'.format(str_sl)


def chk_sl_ssh_ma(str_ma):
    proc = pexpect.spawn(SSH + 'worker@' + SLAVE_IP)
    proc.expect("password:", timeout=3)
    proc.sendline('uisee')
    proc.expect('worker@slave')
    proc.sendline(SSH + str_ma)
    idx = proc.expect(['worker@master', pexpect.TIMEOUT], timeout=3)
    if 0 == idx:
        print('slave ssh ' + str_ma + ' OK.')
        proc.sendline('exit')
        proc.expect('worker@slave')
        proc.sendline('exit')
        return True
    if 1 == idx:
        proc.kill(0)
        assert False, 'slave ssh [{}] fail'.format(str_ma)


def chk_ma_sl_time():
    tm_ma = g_ssh_master.exec_cmd(DATE).strip()
    tm_sl = g_ssh_slave.exec_cmd(DATE).strip()
    tm_ma = datetime.strptime(tm_ma, '%a %b %d %H:%M:%S CST %Y')
    tm_sl = datetime.strptime(tm_sl, '%a %b %d %H:%M:%S CST %Y')

    dif_ma_sl = abs(tm_ma - tm_sl).seconds

    if dif_ma_sl > 1:
        assert False, 'master and slave time diffs [{}] seconds'.format(dif_ma_sl)

    return True


def chk_ma_loc_time():
    tm_ma = g_ssh_master.exec_cmd(DATE).strip()
    tm_ma = datetime.strptime(tm_ma, '%a %b %d %H:%M:%S CST %Y')
    tm_lo = datetime.now()
    g_logger.info('internet time: {}'.format(tm_lo))

    dif_ma_lo = abs(tm_ma - tm_lo).seconds
    dif_ma_lo_days = abs(tm_ma - tm_lo).days

    if dif_ma_lo > 1:
        assert False, 'master and local time diffs [{}] days [{}] seconds'.format(dif_ma_lo_days, dif_ma_lo)

    return True


def chk_sl_loc_time():
    tm_sl = g_ssh_slave.exec_cmd(DATE).strip()
    tm_sl = datetime.strptime(tm_sl, '%a %b %d %H:%M:%S CST %Y')
    tm_lo = datetime.now()
    g_logger.info('internet time: {}'.format(tm_lo))

    dif_sl_lo = abs(tm_sl - tm_lo).seconds
    dif_sl_lo_days = abs(tm_sl - tm_lo).days

    if dif_sl_lo > 1:
        assert False, 'master and local time diffs [{}] days [{}] seconds'.format(dif_sl_lo_days, dif_sl_lo)

    return True


def mod_and_chk_ma_time():
    tm_ma = g_ssh_master.exec_cmd(DATE).strip()
    tm_ma = datetime.strptime(tm_ma, '%a %b %d %H:%M:%S CST %Y')

    tm_for_mod = str(tm_ma + timedelta(seconds=-180))
    cmd = DATE + ' -s ' + '"' + tm_for_mod + '"'
    g_ssh_master.exec_cmd(cmd)
    g_ssh_master.exec_cmd(HWCLOCK)

    reboot_os()

    print('waiting for master and slave time synchronization, cost 210s...')
    time.sleep(210)

    chk_ma_sl_time()

    return True


def mod_and_chk_sl_time():
    tm_ma = g_ssh_slave.exec_cmd(DATE).strip()
    tm_ma = datetime.strptime(tm_ma, '%a %b %d %H:%M:%S CST %Y')

    tm_for_mod = str(tm_ma + timedelta(seconds=-180))
    print(tm_for_mod)
    cmd = DATE + ' -s ' + '"' + tm_for_mod + '"'
    g_ssh_slave.exec_cmd(cmd)
    g_ssh_slave.exec_cmd(HWCLOCK)

    reboot_os()

    print('waiting for master and slave time synchronization, cost 40s...')
    time.sleep(40)

    chk_ma_sl_time()

    return True


def chk_ftp_file_exist(fname):
    proc = open_ma_ftp()

    promp = 'ftp>'
    proc.sendline(CD + os.path.basename(UOS_LOG_DIR))
    proc.expect(promp)
    proc.sendline(LS)
    idx = proc.expect([fname, pexpect.TIMEOUT], timeout=3)

    if 1 == idx:
        proc.kill(0)
        assert False, 'UISEE_LOGS added file [{}] not found in ftp!'.format(fname)

    close_ftp(proc)

    return True


def chk_ftp_file_not_exist(fname):
    proc = open_ma_ftp()

    promp = 'ftp>'
    proc.sendline(CD + os.path.basename(UOS_LOG_DIR))
    proc.expect(promp)
    proc.sendline(LS)
    idx = proc.expect([fname, pexpect.TIMEOUT], timeout=3)

    if 0 == idx:
        proc.kill(0)
        assert False, 'UISEE_LOGS removed file [{}] found in ftp!'.format(fname)

    close_ftp(proc)

    return True


def chk_ftp_file_content(fname, text):
    ftp_get(fname)

    fpath_loc = os.path.join(os.getcwd(), fname)
    if text != open(fpath_loc).read().strip():
        assert False, 'ftp downloaded file [{}] content diff from master\'s'.format(fname)

    return True


def chk_ftp_open():
    proc = open_ma_ftp()

    close_ftp(proc)

    return True


def chk_ftp_closed():
    proc = pexpect.spawn('ftp -p ' + MASTER_IP)
    idx = proc.expect(['Connection refused', pexpect.TIMEOUT], timeout=3)

    if 1 == idx:
        proc.kill(0)
        assert False, 'no [Connection refused] replied, check fail!'

    close_ftp(proc)

    return True


def chk_ping_ip():
    cmd = PING + '-c 1 -w 1 8.8.8.8'
    stdout = g_ssh_master.exec_cmd(cmd)

    loss_num = get_val_by_re(r'(\d*)% packet loss', stdout)
    if '' == loss_num:
        assert False, 'master ping fail, time out!'

    if int(loss_num):
        assert False, 'master ping fail, [{}%] packet loss!'.format(loss_num)

    stdout = g_ssh_slave.exec_cmd(cmd)

    loss_num = get_val_by_re(r'(\d*)% packet loss', stdout)
    if '' == loss_num:
        assert False, 'slave ping fail, time out!'

    if int(loss_num):
        assert False, 'slave ping fail, [{}%] packet loss!'.format(loss_num)


def chk_ping_url():
    cmd = PING + '-c 1 -w 1 www.baidu.com'
    stdout = g_ssh_master.exec_cmd(cmd)

    loss_num = get_val_by_re(r'(\d*)% packet loss', stdout)
    if '' == loss_num:
        assert False, 'master ping fail, time out!'

    if int(loss_num):
        assert False, 'master ping fail, [{}%] packet loss!'.format(loss_num)

    stdout = g_ssh_slave.exec_cmd(cmd)

    loss_num = get_val_by_re(r'(\d*)% packet loss', stdout)
    if '' == loss_num:
        assert False, 'slave ping fail, time out!'

    if int(loss_num):
        assert False, 'slave ping fail, [{}%] packet loss!'.format(loss_num)


def chk_wvdial_info(info):
    keyword = 'pppd: [7f]'
    if keyword not in info.split('\n')[-2]:
        assert False, '{} not found in wvdial.log'.format(keyword)


def chk_wlan0_exists():
    stdout = g_ssh_master.exec_cmd(IFCONFIG + '|grep wlan0')

    chk_keyword_exists('wlan0', stdout)


def chk_ppp0_exists():
    stdout = g_ssh_master.exec_cmd(IFCONFIG + '|grep ppp0')

    chk_keyword_exists('ppp0', stdout)


def chk_ppp0_not_exist():
    stdout = g_ssh_master.exec_cmd(IFCONFIG + '|grep ppp0')

    chk_keyword_not_exist('ppp0', stdout)


def chk_wvdial_not_exist():
    fname = 'wvdial.log'

    try:
        g_ssh_master.get_stat(os.path.join(HOME_DIR, fname))
    except FileNotFoundError:
        return True
    else:
        assert False, '[{}] expect not exist!'.format(fname)


def chk_ftp_fs_log_size(log_date):
    ftper = FtpHandler(hostip=LOG_FTP_IP)

    list_log = g_ssh_master.ls_dir(os.path.join(UOS_LOG_DIR, log_date))

    for fname in list_log:
        log_path_uos = os.path.join(UOS_LOG_DIR, log_date, fname)
        fsize_uos = g_ssh_master.get_stat(log_path_uos).st_size

        log_path_ftp = os.path.join(FTP_LOG_DIR_FS, log_date, fname)
        fsize_ftp = ftper.get_size(log_path_ftp)

        if fsize_ftp != fsize_uos:
            assert False, 'log [{}] ftp size [{}], expect [{}]'.format(fname, fsize_ftp, fsize_uos)


def chk_download():
    g_ssh_master.exec_cmd(WGET + 'www.baidu.com')

    down_file = 'index.html'
    fpath = os.path.join(HOME_DIR, down_file)
    try:
        fstat = g_ssh_master.get_stat(fpath)
    except FileNotFoundError:
        assert False, '[{}] download fail!'.format(down_file)
    else:
        fsize = fstat.st_size
        if 2000 > fsize:
            assert False, 'downloaded file [{}] size [{}], expect > 2000 bytes'.format(down_file, fsize)

        g_ssh_master.rm_file(fpath)


def chk_exter_gateway():
    stdout = g_ssh_master.exec_cmd(ROUTE)

    chk_keyword_exists('192.168.100.1', stdout)


def chk_wifi_cfg(uname, pwd):
    stdout = g_ssh_master.exec_cmd(CAT + NETWORK_CFG_PATH)

    chk_keyword_exists(uname, stdout)
    chk_keyword_exists(pwd, stdout)


def chk_ota_version(ver):
    cmd = 'cd ~/uos/run/;strings bin/uos_daemon|grep ' + ver
    if not g_ssh_master.exec_cmd(cmd):
        assert False, '[{}] not found in uos_daemon date!'.format(ver)

    cmd = 'cd ~/;dpkg -l|grep hmi'
    if ver not in g_ssh_master.exec_cmd(cmd):
        assert False, '[{}] not found in [dpkg -l|grep hmi]!'.format(ver)

    list_info = get_apu_info()
    apu_ver = ver.replace('-', '/')
    apu_cmp_time = list_info['apu compile time']
    if apu_ver != apu_cmp_time:
        assert False, 'apu compile time get [{}], expect [{}]!'.format(apu_cmp_time, apu_ver)


def chk_uos_launch(uosdir):
    first_flag = False
    logdir = get_uos_logdir()
    try:
        logs_old = ls_ma_dir(logdir)
    except FileNotFoundError:
        first_flag = True
        logs_old = list()

    launch_uos_pexpt(uosdir)
    stop_uos(uosdir)

    logs_new = ls_ma_dir(logdir)
    diff = list(set(logs_new) - set(logs_old))
    if not diff:
        assert False, 'uos log not generated!'

    if not first_flag:
        for item in diff:
            if 1400000 > get_ma_fsize(os.path.join(logdir, item)):
                assert False, 'uos log [{}] size less than 1.4M!'.format(item)

    if first_flag:
        logs_true = [item for item in diff if 'bak' not in item]

        if not logs_true:
            assert False, 'uos log not generated!'

        for item in logs_true:
            if 1400000 > get_ma_fsize(os.path.join(logdir, item)):
                assert False, 'uos log [{}] size less than 1.4M!'.format(item)


def chk_ssd_exists(hostname):
    if 'master' == hostname:
        ssh_host = g_ssh_master
    else:
        ssh_host = g_ssh_slave

    cmd = FDISK + '| grep /dev/sda'
    stdout = ssh_host.exec_cmd(cmd)

    if '/dev/sda' not in stdout:
        assert False, 'ssd not exist in fdisk!'

    cmd = LSBLK + '| grep -E "NAME|sda"'
    stdout = ssh_host.exec_cmd(cmd)

    if 'sda' not in stdout:
        assert False, 'ssd not exist in lsblk!'


def chk_exter_disk_type(hostname):
    if 'master' == hostname:
        ssh_host = g_ssh_master
    else:
        ssh_host = g_ssh_slave

    # cmd = CAT + '/sys/block/mmcblk0/queue/rotational'
    cmd = CAT + '/sys/block/sda/queue/rotational'
    stdout = ssh_host.exec_cmd(cmd)

    if '0' != stdout.strip():
        assert False, 'disk type expect ssd!'

    stdout = ssh_host.exec_cmd(LSBLK)
    for line in stdout.splitlines():
        words = line.split()
        if 'sda' == words[0]:
            if '0' != words[-1]:
                assert False, 'disk type expect ssd!'


def chk_ssd_size(hostname):
    if 'master' == hostname:
        ssh_host = g_ssh_master
    else:
        ssh_host = g_ssh_slave

    cmd = DF + '| grep -E "Filesystem|sda"'
    stdout = ssh_host.exec_cmd(cmd)

    expt_disk_size = 218
    if 'sda' in stdout:
        sda_size = float(stdout.splitlines()[-1].strip().split()[3].rstrip('G'))

        if expt_disk_size > sda_size:
            assert False, 'disk size expect [{}G], get [{}G]'.format(str(expt_disk_size), str(sda_size))
    else:
        assert False, 'sda not exist in [df -hl]!'


def ps_ef_grep(terminal,process):
    stdout = ""
    if terminal == "s":
        stdout = g_ssh_slave.exec_cmd(process)
        print(stdout)
    elif terminal == "m":
        stdout = g_ssh_master.exec_cmd(process)
    else:
        print("error")
    if not stdout:
        assert False, 'There is no such process'


def chk_cp_file_to_disk(hostname):
    if 'master' == hostname:
        ifpath = os.path.join(HOME_DIR, 'iofile')
        ofpath = os.path.join(HOME_DIR, 'disk', 'iofile')

        rm_ma_file(ifpath)
        rm_ma_file(ofpath)

        g_ssh_master.exec_cmd('dd if=/dev/zero of=~/iofile bs=1M count=1000')
        g_ssh_master.exec_cmd('cp ~/iofile ~/disk/')

        ifsize = get_ma_file_size(ifpath) / 10 ** 6
        try:
            ofsize = get_ma_file_size(ofpath) / 10 ** 6
        except FileNotFoundError:
            assert False, '[iofile] copied to ~/disk fail!'

        if ofsize != ifsize:
            assert False, '[iofile] copied to disk size wrong, expect [{}M] get [{}M]!'.format(ifsize, ofsize)

        rm_ma_file(ifpath)
        rm_ma_file(ofpath)

    if 'slave' == hostname:
        ifpath = os.path.join(HOME_DIR, 'iofile')
        ofpath = os.path.join(HOME_DIR, 'disk', 'iofile')

        rm_sl_file(ifpath)
        rm_sl_file(ofpath)

        g_ssh_slave.exec_cmd('dd if=/dev/zero of=~/iofile bs=1M count=1000')
        g_ssh_slave.exec_cmd('cp ~/iofile ~/disk/')

        ifsize = get_sl_file_size(ifpath)/10**6
        try:
            ofsize = get_sl_file_size(ofpath)/10**6
        except FileNotFoundError:
            assert False, '[iofile] copied to ~/disk fail!'

        if ofsize != ifsize:
            assert False, '[iofile] copied to disk size wrong, expect [{}M] get [{}M]!'.format(ifsize, ofsize)

        rm_sl_file(ifpath)
        rm_sl_file(ofpath)


def chk_dd_file_to_disk(hostname):
    ofpath = os.path.join(HOME_DIR, 'disk', 'iofile')

    if 'master' == hostname:
        rm_ma_file(ofpath)
        stdout = g_ssh_master.exec_cmd('dd if=/dev/zero of=~/disk/iofile bs=1M count=1000')

        try:
            ofsize = get_ma_file_size(ofpath)
        except FileNotFoundError:
            assert False, '[iofile] written to ~/disk fail!'

        if '1048576000' != str(ofsize):
            assert False, '[iofile] written to disk size wrong, expect [1048567000] get [{}]!'.format(str(ofsize))

        rate = get_val_by_re(r', (\S+) MB/s', stdout)

        rate_expt = 500
        if rate_expt > math.floor(eval(rate)):
            assert False, 'write rate too low, expect > {} MB/s get [{} MB/s]'.format(str(rate_expt), rate)

        rm_ma_file(ofpath)
    else:
        rm_sl_file(ofpath)
        stdout = g_ssh_slave.exec_cmd('dd if=/dev/zero of=~/disk/iofile bs=1M count=1000')

        try:
            ofsize = get_sl_file_size(ofpath)
        except FileNotFoundError:
            assert False, '[iofile] written to ~/disk fail!'

        if '1048576000' != str(ofsize):
            assert False, '[iofile] written to disk size wrong, expect [1048567000] get [{}]!'.format(str(ofsize))

        rate = get_val_by_re(r', (\S+) MB/s', stdout)

        rate_expt = 500
        if rate_expt > math.floor(eval(rate)):
            assert False, 'write rate too low, expect > {} MB/s get [{} MB/s]'.format(str(rate_expt), rate)

        rm_sl_file(ofpath)


def chk_dd_file_to_disk_sync(hostname):
    ofpath = os.path.join(HOME_DIR, 'disk', 'iofile')

    if 'master' == hostname:
        rm_ma_file(ofpath)

        stdout = g_ssh_master.exec_cmd('dd if=/dev/zero of=~/disk/iofile bs=1M count=1000;sync')

        try:
            ofsize = get_ma_file_size(ofpath)
        except FileNotFoundError:
            assert False, '[iofile] written to ~/disk fail!'

        if '1048576000' != str(ofsize):
            assert False, '[iofile] written to disk size wrong, expect [1048567000] get [{}]!'.format(str(ofsize))

        rate = get_val_by_re(r', (\S+) MB/s', stdout)

        rate_expt = 480
        if rate_expt > math.floor(eval(rate)):
            assert False, 'write rate too low, expect > {} MB/s get [{} MB/s]'.format(str(rate_expt), rate)

        rm_ma_file(ofpath)
    else:
        rm_sl_file(ofpath)

        stdout = g_ssh_slave.exec_cmd('dd if=/dev/zero of=~/disk/iofile bs=1M count=1000;sync')

        try:
            ofsize = get_sl_file_size(ofpath)
        except FileNotFoundError:
            assert False, '[iofile] written to ~/disk fail!'

        if '1048576000' != str(ofsize):
            assert False, '[iofile] written to disk size wrong, expect [1048567000] get [{}]!'.format(str(ofsize))

        rate = get_val_by_re(r', (\S+) MB/s', stdout)

        rate_expt = 480
        if rate_expt > math.floor(eval(rate)):
            assert False, 'write rate too low, expect > {} MB/s get [{} MB/s]'.format(str(rate_expt), rate)

        rm_sl_file(ofpath)


def chk_dd_file_to_disk_fdsync(hostname):
    ofpath = os.path.join(HOME_DIR, 'disk', 'iofile')

    if 'master' == hostname:
        rm_ma_file(ofpath)

        stdout = g_ssh_master.exec_cmd('dd if=/dev/zero of=~/disk/iofile bs=1M count=1000 conv=fdatasync')

        try:
            ofsize = get_ma_file_size(ofpath)
        except FileNotFoundError:
            assert False, '[iofile] written to ~/disk fail!'

        if '1048576000' != str(ofsize):
            assert False, '[iofile] written to disk size wrong, expect [1048567000] get [{}]!'.format(str(ofsize))

        rate = get_val_by_re(r', (\S+) MB/s', stdout)

        rate_expt = 180
        if rate_expt > math.floor(eval(rate)):
            assert False, 'write rate too low, expect > {} MB/s get [{} MB/s]'.format(str(rate_expt), rate)

        rm_ma_file(ofpath)
    else:
        rm_sl_file(ofpath)

        stdout = g_ssh_slave.exec_cmd('dd if=/dev/zero of=~/disk/iofile bs=1M count=1000 conv=fdatasync')

        try:
            ofsize = get_sl_file_size(ofpath)
        except FileNotFoundError:
            assert False, '[iofile] written to ~/disk fail!'

        if '1048576000' != str(ofsize):
            assert False, '[iofile] written to disk size wrong, expect [1048567000] get [{}]!'.format(str(ofsize))

        rate = get_val_by_re(r', (\S+) MB/s', stdout)

        rate_expt = 180
        if rate_expt > math.floor(eval(rate)):
            assert False, 'write rate too low, expect > {} MB/s get [{} MB/s]'.format(str(rate_expt), rate)

        rm_sl_file(ofpath)


def chk_dd_file_to_disk_dsync(hostname):
    ofpath = os.path.join(HOME_DIR, 'disk', 'iofile')

    if 'master' == hostname:
        rm_ma_file(ofpath)

        stdout = g_ssh_master.exec_cmd('dd if=/dev/zero of=~/disk/iofile bs=1M count=1000 oflag=dsync')

        try:
            ofsize = get_ma_file_size(ofpath)
        except FileNotFoundError:
            assert False, '[iofile] written to ~/disk fail!'

        if '1048576000' != str(ofsize):
            assert False, '[iofile] written to disk size wrong, expect [1048567000] get [{}]!'.format(str(ofsize))

        rate = get_val_by_re(r', (\S+) MB/s', stdout)

        rate_expt = 78
        if rate_expt > math.floor(eval(rate)):
            assert False, 'write rate too low, expect > {} MB/s get [{} MB/s]'.format(str(rate_expt), rate)

        rm_ma_file(ofpath)
    else:
        rm_sl_file(ofpath)

        stdout = g_ssh_slave.exec_cmd('dd if=/dev/zero of=~/disk/iofile bs=1M count=1000 oflag=dsync')

        try:
            ofsize = get_sl_file_size(ofpath)
        except FileNotFoundError:
            assert False, '[iofile] written to ~/disk fail!'

        if '1048576000' != str(ofsize):
            assert False, '[iofile] written to disk size wrong, expect [1048567000] get [{}]!'.format(str(ofsize))

        rate = get_val_by_re(r', (\S+) MB/s', stdout)

        rate_expt = 78
        if rate_expt > math.floor(eval(rate)):
            assert False, 'write rate too low, expect > {} MB/s get [{} MB/s]'.format(str(rate_expt), rate)

        rm_sl_file(ofpath)


def chk_cp_file_from_disk(hostname):
    ifpath = os.path.join(HOME_DIR, 'disk', 'iofile')
    ofpath = os.path.join(HOME_DIR, 'iofile')

    if 'master' == hostname:
        rm_ma_file(ifpath)
        rm_ma_file(ofpath)

        g_ssh_master.exec_cmd('dd if=/dev/zero of=~/disk/iofile bs=1M count=1000')
        g_ssh_master.exec_cmd('cp ~/disk/iofile ~/')

        ifsize = get_ma_file_size(ifpath)
        try:
            ofsize = get_ma_file_size(ofpath)
        except FileNotFoundError:
            assert False, '[iofile] copied to ~/ fail!'

        if ofsize != ifsize:
            assert False, 'iofile read from ~/disk size wrong, expect [{} byte] get [{} byte]'.format(ifsize, ofsize)

        rm_ma_file(ifpath)
        rm_ma_file(ofpath)
    else:
        rm_sl_file(ifpath)
        rm_sl_file(ofpath)

        g_ssh_slave.exec_cmd('dd if=/dev/zero of=~/disk/iofile bs=1M count=1000')
        g_ssh_slave.exec_cmd('cp ~/disk/iofile ~/')

        ifsize = get_sl_file_size(ifpath)
        try:
            ofsize = get_sl_file_size(ofpath)
        except FileNotFoundError:
            assert False, '[iofile] copied to ~/ fail!'

        if ofsize != ifsize:
            assert False, 'iofile read from ~/disk size wrong, expect [{} byte] get [{} byte]'.format(ifsize, ofsize)

        rm_sl_file(ifpath)
        rm_sl_file(ofpath)


def chk_dd_file_from_disk(hostname):
    ifpath = os.path.join(HOME_DIR, 'disk', 'iofile')

    if 'master' == hostname:
        rm_ma_file(ifpath)

        g_ssh_master.exec_cmd('dd if=/dev/zero of=~/disk/iofile bs=1M count=1000')
        stdout = g_ssh_master.exec_cmd('dd if=~/disk/iofile of=/dev/null bs=1M count=1000')

        rate = get_val_by_re(r', (\S+) GB/s', stdout)

        if not rate:
            assert False, 'write rate get fail!'

        rate_expt = 4.0
        if rate_expt > math.floor(eval(rate)):
            assert False, 'write rate too low, expect > {} GB/s get [{} GB/s]'.format(str(rate_expt), rate)

        rm_ma_file(ifpath)
    else:
        rm_sl_file(ifpath)

        g_ssh_slave.exec_cmd('dd if=/dev/zero of=~/disk/iofile bs=1M count=1000')
        stdout = g_ssh_slave.exec_cmd('dd if=~/disk/iofile of=/dev/null bs=1M count=1000')

        rate = get_val_by_re(r', (\S+) GB/s', stdout)

        if not rate:
            assert False, 'write rate get fail!'

        rate_expt = 4.0
        if rate_expt > math.floor(eval(rate)):
            assert False, 'write rate too low, expect > {} GB/s get [{} GB/s]'.format(str(rate_expt), rate)

        rm_sl_file(ifpath)


def chk_dd_file_from_disk_sync(hostname):
    ifpath = os.path.join(HOME_DIR, 'disk', 'iofile')

    if 'master' == hostname:
        rm_ma_file(ifpath)

        g_ssh_master.exec_cmd('dd if=/dev/zero of=~/disk/iofile bs=1M count=1000')
        stdout = g_ssh_master.exec_cmd('dd if=~/disk/iofile of=/dev/null bs=1M count=1000;sync')

        rate = get_val_by_re(r', (\S+) GB/s', stdout)

        if not rate:
            assert False, 'write rate get fail!'

        rate_expt = 4.0
        if rate_expt > math.floor(eval(rate)):
            assert False, 'write rate too low, expect > {} GB/s get [{} GB/s]'.format(str(rate_expt), rate)

        rm_ma_file(ifpath)
    else:
        rm_sl_file(ifpath)

        g_ssh_slave.exec_cmd('dd if=/dev/zero of=~/disk/iofile bs=1M count=1000')
        stdout = g_ssh_slave.exec_cmd('dd if=~/disk/iofile of=/dev/null bs=1M count=1000;sync')

        rate = get_val_by_re(r', (\S+) GB/s', stdout)

        if not rate:
            assert False, 'write rate get fail!'

        rate_expt = 4.0
        if rate_expt > math.floor(eval(rate)):
            assert False, 'write rate too low, expect > {} GB/s get [{} GB/s]'.format(str(rate_expt), rate)

        rm_sl_file(ifpath)


def chk_dd_file_from_disk_fdsync(hostname):
    ifpath = os.path.join(HOME_DIR, 'disk', 'iofile')

    if 'master' == hostname:
        rm_ma_file(ifpath)

        g_ssh_master.exec_cmd('dd if=/dev/zero of=~/disk/iofile bs=1M count=1000')
        stdout = g_ssh_master.exec_cmd('dd if=~/disk/iofile of=/dev/null bs=1M count=1000 conv=fdatasync')

        rate = get_val_by_re(r', (\S+) GB/s', stdout)

        if not rate:
            assert False, 'write rate get fail!'

        rate_expt = 4.0
        if rate_expt > math.floor(eval(rate)):
            assert False, 'write rate too low, expect > {} GB/s get [{} GB/s]'.format(str(rate_expt), rate)

        rm_ma_file(ifpath)
    else:
        rm_sl_file(ifpath)

        g_ssh_slave.exec_cmd('dd if=/dev/zero of=~/disk/iofile bs=1M count=1000')
        stdout = g_ssh_slave.exec_cmd('dd if=~/disk/iofile of=/dev/null bs=1M count=1000 conv=fdatasync')

        rate = get_val_by_re(r', (\S+) GB/s', stdout)

        if not rate:
            assert False, 'write rate get fail!'

        rate_expt = 4.0
        if rate_expt > math.floor(eval(rate)):
            assert False, 'write rate too low, expect > {} GB/s get [{} GB/s]'.format(str(rate_expt), rate)

        rm_sl_file(ifpath)


def chk_dd_file_from_disk_dsync(hostname):
    ifpath = os.path.join(HOME_DIR, 'disk', 'iofile')

    if 'master' == hostname:
        rm_ma_file(ifpath)

        g_ssh_master.exec_cmd('dd if=/dev/zero of=~/disk/iofile bs=1M count=1000')
        stdout = g_ssh_master.exec_cmd('dd if=~/disk/iofile of=/dev/null bs=1M count=1000 oflag=dsync')

        rate = get_val_by_re(r', (\S+) GB/s', stdout)

        if not rate:
            assert False, 'write rate get fail!'

        rate_expt = 4.0
        if rate_expt > math.floor(eval(rate)):
            assert False, 'write rate too low, expect > {} GB/s get [{} GB/s]'.format(str(rate_expt), rate)

        rm_ma_file(ifpath)
    else:
        rm_sl_file(ifpath)

        g_ssh_slave.exec_cmd('dd if=/dev/zero of=~/disk/iofile bs=1M count=1000')
        stdout = g_ssh_slave.exec_cmd('dd if=~/disk/iofile of=/dev/null bs=1M count=1000 oflag=dsync')

        rate = get_val_by_re(r', (\S+) GB/s', stdout)

        if not rate:
            assert False, 'write rate get fail!'

        rate_expt = 4.0
        if rate_expt > math.floor(eval(rate)):
            assert False, 'write rate too low, expect > {} GB/s get [{} GB/s]'.format(str(rate_expt), rate)

        rm_sl_file(ifpath)


def chk_ma_udisk_exists():
    if not get_ma_udisk_paths():
        assert False, 'flash disk not found in df -hl!'


def chk_ma_ehd_exists():
    if not get_ma_ehd_paths():
        assert False, 'external hdd not found in df -hl!'


def chk_sl_udisk_exists():
    if not get_sl_udisk_paths():
        assert False, 'flash disk not found in df -hl!'


def chk_sl_ehd_exists():
    if not get_sl_ehd_paths():
        assert False, 'external hdd not found in df -hl!'


def chk_ma_file_io_exter(dtype):
    path_ma = os.path.join(HOME_DIR, 'iofile')
    rm_ma_file(path_ma)

    paths = list()
    if 'udisk' == dtype:
        paths = get_ma_udisk_paths()
    if 'ehd' == dtype:
        paths = get_ma_ehd_paths()

    if not paths:
        assert False, '{} not found in df -hl!'.format(dtype)

    g_ssh_master.exec_cmd('dd if=/dev/zero of=~/iofile bs=1M count=1000')
    fsize = get_ma_fsize(path_ma)
    for path in paths:
        start_time = time.time()

        g_ssh_master.exec_cmd('mv ~/iofile ' + path + '/')

        end_time = time.time()
        cost_time = end_time - start_time
        logger.info('mv 1G file from master to %s cost %.2fs' % (dtype, cost_time))

        try:
            chksize = get_ma_fsize(os.path.join(path, 'iofile'))
        except FileNotFoundError:
            assert False, 'file moved to udisk not found!'
        if chksize != fsize:
            assert False, 'file moved to udisk size wrong, expect [{}] get [{}]'.format(fsize, chksize)

        start_time = time.time()

        g_ssh_master.exec_cmd('mv ' + path + '/iofile ~/')

        end_time = time.time()
        cost_time = end_time - start_time
        logger.info('mv 1G file from %s to master cost %.2fs' % (dtype, cost_time))

        try:
            chksize = get_ma_fsize(path_ma)
        except FileNotFoundError:
            assert False, 'file moved to master not found!'
        if chksize != fsize:
            assert False, 'file moved to master size wrong, expect [{}] get [{}]'.format(fsize, chksize)

        rm_ma_file(path_ma)


def chk_sl_file_io_exter(dtype):
    path_sl = os.path.join(HOME_DIR, 'iofile')
    rm_sl_file(path_sl)

    paths = list()
    if 'udisk' == dtype:
        paths = get_sl_udisk_paths()
    if 'ehd' == dtype:
        paths = get_sl_ehd_paths()

    if not paths:
        assert False, '{} not found in df -hl!'.format(dtype)

    g_ssh_master.exec_cmd('dd if=/dev/zero of=~/iofile bs=1M count=1000')
    fsize = get_sl_fsize(path_sl)
    for path in paths:
        start_time = time.time()

        g_ssh_slave.exec_cmd('mv ~/iofile ' + path + '/')

        end_time = time.time()
        cost_time = end_time - start_time
        logger.info('mv 1G file from slave to %s cost %.2fs' % (dtype, cost_time))

        try:
            chksize = get_sl_fsize(os.path.join(path, 'iofile'))
        except FileNotFoundError:
            assert False, 'file moved to udisk not found!'
        if chksize != fsize:
            assert False, 'file moved to udisk size wrong, expect [{}] get [{}]'.format(fsize, chksize)

        start_time = time.time()

        g_ssh_slave.exec_cmd('mv ' + path + '/iofile ~/')

        end_time = time.time()
        cost_time = end_time - start_time
        logger.info('mv 1G file from  %s to slave cost %.2fs' % (dtype, cost_time))

        try:
            chksize = get_sl_fsize(path_sl)
        except FileNotFoundError:
            assert False, 'file moved to slave not found!'
        if chksize != fsize:
            assert False, 'file moved to slave size wrong, expect [{}] get [{}]'.format(fsize, chksize)

        rm_sl_file(path_sl)


def chk_len_str(str_expt, str_rey):
    for data in str_rey:
        if str(data) != str_expt:
            assert False, "Wrong camera echo result"


def chk_result_com(terminal):
    if "s" == terminal:
        stdout = g_ssh_slave.exec_cmd("echo $?")
    elif "m" == terminal:
        stdout = g_ssh_master.exec_cmd("echo $?")
    else:
        print("Parameter error")
    if stdout != "0":
        assert False, "Command not found"


def chk_dmesg_info(hostname, dmesg_info):
    if not dmesg_info:
        assert False, '[%s] dmesg is null!' % hostname

    found = False
    # check error in dmesg info
    list_error = ['error', 'Error']
    for item in list_error:
        if item in dmesg_info:
            found |= True

    if found:
        g_ssh_master.exec_cmd('dmesg | grep error -i')
        assert False, '[error] exists in [%s] dmesg!' % hostname


def chk_dump_video0(host='master', num=4):
    g_ssh_master.exec_cmd(CONFIG_UB964)

    time.sleep(5)

    cmd = DUMP_VIDEO0 + str(num)
    (parent_end, child_end) = Pipe()
    child = Process(target=exec_cmd_subproc, args=(host, cmd, child_end))
    child.start()

    time.sleep(5)

    if child.is_alive():
        child_end.close()
        child.terminate()
        child.join()
        assert False, '%s exec [%s] time out' % (host, cmd)

    stdout = parent_end.recv()
    parent_end.close()

    pat = r'(\S*?) fps'
    list_fps = get_list_by_re_findall(pat, stdout)

    if list_fps:
        for item in list_fps:
            if '25.00' != item:
                assert False, '%s video0 fps != 25.00' % host

        num_fps = len(list_fps)
        if 3 != num_fps:
            assert False, '%s video0 25.00 fps num got %d, expect 3' % (host, num_fps)
    else:
        assert False, '%s video0 got no fps result' % host


def chk_dump_video1(host='master', num=4):
    # g_ssh_master.exec_cmd(CONFIG_UB964)
    #
    # time.sleep(5)

    cmd = DUMP_VIDEO1 + str(num)
    (parent_end, child_end) = Pipe()
    child = Process(target=exec_cmd_subproc, args=(host, cmd, child_end))
    child.start()

    time.sleep(5)

    if child.is_alive():
        child_end.close()
        child.terminate()
        child.join()
        assert False, '%s exec [%s] time out' % (host, cmd)

    stdout = parent_end.recv()
    parent_end.close()

    pat = r'(\S*?) fps'
    list_fps = get_list_by_re_findall(pat, stdout)

    if list_fps:
        for item in list_fps:
            if '25.00' != item:
                assert False, '%s video1 fps != 25.00' % host

        num_fps = len(list_fps)
        if 3 != num_fps:
            assert False, '%s video1 25.00 fps num got %d, expect 3' % (host, num_fps)
    else:
        assert False, '%s video1 got no fps result' % host


if '__main__' == __name__:
    chk_dump_video0('master', 4)
