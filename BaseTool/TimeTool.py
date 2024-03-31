#!/usr/bin/env python  
# -*- coding:utf-8 _*-
""" 
@author:wangjianlong
@file: TimeTool.py 
@time: 2024/03/31
@contact: jlwang108@gmail.com
@site:  
@software: PyCharm 
"""
import time
from datetime import datetime

def get_current_timestr_YMDH():
	# 时间戳
	timestamp = time.time()  # 2021-12-09 00:00:00
	# 使用time.localtime()方法将时间戳转换为struct_time对象
	time_struct = time.localtime(timestamp)
	# 使用time.strftime()方法将struct_time对象格式化为字符串
	formatted_time = time.strftime('%Y%m%d%H', time_struct)
	return formatted_time

# t = "2020-10-31 12:44:27"
def is_early_time_for_now(time_str=''):
	# 获取当前时间戳 秒
	nowstamp = time.time()
	# millNow = int(round(nowstamp * 1000))
	# 将字符串形式的时间转换为时间元组
	t = time.strptime(time_str, "%Y-%m-%d %H:%M:%S")
	t = time.mktime(t)
	# t = int(t)
	# 1604119467.0
	# print(t)
	# print(nowstamp)

	# 比较日期时间
	if t < nowstamp:
		return True
	elif t > nowstamp:
		return False
	else:
		return True


if __name__ == '__main__':
	print(get_current_timestr_YMDH())
	print(is_early_time_for_now("2020-10-31 12:44:27"))