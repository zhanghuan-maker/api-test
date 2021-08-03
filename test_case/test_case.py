#!/user/bin/env python
#coding:utf-8
'''
@project : shell
@author  : zhanghuan
#@file   : test_case.py
#@ide    : PyCharm
#@time   : 2021-06-21 15:27:00
'''
#coding=utf-8

import unittest
from ddt import *
from core.readExcel import *
from core.testBase import *
import jsonpath
from core.functions import *
from db_operate.mysql_operate import Operate
from conf.settings import *
from runCase import *
import threading


@ddt
class Test(unittest.TestCase):

    api_data=read_excel(Case)
    # 全局变量池
    saves = {}
    saves['IMAGE_PATH'] = IMAGE_PATH
    mongo_db_connect = Operate('IOT')


    #识别${key}的正则表达式
    EXPR = '\$\{(.*?)\}'
    #识别函数助手
    FUNC_EXPR = "__.*?\(.*?\)'/';m "

    def save_date(self,source,key,jexpr):
        '''
        提取参数并保存至全局变量池
        :param source: 目标字符串
        :param key: 全局变量池的key
        :param jexpr: jsonpath表达式
        :return:
        '''

        value = jsonpath.jsonpath(source,jexpr)[0]
        if key.startswith("authorization"):
            self.saves[key] = "Bearer "+ str(value)
            logger.info('保存 {}=>{} 到全局变量池'.format(key, "Bearer "+ str(value)))
        else:
            self.saves[key] = value
            logger.info('保存 {}=>{} 到全局变量池'.format(key,str(value)))


    def build_param(self,string):
        '''
        识别${key}并替换成全局变量池的value,处理__func()函数助手
        :param str: 待替换的字符串
        :return:
        '''
        #遍历所有取值并做替换
        keys = re.findall(self.EXPR, string)

        for key in keys:
            value = self.saves.get(key)
            string = string.replace('${'+key+'}',str(value))


        #遍历所有函数助手并执行，结束后替换
        funcs = re.findall(self.FUNC_EXPR, string)
        for func in funcs:
            fuc = func.split('__')[1]
            fuc_name = fuc.split("(")[0]
            fuc = fuc.replace(fuc_name,fuc_name.lower())
            value = eval(fuc)
            string = string.replace(func,str(value))
        return string


    def execute_setup_sql(self,db_connect,setup_sql):
        '''
        执行setup_sql,并保存结果至参数池
        :param db_connect: mysql数据库实例
        :param setup_sql: 前置sql
        :return:
        '''
        for sql in [i for i in setup_sql.split(";") if i != ""]:
            result = db_connect.execute_sql(sql)
            logger.info("执行前置sql====>{}，影响条数:{}".format(sql,result))
            if sql.lower().startswith("select"):
                logger.info("执行前置sql====>{}，获得以下结果集:{}".format(sql,result))
                # 获取所有查询字段，并保存至公共参数池
                for key in result.keys():
                    self.saves[key] = str(result[key])
                    logger.info("保存 {}=>{} 到全局变量池".format(key, result[key]))


    def execute_setup_mongodb(self,db_connect,setup_sql):
        '''
        执行setup_mongodb,并保存结果至参数池
        :param db_connect: mysql数据库实例
        :param setup_sql: 前置sql
        :return:
        '''
        for mongodb in [i for i in setup_sql.split(";") if i != ""]:
            result = db_connect.execute_mongodb(mongodb)
            logger.info("执行前置mongodb====>{}，影响条数:{}".format(mongodb,result))
            if mongodb.startswith("db"):
                logger.info("执行前置mongodb====>{}，获得以下结果集:{}".format(mongodb,result))
                # 获取所有查询字段，并保存至公共参数池
                if isinstance(result,int):
                    self.saves['totalNumber'] = result
                else:
                    for key in result.keys():
                        self.saves[key] = result[key]
                        logger.info("保存 {}=>{} 到全局变量池".format(key, result[key]))


    def execute_teardown_sql(self,db_connect,teardown_sql):
        '''
        执行teardown_sql,并保存结果至参数池
        :param db_connect: mysql数据库实例
        :param teardown_sql: 后置sql
        :return:
        '''
        for sql in [i for i in teardown_sql.split(";") if i != ""]:
            result = db_connect.execute_sql(sql)
            logger.info("执行后置sql====>{}，影响条数:{}".format(sql, result))
            if sql.lower().startswith("select"):
                logger.info("执行后置sql====>{}，获得以下结果集:{}".format(sql, result))
                # 获取所有查询字段，并保存至公共参数池
                for key in result.keys():
                    self.saves[key] = result[key]
                    logger.info("保存 {}=>{} 到全局变量池".format(key, result[key]))


    def execute_teardown_mongodb(self,db_connect,teardown_sql):
        '''
        执行teardown_sql,并保存结果至参数池
        :param db_connect: mysql数据库实例
        :param teardown_sql: 后置sql
        :return:
        '''
        for mongodb in [i for i in teardown_sql.split(";") if i != ""]:
            result = db_connect.execute_sql(mongodb)
            logger.info("执行后置mongodb====>{}，影响条数:{}".format(mongodb,result))
            if mongodb.startswith("db"):
                logger.info("执行后置mongodb====>{}，获得以下结果集:{}".format(mongodb,result))
                # 获取所有查询字段，并保存至公共参数池
                if isinstance(result,int):
                    self.saves['totalNumber'] = result
                else:
                    for key in result.keys():
                        self.saves[key] = result[key]
                        logger.info("保存 {}=>{} 到全局变量池".format(key, result[key]))


    def ttestonework(self,ONE_WORKER_NUM,LOOP_SLEEP,url, method, headers, cookies, params, body, file, verify, saves,ERROR_NUM):
        '''一次并发处理单个任务'''
        i = 0
        while i < int(ONE_WORKER_NUM):
            i += 1
            if ONE_WORKER_NUM==1:
                self.press_work(url, method, headers, cookies, params, body, file, verify, saves)
            else:
                try:
                    self.press_work(url, method, headers, cookies, params, body, file, verify, saves)
                except Exception:
                    ERROR_NUM=ERROR_NUM+1
            time.sleep(LOOP_SLEEP)


    def run_work(self,THREAD_NUM,ONE_WORKER_NUM,LOOP_SLEEP,url, method, headers, cookies, params, body, file, verify,saves):
        '''使用多线程进程并发测试'''
        t1 = time.time()#并发测试开始时间
        Threads = []
        ERROR_NUM=0
        for i in range(int(THREAD_NUM)):
            t = threading.Thread(target=self.ttestonework(ONE_WORKER_NUM,LOOP_SLEEP,url, method, headers, cookies, params, body, file, verify, saves,ERROR_NUM), name="T" + str(i))
            t.setDaemon(True)#守护线程
            Threads.append(t)

        for t in Threads:
            t.start()#启动线程
        for t in Threads:
            t.join()#等待至线程终止
        t2 = time.time()#并发测试结束时间

        if THREAD_NUM!=1:
            self.request.api_log_pressure(THREAD_NUM, ONE_WORKER_NUM, url, t1, t2,ERROR_NUM)


    def press_work(self,url, method, headers, cookies, params, body, file, verify, saves):

        res = None

            # 判断接口请求类型
        if method.upper() == 'GET':
            res = self.request.get_request(url=url, params=params, headers=headers, cookies=cookies)

        elif method.upper() == 'POST':
            res = self.request.post_request(url=url, headers=headers, cookies=cookies, params=params, data=body,files=file)

        elif method.upper() == 'DELETE':
            res = self.request.delete_request(url=url, headers=headers, cookies=cookies, params=params)

        if method.upper() == 'UPLOAD':
            res = self.request.upload_request(url=url, headers=headers, cookies=cookies, params=params, data=body,
                                              files=file)
        else:
            # 待扩充，如PUT方法
            pass
        res.encoding = 'utf-8'

        if saves:
            # 遍历saves
            for save in saves.split(";"):
                # 切割字符串 如 key=$.data
                if save.split("=")[1].startswith("$."):
                    key = save.split("=")[0]
                    jsp = save.split("=")[1]
                    self.save_date(res.json(), key, jsp)
                elif save.split("=")[1].startswith("text"):
                    key = save.split("=")[0]
                    self.saves[key] = "Bearer " + str(res.text)

        if verify:
            # 遍历verify:
            verify = self.build_param(verify)
            for ver in verify.split(";"):
                if ver.startswith("$.") and '=' in ver:
                    expr = ver.split("=")[0]
                    actual = str(jsonpath.jsonpath(res.json(), expr)[0])
                    expect = ver.split("=")[1]
                    self.request.assertEquals(actual, expect)
                elif ver.startswith("status"):
                    actual = str(res.status_code)
                    expect = ver.split("=")[1]
                    self.request.assertEquals(actual, expect)
                elif ver.startswith("time"):
                    actual = res.elapsed.total_seconds() * 1000
                    expect = int(ver.split("<")[1])
                    self.request.assertLessThan(actual, expect)
                elif ver.startswith("textIn"):
                    expect = ver.split("=")[1]
                    self.request.assertIn(expect, res.text)
                elif ver.startswith("resHeader"):
                    expect = ver.split("=")[1]
                    self.request.assertIn(expect, res.headers)
                elif ver.startswith("$.") and '>' in ver:
                    expr = ver.split(">")[0]
                    actual = str(jsonpath.jsonpath(res.json(), expr)[0])
                    expect = ver.split(">")[1]
                    self.request.assertMoreThan(actual, expect)
                elif ver.startswith("resCount"):
                    expect = ver.split("=")[1]
                    self.request.assertEquals(len(res.json()), int(expect))

                # actual = re.findall(expr,res.text)[0]


    @classmethod
    def setUpClass(cls):
        # 实例化测试基类，自带cookie保持
        cls.request = BaseTest()


    @classmethod
    def tearDownClass(cls):
        pass

    @data(*api_data)
    @unpack
    def test_(self,descrption, url, method, headers, cookies, params, body, file, verify, saves, dbtype, dbname, setup_sql, teardown_sql,THREAD_NUM,ONE_WORKER_NUM,LOOP_SLEEP):



        if THREAD_NUM=='':
            THREAD_NUM=1
        if ONE_WORKER_NUM=='':
            ONE_WORKER_NUM=1
        if LOOP_SLEEP=='':
            LOOP_SLEEP=0

        environment = os.getenv('Environment')
        if environment=="dev":
            for i in range(len(DEV)):
                self.saves[list(DEV.keys())[i]]=list(DEV.values())[i]

        elif environment=="qa":
            for i in range(len(QA)):
                self.saves[list(QA.keys())[i]]=list(QA.values())[i]

        elif environment=="uat":
            for i in range(len(UAT)):
                self.saves[list(UAT.keys())[i]]=list(UAT.values())[i]


        logger.info("用例描述====>"+descrption)
        url = self.build_param(url)
        headers = self.build_param(headers)
        params = self.build_param(params)
        body = self.build_param(body)
        file = self.build_param(file)

        setup_sql = self.build_param(setup_sql)
        teardown_sql = self.build_param(teardown_sql)
        params = eval(params) if params else params
        headers = eval(headers) if headers else headers
        cookies = eval(cookies) if cookies else cookies
        body = eval(body) if body else body
        if 'content-type' in headers.keys():
            if headers['content-type'] == 'application/json;charset=UTF-8':
                body =json.dumps(body)
        file = eval(file) if file else file
        # 判断数据库类型,暂时只有mysql和mongodb

        db_connect = None
        # mongo_db_connect = None


        if dbtype.lower() == "mysql":
            db_connect = Operate(dbname)

        # if dbtype.lower() == "mongodb":
        #     mongo_db_connect = Operate(dbname)



        if db_connect and dbtype.lower() == "mysql":
            self.execute_setup_sql(db_connect,setup_sql)

        if self.mongo_db_connect and dbtype.lower() == "mongodb":
            self.execute_setup_mongodb(self.mongo_db_connect, setup_sql)

        self.run_work(THREAD_NUM,ONE_WORKER_NUM,LOOP_SLEEP,url, method, headers, cookies, params, body, file, verify,saves)

        if db_connect and dbtype.lower() =="mysql":
            # 执行teardown_sql
            self.execute_teardown_sql(db_connect,teardown_sql)

        if self.mongo_db_connect and dbtype.lower() =="mongodb":
            # 执行teardown_sql
            self.execute_teardown_mongodb(self.mongo_db_connect,teardown_sql)

        #最后关闭数据库连接
        if db_connect and dbtype.lower() =="mysql":
            db_connect.db.close()
        #
        # if mongo_db_connect and dbtype.lower() =="mongodb":
        #     mongo_db_connect.client.close()


        if dbname=='OPS' and db_connect:
            db_connect.server.close()


        # if dbname=='IOT' and mongo_db_connect:
        #     mongo_db_connect.server.close()




