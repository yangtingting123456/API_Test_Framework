# -*- coding: utf-8 -*-
# @Time    : 2021/1/6 17:22
# @Author  : tingting.yang
# @FileName: demo_01.py

from nb_log import LogManager
logger = LogManager('lalala').get_logger_and_add_handlers(is_add_mail_handler=True,log_filename='ha.log')
logger.info('绿色')


