from utils.excel_utls import ExcelUtils
import os

excel_file_path = os.path.join(os.path.dirname(__file__), '..','data','testcase_datas.xlsx')
sheet_name = 'testcase01'

class TestcaseDataUtils:
    def __init__(self):
        self.excel_data = ExcelUtils(excel_file_path=excel_file_path,sheet_name=sheet_name)

    def conver_testcase_data_to_dict(self):
        '''数据类型转换成字典'''
        testcase_dict = {}
        for row_data in self.excel_data.get_all_data_by_dict():
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
