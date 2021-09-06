#!/user/bin/env python
#coding=utf-8
'''
@project : shell
@author  : zhanghuan
#@file   : mysql_operate.py
#@ide    : PyCharm
#@time   : 2021-06-21 15:27:00
'''

from conf.settings import *
import pymysql
import os
from sshtunnel import SSHTunnelForwarder
import pymongo
from urllib import parse
import yaml





class Operate():
    '''
        mysql执行器
    '''
    def __init__(self,dbname):

        # 读取yaml文件
        yamlinsex = open('./conf/'+Case+'/global_variable.yaml', 'r', encoding='utf-8')
        data = yaml.load(yamlinsex)

        self.conf=[]
        environment = os.getenv('Environment')
        if environment == "dev":
            self.conf = data['DEV'][0]
        elif environment == "qa":
            self.conf = data['QA'][0]
        elif environment == "uat":
            self.conf = data['UAT'][0]
        elif environment == "prod":
            self.conf = data['PROD'][0]

        if dbname=='OPS':
            self.server=SSHTunnelForwarder(
                ssh_address_or_host=(self.conf[dbname + '_SSH_IP'], int(self.conf[dbname +'_SSH_PORT'])),  # 指定ssh登录的跳转机的address，端口号
                ssh_username=self.conf[dbname + '_SSH_NAME'],  # 跳转机的用户
                ssh_pkey=self.conf[dbname + '_SSH_PKEY'],  # 私钥路径
                ssh_password=self.conf[dbname + '_SSH_PASSWORD'],  # 密码(电脑开机密码)
                remote_bind_address=(self.conf[dbname + '_DB_IP'], 3306)) # mysql服务器的address，端口号
            self.server.start()
            self.db = pymysql.connect(
                host='127.0.0.1',
                port=self.server.local_bind_port,
                user=self.conf[dbname + '_DB_NAME'],
                passwd=self.conf[dbname + '_DB_PASSWORD'],
                db=self.conf[dbname + '_DB'],
                charset='utf8')

        elif dbname=='B2B':
            self.db = pymysql.connect(
                host=self.conf[dbname+'_DB_IP'],
                user=self.conf[dbname+'_DB_NAME'],
                password=self.conf[dbname+'_DB_PASSWORD'],
                database=self.conf[dbname+'_DB'],
                charset='utf8',
              )
        elif dbname=='IOT':

                self.server=SSHTunnelForwarder(
                    ssh_address_or_host=(self.conf[dbname + '_SSH_IP'], int(self.conf[dbname +'_SSH_PORT'])),  # 指定ssh登录的跳转机的address，端口号
                    ssh_username=self.conf[dbname + '_SSH_NAME'],  # 跳转机的用户
                    ssh_pkey=self.conf[dbname + '_SSH_PKEY'],  # 私钥路径
                    ssh_password=self.conf[dbname + '_SSH_PASSWORD'],  # 密码(电脑开机密码)
                    remote_bind_address=(self.conf[dbname + '_DB_IP'], 27017)) # mongodb服务器的address，端口号
                self.server.start()
                self.conf[dbname + '_DB_PASSWORD'] = parse.quote(self.conf[dbname + '_DB_PASSWORD'])
                self.url= "mongodb://" + self.conf[dbname + '_DB_NAME']+":" + self.conf[dbname + '_DB_PASSWORD']+'@'+'127.0.0.1'+":" + str(self.server.local_bind_port)+'/iot-dev?authSource=admin&authmechanism=SCRAM-SHA-1&waitQueueTimeoutMS=100'
                self.client = pymongo.MongoClient(self.url)
                self.db = self.client[self.conf[dbname + '_DB']]


    def execute_sql(self,sql):
        '''
        执行sql
        :param sql: 增删改查
        :return:
        '''
        cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)
        result = cursor.execute(sql)
        if sql.lower().startswith("select"):
            return cursor.fetchone()
        else:
            self.db.commit()
            return result

    def execute_mongodb(self,mongodb):
        '''
        执行mongodb
        :param mongodb: 增删改查
        :return:
        '''
        if mongodb.startswith("db"):
            data=eval('self.'+mongodb)
            if type(data)==type({}) or type(data)==type(1):
                data1=data
            else:
                for i in data:
                    data1 = i
                    break
            if isinstance(data1,int):
                result= data1
            else:
                result = data1
            return result
