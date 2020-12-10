import os
import xlrd3

a= {'one':1,'two':2}
a.setdefault('three',3)
print(a)
print(a.setdefault('three',30))
print(a)

data_list = [{'事件': '学习python编程', '步骤序号': 'step_01', '步骤操作': '购买微客', '完成情况': 1.0},
             {'事件': '学习python编程', '步骤序号': 'step_02', '步骤操作': '根据微客搭建好测试环境', '完成情况': 1.0},
             {'事件': '学习python编程', '步骤序号': 'step_03', '步骤操作': '做好笔记', '完成情况': 1.0},
             {'事件': '学习python编程', '步骤序号': 'step_04', '步骤操作': 'python应用', '完成情况': 1.0},
             {'事件': '学习python编程', '步骤序号': 'step_05', '步骤操作': '接口测试', '完成情况': 1.0},
             {'事件': '学习java编程', '步骤序号': 'step_01', '步骤操作': '购买微客', '完成情况': 1.0},
             {'事件': '学习java编程', '步骤序号': 'step_02', '步骤操作': '根据微客搭建好测试环境', '完成情况': 1.0},
             {'事件': '学习java编程', '步骤序号': 'step_03', '步骤操作': '做好笔记', '完成情况': 1.0},
             {'事件': '学习java编程', '步骤序号': 'step_04', '步骤操作': 'python应用', '完成情况': 1.0},
             {'事件': '学习java编程', '步骤序号': 'step_05', '步骤操作': '接口测试', '完成情况': 1.0}
             ]

print(data_list)

data_dict = { }
for d in data_list:
    data_dict.setdefault(d['事件'],[]).append(d)

print(data_dict)