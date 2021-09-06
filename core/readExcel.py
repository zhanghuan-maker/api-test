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
import csv
import re
from core.generate_yaml import *


EXPR = '\@\{(.*?)\}'
def getdata1(description,Case):
    # 读取yaml的值
    yamlinsex= open('./conf/'+Case+'/'+description+'.yaml','r',encoding='utf-8')
    data = yaml.load(yamlinsex)
    return data[description]


def build_param(string,target,i):
    '''
    识别@{key}并替换成全局变量池的value
    :param string: 待替换的字符串
    :return:
    '''
    # 遍历所有取值并做替换
    keys = re.findall(EXPR, string)
    for key in keys:
        value = target[i][key]
        string = string.replace('@{' + key + '}', str(value))
    return string

def read_excel(Case=None,sheet_name="Sheet1"):
    '''
    读取excel文件内容
    :param excel_path: xlsx文件的路径
    :param sheet_name: 表格名称
    :return: k-v的列表
    '''
    #定义两个空列表，存放每行的数据
    all_rows = []
    #case为测试用例集的路径
    case = []
    #filename为测试用例的名字
    filename=[]
    #定义返回的字典
    rows_dict = []
    if Case=='FULL':
        for root, dirs, files in os.walk(BASE_PATH+"/conf/"):
            for file in files:
                if file.endswith('.xlsx'):
                    case.append(os.path.join(root, file))
                    filename.append(file)
    elif ";" in Case:
        case1=Case.split(";")
        for i in range(len(case1)):
            for root, dirs, files in os.walk(BASE_PATH + "/conf/"+case1[i]):
                for file in files:
                    if file.endswith('xlsx'):
                        case.append(os.path.join(root, file))
                        filename.append(file)
    else:
        case1 = Case
        for root, dirs, files in os.walk(BASE_PATH + "/conf/" + case1):
            for file in files:
                if file.endswith('xlsx'):
                    case.append(os.path.join(root, file))
                    filename.append(file)

    #自动生成变量集合
    for root, dirs, files in os.walk(BASE_PATH + "/conf/" + case1):
        for dir in dirs:
            if dir == 'old_yaml':
                  main_generate_yaml(Case)

    # 打开文件
    for i in range(len(case)):
        excel_path=case[i]
        workbook = xlrd.open_workbook(excel_path)
    # 根据sheet索引或者名称获取sheet内容
        sheet = workbook.sheet_by_name(sheet_name) # sheet索引从0开始
    # 获取第一行作为key
        first_row = sheet.row_values(0)  # 获取第一行内容
    # 获取表的行数
        rows_length = sheet.nrows
        for j in range(rows_length):  # 循环逐行打印
            if j == 0:  # 跳过第一行
                continue
            k=sheet.row_values(j)
            if re.findall(EXPR, str(k)):
                description=k[1]
                lenth=len(getdata1(description,Case))
                for i in range(lenth):
                    k=eval(build_param(str(k),getdata1(description,Case),i))
                    all_rows.append(k)
                    k=sheet.row_values(j)
            else:
                all_rows.append(k)
    # 获取每张表的测试用例
        rows_dict=[]
        for row in all_rows:
            lis = dict(zip(first_row,row))
            rows_dict.append(lis)

    return rows_dict

# #创建缓存文件
# def cache_write(api_data):
#     api_data=list(api_data)
#     with open("cache.csv","w") as csvfile:
#         writer =csv.writer(csvfile)
#         writer.writerow(["detail"])
#     with open("cache.csv","a") as csvfile:
#         writer =csv.writer(csvfile)
#         writer.writerow(api_data)
#         csvfile.close()
# #读取缓存信息
# def cache_read():
#     detail=[]
#     with open("cache.csv","r") as csvfile:
#         reader =csv.reader(csvfile)
#         for line in reader:
#             detail.append(line)
#         return ''.join(detail[-1])