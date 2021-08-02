#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from runCase import *


# 获取项目路径
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 定义测试用例的路径
TESTCASE_PATH =  os.path.join(BASE_PATH,'test_case')
# 定义测报告的路径
REPORT_PATH =  os.path.join(BASE_PATH,'report/')
# 定义日志文件的路径
LOG_PATH = os.path.join(BASE_PATH,'log/log.txt')
IMAGE_PATH = os.getcwd()+'/conf/'+Case



# mysql数据库的连接信息
DEV={}

DEV['client_secret']='b71ba6e5-8e46-458c-9ee1-abe255145ee5'
DEV['url']='b2b-dev.digitalshell.com.cn'
DEV['url_direct']='shell-sso-dev'
DEV['factoryId']='d3a92734-58e1-4be8-a9a2-521c1554b5a8'
DEV['equipmentId']='f091b770-eec9-401c-93c6-91d3662e0eb9'
DEV['workshopId']='62b5f3d8-3aa7-4b2f-b704-8b9bf7d9eabc'
DEV['sensorId']='C01'
DEV['fuzzyCheckpointName']='3#粗轧润滑系统-含水率'

DEV['B2B_DB_NAME']='b2bdevnew%b2b'
DEV['B2B_DB_PASSWORD']='ywgmS61Mb9GT'
DEV['B2B_DB_IP']='b2bdevnew.mysqldb.chinacloudapi.cn'
DEV['B2B_DB']='shell_b2b_dev'

DEV['OPS_DB_NAME']='iot_ops_dev'
DEV['OPS_DB_PASSWORD']='X8rPTxle6J3Y'
DEV['OPS_DB_IP']='172.16.0.14'
DEV['OPS_DB']='iot_ops_dev'
DEV['OPS_SSH_PKEY']=r'/Users/huanzhang/.ssh/keys_iot_iot_id_rsa.txt'
DEV['OPS_SSH_NAME']='docker'
DEV['OPS_SSH_PASSWORD']=''
DEV['OPS_SSH_IP']='iot-dtu-dev.digitalshell.com.cn'
DEV['OPS_SSH_PORT']='22'

DEV['IOT_DB_NAME']='mongouser'
DEV['IOT_DB_PASSWORD']='b2b@mongodev'
DEV['IOT_DB_IP']='172.16.32.8'
DEV['IOT_DB_PORT']='27017'
DEV['IOT_DB']='iot-dev'
DEV['IOT_SSH_PKEY']=r'/Users/huanzhang/Documents/未命名文件夹/private-key'
DEV['IOT_SSH_NAME']='docker'
DEV['IOT_SSH_PASSWORD']=''
DEV['IOT_SSH_IP']='iot-dtu-dev.digitalshell.com.cn'
DEV['IOT_SSH_PORT']='22'

QA={}
QA['client_secret']='4f136a75-0592-4b2e-844b-3116331d9832'
QA['url']='b2b-qa.digitalshell.com.cn'
QA['url_direct']='shell-sso-qa'
QA['factoryId']='2ef040b5-fdf4-48f3-a06d-ecbf909bf564'
QA['equipmentId']='4c68373f-c8ef-4c00-a94e-6ce36addad7b'
QA['workshopId']='9c4be079-57eb-4f0e-9f84-e49baff31a51'
QA['sensorId']='003'
QA['fuzzyCheckpointName']='K1粗轧-金属磨粒'

QA['B2B_DB_NAME']='b2bdevnew%b2b'
QA['B2B_DB_PASSWORD']='ywgmS61Mb9GT'
QA['B2B_DB_IP']='b2bdevnew.mysqldb.chinacloudapi.cn'
QA['B2B_DB']='shell_b2b_qa'


QA['OPS_DB_NAME']='iot_ops_dev'
QA['OPS_DB_PASSWORD']='X8rPTxle6J3Y'
QA['OPS_DB_IP']='172.16.0.14'
QA['OPS_DB']='iot_ops_qa'
QA['OPS_SSH_PKEY']=r'/Users/huanzhang/.ssh/keys_iot_iot_id_rsa.txt'
QA['OPS_SSH_NAME']='docker'
QA['OPS_SSH_PASSWORD']=''
QA['OPS_SSH_IP']='iot-dtu-dev.digitalshell.com.cn'
QA['OPS_SSH_PORT']='22'

QA['IOT_DB_NAME']='mongouser'
QA['IOT_DB_PASSWORD']='b2b@mongodev'
QA['IOT_DB_IP']='172.16.32.8'
QA['IOT_DB_PORT']='27017'
QA['IOT_DB']='iot-qa'
QA['IOT_SSH_PKEY']=r'/Users/huanzhang/Documents/未命名文件夹/private-key'
QA['IOT_SSH_NAME']='docker'
QA['IOT_SSH_PASSWORD']=''
QA['IOT_SSH_IP']='iot-dtu-dev.digitalshell.com.cn'
QA['IOT_SSH_PORT']='22'

UAT={}
UAT['client_secret']='8ac575eb-0d5b-4862-bc9b-5ed35fab4cb0'
UAT['url']='b2b-uat.digitalshell.com.cn'
UAT['url_direct']='shell-sso-uat'
UAT['factoryId']='1f4e83ef-7145-4e55-b4c8-fba7f5818696'
UAT['equipmentId']='56bf29a3-5884-47ee-96c8-0e907ab7efeb'
UAT['workshopId']='d5d3d0f1-84cf-45b5-bece-cfd01721b461'
UAT['sensorId']='z05'
UAT['fuzzyCheckpointName']='K1粗轧-金属磨粒'


UAT['B2B_DB_NAME']='b2bdevnew%b2b'
UAT['B2B_DB_PASSWORD']='ywgmS61Mb9GT'
UAT['B2B_DB_IP']='b2bdevnew.mysqldb.chinacloudapi.cn'
UAT['B2B_DB']='shell_b2b_uat'

UAT['OPS_DB_NAME']='iot_ops_dev'
UAT['OPS_DB_PASSWORD']='X8rPTxle6J3Y'
UAT['OPS_DB_IP']='172.16.0.14'
UAT['OPS_DB']='iot_ops_uat'
UAT['OPS_SSH_PKEY']=r'/Users/huanzhang/.ssh/keys_iot_iot_id_rsa.txt'
UAT['OPS_SSH_NAME']='docker'
UAT['OPS_SSH_PASSWORD']=''
UAT['OPS_SSH_IP']='iot-dtu-dev.digitalshell.com.cn'
UAT['OPS_SSH_PORT']='22'

UAT['IOT_DB_NAME']='mongouser'
UAT['IOT_DB_PASSWORD']='b2b@mongodev'
UAT['IOT_DB_IP']='172.16.32.8'
UAT['IOT_DB_PORT']='27017'
UAT['IOT_DB']='iot-uat'
UAT['IOT_SSH_PKEY']=r'/Users/huanzhang/Documents/未命名文件夹/private-key'
UAT['IOT_SSH_NAME']='docker'
UAT['IOT_SSH_PASSWORD']=''
UAT['IOT_SSH_IP']='iot-dtu-dev.digitalshell.com.cn'
UAT['IOT_SSH_PORT']='22'