import xlrd
import os
excel_path = os.path.join(os.path.dirname(__file__),'..','data','TestData.xlsx')
workbook = xlrd.open_workbook(excel_path)
sheet = workbook.sheet_by_name('Sheet1')
print(sheet.cell_value(1,0))
print(sheet.merged_cells)



