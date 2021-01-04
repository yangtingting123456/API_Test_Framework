# -*- coding: utf-8 -*-
# @Time    : 2020/12/31 11:06
# @Author  : tingting.yang
# @FileName: demo01.py
import pytest
def add(a, b):
    return a + b

def test_add():
    ret = add(3, 4)
    if ret == 7:
        print("add 函数的测试通过")
    else:
        print("add 函数的测试失败")

print(test_add())