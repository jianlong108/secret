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
import json
from GetData.TIME_TOOL import get_current_timestr_YMDH
from colorama import Fore, init
import re
import ast


def getCupSeasonGamelist(season='2022-2023', leagueid=103, leaguename='欧冠', minCount=6, subleagueid=None):
	# url = https://zq.titan007.com/jsData/matchResult/2022-2023/c103.js?version=2023121823
	timestr = get_current_timestr_YMDH()
	print(Fore.GREEN + f"正在进行{season} {timestr}")
	url = f'https://zq.titan007.com/jsData/matchResult/{season}/c{leagueid}.js?version={timestr}'

	HEADERS = {
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
		'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
		'Content-type': 'application/javascript',
		'referer': f'https://zq.titan007.com/cn/CupMatch/{season}/{leagueid}.html'
	}
	response = requests.get(url, headers=HEADERS, timeout=7)
	if response.status_code == 200:
		js_code = response.text
		print('数据：', js_code)
		# 使用正则表达式提取变量值
		pattern = re.compile(r'var (\w+)\s*=\s*(.*?);', re.DOTALL)
		matches = pattern.findall(js_code)

		# 创建一个字典，用于存储变量名和对应的值
		variables = {}

		# 将提取的变量值转化为 Python 对象
		for match in matches:
			var_name, var_value = match
			try:
				var_value = ast.literal_eval(var_value)
				variables[var_name] = var_value
			except (ValueError, SyntaxError):
				variables[var_name] = var_value

		pattern = re.compile(r'jh\["([^"]+)"\]\s*=\s*(.*?);', re.DOTALL)
		matches = pattern.findall(js_code)
		for match in matches:
			var_name, var_value = match
			try:
				var_value = ast.literal_eval(var_value)
				variables[var_name] = var_value
				print(var_name)
			except (ValueError, SyntaxError):
				variables[var_name] = var_value
		print(variables)
	# teamArr = variables.get('arrTeam', [])
	# totoalJifenArr = variables.get('arrCupKind', [])
	# print(variables)
	# HomeJifenArr = variables.get('homeScore', [])
	# guestJifenArr = variables.get('guestScore', [])
	# halfScoreArr = variables.get('halfScore', [])
	# halfHomeScoreArr = variables.get('homeHalfScore', [])
	# halfGuestScoreArr = variables.get('guestHalfScore', [])


if __name__ == '__main__':
	# getCupSeasonGamelist()
	# # 欧冠   已完成 103
	# _league_id = 103
	# # _sub_league_id = 94
	# _league_name = '欧冠'
	# headers = {
	# 	'User-Agent': 'QTimesApp/3.0 (Letarrow.QTimes; build:39; iOS 17.1.0) Alamofire/5.4.',
	# 	'cookie': 'aiappfrom=48'
	# }
	# timestr = str(int(time.time()))
	# url = f"http://api.letarrow.com/pcf/bfmatch/api/database/v1/leaguedetail?kind=1&lang=0&sid={_league_id}&_t={timestr}"
	# try:
	# 	response = requests.get(url, headers=headers)
	# 	if response.ok:
	# 		content_type = response.headers.get('Content-Type')
	# 		# print(content_type)
	# 		if 'application/x-protobuf' == content_type:
	# 			resultStr = response.content
	# 			print(url, resultStr)
	# 			temp_message, typedef = blackboxprotobuf.protobuf_to_json(resultStr)
	# 			print(temp_message)
	# 			leaguedic = json.loads(temp_message)
	# 			league_id = int(leaguedic.get('1', '0'))
	# 			if league_id != _league_id:
	# 				raise ValueError("联赛id异常")
	#
	# 			leaguename = leaguedic.get('2', '')
	# 			seasons = leaguedic.get('4', [])
	# 			for s in seasons:
	# 				print(s)
				# parsePanlu(season=s,leagueid=league_id,leaguename=_league_name)
				# parseJifen(season=s, leagueid=league_id, leaguename=_league_name, subleagueid=_sub_league_id)
				# time.sleep(8)
	# except Exception as e:
	# 	print('获取杯赛数据', url, e)

	headers = {
		'User-Agent': 'QTimesApp/3.0 (Letarrow.QTimes; build:39; iOS 17.1.0) Alamofire/5.4.',
		'cookie': 'aiappfrom=48'
	}
	# 获取欧洲杯赛程概括 包括外围赛
	# season = '2002-2004'
	#67 欧洲杯
	#103 欧冠
	leagueID = 103
	season = '2022-2023'
	timestr = str(int(time.time()))
	url = f"http://api.letarrow.com/ios/Phone/FBDataBase/CupInfo.aspx?id={103}&lang=0&season={season}&from=48&_t={timestr}"
	try:
		response = requests.get(url, headers=headers)
		if response.ok:
			content_type = response.headers.get('Content-Type')
			print(content_type)
			if 'application/x-protobuf' == content_type:
				resultStr = response.content
				print(url, resultStr)
				temp_message, typedef = blackboxprotobuf.protobuf_to_json(resultStr)
				p = os.path.expanduser(f'~/Desktop/{season}欧冠.json')
				with open(p, 'w+') as f:
					f.write(temp_message)
					f.close()
				protobufdic = json.loads(temp_message)
	except Exception as e:
		print('获取杯赛数据', url, e)
