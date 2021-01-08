# -*- coding: utf-8 -*-
# @Time    : 2021/1/8 15:23
# @Author  : tingting.yang
# @FileName: mysql_demo01.py
import pymysql


conn = pymysql.connect(
    host = '127.0.0.1',
    port = 3306,
    user = 'ytt',
    password = '123456',
    database = 'interface_test_db',
    charset = 'utf8'
)
cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

sql_str = 'select * from case_info;'
cursor.execute(sql_str)
print(cursor.fetchall())
cursor.close()
conn.close()