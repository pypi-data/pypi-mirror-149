#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   log.py
@Time    :   2022/05/05 14:43:43
@Author  :   xy.xu
@Version :   1.0
@Contact :   xy.xu@shunwang.com
@Desc    :   None
'''


import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler

from sw_ops_common.config import settings


_logger = logging.getLogger('swomc')

debug = _logger.debug
info = _logger.info
warning = _logger.warning
warn = _logger.warn
error = _logger.error
critical = _logger.critical
log = _logger.log
exception = _logger.exception

DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL


LOG_FORMAT = '{"@timestamp":"%(asctime)s" ,"name":"%(name)s","levelname":"%(levelname)s","file_name":"%(filename)s",' \
                     '"threadName":"%(threadName)s","processName":"%(processName)s","lineno":"%(lineno)d", "msg":"%(message)s"}'


def init_log(rotate_type='time', **kwargs):
    if rotate_type == 'time':
        init_time_rotate_log(**kwargs)
    else:
        init_rotate_log(**kwargs)


def init_time_rotate_log(**kwargs):
    root_logger = logging.getLogger()
    logger_handler = TimedRotatingFileHandler(
        filename=kwargs.get('filename') or settings.LOG_FILENAME,
        when='midnight',
        interval=1,
        backupCount=settings.LOG_BACKUP_COUNT or 30,
        encoding='utf-8')
    formatter = logging.Formatter(LOG_FORMAT)
    logger_handler.setLevel(INFO)
    logger_handler.setFormatter(formatter)
    root_logger.addHandler(logger_handler)
    root_logger.setLevel(INFO)


def init_rotate_log(**kwargs):
    root_logger = logging.getLogger()
    logger_handler = RotatingFileHandler(
        filename=kwargs.get('filename') or settings.LOG_FILENAME,
        maxBytes=settings.LOG_SIZE or 1024 * 1024 * 500,
        backupCount=settings.LOG_BACKUP_COUNT or 5,
        encoding='utf-8')
    formatter = logging.Formatter(LOG_FORMAT)
    logger_handler.setLevel(INFO)
    logger_handler.setFormatter(formatter)
    root_logger.addHandler(logger_handler)
    root_logger.setLevel(INFO)


if __name__ == "__main__":
    init_log()
    info('hello world')
    error('good bye')