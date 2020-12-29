import requests
import jsonpath
import re
session = requests.session()
get_token_params = {
    "grant_type":"client_credential",
    "appid":"wxf26ad2ae7497289a",
    "secret":"177931a321a1f39a47a1ef202d8a3497"
}

response = session.get(url=' https://api.weixin.qq.com/cgi-bin/token',params = get_token_params,verify=False)
response.encoding = response.apparent_encoding

# list1={'测试用例编号': 'api_case_02', '测试用例名称': '创建标签接口测试', '用例执行': '否', '用例步骤': 'step_01', '接口名称': '获取access_token接口',
#  '请求方式': 'get', '请求头部信息': '', '请求地址': '/cgi-bin/token',
#  '请求参数(get)': '{"grant_type":"client_credential","appid":"wx55614004f367f8ca","secret":"65515b46dd758dfdb09420bb7db2c67f"}',
#  '请求参数(post)': '', '取值方式': '正则取值', '取值代码': '$.access_token', '取值变量': 'token', '断言类型': 'json_key_value',
#  '期望结果': '{"expires_in":7200}'}
# v = response.json()
# v1 = jsonpath.jsonpath(v,list1['取值代码'])[0]
# print(v1)
body = response.text
token_value = re.findall('"access_token":"(.+?)"',body)[0]
print(token_value)


