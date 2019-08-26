#!/usr/bin/env python3
# -*- coding: utf-8 -*-

CD = 'cd '
LS = 'ls '
CAT = 'cat '
TOUCH = 'touch '
ECHO = 'echo '
LIST_VER = 'list_version.sh'
CAT_REL = 'cat /etc/uisee_release'
APPLY_OS = 'apply_os.sh -f '
SET_PROD_TYPE = 'set_product_type.sh '
BURN_FPGA = 'burn_fpga.sh -f '
REBOOT = 'ssh slave sudo reboot;sudo reboot > /dev/null 2>&1 &'
IFCONFIG = 'ifconfig'
DF = 'df -hl'
LSMOD = 'lsmod'
MODINFO = 'modinfo '
SSH = 'ssh '
DATE = 'sudo date'
HWCLOCK = 'sudo hwclock -w'
LAUNCH_UOS = './launch_uos.sh > /dev/null 2>&1 &'
STOP_UOS = './stop_uos.sh'
SWITCH_FTP = 'switch_ftp.sh '
BURN_APU = "burn_apu.sh -f "
DEV = " /dev/ttyTHS2"

GET = 'get '

PYTHON = "python3 "

SWITCH_NET = 'switch_net.sh '
PING = 'ping '
LSUSB = 'lsusb'
WGET = 'wget '
ROUTE = 'route -n'
SET_WIFI = 'set_wifi.sh '
OTA = 'ota-client '
APU_INFO = 'cd /home/worker/firmware/APU/host;python3 apu_info.py'

FDISK = 'sudo fdisk -l '
LSBLK = 'lsblk -d -o name,size,rota '
DF = 'df -hl '

KILLALL = "killall"
CV_MAIN = "cd ~/uisee*/run/;source set_env.sh;./bin/uos_cv_framework-main"
CAMERA_MAIN = "cd /uisee*/run/;source set_env.sh;./bin/uos_camera-main"
PS_EF = "ps -ef |grep -v grep|grep {}|awk '{print $2}'"
UPDATA_FPGA = "cd /opt/pcie_v4l2_mono6/util/ ; ./uisee-test /dev/video0 30 0 2 "

UNTAR = 'tar zxf '
UNTAR2 = 'tar xf '

DD_FILE_100M = 'dd if=/dev/zero of=~/iofile bs=1M count=100'

DF_SPACE = "df -m|grep home|awk '{print $4}'"
FALLOCATE = "fallocate -l {}M test.sh"

UPDATE_APU = "cd firmware/APU/host ; ./updata_apu.sh /dev/ttyTHS2 "

# dump video
CONFIG_UB964 = 'config_ub964.sh'
DUMP_VIDEO0 = 'dump_video0.sh -n '
DUMP_VIDEO1 = 'dump_video1.sh -n '
