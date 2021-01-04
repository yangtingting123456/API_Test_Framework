# -*- coding: utf-8 -*-
# @Time    : 2021/1/4 17:22
# @Author  : tingting.yang
# @FileName: demo09.py
import paramunittest
import  unittest

test_data = [{'a':10,'b':10},{'a':5,'b':15},(10,1)]
def get_data():
    return test_data
@paramunittest.parametrized(
    *get_data()
)

class TestApi(unittest.TestCase):
    def setParameters(self,a,b):
        self.a = a
        self.b = b

    def testApi(self):
        self.assertEqual(self.a+self.b,20)

if __name__ == '__main__':
    unittest.main(verbosity=1)
