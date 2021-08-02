#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests, time, json, threading, random,os


class Presstest(object):


    def __init__(self, url, headers):
        self.url = url
        self.headers = headers

    def testinterface(self):
        '''压测接口'''

        res = requests.get(url=url,headers=headers)  # 第一个url指get方法的参数，第二个url指上一行我们定义的接口地址
        print(res.text)

    def testonework(self):
        '''一次并发处理单个任务'''
        i = 0
        while i < ONE_WORKER_NUM:
            i += 1
            self.testinterface()
            time.sleep(LOOP_SLEEP)

    def run(self):
        '''使用多线程进程并发测试'''
        t1 = time.time()#并发测试开始时间
        Threads = []

        for i in range(THREAD_NUM):
            t = threading.Thread(target=self.testonework, name="T" + str(i))
            t.setDaemon(True)#守护线程
            Threads.append(t)

        for t in Threads:
            t.start()#启动线程
        for t in Threads:
            t.join()#等待至线程终止
        t2 = time.time()#并发测试结束时间

        print("===============压测结果===================")
        print("URL:", self.url)
        print("任务数量:", THREAD_NUM, "*", ONE_WORKER_NUM, "=", THREAD_NUM * ONE_WORKER_NUM)
        print("总耗时(秒):", t2 - t1)
        print("每次请求耗时(秒):", (t2 - t1) / (THREAD_NUM * ONE_WORKER_NUM))
        print("每秒承载请求数:", 1 / ((t2 - t1) / (THREAD_NUM * ONE_WORKER_NUM)))
        print("错误数量:", ERROR_NUM)


if __name__ == '__main__':
    url = 'https://b2b-qa.digitalshell.com.cn/api/bi/factories'

    headers={'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICIyQVFXRmNtR0pRQ1F4T3k3TWJlMUxxT2Exb21PbEJSbUtKZm5FaUdta19nIn0.eyJqdGkiOiIwYjA4YjFmZC1mZmQ5LTQzMzItOThmOC1kMmQ0MjY1Zjk0OGYiLCJleHAiOjE2Mjc1NjY3MzcsIm5iZiI6MCwiaWF0IjoxNjI3NTQ1MTM3LCJpc3MiOiJodHRwczovL3Nzby5kaWdpdGFsc2hlbGwuY29tLmNuL2F1dGgvcmVhbG1zL3NoZWxsLXNzby1xYSIsInN1YiI6ImQxMmI5ZDUxLTBlNjYtNGUxMS1hYjk2LTVkMjJlNjc5MmUwNSIsInR5cCI6IkJlYXJlciIsImF6cCI6Imx1YmVtYXN0ZXItYmktZnJvbnRlbmQiLCJub25jZSI6Ijc1OTg0NDhjLTVlYzYtNDMyMi04NjFkLWJhOTcyNTM0NzFmMCIsImF1dGhfdGltZSI6MTYyNzU0NTEzNiwic2Vzc2lvbl9zdGF0ZSI6ImE0MmRjODVjLTllOWYtNDI3Zi1hZWM5LTkyOGJhZGJhYThmZCIsImFjciI6IjEiLCJhbGxvd2VkLW9yaWdpbnMiOlsiaHR0cHM6Ly9iMmItcWEuZGlnaXRhbHNoZWxsLmNvbS5jbiJdLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsibG9naXN0aWNzaHViLXdheWJpbGwiLCJsdWJlbWFzdGVyLWJpIiwibG9naXN0aWNzaHViLWFkbWluIiwib2ZmbGluZV9hY2Nlc3MiLCJsb2dpc3RpY3NodWIiLCJsb2dpc3RpY3NodWItdXBsb2FkIiwidW1hX2F1dGhvcml6YXRpb24iLCJzaGVsbF9lbXBsb3llZSIsIm5vbl9zaGVsbF9lbXBsb3llZSJdfSwic2NvcGUiOiJvcGVuaWQgZW1haWwgcHJvZmlsZSIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwicHJlZmVycmVkX3VzZXJuYW1lIjoiYWRtaW4iLCJsb2NhbGUiOiJ6aC1DTiJ9.Ov73imYmfU4ZNPMDvSYLR4imzazp_Z8NQwgAnWX9BFkEPREoI1_VUVUnuIA5idzPMr_exsOAzUORjXRPXN_hUvc9PcntBb5MpUjKqX4_DBssA3AuEXGJcziH9i2zMwtXocNAAjnZrV0OMgFbN1VVuuvPKj20MmnalJJoKHYEqed2j3giFLI9DP4L0rHBOT-w_PcvS93l4rHf8tCgrSDLVMXflTZumaCWuMMnZySIY2Rxi_gPGjTnSeMUi0MsvRlGH4vqQrvEVRbMDdMwaw_o_4-2O5wzb6UYvmAMbwHHfDkXmRsD5kVlHAyzaXCwYD0-HkAn0WIf1Kb25huHv5-kgA','content-type':'application/json;charset=UTF-8'}
    THREAD_NUM = 5  # 并发线程总数
    ONE_WORKER_NUM = 2  # 每个线程的循环次数
    LOOP_SLEEP = 0.1  # 每次请求时间间隔(秒)
    ERROR_NUM = 0  # 出错数

    obj = Presstest(url=url, headers=headers)
    obj.run()
    print(os.getcwd())
