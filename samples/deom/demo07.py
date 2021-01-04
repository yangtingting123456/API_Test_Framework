# -*- coding: utf-8 -*-
# @Time    : 2021/1/4 14:03
# @Author  : tingting.yang
# @FileName: demo07.py
import re
str_list1 = '{"tag":{"id":151,"name":"444"}}'
str_list2 = '"id":(.+?)'
v = re.findall(str_list2,str_list1)[0]
if v:
    print(True)
else:
    print(False)


