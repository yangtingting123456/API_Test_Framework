import xlrd3
import os
workbook = xlrd3.open_workbook(os.path.join(os.path.dirname(__file__),'..','data','TestData.xlsx'))
sheet = workbook.sheet_by_name('testcase01')
# merged_cells 获取当前表格所有合并单元格的位置信息 ，返回一个列表
def get_cell_merge_values(row_index,col_index):
    cell_value = None
    merged = sheet.merged_cellsSheet1
    for (rlow, rhigh, clow, chigh) in merged:  # 遍历表格中所有合并单元格位置信息
        if (row_index >= rlow and row_index < rhigh):  # 行坐标判断
            if (col_index >= clow and col_index < chigh):  # 列坐标判断
                # 如果满足条件，就把合并单元格第一个位置的值赋给其它合并单元格
                cell_value = sheet.cell_value(rlow, clow)
                break;
            else:
                cell_value = sheet.cell_value(row_index, col_index)
        else:
            cell_value = sheet.cell_value(row_index, col_index)
    return cell_value
#
# for i in range(0,11):
#     for j in range(0,3):
#         print(get_cell_merge_values(i,j),end=' ')
#     print()

# excel_list_data = []
# row_head = sheet.row_values(0)
# row_dict = {}
# row_dict[row_head[0]] = get_cell_merge_values(1,0)
# row_dict[row_head[1]] = get_cell_merge_values(1,1)
# row_dict[row_head[2]] = get_cell_merge_values(1,2)
# row_dict[row_head[3]] = get_cell_merge_values(1,3)
# print(row_dict)

#步骤二： 改为循环一行
excel_list_data = []
row_head = sheet.row_values(0)
for row_num in range(1,sheet.nrows):
    row_dict = {}
    for col_num in range(sheet.ncols):
        row_dict[row_head[col_num]] = get_cell_merge_values(row_num, col_num)
    excel_list_data.append(row_dict)
print(excel_list_data)
for  data  in excel_list_data:
    print(data)