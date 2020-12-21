#requests封装
import requests
from utils.config_utils import local_config
import json
import jsonpath
import re
class RequestsUtils:
    def __init__(self):
        self.hosts = local_config.HOSTS
        self.session = requests.session()
        self.tmp_variables = {}

    def __get(self,requests_info):
        url = self.hosts+requests_info['请求地址']
        variable_list = re.findall('\\${\w+}', requests_info['请求参数(get)'])
        for variable in variable_list:
            requests_info['请求参数(get)'] = requests_info['请求参数(get)'].replace(variable,
                                                                            '"%s"' % self.tmp_variables[variable[2:-1]])
        response = self.session.get(url = url,
                                    params = json.loads(requests_info['请求参数(get)']),
                                    headers = requests_info['请求头部信息'])
        response.encoding = response.apparent_encoding  #保证不乱吗
        if requests_info['取值方式'] == 'jsonpath取值':
            value = jsonpath.jsonpath(response.json(),requests_info['取值代码'])[0]
            self.tmp_variables[requests_info['取值变量']] = value
        result = {
            'code':0,
            'response_code':response.status_code,
            'response_reason':response.reason,
            'response_headers':response.headers,
            'response_body':response.text
        }
        return result

    def __post(self,requests_info):
        url = self.hosts+requests_info['请求地址']
        variable_list = re.findall('\\${\w+}', requests_info['请求参数(get)'])
        for variable in variable_list:
            requests_info['请求参数(get)'] = requests_info['请求参数(get)'].replace(variable,
                                                                            '"%s"' % self.tmp_variables[variable[2:-1]])
        response = self.session.post(url = url,
                                     params = json.loads(requests_info['请求参数(get)']),
                                     json = json.dumps(requests_info['请求参数(post)']),
                                     headers = requests_info['请求头部信息'])
        response.encoding = response.apparent_encoding  #保证不乱吗
        if requests_info['取值方式'] == 'jsonpath取值':
            value = jsonpath.jsonpath(response.json(),requests_info['取值代码'])[0]
            self.tmp_variables[requests_info['取值变量']] = value

        result = {
            'code':0,
            'response_code':response.status_code,
            'response_reason':response.reason,
            'response_headers':response.headers,
            'response_body':response.text,
            'response':response
        }
        return result

    def request(self,step_info):
        request_type = step_info['请求方式']
        if request_type == 'get':
            result = self.__get(step_info)
        elif request_type == 'post':
            result = self.__post(step_info)
        else:
            result = {'code':1,'result':'请求方式不支持'}
        print(self.tmp_variables)
        return result

    def request_by_step(self,test_steps):
        for test_step in test_steps:
            result = self.request(test_step)
            if result['code'] != 0:
                break
        return result

if __name__ == '__main__':
   # step_list = [{'测试用例编号': 'api_case_02', '测试用例名称': '测试能否创建标签接口测试', '用例执行': '是', '用例步骤': 'step01',
   #               '接口名称': '获取access_token接口', '请求方式': 'get', '请求头部信息': '', '请求地址': '/cgi-bin/token',
   #               '请求参数（get）': '{"grant_type":"client_credential","appid":"wxf26ad2ae7497289a","secret":"177931a321a1f39a47a1ef202d8a3497"}', '请求参数（post）': ''}, {'测试用例编号': 'api_case_02', '测试用例名称': '测试能否创建标签接口测试', '用例执行': '是', '用例步骤': 'step02', '接口名称': '创建标签接口', '请求方式': 'post', '请求头部信息': '', '请求地址': 'cgi-bin/tags/create', '请求参数（get）':
   #           '{"access_token":"$access_token"}', '请求参数（post）': '{   "tag" : {     "name" : "广东"//标签名   } } '}]
   # requestsUtils =RequestsUtils()
   # v = requestsUtils.request_by_step(step_list)
   # print(v)
    step_list1 ={'测试用例编号': 'api_case_02', '测试用例名称': '创建标签接口测试', '用例执行': '否', '用例步骤': 'step_01', '接口名称': '获取access_token接口', '请求方式': 'get', '请求头部信息': '', '请求地址': '/cgi-bin/token', '请求参数(get)': '{"grant_type":"client_credential","appid":"wx55614004f367f8ca","secret":"65515b46dd758dfdb09420bb7db2c67f"}', '请求参数(post)': '', '取值方式': '正则取值', '取值代码': '"access_token":"(.+?)"', '取值变量': 'token', '断言类型': 'json_key_value', '期望结果': '{"expires_in":7200}'}
    step_list2 = {'测试用例编号': 'api_case_02', '测试用例名称': '创建标签接口测试', '用例执行': '否', '用例步骤': 'step_02', '接口名称': '创建标签接口', '请求方式': 'post', '请求头部信息': '', '请求地址': '/cgi-bin/tags/create', '请求参数(get)': '{"access_token":"40_86J6fB6om3uNj_S-EqISPwK4pR_n9FeE48KvOkLWf4DtcD2JA8hqfEbrb3nwy-XfFHD8JtA3s6zqtzfnHfq6QWwc1k99yPthnNkqQ2wDa-riYVKXBdVHdZOfmsIeGxsXkcyzTTs5bvb-D0E8WVWbADAHGH"}', '请求参数(post)': '{   "tag" : {     "name" : "bb"} }', '取值方式': '无', '取值代码': '', '取值变量': '', '断言类型': 'json_key', '期望结果': 'tag'}
    step_list3 = {'测试用例编号': 'api_case_03', '测试用例名称': '删除标签接口测试', '用例执行': '否', '用例步骤': 'step_03', '接口名称': '删除标签接口', '请求方式': 'post', '请求头部信息': '', '请求地址': '/cgi-bin/tags/delete', '请求参数(get)': '{"access_token":"40_86J6fB6om3uNj_S-EqISPwK4pR_n9FeE48KvOkLWf4DtcD2JA8hqfEbrb3nwy-XfFHD8JtA3s6zqtzfnHfq6QWwc1k99yPthnNkqQ2wDa-riYVKXBdVHdZOfmsIeGxsXkcyzTTs5bvb-D0E8WVWbADAHGH"}', '请求参数(post)': '{   "tag":{"id" : 766} }', '取值方式': '无', '取值代码': '', '取值变量': '', '断言类型': 'json_key_value', '期望结果': '{"errcode":0}'}
    step_list4 =  [
        {'测试用例编号': 'api_case_02', '测试用例名称': '创建标签接口测试', '用例执行': '是', '用例步骤': 'step_01', '接口名称': '获取access_token接口', '请求方式': 'get', '请求头部信息': '', '请求地址': '/cgi-bin/token', '请求参数(get)': '{"grant_type":"client_credential","appid":"wx55614004f367f8ca","secret":"65515b46dd758dfdb09420bb7db2c67f"}', '请求参数(post)': '', '取值方式': 'jsonpath取值', '取值代码': '$.access_token', '取值变量': 'token'},
        {'测试用例编号': 'api_case_02', '测试用例名称': '创建标签接口测试', '用例执行': '是', '用例步骤': 'step_02', '接口名称': '创建标签接口', '请求方式': 'post', '请求头部信息': '', '请求地址': '/cgi-bin/tags/create', '请求参数(get)': '{"access_token":${token}}', '请求参数(post)': '{   "tag" : {     "name" : "56789" } } ', '取值方式': '无', '取值代码': '', '取值变量': ''}
                   ]

    requestsUtils =RequestsUtils()
    v = requestsUtils.request_by_step(step_list4)
    print(v)

