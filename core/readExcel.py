#!/user/bin/env python
#coding=utf-8
'''
@project : shell
@author  : zhanghuan
#@file   : readExcel.py
#@ide    : PyCharm
#@time   : 2021-06-21 15:27:00
'''
import xlrd
from conf.settings import *
import os



def read_excel(Case=None,sheet_name="Sheet1"):
    '''
    读取excel文件内容
    :param excel_path: xlsx文件的路径
    :param sheet_name: 表格名称
    :return: k-v的列表
    '''
    #定义两个空列表，存放每行的数据
    all_rows = []
    rows_dict = []
    case = []
    if Case=='FULL':
        for root, dirs, files in os.walk(BASE_PATH+"/conf/"):
            for file in files:
                if file.endswith('.xlsx'):
                    case.append(os.path.join(root, file))
    elif ";" in Case:
        case1=Case.split(";")
        for i in range(len(case1)):
            for root, dirs, files in os.walk(BASE_PATH + "/conf/"+case1[i]):
                for file in files:
                    if file.endswith('xlsx'):
                        case.append(os.path.join(root, file))
    else:
        case1 = Case
        for root, dirs, files in os.walk(BASE_PATH + "/conf/" + case1):
            for file in files:
                if file.endswith('xlsx'):
                    case.append(os.path.join(root, file))
        print(case)
    # 打开文件

    for i in range(len(case)):
        excel_path=case[i]
        workbook = xlrd.open_workbook(excel_path)
    # 获取所有sheet
    # print(workbook.sheet_names())  # [u'sheet1', u'sheet2']

    # 根据sheet索引或者名称获取sheet内容
        sheet = workbook.sheet_by_name(sheet_name) # sheet索引从0开始

    # 获取第一行作为key
        first_row = sheet.row_values(0)  # 获取第一行内容

    # 获取表的行数
        rows_length = sheet.nrows


        for i in range(rows_length):  # 循环逐行打印
            if i == 0:  # 跳过第一行
                continue
            all_rows.append(sheet.row_values(i))
        rows_dict=[]
        for row in all_rows:
            lis = dict(zip(first_row,row))
            rows_dict.append(lis)


    return rows_dict


