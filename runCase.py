#!/user/bin/env python
#coding:utf-8
'''
@project : shell
@author  : zhanghuan
#@file   : runCase.py
#@ide    : PyCharm
#@time   : 2021-06-21 15:27:00
'''

'''
    pytest用例执行文件
'''
import pytest
import time
import os

Case = os.getenv('Case')
Environment = os.getenv('Environment')


if __name__ == '__main__':

    now = time.strftime("%Y-%m-%d_%H_%M_%S")
    pytest.main(['-s', './test_case/test_case.py', '--html=report/{}_{}_{}_report.html'.format(now, Case, Environment)])
