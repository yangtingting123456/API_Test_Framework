#requests封装
import requests
from utils.config_utils import local_config
import json
import jsonpath
import re
from utils.check_utils import CheckUtils
class RequestsUtils:
    def __init__(self):
        self.hosts = local_config.HOSTS
        self.session = requests.session()
        self.tmp_variables = {} #将截取的结构存储到该列表中

    '''对get请求进行封装'''
    def __get(self,requests_info):
        url = self.hosts+requests_info['请求地址']
        variable_list = re.findall('\\${\w+}', requests_info['请求参数(get)'])
        for v in variable_list:
            requests_info['请求参数(get)'] = requests_info['请求参数(get)'].replace(v,
                                                                            '"%s"' % self.tmp_variables[v[2:-1]])
        response = self.session.get(url = url,
                                    params = json.loads(requests_info['请求参数(get)']),
                                    headers = requests_info['请求头部信息'])
        response.encoding = response.apparent_encoding  #保证不乱吗
        if requests_info['取值方式'] == 'jsonpath取值':
            value = jsonpath.jsonpath(response.json(),requests_info['取值代码'])[0]
            self.tmp_variables[requests_info['取值变量']] = value
        elif requests_info['取值方式'] == '正则取值':
            value = re.findall(requests_info['取值代码'],response.text)[0]
            self.tmp_variables[requests_info['取值变量']] = value
        result = CheckUtils(response).run_check(requests_info['断言类型'],requests_info['期望结果'])
        print(result)
        return result

    '''对post请求进行封装'''
    def __post(self,requests_info):
        url = self.hosts+requests_info['请求地址']
        get_variable_list = re.findall('\\${\w+}', requests_info['请求参数(get)'])
        for variable in get_variable_list:
            requests_info['请求参数(get)'] = requests_info['请求参数(get)'].replace(variable,
                                                                            '"%s"' % self.tmp_variables[variable[2:-1]])
        post_variable_list = re.findall('\\${\w+}', requests_info['请求参数(post)'])
        for variable in post_variable_list:
            requests_info['请求参数(post)'] = requests_info['请求参数(post)'].replace(variable,
                                                                              '"%s"' % self.tmp_variables[variable[2:-1]])
        response = self.session.post(url=url,
                                     headers=requests_info['请求头部信息'],
                                     params=json.loads(requests_info['请求参数(get)']),
                                     data=json.dumps(json.loads(requests_info['请求参数(post)']),
                                                     ensure_ascii=False).encode('utf-8')
                                     # json = json.loads(requests_info['请求参数(post)'])
                                     )
        response.encoding = response.apparent_encoding  #保证不乱吗
        if requests_info['取值方式'] == 'jsonpath取值':
            value = jsonpath.jsonpath(response.json(),requests_info['取值代码'])[0]
            self.tmp_variables[requests_info['取值变量']] = value
        elif requests_info['取值方式'] == '正则取值':
            value = re.findall(requests_info['取值代码'], response.text)[0]
            self.tmp_variables[requests_info['取值变量']] = value
        result = CheckUtils(response).run_check(requests_info['断言类型'], requests_info['期望结果'])
        print(result)
        return result

    '''将get请求和post请求封装成私有的方法'''
    def request(self,step_info):
        request_type = step_info['请求方式']
        if request_type == 'get':
            result = self.__get(step_info)
        elif request_type == 'post':
            result = self.__post(step_info)
        else:
            result = {'code':2,'result':'请求方式不支持'}
        return result

    '''批量处理测试用例'''
    def request_by_step(self,test_steps):
        for test_step in test_steps:
            result = self.request(test_step)
            if result['code'] != 0:
                break
        return result

