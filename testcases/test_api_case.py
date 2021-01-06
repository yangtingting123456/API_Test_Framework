# -*- coding: utf-8 -*-
# @Time    : 2021/1/4 17:51
# @Author  : tingting.yang
# @FileName: test_api_case.py
import os
import paramunittest
import unittest
from  utils.testcase_data_utils import TestcaseDataUtils
from utils.requests_utils import RequestsUtils
import warnings
from nb_log import LogManager

logger = LogManager('Api_Test_Framework').get_logger_and_add_handlers(is_add_mail_handler=True,log_filename='Api_Test_Framework.log')
current_path = os.path.dirname(__file__)
test_case_lists = TestcaseDataUtils().conver_testcase_data_to_list()
@paramunittest.parametrized(
    *test_case_lists
)

class TestApiCase(paramunittest.ParametrizedTestCase):
    def setUp(self) -> None:
        warnings.simplefilter('ignore',ResourceWarning)
    def setParameters(self, case_id, case_step):
        self.case_id = case_id
        self.case_step = case_step

    def test_api_case(self):
        logger.info('测试用例编号：%s开始执行'%self.case_step[0].get('测试用例编号'))
        self._testMethodName = self.case_step[0].get('测试用例编号')
        self._testMethodDoc = self.case_step[0].get('测试用例名称')
        test_result = RequestsUtils().request_by_step(self.case_step)
        logger.info('测试用例编号：%s开始结束' % self.case_step[0].get('测试用例编号'))
        self.assertTrue(test_result['check_result'],test_result['message'])

if __name__ == '__main__':
    unittest.main(verbosity=2)
