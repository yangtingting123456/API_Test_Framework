# -*- coding: utf-8 -*-
# @Time    : 2020/12/29 16:44
# @Author  : tingting.yang
# @FileName: check.py
import requests
import json
import re
from nb_log import LogManager

logger = LogManager('Api_Test_Framework').get_logger_and_add_handlers(is_add_mail_handler=True,log_filename='Api_Test_Framework.log')

class CheckUtils:
    def __init__(self,response_data):
        self.response_data = response_data
        self.check_rules = {
            "none" :  self.none_check,
            "json_key" : self.body_key_check,
            "json_key_value" : self.body_key_value_check,
            "body_regexp" : self.regexp_check,
            "header_key":self.header_key_check,
            "header_key_value":self.header_key_value_check,
            'message':'',
            "response_code": self.response_code_check
        }
        self.pass_result  = {
            'code':0,
            'response_code' : self.response_data.status_code,
            'response_reason' : self.response_data.reason,
            'response_headers' : self.response_data.headers,
            'response_body' : self.response_data.text,
            'response_data': self.response_data.url,
            'response' : self.response_data,
            'message':'',
            'check_result': True
        }
        self.fail_result = {
            'code':1,
            'response_code' : self.response_data.status_code,
            'response_reason' : self.response_data.reason,
            'response_headers' : self.response_data.headers,
            'response_body' : self.response_data.text,
            'response_data':self.response_data.url,
            'response' : self.response_data,
            'check_result': False
        }

    ''' nono断言'''
    def none_check(self):
        logger.info('断言类型为无或期望结果无数据，检测通过')
        return self.pass_result

    '''针对接口的json字符串的key进行断言'''
    def __key_check(self,actual_result,check_data):
        key_list = check_data.split(',')
        tmp_result = []
        for key in key_list:
            if key in actual_result.keys():
                tmp_result.append(self.pass_result)
            else:
                tmp_result.append(self.fail_result)
            if self.fail_result in tmp_result:
                 logger.error('断言失败，失败原因%s' % self.fail_result)
                 logger.info('测试实际通过：%s === 测试期望结果：%s 不一致，检测失败'%(json.dumps(actual_result,ensure_ascii=False),check_data))
                 return self.fail_result
            else:
                logger.info('测试实际通过：%s === 测试期望结果：%s 一致，检测通过'%(json.dumps(actual_result,ensure_ascii=False),check_data))
                return self.pass_result
    '''检查接口请求头包含的json key'''
    def header_key_check(self,check_data):
        return self.__key_check(self.response_data.headers,check_data)

    '''检查接口响应体包含的json key言'''
    def body_key_check(self,check_data):
        return self.__key_check(self.response_data.json(),check_data)

    ''' 针对接口字典key-value值进行断言'''
    def __key_value_check(self, actual_result, check_data):
        key_value_dict = json.loads(check_data)
        tmp_result = []
        for key_value in key_value_dict.items():
            if key_value in actual_result.items():
                tmp_result.append(self.pass_result)
            else:
                tmp_result.append(self.fail_result)
        if self.fail_result in tmp_result:
            logger.error('断言失败，失败原因%s' % self.fail_result)
            logger.info('测试实际通过：%s ===测试期望结果：%s 不一致，检测失败'%(json.dumps(actual_result,ensure_ascii=False),check_data))
            logger.info(str(tmp_result)+'tmp_resulttmp_resulttmp_resulttmp_resulttmp_resultasdfa')
            return self.fail_result
        else:
            logger.info('测试实际通过：%s ===测试期望结果：%s 一致，检测通过'%(json.dumps(actual_result),check_data))
            return self.pass_result

    def header_key_value_check(self, check_data):
        return self.__key_value_check(self.response_data.headers, check_data)

    def body_key_value_check(self, check_data):
        return self.__key_value_check(self.response_data.json(), check_data)

    def response_code_check(self,check_data):
        if self.response_data.status_code == check_data:
            logger.info('实际响应状态码和期望结果：%s 一致，检测通过' % (str(self.response_data.status_code),check_data))
            return self.pass_result
        else:
            logger.info('实际响应状态码和期望结果：%s 不一致，检测失败' % (str(self.response_data.status_code),check_data))
            logger.error('断言失败，失败原因%s' % self.fail_result)
            return self.fail_result

    '''针对接口正则进行断言'''
    def regexp_check(self,check_data):
        tmp_result = re.findall(check_data,self.response_data.text)
        if tmp_result:
            logger.info('响应正文期望结果正则表达式：%s 能在响应正文中匹配，检测通过' % check_data)
            return self.pass_result
        else:
            logger.error('断言失败，失败原因%s' %self.fail_result)
            logger.info('响应正文期望结果正则表达式：%s 能在响应正文中匹配，检测失败' % check_data)
            return self.fail_result

    ''' 读取excel接口测试用例断言的类型，与断言结果进行比较，进行断言；'''
    def run_check(self,check_type,check_data=None):
        logger.info('根据 %s 进行断言，检查是否满足期望结果：%s'%(check_type,check_data))
        if check_type=='none' or check_type=='':
            return  self.check_rules['none']()
        else:
            return  self.check_rules[check_type](check_data)

if __name__ == '__main__':
    # session = requests.session()
    # get_token_params = {
    #     "grant_type": "client_credential",
    #     "appid": "wxf26ad2ae7497289a",
    #     "secret": "177931a321a1f39a47a1ef202d8a3497"}
    # response = session.get(url=' https://api.weixin.qq.com/cgi-bin/token', params=get_token_params, verify=False)
    response ='{"tag":{"id":204,"name":"asdf3425"}}'
    response.encoding = response.apparent_encoding
    checkutils = CheckUtils(response)
    # print( checkutils.run_check('access_token,expires_in'))
    # print(checkutils.run_check('{"expires_in":7200}'))
    # print(checkutils.run_check('json_key','access_token,expires_in'))
    print(checkutils.run_check('json_key','tag'))
    # print(checkutils.run_check('body_regexp','"access_token":"(.+?)"'))
    # print(checkutils.run_check('header_key','Connection,Content-Length'))
    # print(checkutils.run_check('header_key_value','{"Connection":"keep-alive","Content-Type":"application/json; encoding=utf-8"}'))
    # print(checkutils.run_check('response_code',200))
    # print(checkutils.run_check('none',""))



