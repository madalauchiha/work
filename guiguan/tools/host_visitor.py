#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import paramiko
# import logging
import subprocess
# from common.record_time_log import logger
from ftplib import FTP


def check_eth_conn(cls):
    def wrapper(*args, **kwargs):
        if 'hostip' not in kwargs:
            kwargs['hostip'] = '192.168.100.99'

        try:
            subprocess.check_output(['ping', '-c', '1', '-w', '1', kwargs['hostip']])
        except subprocess.CalledProcessError:
            # logging.error('\neth connection to %s not established!' % kwargs['hostip'])
            print('\neth connection to %s not established!' % kwargs['hostip'])
            sys.exit(1)

        return cls(*args, **kwargs)
    return wrapper


@check_eth_conn
class HostVisitor(object):
    def __init__(self, hostip=r'192.168.100.99', port=22, usrname=r'worker', passwd=r'uisee'):
        self._hostip = hostip
        self._port = port
        self._usrname = usrname
        self._passwd = passwd
        self._ssh = self._establish_ssh()
        self._sftp = self._establish_sftp()

    def _establish_ssh(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            ssh.connect(hostname=self._hostip, port=self._port,
                        username=self._usrname, password=self._passwd)
        except Exception as e:
            # logging.warning('ssh connect fail: %s' % e)
            print('ssh connect fail: %s' % e)
            return None
        else:
            return ssh

    def _establish_sftp(self):
        try:
            transport = paramiko.Transport((self._hostip, self._port))
            transport.connect(username=self._usrname, password=self._passwd)
            sftp = paramiko.SFTPClient.from_transport(transport)
        except Exception as e:
            # logging.warning('transport connect fail: %s' % e)
            print('transport connect fail: %s' % e)
            return None
        else:
            return sftp

    def _check_remote_dir(self, remote_dir):
        try:
            self._sftp.chdir(remote_dir)
        except IOError:
            self._check_remote_dir(os.path.dirname(remote_dir))
            self._sftp.mkdir(remote_dir)
            print('\ndes_dir "{}" doesn\'t exist, create it.'.format(remote_dir))

    def reconnect(self):
        self.close_conn()

        self._ssh = self._establish_ssh()
        self._sftp = self._establish_sftp()

        if not self._ssh or not self._sftp:
            return False

        return self._ssh.get_transport().is_active()

    def exec_cmd(self, cmd):
        prompt = self._usrname + '@' + self._hostip + ':$ '
        # logger.info(prompt + cmd)

        try:
            stdin, stdout, stderr = self._ssh.exec_command(cmd)
        except Exception as e:
            print('ssh exec command fail: %s' % e)
            # logging.warning('ssh exec command fail: %s' % e)
        else:
            bytes_stdout = stdout.read()
            bytes_stderr = stderr.read()

            try:
                str_stdout = bytes.decode(bytes_stdout)
                str_stderr = bytes.decode(bytes_stderr)
            except UnicodeDecodeError:
                # logger.info(bytes_stdout + bytes_stderr)
                return bytes_stdout + bytes_stderr
            else:
                # logger.info(str_stdout.rstrip('\n') + str_stderr)
                return str_stdout + str_stderr

    def get_stat(self, path):
        return self._sftp.stat(path)

    def ls_dir(self, dir):
        list_dir = self._sftp.listdir(dir)
        print(list_dir)
        return list_dir

    def rm_file(self, fpath):
        try:
            self._sftp.remove(fpath)
        except FileNotFoundError:
            pass

    def rm_dir(self, dir):
        for f in self._sftp.listdir(dir):
            file_path = os.path.join(dir, f)
            try:
                self._sftp.remove(file_path)
            except IOError:
                self.rm_dir(file_path)

        self._sftp.rmdir(dir)

        print(dir + ' remove ok.')

    def download(self, srcpath, dstpath):
        try:
            print('copying: %s => %s ...' % (srcpath, dstpath))
            self._sftp.get(srcpath, dstpath)
        except Exception as e:
            # logging.warning('file [{}] download fail: {}'.format(os.path.basename(srcpath), e))
            return False
        else:
            print('\nfile copied successfully.\n')
            return True

    def upload(self, srcpath, dstpath):
        print('\nsrc_path: "{}"'.format(srcpath))
        print('des_path: "{}"'.format(dstpath))

        filecnt = 0

        if os.path.isfile(srcpath):
            self._check_remote_dir(dstpath)

            desfile = os.path.join(dstpath, os.path.basename(srcpath))
            try:
                filecnt += 1
                print('copying: %s => %s ...' % (srcpath, desfile))
                self._sftp.put(srcpath, desfile)
            except Exception as e:
                # logging.warning('file upload fail: %s' % e)
                return False
            else:
                print('\nfile copied successfully.\n')
                return True
        else:
            try:
                for (root, dirs, files) in os.walk(srcpath):
                    desdir = root.replace(srcpath, dstpath)

                    self._check_remote_dir(desdir)

                    for file in files:
                        srcfile = os.path.join(root, file)
                        desfile = os.path.join(desdir, file)
                        filecnt += 1
                        print('copying: %s => %s ...' % (srcfile, desfile))
                        self._sftp.put(srcfile, desfile)
            except Exception as e:
                # logging.warning('files upload fail: %s' % e)
                return False
            else:
                print('\n' + str(filecnt) + ' files copied successfully.')
                return True

    def close_conn(self):

        if self._sftp:
            try:
                self._sftp.close()
            except EOFError:
                pass
        if self._ssh:
            self._ssh.close()


@check_eth_conn
class FtpHandler(object):
    def __init__(self, hostip=r'10.0.89.16', port=21, usrname=r'uisee', passwd=r'uisee123'):
        self._hostip = hostip
        self._port = port
        self._usrname = usrname
        self._passwd = passwd
        self._ftp = self._establish_ftp()

    def _establish_ftp(self):
        ftp = FTP()

        try:
            ftp.connect(self._hostip, self._port, timeout=30)
            ftp.login(self._usrname, self._passwd)
        except Exception as e:
            # logging.warning('ftp connect fail: %s' % e)
            return None
        else:
            print(ftp.getwelcome())
            return ftp

    def ls_dir(self, dir):
        self._ftp.cwd(dir)
        list_dir = self._ftp.nlst()

        print(list_dir)
        return list_dir

    def get_size(self, fpath):
        self._ftp.voidcmd('TYPE I')
        return self._ftp.size(fpath)

    def close(self):
        self._ftp.quit()


if __name__ == '__main__':
    hv = HostVisitor()
    hv._check_remote_dir('/home/worker/uos/data')
