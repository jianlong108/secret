#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from datetime import datetime,timedelta

"""
time
表示日常所用时间的类，是用C实现的内嵌类。
功能比较简单，但效率高。表示的时间范围有限1970年1月1日到2038年1月19日。
"""

"""
当前时间
返回的一个float型，以一个固定时间epoch(1970年1月1日0时起经过的秒数)
因为time终究是以float型来表示的，所以对于timespan的问题，基本就成了数字问题。
"""
now = time.time()
print now

"""
使用localtime 返回一个time结构，
其中包括tm_year,tm_mon,tm_mday,tm_hour,tm_min,tm_sec,tm_wday,tm_yday,tm_isdst=0 夏令时间标志
tm_wday为周几，0是周一，6是周日
"""
now = time.localtime(now)
print now
#如果是返回当前时间，可以简单的写成
print time.localtime().tm_year
#这个返回UTC时间
print time.gmtime()


"""
转成字符串
%y 两位数的年份表示（00-99）
%Y 四位数的年份表示（000-9999）
%m 月份（01-12）
%d 月内中的一天（0-31）
%H 24小时制小时数（0-23）
%I 12小时制小时数（01-12）
%M 分钟数（00=59）
%S 秒（00-59）

%a 本地简化星期名称
%A 本地完整星期名称
%b 本地简化的月份名称
%B 本地完整的月份名称
%c 本地相应的日期表示和时间表示
%j 年内的一天（001-366）
%p 本地A.M.或P.M.的等价符
%U 一年中的星期数（00-53）星期天为星期的开始
%w 星期（0-6），星期天为星期的开始
%W 一年中的星期数（00-53）星期一为星期的开始
%x 本地相应的日期表示
%X 本地相应的时间表示
%Z 当前时区的名称
%% %号本身
"""
print '当前时间:字符串 ' + time.strftime("%Y-%m-%d %H:%M:%S",now)
#如果打印当前时间，同样也可以简单的写成
strtime = time.strftime("%Y-%m-%d %H:%M:%S")
print '当前时间:字符串 ' + strtime

"""
字符串转成time结构
"""
print time.strptime(strtime, "%Y-%m-%d %H:%M:%S")

"""
用tuple构建一个time结构
分别是年、月、日、小时、分、秒，后面两个都是0就好，自动计算出来。最后一个写成0
"""
past = (2010, 11, 12, 13, 14, 15,0,0,0)
time.localtime(time.mktime(past))

# ================================================================
# ================================================================

"""
datetime的功能强大
能支持0001年到9999年
"""

"""
当前时间
返回的是一个datetime类型
now方法有个参数tz，设置时区类型。如果没有和方法today的效果一样
"""
now = datetime.now()
#UTC时间
print datetime.utcnow()
attrs = [
("year","年"),('month',"月"),("day","日"),('hour',"小时"),( 'minute',"分"),( 'second',"秒"),( 'microsecond',"毫秒"),(
'min',"最小"),( 'max',"最大"),
]
for k,v in attrs:
   print "now.%s = %s #%s" % (k,getattr(now, k),v)

"""
返回一个time结构
"""
print '返回一个time结构 :'
print now.timetuple()


# 返回一个date类型
print now.date()

"""
返回一个time类型
http://www.cnblogs.com/goodspeed/archive/2011/11/07/python_date_time.html
"""
print now.time()

"""
当前星期几。星期一是0，星期于是6
注意这里是方法，不是属性哦。
"""
print now.weekday()

"""
当前星期几。星期一是1，星期于是7
注意这里是方法，不是属性哦。
"""
print now.isoweekday()

"""
修改当前时间。比如修改成当月1号
"""
now = now.replace(day=1)
print '修改当前时间: '
print now

"""
timedelta代表两个datetime之间的时间差
"""
now = datetime.now()
past = datetime(2017,10,10,15,30,0,0)

timespan = now - past
#这会得到一个负数

attrs = [
("days","日"),( 'seconds',"秒"),( 'microseconds',"毫秒")
#('min',"最小"),( 'max',"最大"),
]
for k,v in attrs:
    print "timespan.%s = %s #%s" % (k,getattr(timespan, k),v)

"""
总共相差的秒数
.之前的是秒数.之后的毫秒数
"""
print timespan.total_seconds()

"""
实例化一个timespan
请注意它的参数顺序
def __new__(cls, days=None, seconds=None, microseconds=None, milliseconds=None, minutes=None, hours=None, weeks=None):
"""
timespan = timedelta(days=1)
tomorrow = now + timespan #返回的是datetime型
print tomorrow

yesterday = now - timespan
print yesterday

timespan = timespan * 2 #还可以乘哦。代表二倍
yesterday = now - timespan
print yesterday

#增加一个月
from calendar import monthrange

print now + timedelta(days=monthrange(now.year,now.month)[1])

# ================================================================
# ================================================================