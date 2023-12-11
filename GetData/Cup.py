#!/usr/bin/env python  
# -*- coding:utf-8 _*-
""" 
@author:wangjianlong
@file: Cup.py 
@time: 2023/11/30
@contact: jlwang108@gmail.com
@site:  
@software: PyCharm 
"""

import requests
import time
import blackboxprotobuf
import os

if __name__ == '__main__':
	headers = {
		'User-Agent': 'QTimesApp/3.0 (Letarrow.QTimes; build:39; iOS 17.1.0) Alamofire/5.4.',
		'cookie': 'aiappfrom=48'
	}
	# 获取欧洲杯赛程概括 包括外围赛
	season = '2002-2004'
	timestr = str(int(time.time()))
	url = f"http://api.letarrow.com/ios/Phone/FBDataBase/CupInfo.aspx?id=67&lang=0&season={season}&from=48&_t={timestr}"
	try:
		response = requests.get(url, headers=headers)
		if response.ok:
			content_type = response.headers.get('Content-Type')
			print(content_type)
			if 'application/x-protobuf' == content_type:
				resultStr = response.content
				print(url, resultStr)
				temp_message, typedef = blackboxprotobuf.protobuf_to_json(resultStr)
				print(temp_message)
				print(typedef)
				p = os.path.expanduser('~/Desktop/2004欧洲杯.json')
				with open(p, 'w+') as f:
					f.write(temp_message)
					f.close()
	except Exception as e:
		print('获取杯赛数据', url, e)
