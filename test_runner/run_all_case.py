# -*- coding: utf-8 -*-
# @Time    : 2021/1/5 18:08
# @Author  : tingting.yang
# @FileName: run_all_case.py
import unittest
import shutil
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__),'..'))
from utils import HTMLTestReportCN
from utils.config_utils import local_config
from nb_log import LogManager
from utils.email_utils import EmailUtils

logger = LogManager('Api_Test_Framework').get_logger_and_add_handlers(is_add_mail_handler=True,log_filename=local_config.LOG_NAME)
current_path = os.path.dirname(__file__)
case_path = os.path.join(current_path,'..','testcases')
report_path = os.path.join(current_path,'..',local_config.REPORT_PATH)

def load_testcase():
    logger.info('加载接口测试用例')
    discover = unittest.defaultTestLoader.discover(start_dir=case_path,pattern='test_api_case.py',top_level_dir = case_path)
    all_case_suit = unittest.TestSuite()
    all_case_suit.addTest(discover)
    return all_case_suit

result_dir = HTMLTestReportCN.ReportDirectory(report_path)
result_dir.create_dir('interfacereport_')
report_html_path = HTMLTestReportCN.GlobalMsg.get_value('report_path')
logger.info(report_html_path)
report_html_obj = open(report_html_path,'wb')
runner = HTMLTestReportCN.HTMLTestRunner(stream=report_html_obj,
                                         title='interfacereport',
                                         description='数据驱动+关键字驱动',
                                         tester='yangtingting')
logger.info('接口自动化开始执行')
runner.run(load_testcase())
report_html_obj.close()
# EmailUtils('微信公众号接口测试报告',report_html_path).send_mail()
# os.system('copy %s %s/接口自动化测试报告.html /e'
#           %(report_html_path,sys.argv[1]))
shutil.copyfile(report_html_path,'%s/接口自动化测试报告.html'%sys.argv[1])
