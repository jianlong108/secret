#!/usr/bin/env python  
# -*- coding:utf-8 _*-
""" 
@author:wangjianlong
@file: TIME_TOOL.py 
@time: 2023/12/15
@contact: jlwang108@gmail.com
@site:  
@software: PyCharm 
"""

import time

def get_current_timestr_YMDHms():
	# 时间戳
	timestamp = time.time()  # 2021-12-09 00:00:00
	# 使用time.localtime()方法将时间戳转换为struct_time对象
	time_struct = time.localtime(timestamp)
	# 使用time.strftime()方法将struct_time对象格式化为字符串
	formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time_struct)
	return formatted_time

def get_current_timestr_YMDH():
	# 时间戳
	timestamp = time.time()  # 2021-12-09 00:00:00
	# 使用time.localtime()方法将时间戳转换为struct_time对象
	time_struct = time.localtime(timestamp)
	# 使用time.strftime()方法将struct_time对象格式化为字符串
	formatted_time = time.strftime('%Y%m%d%H', time_struct)
	return formatted_time

if __name__ == '__main__':
	print(get_current_timestr_YMDH(),get_current_timestr_YMDHms())