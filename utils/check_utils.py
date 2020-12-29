# -*- coding: utf-8 -*-
# @Time    : 2020/12/29 16:44
# @Author  : tingting.yang
# @FileName: check.py
import requests
import json
class CheckUtils:
    def __init__(self,response_data):
        self.response_data = response_data
    def key_check(self,check_data):
        key_list = check_data.split(',')
        tmp_result = []
        for key in key_list:
            if key in self.response_data.json().keys():
                tmp_result.append(True)
            else:
                tmp_result.append(False)
            if False in tmp_result:
                 return False
            else:
                return True
if __name__ == '__main__':
    session = requests.session()
    get_token_params = {
        "grant_type": "client_credential",
        "appid": "wxf26ad2ae7497289a",
        "secret": "177931a321a1f39a47a1ef202d8a3497"}
    response = session.get(url=' https://api.weixin.qq.com/cgi-bin/token', params=get_token_params, verify=False)
    response.encoding = response.apparent_encoding
    checkutils = CheckUtils(response)
    print( checkutils.key_check('access_token,expires_in'))


