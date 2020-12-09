import xlrd3
import os
excel_path = os.path.join(os.path.dirname(__file__),'..','data','TestData.xlsx')
workbook = xlrd3.open_workbook(excel_path)
sheet = workbook.sheet_by_name('Sheet1')
# merged_cells 获取当前表格所有合并单元格的位置信息 ，返回一个列表
merged = sheet.merged_cells
row_index = 3  ; col_index = 0
for (rlow, rhigh, clow, chigh) in merged:  # 遍历表格中所有合并单元格位置信息
    if (row_index >= rlow and row_index < rhigh):  # 行坐标判断
        if (col_index >= clow and col_index < chigh):  # 列坐标判断
            # 如果满足条件，就把合并单元格第一个位置的值赋给其它合并单元格
            cell_value = sheet.cell_value(rlow,clow)
print( cell_value )