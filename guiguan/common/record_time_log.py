'''
The log configuration

1. Configure log output format; Time - loglevel - file - func - line - MSG

2. Support output to log file and screen

3. Return a logger for other modules to call
'''


import time
import logging
import os


def make_log():
    root_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    log_dir = os.path.join(root_dir, 'log')
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)

    today = time.strftime("%Y%m%d%H%M%S",time.localtime(time.time()))

    # today = time.strftime("%Y%m%d%H%M%S",time.localtime(time.time()))
    # logpath = os.path.join(curdir, 'log',r'{}.log'.format(today))

    logpath = os.path.join(root_dir, 'log',r'{}.log'.format(today))

    log_file = r"{}".format(logpath)

    return log_file


def get_logger():
    file_path = make_log()

    # create logger
    logger = logging.getLogger('changqing')
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter
    fh = logging.FileHandler(file_path,mode="a",encoding="utf-8")
    fh.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")

    # add formatter to ch
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    # add ch to logger
    if not logger.handlers:
        logger.addHandler(ch)
        logger.addHandler(fh)

    return logger


logger = get_logger()

if __name__ == "__main__":
    l = get_logger("/home/litao/project/changqing/log")
    l.info("sd")
    l.debug("sdsd")
    l.error("sdsd")