if __name__ == '__main__':
    step_list1 ={'测试用例编号': 'api_case_03', '测试用例名称': '删除标签接口测试', '用例执行': '否', '用例步骤': 'step_01', '接口名称': '获取access_token接口', '请求方式': 'get', '请求头部信息': '', '请求地址': '/cgi-bin/token', '请求参数(get)': '{"grant_type":"client_credential","appid":"wxf26ad2ae7497289a","secret":"177931a321a1f39a47a1ef202d8a3497"}', '请求参数(post)': '', '取值方式': 'jsonpath取值', '取值代码': '$.access_token', '取值变量': 'token', '断言类型': 'json_key', '期望结果': 'access_token'}
    step_list2 = [
            {'测试用例编号': 'api_case_02', '测试用例名称': '创建标签接口测试', '用例执行': '否', '用例步骤': 'step_01', '接口名称': '获取access_token接口', '请求方式': 'get', '请求头部信息': '', '请求地址': '/cgi-bin/token', '请求参数(get)': '{"grant_type":"client_credential","appid":"wxf26ad2ae7497289a","secret":"177931a321a1f39a47a1ef202d8a3497"}', '请求参数(post)': '', '取值方式': '正则取值', '取值代码': '"access_token":"(.+?)"', '取值变量': 'token', '断言类型': 'json_key_value', '期望结果': '{"expires_in":7200}'},
            {'测试用例编号': 'api_case_02', '测试用例名称': '创建标签接口测试', '用例执行': '否', '用例步骤': 'step_02', '接口名称': '创建标签接口', '请求方式': 'post', '请求头部信息': '', '请求地址': '/cgi-bin/tags/create', '请求参数(get)': '{"access_token":${token}}', '请求参数(post)': '{"tag":{"name" :"fh"}} ', '取值方式': 'body_regexp', '取值代码': '"id":(.+?)', '取值变量': '', '断言类型': 'json_key', '期望结果': 'tag'}
        ]
    step_list3 =  {'测试用例编号': 'api_case_02', '测试用例名称': '创建标签接口测试', '用例执行': '否', '用例步骤': 'step_01', '接口名称': '获取access_token接口', '请求方式': 'get', '请求头部信息': '', '请求地址': '/cgi-bin/token', '请求参数(get)': '{"grant_type":"client_credential","appid":"wxf26ad2ae7497289a","secret":"177931a321a1f39a47a1ef202d8a3497"}', '请求参数(post)': '', '取值方式': 'body_regexp', '取值代码': '"access_token":"(.+?)"', '取值变量': 'token', '断言类型': 'json_key_value', '期望结果': '{"expires_in":7200}'},
    requestsUtils = RequestsUtils()
    requestsUtils.request_by_step(step_list2)

