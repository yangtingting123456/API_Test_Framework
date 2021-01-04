# -*- coding: utf-8 -*-
# @Time    : 2021/1/4 17:02
# @Author  : tingting.yang
# @FileName: demo08.py
import paramunittest
import unittest

@paramunittest.parametrized(
    (10,20),
    (30,40),
    (1,29)
)
class ApiTestDemo(unittest.TestCase):
    def setParameters(self, numa, numb):
        self.a = numa
        self.b = numb

    def test_add_case(self):
        print('%d+%d=%d'%(self.a,self.b,30))
        self.assertEqual(self.a+self.b,30)

if __name__ == '__main__':
    unittest.main(verbosity=2)