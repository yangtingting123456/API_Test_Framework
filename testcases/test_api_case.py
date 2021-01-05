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
        test_result = RequestsUtils().request_by_step(self.case_step)
        self.assertTrue(test_result['check_result'])

if __name__ == '__main__':
    unittest.main(verbosity=2)
