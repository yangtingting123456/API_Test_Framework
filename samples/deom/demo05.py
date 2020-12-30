# -*- coding: utf-8 -*-
# @Time    : 2020/12/30 14:28
# @Author  : tingting.yang
# @FileName: demo05.py

class Demo5:
    def __init__(self):
        self.function = {
            'json_key':self.key_check,
            'key_value_check':self.key_value_check
        }
    def key_check(self):
        print( 'key_check.....' )
    def key_value_check(self):
        print( 'key_value_check........' )

    def run_check(self,check_type):
        self.function[check_type]()

if __name__ == '__main__':
    demo5= Demo5()
    demo5.run_check('key_value_check')