20201209：
1.项目初始化配置 == 放到github上面
2.数据处理
2.1 config 读取的封装
2.2 excel存放测试数据转换到代码中处理
合并单元格 ==> 封装excel_utils ==> 把excel数据转换成测试用例业务数据（setdefault 为了把用例步骤整合到对应的
测试编号中） ==> 封装testcase_data_utils ==>形态变化
{[],[]} == {"":[],"":[]} ==[{'case_id'：'','case_step':[]}.....]
20201216:
1.根据上一次excel封装的测试数据，来进行requests封装
2.ast.literral_eval response.apparent_encoding
3.requests_utils 模块
request_by_step-->request -->__get/__post
4.excel 为后续课程准备，增加了字段：取值方式，取值代码，取值变量

