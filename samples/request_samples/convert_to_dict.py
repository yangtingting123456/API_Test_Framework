import json
import ast
str1 = '{"grant_type":"client_credential","appid":"wxf26ad2ae7497289a","secret":"177931a321a1f39a47a1ef202d8a3497"}'
json_data = json.loads(str1)
print(json_data)
dict1 = ast.literal_eval(str1)
print(type(dict1))


str2 = '3+3'
c=ast.literal_eval(str2)
print(type(str2))