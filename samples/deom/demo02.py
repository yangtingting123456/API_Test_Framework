import re
import ast
str1 = '{"access_tokne":${token}}'
variables_list = re.findall('\\${\w+}',str1)

dict1 = {'token':'adasd'}
print(dict1[variables_list[0][2:-1]])
str1 = str1.replace(variables_list[0],'"%s"'%dict1[variables_list[0][2:-1]])
print(str1)
#成果：{"access_tokne":${token}} 考虑：多个变量怎么办？不需要替换的情况怎么办
str2 = '{"name":${n},"age":${a}}'
dict2 = {'n':'xiaoming','a':18}
variables_list2 = re.findall('\\${\w+}',str2)
print(variables_list2)
for v in variables_list2:
    str2 = str2.replace(v,'"%s"'%dict2[v[2:-1]])
print(str2)

