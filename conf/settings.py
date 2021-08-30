#!/usr/bin/env python
# -*- coding: utf-8 -*-



import os

Case = os.getenv('Case')
# 获取项目路径
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 定义测试用例的路径
TESTCASE_PATH =  os.path.join(BASE_PATH,'test_case')
# 定义测报告的路径
REPORT_PATH =  os.path.join(BASE_PATH,'report/')
# 定义日志文件的路径
LOG_PATH = os.path.join(BASE_PATH,'log/log.txt')

