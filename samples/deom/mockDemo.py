from unittest import mock
def add(num1,num2):
    return num1 + num2   # pass

add_value = mock.Mock(return_value=200)  # 创建mock对象
add = add_value # 把mock对象赋值给add方法

print( add(10,20) )