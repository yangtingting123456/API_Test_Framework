# -*- coding: utf-8 -*-
# @Time    : 2021/1/5 18:08
# @Author  : tingting.yang
# @FileName: run_all_case.py
import unittest
import os
from utils import HTMLTestReportCN
from utils.config_utils import local_config

current_path = os.path.dirname(__file__)
case_path = os.path.join(current_path,'..','testcases')
report_path = os.path.join(current_path,'..',local_config.REPORT_PATH)

def load_testcase():
    discover = unittest.defaultTestLoader.discover(start_dir=case_path,pattern='test_api_case.py',top_level_dir = case_path)
    all_case_suit = unittest.TestSuite()
    all_case_suit.addTest(discover)
    return all_case_suit

result_dir = HTMLTestReportCN.ReportDirectory(report_path)
result_dir.create_dir('接口框架自动化测试报告_')
report_html_path = HTMLTestReportCN.GlobalMsg.get_value('report_path')
report_html_obj = open(report_html_path,'wb')
runner = HTMLTestReportCN.HTMLTestRunner(stream=report_html_obj,
                                         title='接口自动化测试框架报告',
                                         description='数据驱动+关键字驱动',
                                         tester='ytt')
runner.run(load_testcase())
report_html_obj.close()
