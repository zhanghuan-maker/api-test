#!/user/bin/env python
#coding:utf-8
'''
@project : shell
@author  : zhanghuan
#@file   : test_case.py
#@ide    : PyCharm
#@time   : 2021-06-21 15:27:00
'''


from core.generate_yaml import *
from db_operate.mysql_operate import Operate
from core.readExcel import *
from core.testBase import *
from ddt import *
import unittest
import jsonpath
import threading
import time
import yaml
from core.time_caculate import *


@ddt
class Test(unittest.TestCase):

    #变量值置空
    saves_eve={}
    #局部变量标记
    saves_eve_flag={}

    #识别${key}变量的正则表达式
    EXPR = '\$\{(.*?)\}'
    #识别函数助手
    FUNC_EXPR = "__.*?\(.*?\)'/';m "

    #读取excel中的api_data
    api_data=read_excel(Case)

    #mogodb的数据库连接默认直接连上
    mongo_db_connect = Operate('IOT')

    def save_data_eve(self,source,key,jexpr,testcase):
        '''
        提取参数并保存至变量池
        :param source: 目标字符串
        :param key: 全局变量池的key
        :param jexpr: jsonpath表达式
        :param testcase: 测试集名
        :return:
        '''

        #防止创建第一个变量时出错
        if testcase not in self.saves_eve.keys():
            self.saves_eve[testcase] = {}
        #保存变量
        value = jsonpath.jsonpath(source,jexpr)[0]
        if key.startswith("authorization"):
            self.saves_eve[testcase][key] = "Bearer "+ str(value)
        else:
            self.saves_eve[testcase][key] = value
        #打印日志

        logger.info('保存 {}=>{} 到局部变量池'.format(key, self.saves_eve[testcase][key]))


    def delete_date_eve(self,saves_eve,saves_eve_flag,testcase):
        '''
        释放局部变量
        :return:
        '''
        keyss = list(saves_eve_flag[testcase].keys())
        for i in keyss:
            del saves_eve[testcase][i]
            del saves_eve_flag[testcase][i]


    def build_param(self,string,testcase):
        '''
        识别${key}并替换成全局变量池的value,处理__func()函数助手
        :param string: 待替换的字符串
        :return:
        '''
        #遍历所有并做替换
        keys = re.findall(self.EXPR, string)
        for key in keys:
            value = self.saves_eve[testcase].get(key)
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


    def execute_sql(self,db_connect,sqlds,testcase):
        '''
        执行sql,并保存结果至参数池
        :param db_connect: mysql数据库实例
        :param sqlds: sql查询语句
        :return:
        '''
        for sql in [i for i in sqlds.split(";") if i != ""]:
            result = db_connect.execute_sql(sql)
            logger.info("执行sql====>{}，影响条数:{}".format(sql,result))
            if sql.lower().startswith("select"):
                logger.info("执行sql====>{}，获得以下结果集:{}".format(sql,result))
                # 获取所有查询字段，并保存至参数池
                for key in result.keys():
                    self.saves_eve[testcase][key] = str(result[key])
                    if testcase not in self.saves_eve_flag.keys():
                        self.saves_eve_flag[testcase]={}
                    self.saves_eve_flag[testcase][key] = str(result[key])
                    logger.info("保存 {}=>{} 到局部变量池".format(key, result[key]))


    def execute_mongodb(self,db_connect,mongodbds,testcase):
        '''
        执行mongodb,并保存结果至参数池
        :param db_connect: mongodb数据库实例
        :param mongodbds: mongodb查询语句
        :return:
        '''
        for mongodb in [i for i in mongodbds.split(";") if i != ""]:
            result = db_connect.execute_mongodb(mongodb)
            logger.info("执行mongodb====>{}，影响条数:{}".format(mongodb,result))
            if mongodb.startswith("db"):
                logger.info("执行mongodb====>{}，获得以下结果集:{}".format(mongodb,result))
                # 获取所有查询字段，并保存至参数池
                if testcase not in self.saves_eve_flag.keys():
                    self.saves_eve_flag[testcase] = {}
                if isinstance(result,int):
                    self.saves_eve[testcase]['totalNumber'] = result
                    self.saves_eve_flag[testcase]['totalNumber'] = result
                    logger.info("保存 {}=>{} 到局部变量池".format('totalNumber', result))
                else:
                    for key in result.keys():
                        self.saves_eve[testcase][key] = result[key]
                        self.saves_eve_flag[testcase][key] = result[key]
                        logger.info("保存 {}=>{} 到局部变量池".format(key, result[key]))


    def verify_process(self,verifyds,testcase):
        verify = self.build_param(verifyds, testcase)
        for ver in verify.split(";"):
            if ver.startswith("$.") and '=' in ver:
                expr = ver.split("=")[0]
                actual = str(jsonpath.jsonpath(res.json(), expr)[0])
                expect = ver.split("=")[1]
                self.request.assertEquals(actual, expect)
            elif ver.startswith("$.") and '!~' in ver:
                expr = ver.split("!~")[0]
                actual = str(jsonpath.jsonpath(res.json(), expr)[0])
                expect = ver.split("!~")[1]
                self.request.assertnotEquals(actual, expect)
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
            elif ver.startswith("res.json()") and '=' in ver:
                expect = ver.split("=")[1]
                actual = ver.split("=")[0]
                self.request.assertEqualsValue(eval(actual), expect)
            elif ver.startswith("res.json()") and '!~' in ver:
                expect = ver.split("=")[1]
                actual = ver.split("=")[0]
                self.request.assertNotEqualsValue(eval(actual), expect)

    def ttestonework(self,ONE_WORKER_NUM,LOOP_SLEEP,url, method, headers, cookies, params, body, file, verify, saves,after_verify,ERROR_NUM,testcase):
        '''一次并发处理单个任务'''
        i = 0
        while i < int(ONE_WORKER_NUM):
            i += 1
            if ONE_WORKER_NUM == 1:
                self.press_work(url, method, headers, cookies, params, body, file, verify, saves,testcase)
            else:
                try:
                    self.press_work(url, method, headers, cookies, params, body, file, verify, saves,testcase)
                except Exception:
                    ERROR_NUM = ERROR_NUM+1
            time.sleep(LOOP_SLEEP)


    def run_work(self,THREAD_NUM,ONE_WORKER_NUM,LOOP_SLEEP,url, method, headers, cookies, params, body, file, verify,saves,after_verify,testcase):
        '''使用多线程进行并发测试'''
        t1 = time.time()#并发测试开始时间
        Threads = []
        ERROR_NUM=0
        for i in range(int(THREAD_NUM)):
            t = threading.Thread(target=self.ttestonework(ONE_WORKER_NUM,LOOP_SLEEP,url, method, headers, cookies, params, body, file, verify, saves,after_verify,ERROR_NUM,testcase), name="T" + str(i))
            t.setDaemon(True)#守护线程
            Threads.append(t)

        for t in Threads:
            t.start()#启动线程
        for t in Threads:
            t.join()#等待至线程终止
        t2 = time.time()#并发测试结束时间

        if THREAD_NUM!=1:
            self.request.api_log_pressure(THREAD_NUM, ONE_WORKER_NUM, url, t1, t2,ERROR_NUM)


    def press_work(self,url, method, headers, cookies, params, body, file, verify, saves,testcase):

        global res
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

        if saves and res.status_code<=201:

            # 遍历saves
            for save in saves.split(";"):
                # 切割字符串 如 key=$.data
                if save.split("=")[1].startswith("$."):
                    self.save_data_eve(res.json(), save.split("=")[0], save.split("=")[1],testcase)
                elif save.split("=")[1].startswith("text"):
                    self.saves_eve[testcase] = {}
                    self.saves_eve[testcase][save.split("=")[0]] = "Bearer " + str(res.text)
                else:
                    self.saves_eve[testcase] = {}
                    self.saves_eve[testcase][save.split("=")[0]] = self.saves_eve[testcase][save.split("=")[1]]

        if verify:
            self.verify_process(verify,testcase)


    @classmethod
    def setUpClass(cls):
        # 实例化测试基类，自带cookie保持
        cls.request = BaseTest()


    @classmethod
    def tearDownClass(cls):
        pass

    @data(*api_data)
    @unpack
    def test_(self,testcase,descrption, url, method, headers, cookies, params, body, file, verify, saves,after_verify,after_saves, dbtype, dbname, setup_sql, teardown_sql,THREAD_NUM,ONE_WORKER_NUM,LOOP_SLEEP):

        # 读取yaml文件
        yamlinsex = open('./conf/'+Case+'/global_variable.yaml', 'r', encoding='utf-8')
        data = yaml.load(yamlinsex)

        DEV,QA,UAT,PROD = data['DEV'][0],data['QA'][0],data['UAT'][0],data['PROD'][0]

        if THREAD_NUM == '':
            THREAD_NUM = 1
        if ONE_WORKER_NUM == '':
            ONE_WORKER_NUM = 1
        if LOOP_SLEEP == '':
            LOOP_SLEEP = 0

        #生成常用时间戳
        timeCaculateDict=timeCaculate()

        #环境配置参数保存至全局变量
        environment = os.getenv('Environment')
        if testcase not in self.saves_eve.keys():
            self.saves_eve[testcase] = {}
        if environment == "dev":
            for i in range(len(DEV)):
                self.saves_eve[testcase][list(DEV.keys())[i]]=list(DEV.values())[i]
        elif environment=="qa":
            for i in range(len(QA)):
                self.saves_eve[testcase][list(QA.keys())[i]]=list(QA.values())[i]
        elif environment=="uat":
            for i in range(len(UAT)):
                self.saves_eve[testcase][list(UAT.keys())[i]]=list(UAT.values())[i]
        elif environment=="prod":
            for i in range(len(PROD)):
                self.saves_eve[testcase][list(PROD.keys())[i]]=list(PROD.values())[i]

        for i in range(len(timeCaculateDict)):
            self.saves_eve[testcase][list(timeCaculateDict.keys())[i]] = list(timeCaculateDict.values())[i]

        logger.info("用例描述====>"+descrption)

        # 判断数据库类型,暂时只有mysql和mongodb
        setup_sql = self.build_param(setup_sql, testcase)
        db_connect = None
        if dbtype.lower() == "mysql":
            db_connect = Operate(dbname)
        if db_connect and dbtype.lower() == "mysql":
            self.execute_sql(db_connect,setup_sql,testcase)
        if self.mongo_db_connect and dbtype.lower() == "mongodb":
            self.execute_mongodb(self.mongo_db_connect, setup_sql,testcase)


        url = self.build_param(url,testcase)
        headers = self.build_param(headers,testcase)
        params = self.build_param(params,testcase)
        body = self.build_param(body,testcase)
        file = self.build_param(file,testcase)


        teardown_sql = self.build_param(teardown_sql,testcase)
        params = eval(params) if params else params
        headers = eval(headers) if headers else headers
        cookies = eval(cookies) if cookies else cookies
        body = eval(body) if body else body

        if 'content-type' in headers.keys():
            if headers['content-type'] == 'application/json;charset=UTF-8':
                body =json.dumps(body)
        file = eval(file) if file else file




        self.run_work(THREAD_NUM,ONE_WORKER_NUM,LOOP_SLEEP,url, method, headers, cookies, params, body, file, verify,saves,after_verify,testcase)



        if db_connect and dbtype.lower() =="mysql":
            self.execute_sql(db_connect,teardown_sql,testcase)
        if self.mongo_db_connect and dbtype.lower() =="mongodb":
            self.execute_mongodb(self.mongo_db_connect,teardown_sql,testcase)

        if after_saves and res.status_code<=201:
            # 遍历saves
            for save in after_saves.split(";"):
                # 切割字符串 如 key=$.data
                if save.split("=")[1].startswith("$."):
                    self.save_data_eve(res.json(), save.split("=")[0], save.split("=")[1],testcase)
                elif save.split("=")[1].startswith("text"):
                    self.saves_eve[testcase]={}
                    self.saves_eve[testcase][save.split("=")[0]] = "Bearer " + str(res.text)

        if after_verify:
            self.verify_process(after_verify,testcase)

        #最后关闭数据库连接
        if db_connect and dbtype.lower() =="mysql":
            db_connect.db.close()
        if dbname=='OPS' and db_connect:
            db_connect.server.close()
        #释放变量
        if testcase in self.saves_eve_flag.keys():
            if self.saves_eve_flag[testcase]!={}:
                self.delete_date_eve(self.saves_eve,self.saves_eve_flag,testcase)
        #
        # if mongo_db_connect and dbtype.lower() =="mongodb":
        #     mongo_db_connect.client.close()
        # if dbname=='IOT' and mongo_db_connect:
        #     mongo_db_connect.server.close()



