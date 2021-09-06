
import datetime
import time

def timeCaculate():

    timeCaculateDict = {}

    # n天前的时间
    for i in range(200):
       key = 'day'+str(i)+'_before'
       timeCaculateDict[key] = timeDay(i)

    # n小时前时间
    for i in range(25):
       key = 'hour'+str(i)+'_before'
       timeCaculateDict[key] = timeHour(i)

    return (timeCaculateDict)

def timeDay(number):
    today = datetime.date.today()
    value = today - datetime.timedelta(days=number)
    value = int(time.mktime(time.strptime(str(value), '%Y-%m-%d')))
    value = value * 1000
    return (value)

def timeHour(number):
    timeNow = time.time()
    value = timeNow-number*60*60
    value = int(round(value*1000))
    return (value)

