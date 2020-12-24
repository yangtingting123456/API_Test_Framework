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
body = response.text
value = re.findall('"access_token":"(.+?)"',body)[0]
print(value)
