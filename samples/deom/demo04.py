# -*- coding: utf-8 -*-
# @Time    : 2020/12/29 17:26
# @Author  : tingting.yang
# @FileName: demo04.py
import json
json_obj = {"access_token":"40_FwH70OJu-kiO9ys9xywWS0aHhGKpugPB3Vmf_aCS2tLD6tbfKRDBi42GxAsoggAAOIxpXuJUPcogJLqIgMDEuV5LF6RibZHIrcEx31ARVLiNBZ2gFchy2KDKMh48bN6_L-xQFY5FsMrm8y66XHIdADALVW","expires_in":7200}
except_str = '{"expires_in":7200}'
except_dict = json.loads(except_str)
# print(except_dict.items())
# print(json_obj.items())
# 方式一：
if list(except_dict.items())[0] in list(json_obj.items()):
    print('true')

# 方式二：考虑多项
yes_no = []
for except_item in except_dict.items():
    if except_item in json_obj.items():
        yes_no.append( True )
    else:
        yes_no.append( False )
if False in yes_no:
    print( 'False' )
else:
    print( 'true' )




