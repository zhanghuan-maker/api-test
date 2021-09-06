
import datetime
import time

# 今天日期
today = datetime.date.today()

# 0天前的时间
day0_before = today - datetime.timedelta(days=0)
day0_before = int(time.mktime(time.strptime(str(day0_before), '%Y-%m-%d')))
day0_before = day0_before * 1000

# 1天前的时间
day1_before = today - datetime.timedelta(days=1)
day1_before = int(time.mktime(time.strptime(str(day1_before), '%Y-%m-%d')))
day1_before = day1_before * 1000

# 10天前的时间
day10_before = today - datetime.timedelta(days=10)
day10_before = int(time.mktime(time.strptime(str(day10_before), '%Y-%m-%d')))
day10_before = day10_before * 1000

# 30天前的时间
day30_before = today - datetime.timedelta(days=30)
day30_before = int(time.mktime(time.strptime(str(day30_before), '%Y-%m-%d')))
day30_before = day30_before * 1000

# 60天前的时间
day60_before = today - datetime.timedelta(days=60)
day60_before = int(time.mktime(time.strptime(str(day60_before), '%Y-%m-%d')))
day60_before = day60_before * 1000

# 59天前的时间
day59_before = today - datetime.timedelta(days=59)
day59_before = int(time.mktime(time.strptime(str(day59_before), '%Y-%m-%d')))
day59_before = day59_before * 1000

# 90天前的时间
day90_before = today - datetime.timedelta(days=90)
day90_before = int(time.mktime(time.strptime(str(day90_before), '%Y-%m-%d')))
day90_before = day90_before * 1000

# 当前时间
now = int(round(time.time() * 1000))



