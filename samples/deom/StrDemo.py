#字符串切片练习
f = "12345678"
# print(f[0])
# print(f[-1])
f1 = f.replace("1","2")
# print(f1)
# print(f[:])
# print(f[2:])
# print(f[2:4])
# print(f[1:5:2])
# print(f[::-1])


import io
s = "hello world"
s1 = io.StringIO(s)
print(s1.seek(2))
print(s1.write("m"))
print(s1.getvalue())