#  step_list2 = {'测试用例编号': 'api_case_02', '测试用例名称': '创建标签接口测试', '用例执行': '否', '用例步骤': 'step_02', '接口名称': '创建标签接口', '请求方式': 'post', '请求头部信息': '', '请求地址': '/cgi-bin/tags/create', '请求参数(get)': '{"access_token":"40_ni-zkk10K0nRlEp7b4J6oPZDvYoSDS9TODX58cO3e6T5ZdE4SZ-PmIBVp6tuDN7-r3RYAcbVqvpUHpTXyBdQtaf7QcO0isGQnFsUL_siHRUFBzNecAL5iUK_alrfoWB66pFLEEmO4SFo6_t_ZZXiACADDB"}', '请求参数(post)': '{   "tag" : {     "name" : "2"} }', '取值方式': '无', '取值代码': '', '取值变量': '', '断言类型': 'json_key', '期望结果': 'tag'}
   #  step_list3 = {'测试用例编号': 'api_case_03', '测试用例名称': '删除标签接口测试', '用例执行': '否', '用例步骤': 'step_03', '接口名称': '删除标签接口', '请求方式': 'post', '请求头部信息': '', '请求地址': '/cgi-bin/tags/delete', '请求参数(get)': '{"access_token":"40_uacNftEXmPlyo4SsYVWAVVA9s0pGCyPUEmNJ45w1f9btMfyThdno8WVTiY3O31v-C1cTW6OMP2nrbIJbEVwv9gqQeH5sl1x8qJqHkxeebdw3wSPgrH6R6lbf-qzU2qVVxHT3NlcnAzw7pvtxZQVaAHAULQ"}', '请求参数(post)': '{   "tag":{        "id" : 100   } } ',
   #                '取值方式': '无', '取值代码': '', '取值变量': '', '断言类型': 'json_key_value', '期望结果': '{"errcode":0}'}
   #  step_list4 = [
   #     {'测试用例编号': 'api_case_02', '测试用例名称': '创建标签接口测试', '用例执行': '否', '用例步骤': 'step_01',
   #                    '接口名称': '获取access_token接口', '请求方式': 'get', '请求头部信息': '', '请求地址': '/cgi-bin/token',
   #                    '请求参数(get)': '{"grant_type":"client_credential","appid":"wxf26ad2ae7497289a","secret":"177931a321a1f39a47a1ef202d8a3497"}',
   #                    '请求参数(post)': '', '取值方式': 'jsonpath取值', '取值代码': '$.access_token', '取值变量': 'token',
   #                    '断言类型': 'json_key_value', '期望结果': '{"expires_in":7200}'},
   #      {'测试用例编号': 'api_case_03', '测试用例名称': '删除标签接口测试', '用例执行': '否', '用例步骤': 'step_03', '接口名称': '删除标签接口',
   #       '请求方式': 'post', '请求头部信息': '', '请求地址': '/cgi-bin/tags/create',
   #       '请求参数(get)': '{"access_token":${token}}',
   #       '请求参数(post)': '{   "tag":{ "id":134, "name":"广东11"   } }  ',
   #       '取值方式': '无', '取值代码': '', '取值变量': '', '断言类型': 'json_key_value', '期望结果': '{"errcode":0}'}
   # ]
   #
   #  requestsUtils =RequestsUtils()
   #  v = requestsUtils.request_by_step(step_list4)
   #  print(v)

   #接口关联测试
   # step_list =[
   #     {'测试用例编号': 'api_case_02', '测试用例名称': '创建标签接口测试', '用例执行': '否', '用例步骤': 'step_01', '接口名称': '获取access_token接口', '请求方式': 'get', '请求头部信息': '', '请求地址': '/cgi-bin/token', '请求参数(get)': '{"grant_type":"client_credential","appid":"wxf26ad2ae7497289a","secret":"177931a321a1f39a47a1ef202d8a3497"}', '请求参数(post)': '', '取值方式': 'jsonpath取值', '取值代码': '$.access_token', '取值变量': 'token', '断言类型': 'json_key_value', '期望结果': '{"expires_in":7200}'},
   #     {'测试用例编号': 'api_case_02', '测试用例名称': '创建标签接口测试', '用例执行': '否', '用例步骤': 'step_02', '接口名称': '创建标签接口', '请求方式': 'post', '请求头部信息': '', '请求地址': '/cgi-bin/tags/create', '请求参数(get)': '{"access_token":${token}}', '请求参数(post)': '{   "tag" : {     "name" : "aa1231231" } } ', '取值方式': '无', '取值代码': '', '取值变量': '', '断言类型': 'json_key', '期望结果': 'tag'}
   # ]

   # step_list = [
   #     {'测试用例编号': 'api_case_03', '测试用例名称': '删除标签接口测试', '用例执行': '是', '用例步骤': 'step_01', '接口名称': '获取access_token接口', '请求方式': 'get', '请求头部信息': '', '请求地址': '/cgi-bin/token', '请求参数(get)': '{"grant_type":"client_credential","appid":"wxf26ad2ae7497289a","secret":"177931a321a1f39a47a1ef202d8a3497"}', '请求参数(post)': '', '取值方式': 'jsonpath取值', '取值代码': '$.access_token', '取值变量': 'token', '断言类型': 'json_key', '期望结果': 'access_token'},
   #     {'测试用例编号': 'api_case_03', '测试用例名称': '删除标签接口测试', '用例执行': '是', '用例步骤': 'step_02', '接口名称': '创建标签接口', '请求方式': 'post', '请求头部信息': '', '请求地址': '/cgi-bin/tags/create', '请求参数(get)': '{"access_token":${token}}', '请求参数(post)': '{"tag" :{"name" :"3456"}} ', '取值方式': '"id":(.+?),', '取值代码': 'tag_id', '取值变量': 'tag_id', '断言类型': 'json_key', '期望结果': ''},
   #     {'测试用例编号': 'api_case_03', '测试用例名称': '删除标签接口测试', '用例执行': '是', '用例步骤': 'step_03', '接口名称': '删除标签接口', '请求方式': 'post', '请求头部信息': '', '请求地址': '/cgi-bin/tags/delete', '请求参数(get)': '{"access_token":${token}}', '请求参数(post)': '{"tag":{"id" : ${tag_id}}}', '取值方式': '无', '取值代码': '', '取值变量': '', '断言类型': 'json_key_value', '期望结果': '{"errcode":0}'}
   # ]
   # step_list = [
   #     {'测试用例编号': 'api_case_3', '测试用例名称': '删除标签接口测试', '用例执行': '是', '用例步骤': 'step_01', '接口名称': '获取access_token接口',
   #      '请求方式': 'get', '请求头部信息': '', '请求地址': '/cgi-bin/token',
   #      '请求参数(get)': '{"grant_type":"client_credential","appid":"wxf26ad2ae7497289a","secret":"177931a321a1f39a47a1ef202d8a3497"}',
   #      '请求参数(post)': '', '取值方式': 'jsonpath取值', '取值代码': '$.access_token', '取值变量': 'token', '断言类型': 'json_key',
   #      '期望结果': 'access_token'},
   #     {'测试用例编号': 'api_case_3', '测试用例名称': '删除标签接口测试', '用例执行': '是', '用例步骤': 'step_02', '接口名称': '创建标签接口', '请求方式': 'post',
   #      '请求头部信息': '', '请求地址': '/cgi-bin/tags/create', '请求参数(get)': '{"access_token":${token}}',
   #      '请求参数(post)': '{"tag":{"name":"yu"}}', '取值方式': 'jsonpath取值', '取值代码': '$.tag.id', '取值变量': 'tag_id',
   #      '断言类型': 'json_key', '期望结果': ''},
   #     {'测试用例编号': 'api_case_3', '测试用例名称': '删除标签接口测试', '用例执行': '是', '用例步骤': 'step_03', '接口名称': '删除标签接口', '请求方式': 'post',
   #      '请求头部信息': '', '请求地址': '/cgi-bin/tags/delete', '请求参数(get)': '{"access_token":${token}}',
   #      '请求参数(post)': '{"tag":{"id":${tag_id}}}', '取值方式': '无', '取值代码': '', '取值变量': '', '断言类型': 'json_key_value',
   #      '期望结果': '{"errcode":0}'}
   # ]
   # step_list = [
   #     {'测试用例编号': 'api_case_02', '测试用例名称': '创建标签接口测试', '用例执行': '否', '用例步骤': 'step_01', '接口名称': '获取access_token接口', '请求方式': 'get', '请求头部信息': '', '请求地址': '/cgi-bin/token', '请求参数(get)': '{"grant_type":"client_credential","appid":"wxf26ad2ae7497289a","secret":"177931a321a1f39a47a1ef202d8a3497"}', '请求参数(post)': '', '取值方式': '正则取值', '取值代码': '"access_token":"(.+?)"', '取值变量': 'token', '断言类型': 'json_key_value', '期望结果': '{"expires_in":7200}'},
   #     {'测试用例编号': 'api_case_02', '测试用例名称': '创建标签接口测试', '用例执行': '否', '用例步骤': 'step_02', '接口名称': '创建标签接口', '请求方式': 'post', '请求头部信息': '', '请求地址': '/cgi-bin/tags/create', '请求参数(get)': '{"access_token":${token}}', '请求参数(post)': '{"tag":{"name" :"sgs2435"}} ', '取值方式': '无', '取值代码': '', '取值变量': '', '断言类型': 'json_key', '期望结果': 'tag'}
   # ]
   # step_list = [
   #     {'测试用例编号': 'api_case_03', '测试用例名称': '删除标签接口测试', '用例执行': '否', '用例步骤': 'step_01', '接口名称': '获取access_token接口', '请求方式': 'get', '请求头部信息': '', '请求地址': '/cgi-bin/token', '请求参数(get)': '{"grant_type":"client_credential","appid":"wxf26ad2ae7497289a","secret":"177931a321a1f39a47a1ef202d8a3497"}', '请求参数(post)': '', '取值方式': 'jsonpath取值', '取值代码': '$.access_token', '取值变量': 'token', '断言类型': 'json_key', '期望结果': 'access_token'},
   #     {'测试用例编号': 'api_case_03', '测试用例名称': '删除标签接口测试', '用例执行': '否', '用例步骤': 'step_02', '接口名称': '创建标签接口', '请求方式': 'post', '请求头部信息': '', '请求地址': '/cgi-bin/tags/create', '请求参数(get)': '{"access_token":${token}}', '请求参数(post)': '{"tag" : {"name" : "45435" } } ', '取值方式': '正则取值', '取值代码': '"id":(.+?),', '取值变量': 'tag_id', '断言类型': 'json_key', '期望结果': ''},
   #     {'测试用例编号': 'api_case_03', '测试用例名称': '删除标签接口测试', '用例执行': '否', '用例步骤': 'step_03', '接口名称': '删除标签接口', '请求方式': 'post', '请求头部信息': '', '请求地址': '/cgi-bin/tags/delete', '请求参数(get)': '{"access_token":${token}}', '请求参数(post)': '{   "tag":{        "id" : ${tag_id}   } }', '取值方式': '无', '取值代码': '', '取值变量': '', '断言类型': 'json_key_value', '期望结果': '{"errcode":0}'}
   # ]
   # requestsUtils = RequestsUtils()
   # v=requestsUtils.request_by_step( step_list1 )
   # print( v )

