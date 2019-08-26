#!/usr/loacl/bin/env python3
# -*- coding: utf-8 -*-

import os
from common.host_visitor import HostVisitor
from common.comm_paras import MASTER_IP, SLAVE_IP


def exec_cmd_subproc(host, cmd, pipe):
    print('exec_cmd_subproc: name:%s :pid:%s' % (__name__, os.getpid()))

    if 'master' == host:
        stdout = HostVisitor(hostip=MASTER_IP).exec_cmd(cmd)
    else:
        stdout = HostVisitor(hostip=SLAVE_IP).exec_cmd(cmd)

    pipe.send(stdout)
    pipe.close()
