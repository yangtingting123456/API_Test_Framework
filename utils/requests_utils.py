#requests封装
import requests
from utils.config_utils import local_config
import json
import jsonpath
import re
from utils.check_utils import CheckUtils
from requests.exceptions import RequestException,ProxyError,ConnectionError
from nb_log import LogManager

logger = LogManager('Api_Test_Framework').get_logger_and_add_handlers(is_add_mail_handler=True,log_filename=local_config.LOG_NAME)
class RequestsUtils:
    def __init__(self):
        self.hosts = local_config.HOSTS
        self.session = requests.session()
        self.tmp_variables = {} #将截取的结构存储到该列表中

    '''对get请求进行封装'''
    def __get(self,requests_info):
        try:
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
            logger.info(CheckUtils(response).run_check(requests_info['断言类型'], requests_info['期望结果']))
            print(result)
        except ProxyError as e:
            result = {'code': 3, 'message': '调用接口[%s]时发生Proxy异常，异常原因为%s' % (requests_info['接口名称'], e.__str__()),'check_result': False}
            logger.error('调用接口[%s]时发生Proxy异常，异常原因为:%s' % (requests_info['接口名称'], e.__str__()))
        except ConnectionError as e:
            result = {'code': 3, 'message': '调用接口[%s]时发生Connection异常，异常原因为%s' % (requests_info['接口名称'], e.__str__()),'check_result': False}
            logger.error('调用接口[%s]时发生Connection异常，异常原因为:%s' % (requests_info['接口名称'], e.__str__()))
        except RequestException as e:
            result = {'code': 3, 'message': '调用接口[%s]时发生Request异常，异常原因为%s' % (requests_info['接口名称'], e.__str__()),'check_result': False}
            logger.error('调用接口[%s]时发生Request异常，异常原因为:%s' % (requests_info['接口名称'], e.__str__()))
        except Exception as e:
            result = {'code': 3, 'message': '调用接口[%s]时发异常，异常原因为%s' % (requests_info['接口名称'], e.__str__()), 'check_result': False}
            print(logger.info(result))
        return result

    '''对post请求进行封装'''
    def __post(self,requests_info):
        try:
            url = self.hosts+requests_info['请求地址']
            get_variable_list = re.findall('\\${\w+}', requests_info['请求参数(get)'])
            for variable in get_variable_list:
                requests_info['请求参数(get)'] = requests_info['请求参数(get)'].replace(variable,
                                                                                '"%s"' % self.tmp_variables[variable[2:-1]])
            post_variable_list = re.findall('\\${\w+}', requests_info['请求参数(post)'])
            for variable in post_variable_list:
                requests_info['请求参数(post)'] = requests_info['请求参数(post)'].replace(variable,
                                                                                  '"%s"' % self.tmp_variables[variable[2:-1]])
                print(self.tmp_variables)
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
                logger.warning(requests_info['取值代码'] )
                logger.warning(response.text)
                value = re.findall(requests_info['取值代码'], response.text)[0]
                self.tmp_variables[requests_info['取值变量']] = value
            result = CheckUtils(response).run_check(requests_info['断言类型'], requests_info['期望结果'])
            print(result)
        except ProxyError as e:
            result = {'code': 3, 'message': '调用接口[%s]时发生Proxy异常，异常原因为:%s' % (requests_info['接口名称'], e.__str__()),'check_result': False}
            logger.error('调用接口[%s]时发生Proxy异常，异常原因为%s' % (requests_info['接口名称'], e.__str__()))
        except ConnectionError as e:
            result = {'code': 3, 'message': '调用接口[%s]时发生Connection异常，异常原因为:%s' % (requests_info['接口名称'], e.__str__()),'check_result': False}
            logger.error('调用接口[%s]时发生Connection异常，异常原因为%s' % (requests_info['接口名称'], e.__str__()))
        except RequestException as e:
            result = {'code': 3, 'message': '调用接口[%s]时发生Request异常，异常原因为:%s' % (requests_info['接口名称'], e.__str__()),'check_result': False}
            logger.error('调用接口[%s]时发生Request异常，异常原因为%s' % (requests_info['接口名称'], e.__str__()))
        except Exception as e:
            result = {'code': 3, 'message': '调用接口[%s]时发异常，异常原因为:%s' % (requests_info['接口名称'], e.__str__()),'check_result': False}
            logger.error('调用接口[%s]时发异常，异常原因为%s' % (requests_info['接口名称'], e.__str__()))
        return result

    '''将get请求和post请求封装成私有的方法'''
    def request(self,step_info):
        request_type = step_info['请求方式']
        logger.info('%s 接口开始调用'%step_info['接口名称'])
        if request_type == 'get':
            result = self.__get(step_info)
        elif request_type == 'post':
            result = self.__post(step_info)
        else:
            result = {'code':2,'message':'请求方式不支持','check_result':False}
            logger.error('%s 调用时 %s' % (step_info['接口名称'],result['message']))
        logger.info('%s 接口调用结束' % step_info['接口名称'])
        return result

    '''批量处理测试用例'''
    def request_by_step(self,test_steps):
        for test_step in test_steps:
            result = self.request(test_step)
            if result['code'] != 0:
                break
        return result

