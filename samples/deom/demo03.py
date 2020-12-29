# -*- coding: utf-8 -*-
# @Time    : 2020/12/29 15:57
# @Author  : tingting.yang
# @FileName: demo03.py
import json
str1 = '{"access_token": "40_FHP90NHUsYq-JxUEaGWsTsNwAeQndJb3abFAJKD","tags":"11"}'
#方式一：检查key是否存在
json_obj = json.loads(str1)
if 'access_token' in json_obj.keys():
    print('true')
else:
    print('false')
# 方式二：检查多个ke是否存在
print('####################')
check_keys = ['access_token','tag']
yes_no = []
for check_key in check_keys:
    if check_key in json_obj.keys():
        yes_no.append(True)
    else:
        yes_no.append(False)
if False in yes_no:
    print('False')

