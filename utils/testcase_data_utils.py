from utils.excel_utls import ExcelUtils
from utils.mysql_utils import MysqlUtils
import os

excel_file_path = os.path.join(os.path.dirname(__file__), '..','data','testcase_infos.xlsx')
sheet_name = 'Sheet1'

class TestcaseDataUtils:
    def __init__(self):
        # self.excel_data = ExcelUtils(excel_file_path=excel_file_path,sheet_name=sheet_name)
        self.test_data_obj = MysqlUtils()

    def conver_testcase_data_to_dict(self):
        '''数据类型转换成字典'''
        testcase_dict = {}
        for row_data in self.test_data_obj.get_all_data():
            if row_data['用例执行'] == '是':
               testcase_dict.setdefault(row_data['测试用例编号'], []).append(row_data)
        return testcase_dict

    def conver_testcase_data_to_list(self):
        '''把conver_testcase_data_to_dict产生的数据转换成列表并在每个元素中增加key'''
        all_casedata_list=[]
        for key,value in self.conver_testcase_data_to_dict().items():
            b_dict = {}
            b_dict['case_id'] = key
            b_dict['case_step'] = value
            all_casedata_list.append(b_dict)
        return all_casedata_list

if __name__ == '__main__':
    testcaseDateUtils = TestcaseDataUtils()
    #测试conver_testcase_data_to_dict的方法
    # test_case_dicts = testcaseDateUtils.conver_testcase_data_to_dict()
    test_case_lists = testcaseDateUtils.conver_testcase_data_to_list()
    # for testcase in test_case_dicts['api_case_03']:
    #     print(testcase)
    for t in test_case_lists:
        print(t)
    # print(test_case_lists[2]['case_step'][2]['请求参数(post)'])
    # print(test_case_lists[0]['case_step'][0]['请求参数(get)'])