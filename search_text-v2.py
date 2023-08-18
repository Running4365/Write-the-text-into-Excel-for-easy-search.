# -*- coding: utf-8 -*-

'''
把特定后缀的文件，写入到excel中，方便查找。在WPS中，查找范围选择工作簿。

输入：  file_ext  ，选择特定后缀名的文件。
        dest_dir  ，需要查找的文件目录。
输出：
        当前目录下的excel文件。
'''

import os  
import time
import chardet
from utils_demo import find_all_file, get_filename 
import pandas as pd
from pandas import DataFrame


# file_ext = ['.py', '.v', '.vhd', '.txt']
file_ext = [ '.txt']

current_dir = os.path.dirname(os.path.abspath(__file__))
# dest_dir = os.path.join(current_dir, '19_dds')
dest_dir = r'C:\Programs0\gvim90\Vim\vim90\doc'

current_time = time.strftime('%y%m%d_%H%M%S', time.localtime())
gen_excel_path = os.path.join(current_dir, f'{get_filename(dest_dir)}_{current_time}.xlsx')
name_list, path_list = list(), list()

def gen_non_duplicate_names_order(lista):
    '''
    输入：
['tb_dds.v', 'key_filter.v', 'top_dds.v', 'key_filter.v', 'top_dds.v', 'dcfifo_256x8to128x16_sim_netlist.v', 'dds.v', 'key_control.v', 'key_filter.v', 'top_dds.v']    
输出：
['0_tb_dds.v', '1_key_filter.v', '2_top_dds.v', '3_key_filter.v', '4_top_dds.v', '5_dcfifo_256x8to128x16_sim_', '6_dds.v', '7_key_control.v', '8_key_filter.v', '9_top_dds.v']
    '''
    listb = list()
    for ind,val in enumerate(lista):
        if len(val) > 26:
            converted_str = f'{ind}_{val[:25]}'  # Excel worksheet name '44_dcfifo_256x8to128x16_sim_netlist.v' must be <= 31 chars.
        else:
            converted_str = f'{ind}_{val}'
        listb.append(converted_str)
    return listb 

print('running...')
file_path_list = find_all_file(dest_dir)
for file_path in file_path_list:
    for ext in file_ext:
        if(file_path.endswith(ext) and 'usr_' in file_path):
            print(file_path)
            path_list.append(file_path)
            name_list.append(get_filename(file_path))
name_list = gen_non_duplicate_names_order(name_list)


with pd.ExcelWriter(gen_excel_path) as writer:
    for idx,path in enumerate(path_list):
        with open(path, mode='rb') as frb:
            #检测编码方式
            current_encoding = chardet.detect(frb.read())['encoding']
        with open(path, mode='r', encoding=current_encoding, errors='ignore') as f:
            fr = f.readlines()

        fr.insert(0, path)
        fr.insert(1, '\n')
        fr.insert(2, '\n')
        data = {'data': fr}
        df = DataFrame(data)

        df.to_excel(writer, sheet_name=name_list[idx], index=False,header=False)

        worksheet = writer.sheets[name_list[idx]]
        workbook = writer.book 
        formater = workbook.add_format({"border": 0})
        formater.set_border(0)

        for idx23, col in enumerate(df):  # loop through all columns
            series = df[col]
            max_len = max((
                series.astype(str).map(len).max(),  # len of largest item
                len(str(series.name))  # len of column name/header
                )) + 10  # adding a little extra space
            worksheet.set_column(idx23, idx23, max_len)  # set column width
            # worksheet.set_border(0)
    # with open(r'D:\Py\230623_search_text\help_to_excel.txt', 'w') as fhelp:
    #     fhelp.write(help(df.to_excel))
    # print(help(pd.ExcelWriter))
print('done.')