if __name__ == '__main__':
   stetlist = [
       {'测试用例编号': 'api_case_03', '测试用例名称': '删除标签接口测试', '用例执行': '是', '用例步骤': 'step_01', '接口名称': '获取access_token接口', '请求方式': 'get', '请求头部信息': '', '请求地址': '/cgi-bin/token', '请求参数(get)': '{"grant_type":"client_credential","appid":"wxf26ad2ae7497289a","secret":"177931a321a1f39a47a1ef202d8a3497"}', '请求参数(post)': '', '取值方式': 'jsonpath取值', '取值代码': '$.access_token', '取值变量': 'token', '断言类型': 'json_key', '期望结果': 'access_token'},
       {'测试用例编号': 'api_case_03', '测试用例名称': '删除标签接口测试', '用例执行': '是', '用例步骤': 'step_02', '接口名称': '创建标签接口', '请求方式': 'post', '请求头部信息': '', '请求地址': '/cgi-bin/tags/create', '请求参数(get)': '{"access_token":${token}}', '请求参数(post)': '{"tag" : {"name" : "asdfa2345234534" } } ', '取值方式': '正则取值', '取值代码': '"id":(.+?),', '取值变量': 'tag_id', '断言类型': 'json_key', '期望结果': 'tag'},
       {'测试用例编号': 'api_case_03', '测试用例名称': '删除标签接口测试', '用例执行': '是', '用例步骤': 'step_03', '接口名称': '删除标签接口', '请求方式': 'post', '请求头部信息': '', '请求地址': '/cgi-bin/tags/delete', '请求参数(get)': '{"access_token":${token}}', '请求参数(post)': '{"tag":{ "id":${tag_id}}}', '取值方式': '无', '取值代码': '', '取值变量': '', '断言类型': 'json_key_value', '期望结果': '{"errcode":0}'}
   ]
   stetlist1= [
       {'测试用例编号': 'api_case_03', '测试用例名称': '删除标签接口测试', '用例执行': '是', '用例步骤': 'step_01', '接口名称': '获取access_token接口', '请求方式': 'get', '请求头部信息': '', '请求地址': '/cgi-bin/token', '请求参数(get)': '{"grant_type":"client_credential","appid":"wxf26ad2ae7497289a","secret":"177931a321a1f39a47a1ef202d8a3497"}', '请求参数(post)': '', '取值方式': 'jsonpath取值', '取值代码': '$.access_token', '取值变量': 'token', '断言类型': 'json_key', '期望结果': 'access_token'},
       {'测试用例编号': 'api_case_03', '测试用例名称': '删除标签接口测试', '用例执行': '是', '用例步骤': 'step_02', '接口名称': '创建标签接口', '请求方式': 'post', '请求头部信息': '', '请求地址': '/cgi-bin/tags/create', '请求参数(get)': '{"access_token":${token}}', '请求参数(post)': '{"tag" : {"name" : "345sgfd" } } ', '取值方式': '正则取值', '取值代码': '"id":(.+?),', '取值变量': 'tag_id', '断言类型': 'json_key', '期望结果': 'tag'},
       {'测试用例编号': 'api_case_03', '测试用例名称': '删除标签接口测试', '用例执行': '是', '用例步骤': 'step_03', '接口名称': '删除标签接口', '请求方式': 'post', '请求头部信息': '', '请求地址': '/cgi-bin/tags/delete', '请求参数(get)': '{"access_token":${token}}', '请求参数(post)': '{"tag":{ "id":${tag_id}}}', '取值方式': '无', '取值代码': '', '取值变量': '', '断言类型': 'json_key_value', '期望结果': '{"errcode":0}'}
   ]


   step_list1=[
    {'测试用例编号': 'api_case_02', '测试用例名称': '创建标签接口测试', '用例执行': '是', '用例步骤': 'step_01', '接口名称': '获取access_token接口', '请求方式': 'get', '请求头部信息': '', '请求地址': '/cgi-bin/token', '请求参数(get)': '{"grant_type":"client_credential","appid":"wxf26ad2ae7497289a","secret":"177931a321a1f39a47a1ef202d8a3497"}', '请求参数(post)': '', '取值方式': '正则取值', '取值代码': '"access_token":"(.+?)"', '取值变量': 'token', '断言类型': 'json_key_value', '期望结果': '{"expires_in":7200}'},
    {'测试用例编号': 'api_case_02', '测试用例名称': '创建标签接口测试', '用例执行': '是', '用例步骤': 'step_02', '接口名称': '创建标签接口测试', '请求方式': 'post', '请求头部信息': '', '请求地址': '/cgi-bin/tags/create', '请求参数(get)': '{"access_token":${token}}', '请求参数(post)': '{"tag":{"name" :"aa1231231"}}', '取值方式': '无', '取值代码': '', '取值变量': '', '断言类型': 'json_key', '期望结果': 'tag'}
   ]
   step_list3 =[
       {'测试用例编号': 'api_case_03', '测试用例名称': '删除标签接口', '用例执行': '是', '用例步骤': 'step_id_01', '接口名称': '获取access_token接口测试', '请求方式': 'get', '请求头部信息': '', '请求地址': '/cgi-bin/token', '请求参数(get)': '{"grant_type":"client_credential","appid":"wxf26ad2ae7497289a","secret":"177931a321a1f39a47a1ef202d8a3497"}', '请求参数(post)': '', '取值方式': 'jsonpath取值', '取值代码': '$.access_token', '取值变量': 'token', '断言类型': 'json_key', '期望结果': 'access_token'},
       {'测试用例编号': 'api_case_03', '测试用例名称': '删除标签接口', '用例执行': '是', '用例步骤': 'step_id_02', '接口名称': '创建标签接口测试', '请求方式': 'post', '请求头部信息': '', '请求地址': '/cgi-bin/tags/create', '请求参数(get)': '{"access_token":${token}}', '请求参数(post)': '{"tag":{"name" :"777gl"}}', '取值方式': '正则取值', '取值代码': '"id":(.+?),', '取值变量': 'tag_id', '断言类型': 'json_key', '期望结果': 'tag'},
       {'测试用例编号': 'api_case_03', '测试用例名称': '删除标签接口', '用例执行': '是', '用例步骤': 'step_id_03', '接口名称': '删除标签接口测试', '请求方式': 'post', '请求头部信息': '', '请求地址': '/cgi-bin/tags/delete', '请求参数(get)': '{"access_token":${token}}', '请求参数(post)': '{"tag":{ "id":${tag_id}}}', '取值方式': '无', '取值代码': '', '取值变量': '', '断言类型': 'json_key_value', '期望结果': '{"errcode":0}'}
                ]

   step_list5=[
       {'测试用例编号': 'api_case_03', '测试用例名称': '删除标签接口', '用例执行': '是', '用例步骤': 'step_01', '接口名称': '获取access_token接口', '请求方式': 'get', '请求头部信息': '', '请求地址': '/cgi-bin/token', '请求参数(get)': '{"grant_type":"client_credential","appid":"wxf26ad2ae7497289a","secret":"177931a321a1f39a47a1ef202d8a3497"}', '请求参数(post)': '', '取值方式': 'jsonpath取值', '取值代码': '$.access_token', '取值变量': 'token', '断言类型': 'json_key', '期望结果': 'access_token'},
       {'测试用例编号': 'api_case_03', '测试用例名称': '删除标签接口', '用例执行': '是', '用例步骤': 'step_02', '接口名称': '创建标签接口', '请求方式': 'post', '请求头部信息': '', '请求地址': '/cgi-bin/tags/create', '请求参数(get)': '{"access_token":${token}}', '请求参数(post)': '{"tag":{"name":"45sdfg"}}', '取值方式': '正则取值', '取值代码': '"id":(.+?),', '取值变量': 'tag_id', '断言类型': 'json_key', '期望结果': 'tag'},
       {'测试用例编号': 'api_case_03', '测试用例名称': '删除标签接口', '用例执行': '是', '用例步骤': 'step_id_03', '接口名称': '删除标签接口测试', '请求方式': 'post', '请求头部信息': '', '请求地址': '/cgi-bin/tags/delete', '请求参数(get)': '{"access_token":${token}}', '请求参数(post)': '{"tag":{ "id":${tag_id}}}', '取值方式': '无', '取值代码': '', '取值变量': '', '断言类型': 'json_key_value', '期望结果': '{"errcode":0}'}
   ]


   requestsUtils = RequestsUtils()
   v=requestsUtils.request_by_step( step_list5)
   print( v )

