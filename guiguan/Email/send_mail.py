#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from common.manip_cfg_file import get_mail_cfg
import os
import time
from common.comm_paras import CASE_XLS_PATH


def mail_report(report_path):
    curdir = os.path.dirname(os.path.realpath(__file__))
    cfgpath = os.path.join(os.path.dirname(curdir), 'configs', 'config.ini')
    # print(cfgdir)

    dict_mail_info = get_mail_cfg(cfgpath)
    sender = dict_mail_info['sender']
    receivers = dict_mail_info['receivers'].split(',')
    smtpserver = dict_mail_info['smtpserver']
    username = dict_mail_info['username']
    password = dict_mail_info['password']

    timefmt = '%Y-%m-%d %X'
    curtime = time.strftime(timefmt, time.localtime())
    # print(curtime)
    mail_title = 'Test Report ' + '[' + curtime + ']'
    # print(mail_title)

    f = open(report_path, 'rb')
    mail_body = f.read()
    f.close()

    str_receivers = ','.join(receivers)
    msg = MIMEMultipart()
    # msg = MIMEText(mail_body, 'html', 'utf-8')
    msg['From'] = sender
    msg['To'] = str_receivers
    msg['Subject'] = Header(mail_title, 'utf-8')

    part = MIMEText(mail_body, 'html', 'utf-8')
    msg.attach(part)

    part = MIMEApplication(open(report_path, 'rb').read())
    part.add_header('Content-Disposition', 'attachment', filename="report.html")
    msg.attach(part)

    part = MIMEApplication(open(CASE_XLS_PATH, 'rb').read())
    part.add_header('Content-Disposition', 'attachment', filename="case.xlsx")
    msg.attach(part)

    try:
        smtp = smtplib.SMTP()
        smtp.connect(smtpserver)
        smtp.login(username, password)
        smtp.sendmail(sender, receivers, msg.as_string())
        print("mail send ok")
        smtp.quit()
    except smtplib.SMTPException:
        print("mail send fail")


if __name__ == '__main__':
    mail_report('../report/report.html')
