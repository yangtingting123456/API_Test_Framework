import xlrd
import os
excel_path = os.path.join(os.path.dirname(__file__),'..','data','TestData.xlsx')
workbook = xlrd.open_workbook(excel_path)
sheet = workbook.sheet_by_name('Sheet1')
print(sheet.cell_value(1,0))
print(sheet.merged_cells)  #包含四个元素（起始行，结算行，起始列，介绍列）

#输入行列，判断一个单元格十分始合并过
x=0
y=1
if x>=1 and x<6:
    if y>=0 and y<1:
        print('合并单元格')
    else:
         print('不是合并单元格')
else:
     print('不是合并单元格')




