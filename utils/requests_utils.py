#requests封装
import requests
from utils.config_utils import local_config
import json
class RequestsUtils:
    def __init__(self):
        self.hosts = local_config.HOSTS
        self.session = requests.session()
    def get(self,requests_info):
        url = self.hosts+requests_info['请求地址']
        response = self.session.get(url = url,
                                    params = json.loads(requests_info['请求参数（get）']),
                                    headers = requests_info['请求头部信息'])
        response.encoding = response.apparent_encoding  #保证不乱吗
        result = {
            'code':0,
            'response_code':response.status_code,
            'response_reason':response.reason,
            'response_headers':response.headers,
            'response_body':response.text
        }
        return result

    def post(self,requests_info):
        url = self.hosts+requests_info['请求地址']
        response = self.session.post(url = url,
                                    params = json.loads(requests_info['请求参数（get）']),
                                    json = json.loads(requests_info['请求参数（post)']),
                                    headers = requests_info['请求头部信息'])
        response.encoding = response.apparent_encoding  #保证不乱吗
        result = {
            'code':0,
            'response_code':response.status_code,
            'response_reason':response.reason,
            'response_headers':response.headers,
            'response_body':response.text,
            'response':response
        }
        return result

if __name__ == '__main__':
    req_get_dict = {'测试用例编号': 'api_case_01', '测试用例名称': '获取access_token接口测试', '用例执行': '是', '用例步骤': 'step01', '接口名称': '获取access_token接口', '请求方式': 'get', '请求头部信息': '', '请求地址': '/cgi-bin/token', '请求参数（get）': '{"grant_type":"client_credential","appid":"wxf26ad2ae7497289a","secret":"177931a321a1f39a47a1ef202d8a3497"}', '请求参数（post）': ''}
    req_post_dict ={'测试用例编号': 'api_case_03', '测试用例名称': '测试能否正确删除用户标签', '用例执行': '是', '用例步骤': 'step03', '接口名称': '删除标签接口', '请求方式': 'post', '请求头部信息': '', '请求地址': '/cgi-bin/tags/delete', '请求参数（get）': '{"access_token":"40_e-gBgD_JItrxjkaWJa1By0KGI1h6NNS6Nzs5RIpn2mwZf6ykmZobHnmmjN83kIneSJI9KnEOMwEgGyjwvVHtDctQ0EyntOX7wCHT7oWfxF80P1MiUwqnmck6apQBAcvleUvPHHyV7AGB31ACKHKeAGAOLO"}', '请求参数（post)': '{ "tag":{ "id" :456}} '}
    requestsUtils =RequestsUtils()
    v = requestsUtils.post(req_post_dict)
    print(v)

