import xlrd3
import os

class ExcelUtils:
    def __init__(self,excel_file_path,sheet_name):
        self.excel_file_path = excel_file_path
        self.sheet_name= sheet_name
        self.sheet = self.get_sheet()

    def get_sheet(self):
        '''根据文件路径获取表格对象'''
        workbook = xlrd3.open_workbook(self.excel_file_path)
        sheet = workbook.sheet_by_name(self.sheet_name)
        return sheet

    def get_max_row_number(self):
        '''获取表格行数'''
        max_row_number = self.sheet.nrows
        return max_row_number

    def get_column_count(self):
        '''获取表格列数'''
        column_count = self.sheet.ncols
        return column_count

    def get_merge_cell_values(self,row_index,col_index):
        '''处理excel单元格的数据，包含合并单元格数据'''
        cell_value = None
        merged = self.sheet.merged_cells
        for (rlow, rhigh, clow, chigh) in merged:  # 遍历表格中所有合并单元格位置信息
            if (row_index >= rlow and row_index < rhigh):  # 行坐标判断
                if (col_index >= clow and col_index < chigh):  # 列坐标判断
                    # 如果满足条件，就把合并单元格第一个位置的值赋给其它合并单元格
                    cell_value = self.sheet.cell_value(rlow, clow)
                    break;
                else:
                    cell_value = self.sheet.cell_value(row_index, col_index)
            else:
                cell_value = self.sheet.cell_value(row_index, col_index)
        return cell_value

excel_path = os.path.join(os.path.dirname(__file__), '..','data','TestData.xlsx')
excel_value = ExcelUtils(excel_path,'testcase01')

if __name__ == '__main__':
    for i in range(0, 11):
        for j in range(0, 3):
            print(excel_value.get_merge_cell_values(i, j), end=' ')
        print()
