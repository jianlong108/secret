#!/usr/bin/env python  
# -*- coding:utf-8 _*-
""" 
@author:wangjianlong
@file: GET_GAME_PAN_ODD_DATA.py
@time: 2023/12/02
@contact: jlwang108@gmail.com
@site:  
@software: PyCharm 
"""

import math
import requests
from lxml import etree
from loguru import logger
from colorama import Fore, init
import re
import ast
import random
import traceback
import os

from GetData.MySQLHelper import mysql_insert_game_to_seasonjifen,mysql_insert_game_to_seasonpanlu
from GetData.TIME_TOOL import get_current_timestr_YMDH
from GetData.SOCCER_MODELS import *
from GetData.SOCCER_TOOL import switchHandicap

companydic = {
	"ids": [281, 80, 1129, 82, 81, 90, 104, 16, 370, 110, 499, 474, 432, 517],
	"281": ["365", "英国"],
	"80": ["澳门", "澳门"],
	"115": ["威廉希尔", "英国"],
	"81": ["伟德", "直布罗陀"],
	"82": ["立博", "英国"],
	"1129": ["竞彩", "中国"],
	"90": ["易胜博", "安提瓜和巴布达"],
	"104": ["Interwetten", "塞浦路斯"],
	"16": ["10BET", "英国"],
	"370": ["Oddset", "德国"],
	"110": ["SNAI", "意大利"],
	"499": ["188bet", "马恩岛"],
	"474": ["Sbobet", "英国"],
	"432": ["香港马会", "香港"],
	"517": ["明盛博", "菲律宾"]
}


# result1=html.xpath('//li[@class="item-1"]//text()') #获取li下所有子孙节点的内容
# result=html.xpath('//li/a/@href')  #获取a的href属性
def getOneGameHandiList(gameObj):
	try:
		if not isinstance(gameObj, FootballGame):
			print("传参不正确", gameObj.__class__.__name__)
			return
		# url = 'http://www.310win.com/info/1x2exchange.aspx?id=' + str(soccerid) + '&cids=,' + str(companyid) + ',&type=3'
		# url = 'http://www.310win.com/handicap/' + str(soccerid) + '.html'
		# http://www.310win.com/handicap/2478509.html
		url = f"https://vip.titan007.com/AsianOdds_n.aspx?id={gameObj.soccerID}"
		HEADERS = {
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
			'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
		}
		webpage = requests.get(url, headers=HEADERS)
		webpage.encoding = 'utf-8'
		dom = etree.HTML(webpage.text)
		table_dom = dom.xpath('//table[@id="odds"]')[0]
		tr_list = table_dom.xpath('//tr')
		companies = []
		earlyest_timestamp = 0
		earlyest_company = None
		ori_pan_list = []
		fix_ori_pan_list = []
		now_pan_list = []
		max_handi = 0.0
		max_company = None
		company_365 = None
		min_handi = 0.0
		min_company = None

		# 一般第一个公司就是澳门，判断如果第一个不是澳门 代表澳门没有开盘
		firstCompany = None
		for tr_dom in tr_list:
			dome_list = tr_dom.xpath('.//td[3]/@title')
			if len(dome_list) < 1:
				continue

			# 真TMB坑，需要加个.  https://blog.csdn.net/weixin_44749897/article/details/93637740
			span_dom_right = tr_dom.xpath('.//td[2]/span/@companyid')
			if span_dom_right is not None and len(span_dom_right) > 0:
				# print(type(span_dom_right), span_dom_right)
				name = tr_dom.xpath('.//td[1]//text()')[0]
				# name = [str(s) for s in name]
				name = ''.join([str(s) for s in name])
				# 1
				companyid = tr_dom.xpath('.//td[2]/span/@companyid')[0]
				companyid = ''.join([str(s) for s in companyid])
				oriTime = tr_dom.xpath('.//td[3]/@title')[0]
				oriTime = ''.join([str(s) for s in oriTime])

				orihomeshui = tr_dom.xpath('.//td[3]//text()')[0]
				orihomeshui = ''.join([str(s) for s in orihomeshui])

				oripan = tr_dom.xpath('.//td[4]/@goals')[0]
				oripan = ''.join([str(s) for s in oripan])

				oriawayshui = tr_dom.xpath('.//td[5]//text()')[0]
				oriawayshui = ''.join([str(s) for s in oriawayshui])

				nowhomeshui = tr_dom.xpath('.//td[@oddstype="wholeOdds"][1]//text()')[0]
				nowhomeshui = ''.join([str(s) for s in nowhomeshui])

				nowpan = tr_dom.xpath('.//td[@oddstype="wholeOdds"][2]/@goals')[0]
				nowpan = ''.join([str(s) for s in nowpan])

				nowawayshui = tr_dom.xpath('.//td[@oddstype="wholeOdds"][3]//text()')[0]
				nowawayshui = ''.join([str(s) for s in nowawayshui])
				company = BetCompany(p_gameid=gameObj.soccerID, p_companyid=companyid)
				company.companyTitle = name
				company.oriTimeStr = oriTime
				if '0001-01-01 00:00' != oriTime:
					time_s = time.strptime(oriTime, '%Y-%m-%d %H:%M')
					company.oriTimeStamp = time.mktime(time_s)
					changelist = getOneGameOneCompangHandiChangeDetail(gameObj=gameObj, companyid= companyid, year=time_s.tm_year)
					company.panchangelist = changelist
					if earlyest_company is None:
						earlyest_company = company
						earlyest_timestamp = company.oriTimeStamp

					if earlyest_company is not None and company.oriTimeStamp < earlyest_timestamp:
						earlyest_timestamp = company.oriTimeStamp
						earlyest_company = company
				else:
					print('比赛没有初盘时间')
				company.orignal_Handicap = float(oripan)
				company.orignal_top = orihomeshui
				company.orignal_bottom = oriawayshui
				company.now_Handicap = float(nowpan)

				if firstCompany is None:
					firstCompany = company
					if companyid == '1':
						gameObj.now_aomenHandi = company.now_Handicap
						gameObj.orignal_aomenHandi = company.orignal_Handicap
					else:
						gameObj.haveAomen = False
						return
				if companyid == '8':
					gameObj.now_365Handi = company.now_Handicap
					gameObj.orignal_365Handi = company.orignal_Handicap

				if companyid == '9':
					if math.fabs(float(company.orignal_top) - float(company.orignal_bottom)) > 0.3:
						print("GET_GAME_PAN_ODD 威廉存在水位异常")

				if max_company is None:
					max_company = company
					max_handi = float(oripan)
				if max_company is not None and math.fabs(float(oripan)) > math.fabs(max_handi):
					max_handi = float(oripan)
					max_company = company

				if min_company is None:
					min_company = company
					min_handi = float(oripan)
				if min_company is not None and math.fabs(float(oripan)) < math.fabs(min_handi):
					min_handi = float(oripan)
					min_company = company

				if float(oripan) not in ori_pan_list:
					ori_pan_list.append(float(oripan))

				if float(nowpan) not in now_pan_list:
					now_pan_list.append(float(nowpan))

				company.flip = (float(nowpan) * float(oripan)) < 0
				company.now_top = nowhomeshui
				company.now_bottom = nowawayshui
				company.similerMatchURL = f"https://vip.titan007.com/history/SearchSameAsian.aspx?id={gameObj.soccerID}&companyid={companyid}&l=0&goal={oripan}"
				company.allSamePanURL = f"https://vip.titan007.com/count/goalCount.aspx?t=1&sid={gameObj.soccerID}&cid=1&l=0"
				company.trendURL = f"https://vip.titan007.com/changeDetail/handicap.aspx?id={gameObj.soccerID}&companyID={companyid}&l=0"
				company.homeSamePanURL = f"https://vip.titan007.com/history/SearchAsianByTeamID.aspx?id={gameObj.soccerID}&companyid={companyid}&l=0&teamid={gameObj.homeTeamId}"
				company.similerMatchURL = f"https://vip.titan007.com/history/SearchAsianByTeamID.aspx?id={gameObj.soccerID}&companyid={companyid}&l=0&teamid={gameObj.friendTeamId}"
				companies.append(company)
				# print(name, companyid, oriTime, orihomeshui, oripan, oriawayshui, nowhomeshui, nowpan, nowawayshui)
				# company.print_self()
		if earlyest_company:
			earlyest_company.earlyest = True
			gameObj.earlyestCompany = earlyest_company
		gameObj.yapanCompanies = companies

		fixCompanyKaipanTime(gameObj)
		for company in gameObj.yapanCompanies:
			if str(company.early_fix_change.pan) not in fix_ori_pan_list:
				fix_ori_pan_list.append(str(company.early_fix_change.pan))

		gameObj.fix_orignalHandiList = fix_ori_pan_list
		gameObj.orignalHandiList = ori_pan_list
		gameObj.nowHandiList = now_pan_list
		gameObj.maxHandi = max_handi
		gameObj.maxHandiCompany = max_company
		gameObj.minHandi = min_handi
		gameObj.minHandiCompany = min_company
	except BaseException as e:
		print(e, url, 'getOneGameHandiList')
		traceback.print_exc()

def fixCompanyKaipanTime(p_gameobj):
	try:
		if not isinstance(p_gameobj, FootballGame):
			raise Exception('{}传参不正确'.format(p_gameobj.__class__.__name__))
		if len(p_gameobj.yapanCompanies) < 1:
			raise Exception('亚盘公司数量为空')
		earlyestCompany = p_gameobj.earlyestCompany
		print('最早的：',earlyestCompany.companyTitle,earlyestCompany.panchangelist[0])
		if len(earlyestCompany.panchangelist) < 1:
			print(p_gameobj)
			return
		for company in p_gameobj.yapanCompanies:
			if earlyestCompany.companyID == company.companyID:
				earlyestCompany.early_fix_change = earlyestCompany.panchangelist[0]
				continue
			changedetail = company.panchangelist[0]
			first_time_s = time.strptime(company.panchangelist[0].changetime, "%Y-%m-%d %H:%M")
			first_timestamp = time.mktime(first_time_s)
			for change in earlyestCompany.panchangelist:
				time_s = time.strptime(change.changetime, "%Y-%m-%d %H:%M")
				timestatmp = time.mktime(time_s)
				if first_timestamp >= timestatmp:
					changedetail.upwater = change.upwater
					changedetail.downwater = change.downwater
					changedetail.panstr = change.panstr
				else:
					continue
			company.early_fix_change = changedetail
			# print('fix:',company.early_fix_change)
	except Exception as e:
		print(e)
	finally:
		pass


def getOneGameOneCompangHandiChangeDetail(gameObj, companyid, year=2024):
	# https://vip.titan007.com/changeDetail/handicap.aspx?id=2536570&companyID=9&l=0
	changelist = []
	try:
		if not isinstance(gameObj, FootballGame):
			print("传参不正确", gameObj.__class__.__name__)
			return
		url = f"https://vip.titan007.com/changeDetail/handicap.aspx?id={gameObj.soccerID}&companyID={companyid}&l=0"
		HEADERS = {
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
			'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
		}
		webpage = requests.get(url, headers=HEADERS)
		webpage.encoding = 'GB2312'
		dom = etree.HTML(webpage.text)
		span_dom = dom.xpath('//span[@id="odds2"]')[-1]
		table_dom = span_dom.xpath('//table')[-1]
		trlist_dom = table_dom.xpath('//tr')
		trlist_dom.reverse()
		lastchangetime = None

		for tr_dom in trlist_dom:
			# td_count = tr_dom.xpath('count(.//td)')
			# print(int(td_count))  # 输出: 5
			lasttd = tr_dom.xpath('.//td[last()]//text()')
			state = ''.join(lasttd)
			if state != '即' and state != '早':
				continue

			# 提取第一个 <td> 元素中的文本
			td1 = tr_dom.xpath('.//td[position() = last() - 4]//text()')
			upwater = ''.join(td1)

			# 提取第二个 <td> 元素中的文本
			td2 = tr_dom.xpath('.//td[position() = last() - 3]//text()')
			panstr = ''.join(td2)

			# 提取第三个 <td> 元素中的文本
			td3 = tr_dom.xpath('.//td[position() = last() - 2]//text()')
			downwater = ''.join(td3)

			# 提取第四个 <td> 元素中的文本
			td4 = tr_dom.xpath('.//td[position() = last() - 1]//text()')
			changetime = ''.join(td4)

			onechange = FootballGameHandiChange(gameid=gameObj.soccerID, companyid=companyid)
			onechange.hometeam = gameObj.homeTeam
			onechange.awayteam = gameObj.friendTeam
			onechange.panstr = panstr
			onechange.pan = switchHandicap(panstr)
			onechange.upwater = upwater
			onechange.downwater = downwater
			timestr = f"{year}-{changetime}"
			if changetime == '' or changetime is None:
				continue

			if lastchangetime is not None:
				last_time_s = time.strptime(lastchangetime, '%Y-%m-%d %H:%M')
				time_s = time.strptime(timestr, '%Y-%m-%d %H:%M')
				if time.mktime(time_s) < time.mktime(last_time_s):
					timestr = f"{year+1}-{changetime}"
			onechange.changetime = timestr
			lastchangetime = timestr
			# print(onechange)
			changelist.append(onechange)

	except Exception as e:
		print(e)
	finally:
		return changelist

# TODO: 蓝箭的数据暂时没找到途径
def getOneGameOddListFromLanjian():
	url = f"http://txt.letarrow.com/phone/tx/zqanalysis/cn/89/84/1194898.txt?from=48&_t={str(int(time.time()))}"
	print(url)

	headers = {
		'User-Agent': 'QTimesApp/3.4 (Letarrow.QTimes; build:52; iOS 17.5.1) Alamofire/5.4.3',
		'Accept': '*/*'
	}
	response = requests.get(url, headers=headers)
	if response.ok:
		content_type = response.headers.get('Content-Type')
		# print(content_type)
		if 'text/html' == content_type:
			print(response.content)
		# if 'application/x-protobuf' == content_type:
		# 	resultStr = response.content
		# 	# print(url, resultStr)
		# 	temp_message, typedef = blackboxprotobuf.protobuf_to_json(resultStr)
		# 	# print(temp_message)
		# 	protobufdic = json.loads(temp_message)
		# 	leaguedic = protobufdic.get('3', {})
		# 	gamelist = leaguedic.get('1', [])
		# 	seasonlist = leaguedic.get('2', [])
		# 	if len(gamelist) == 0 or len(seasonlist) == 0:
		# 		print("不存在合法数据")
		# 		return 108
		# 	importantseasonidlist = []
		# 	importantseasoniddic = {}
		# 	gameobjlist = []
		# 	for season in seasonlist:
		# 		if season.get('3', '') == '':
		# 			continue
		# 		importantseasonidlist.append(season.get('1', ''))
		# 		importantseasoniddic[season.get('1', '')] = season.get('2', '')
		#
		# 	for game in gamelist:
		# 		seasonid = game.get('2', '')
		# 		if seasonid not in importantseasonidlist:
		# 			continue
		# 		print(game.get('6', {}).get('2', ''), 'vs', game.get('7', {}).get('2', ''))
		# 		game_id = game.get('1', '0')
		# 		leagueidstr = game.get('2', '0')
		# 		leaguename = importantseasoniddic.get(leagueidstr, '')
		# 		if game_id == '0' or leagueidstr == '0' or leaguename == '':
		# 			continue
		#
		# 		hometeamdic = game.get('6', {})
		# 		if hometeamdic == {}:
		# 			continue
		#
		# 		friendteamdic = game.get('7', {})
		# 		if friendteamdic == {}:
		# 			continue
		# 		gameobj = FootballGame(gameid=int(game_id))
		# 		gameobj.leauge = leaguename
		# 		gameobj.leaugeid = int(leagueidstr)
		# 		# gameobj.round = round
		# 		gameobj.beginTimestamp = int(game.get('4', '0'))
		# 		time_struct = time.localtime(gameobj.beginTimestamp)
		# 		gameobj.beginTime = time.strftime("%Y-%m-%d %H:%M:%S", time_struct)
		# 		gameobj.homeTeamId = int(hometeamdic.get('1', '0'))
		# 		gameobj.friendTeamId = int(friendteamdic.get('1', '0'))
		# 		gameobj.homeTeam = hometeamdic.get('2', '')
		# 		gameobj.friendTeam = friendteamdic.get('2', '')
		# 		gameobj.homeTeamLevel = int(hometeamdic.get('3', '0'))
		# 		gameobj.friendTeamLevel = int(friendteamdic.get('3', '0'))
		# 		gameobj.allHome = int(hometeamdic.get('4', '0'))
		# 		gameobj.allFriend = int(friendteamdic.get('4', '0'))
		# 		gameobj.halfHome = int(hometeamdic.get('5', '0'))
		# 		gameobj.halfFriend = int(friendteamdic.get('5', '0'))
		# 		gameobjlist.append(gameobj)
		# 	return 0, gameobjlist
		else:
			return 0, []
	else:
		print(response)
		return 404, []

def getOneGameOddList(gameObj):
	mailstr = ''
	try:
		if not isinstance(gameObj, FootballGame):
			print("传参不正确", gameObj.__class__.__name__)
			return
		# https://1x2.titan007.com/oddslist/1877964.htm
		# https://op1.titan007.com/oddslist/2467964.htm
		# url = f"https://1x2.titan007.com/oddslist/{gameObj.soccerID}.htm"
		# 生成随机数列表
		random_numbers = [str(random.randint(0, 9)) for _ in range(21)]

		# 将列表转换为字符串
		random_string = ''.join(random_numbers)
		print(Fore.GREEN + f"正在进行 {gameObj.soccerID}")

		companyies = [281, 80, 1129, 82, 81, 90, 104, 16, 370, 110, 499, 474, 432, 517]
		url = f"https://1x2d.titan007.com/{gameObj.soccerID}.js?r={random_string}"
		HEADERS = {
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
			'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
			'Referer': f'https://op1.titan007.com/oddslist/{gameObj.soccerID}.htm',
			'Content-type': 'application/javascript'
		}
		response = requests.get(url, headers=HEADERS, timeout=7)
		if response.status_code == 200:
			js_code = response.text
			# 使用正则表达式提取变量值
			pattern = re.compile(r'var (\w+)\s*=\s*(.*?);', re.DOTALL)
			matches = pattern.findall(js_code)

			# 创建一个字典，用于存储变量名和对应的值
			variables = {}

			# 将提取的变量值转化为 Python 对象
			for match in matches:
				var_name, var_value = match
				try:
					# 尝试使用 ast 模块将字符串转化为 Python 对象
					var_value = ast.literal_eval(var_value)
					variables[var_name] = var_value
				except (ValueError, SyntaxError):
					# 转化失败时，将值保持为字符串
					variables[var_name] = var_value
			oddstr = variables.get('game', [])
			if not oddstr:
				print(f'无法获取对应比赛的欧赔数据{gameObj.soccerID}')
				return
			start_index = oddstr.find('"') + 1
			end_index = oddstr.rfind('"')
			sub_strings = oddstr[start_index:end_index].split('","')

			jingcai = None
			oddset = None
			oddcompanyObjlist = []
			for oneoddstr in sub_strings:
				onecompanyList = oneoddstr.split('|')
				cid = int(onecompanyList[0])
				if cid not in companyies:
					continue
				if '' in onecompanyList:
					print(Fore.RED + f'获取赔率数据不完整 {gameObj.soccerID} {oneoddstr}')
					continue

				company = BetCompany(p_gameid=gameObj.soccerID, p_companyid=cid)
				company.isOdd = True
				company.companyTitle = companydic.get(onecompanyList[0], [onecompanyList[2]])[0]
				company.orignal_winOdd = float(onecompanyList[3])
				company.orignal_drawOdd = float(onecompanyList[4])
				company.orignal_loseOdd = float(onecompanyList[5])
				company.winOdd = float(onecompanyList[10])
				company.drawOdd = float(onecompanyList[11])
				company.loseOdd = float(onecompanyList[12])
				oddcompanyObjlist.append(company)
				if cid == 1129:
					jingcai = company
				elif cid == 370:
					oddset = company
				elif cid == 80:
					gameObj.aomenOddCompany = company
			gameObj.oddCompanies = oddcompanyObjlist
			if jingcai is not None and oddset is not None:
				ishome = jingcai.orignal_winOdd < jingcai.orignal_loseOdd
				'''
				Oddset让球方初赔高于竞彩时
				1.
				西甲、英超、德甲主场让出深盘时，下盘概率高;
				2.
				西甲、英超、德甲主场让出浅盘时，主场胜率高，上盘盈利能力强;
				3.
				英超客场让球方容易赢盘;
				4.
				德甲客场让球方不易打出，下盘占多数。
				'''

				if ishome:
					if oddset.orignal_winOdd > jingcai.orignal_winOdd:
						print(Fore.RED + f"oddset高于竞彩{gameObj}")
						mailstr += f"oddset高于竞彩{gameObj}"
						mailstr += "\n"
						mailstr += "\n"
				else:
					if oddset.orignal_loseOdd > jingcai.orignal_loseOdd:
						print(Fore.RED + f"oddset高于竞彩{gameObj}")
						mailstr += f"oddset高于竞彩{gameObj}"
						mailstr += "\n"
						mailstr += "\n"

	except BaseException as e:
		print(e, gameObj.soccerID,url, oneoddstr)
		traceback.print_exc()
	finally:
		return mailstr


def verify_datetime(datetime_str):
	# 判断输入是否有非法字符或者长度是否为8个数字
	if datetime_str.isdigit() == False or len(datetime_str) != 8:
		print("输入格式不合法！请按照样例格式输入日期！")
		return False

	# 比较日期格式是否正确
	try:
		time.strptime(datetime_str, '%Y%m%d')
		return True
	except ValueError:
		print("输入日期的格式不合法哦，请重新检查")
		return False

def qiutan_get_history_games(daystr="20231125"):
	try:
		if not verify_datetime(daystr):
			return 404, []
		time_s = time.strptime(daystr, '%Y%m%d')
		year = time_s.tm_year
		month = time_s.tm_mon
		url = f"https://bf.titan007.com/football/Over_{daystr}.htm"
		HEADERS = {
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
			'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
		}
		webpage = requests.get(url, headers=HEADERS)
		# webpage.encoding = 'utf-8'
		webpage.encoding = 'gb2312'
		# soup = BeautifulSoup(webpage.content, "html.parser")
		dom = etree.HTML(webpage.text)
		table_dom = dom.xpath('//table[@id="table_live"]')[0]
		# print(type(table_dom), table_dom)
		game_dom_list = table_dom.xpath(".//tr[@sid and not(contains(@style, 'display: none;'))]")
		gameobj_list = []
		for game_dom in game_dom_list:
			homeorder_dom_list = game_dom.xpath('.//td[@align="right"]/span[@name="order"]/font/text()')
			if len(homeorder_dom_list) == 0:
				continue

			awayorder_dom_list = game_dom.xpath('.//td[@align="left"]/span[@name="order"]/font/text()')
			if len(awayorder_dom_list) == 0:
				continue

			score_str_dom = game_dom.xpath('.//td[@style="cursor:pointer;"]/font/text()')
			if len(score_str_dom) == 0:
				continue

			half_score_str_dom = game_dom.xpath('.//td[@align="left"]/following-sibling::td/font/text()')
			if len(half_score_str_dom) == 0:
				continue

			league = game_dom.xpath('.//td[1]/text()')[0]
			league = ''.join([str(s) for s in league])

			tmpleagueid = game_dom.xpath('.//@name')[0]
			tmpleagueid = ''.join([str(s) for s in tmpleagueid])
			leagueid_list = tmpleagueid.split(',')
			# 取列表中的第一个元素
			leagueid = ''.join([str(s) for s in leagueid_list[0]])

			gameid = game_dom.xpath('.//@sid')[0]
			gameid = ''.join([str(s) for s in gameid])

			tmptime = game_dom.xpath('.//td[2]/text()')[0]
			tmptime = ''.join([str(s) for s in tmptime])
			tmptime = tmptime.replace('日', ' ')
			startime = f"{year}-{month}-{tmptime}"
			time_s = time.strptime(startime, '%Y-%m-%d %H:%M')
			startimetimeStamp = time.mktime(time_s)

			homestr = game_dom.xpath('.//td[@align="right"]//text()')[-1]
			hometeam = ''.join([str(s) for s in homestr if str(s) not in ['[', ']']])

			homeorderstr = homeorder_dom_list[0]
			homeorder = ''.join([str(s) for s in homeorderstr if str(s) not in ['[', ']']])

			awaystr = game_dom.xpath('.//td[@align="left"]//text()')[0]
			awayteam = ''.join([str(s) for s in awaystr if str(s) not in ['[', ']']])

			awayorderstr = awayorder_dom_list[0]
			awayorder = ''.join([str(s) for s in awayorderstr if str(s) not in ['[', ']']])

			homescore = score_str_dom[0]
			homescore = ''.join([str(s) for s in homescore if str(s) not in ['[', ']']])
			awayscore = score_str_dom[1]
			awayscore = ''.join([str(s) for s in awayscore if str(s) not in ['[', ']']])

			half_homescore = half_score_str_dom[0]
			half_homescore = ''.join([str(s) for s in half_homescore if str(s) not in ['[', ']']])
			half_awayscore = half_score_str_dom[1]
			half_awayscore = ''.join([str(s) for s in half_awayscore if str(s) not in ['[', ']']])

			gameobj = FootballGame(gameid=int(gameid))
			gameobj.leauge = league
			gameobj.leaugeid = int(leagueid)
			gameobj.homeTeam = hometeam
			gameobj.friendTeam = awayteam
			if homeorder.isdigit():
				gameobj.homeTeamLevel = int(homeorder)
			else:
				gameobj.homeTeamLevelStr = homeorder

			if awayorder.isdigit():
				gameobj.friendTeamLevel = int(awayorder)
			else:
				gameobj.friendTeamLevelStr = awayorder
			gameobj.allHome = int(homescore)
			gameobj.allFriend = int(awayscore)
			gameobj.halfHome = int(half_homescore)
			gameobj.halfFriend = int(half_awayscore)
			gameobj.beginTimestamp = startimetimeStamp
			gameobj.beginTime = startime
			gameobj.beginTimestamp = startimetimeStamp
			gameobj_list.append(gameobj)
		return 0, gameobj_list
	except BaseException as e:
		print(e)
		traceback.print_exc()
		return 300, []

def parseJifen(season='2023-2024', leagueid=36, leaguename='英超', minCount=6, subleagueid=None, writeFile=False,writeSQL=False):
	# url = f"http://api.letarrow.com/ios/Phone/FBDataBase/LeaguePoints.aspx?lang=0&pointsKind=0&sclassid=36&season=2023-2024&subid=0&from=48&_t=1702645393"
	timestr = get_current_timestr_YMDH()
	print(Fore.GREEN + f"正在进行{season} {timestr}")
	# https://zq.titan007.com/jsData/matchResult/2023-2024/s16_98.js?version=2023121517
	if subleagueid is not None:
		url = f'https://zq.titan007.com/jsData/matchResult/{season}/s{leagueid}_{subleagueid}.js?version={timestr}'
	else:
		url = f'https://zq.titan007.com/jsData/matchResult/{season}/s{leagueid}.js?version={timestr}'
	HEADERS = {
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
		'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
		'Content-type': 'application/javascript',
		'referer': f'https://zq.titan007.com/cn/League.aspx?/SclassID={leagueid}'
	}
	response = requests.get(url, headers=HEADERS, timeout=7)
	if response.status_code == 200:
		js_code = response.text
		# 使用正则表达式提取变量值
		pattern = re.compile(r'var (\w+)\s*=\s*(.*?);', re.DOTALL)
		matches = pattern.findall(js_code)

		# 创建一个字典，用于存储变量名和对应的值
		variables = {}

		# 将提取的变量值转化为 Python 对象
		for match in matches:
			var_name, var_value = match
			try:
				# 尝试使用 ast 模块将字符串转化为 Python 对象
				var_value = ast.literal_eval(var_value)
				variables[var_name] = var_value
			except (ValueError, SyntaxError):
				# 转化失败时，将值保持为字符串
				variables[var_name] = var_value
		teamArr = variables.get('arrTeam', [])
		totoalJifenArr = variables.get('totalScore', [])
		HomeJifenArr = variables.get('homeScore', [])
		guestJifenArr = variables.get('guestScore', [])
		halfScoreArr = variables.get('halfScore', [])
		halfHomeScoreArr = variables.get('homeHalfScore', [])
		halfGuestScoreArr = variables.get('guestHalfScore', [])

		if len(teamArr) == 0:
			for var_name, var_value in variables.items():
				print(f"数据出现异常 {var_name}: {var_value}")
			return
		teamlist = []
		for one in teamArr:
			team = TeamPoints()
			team.season = season
			team.league = leaguename
			team.leagueid = leagueid
			team.teamID = one[0]
			team.teamName = one[1]
			teamlist.append(team)

		for p in totoalJifenArr:
			team = next((team for team in teamlist if team.teamID == p[2]), None)
			if team:
				team.ranking = p[1]
				team.gamecount = p[4]
				team.winCount = p[5]
				team.drawCount = p[6]
				team.loseCount = p[7]
				team.goalcount = p[8]
				team.losegoalcount = p[9]
				team.goaloffset = p[10]
				team.winRate = float(p[11])
				team.drawRate = float(p[12])
				team.loseRate = float(p[13])
				team.avgGoal = p[14]
				team.avgLostGoal = p[15]
				team.points = p[16]
		if writeFile:
			teamlist.sort(key=lambda x: x.ranking)
			try:
				for team in teamlist:
					with open(os.path.expanduser(f'~/Desktop/{season}_{leagueid}.md'), "a+", encoding='utf-8') as f:
						f.write(f"## {team.ranking} {team.teamName}:主场盘路\n")
						homeratestrlist = getOneTeamPanlu(season=season, teamid=team.teamID, leagueid=leagueid, lutype=1)
						f.writelines(homeratestrlist)
						time.sleep(2)
						f.write(f"### {team.teamName}:客场盘路\n")
						friendratestrlist = getOneTeamPanlu(season=season, teamid=team.teamID, leagueid=leagueid, lutype=2)
						f.writelines(friendratestrlist)
						time.sleep(2)
						f.close()
			except BaseException as e:
				print(e)
			finally:
				pass
			return
		for p in HomeJifenArr:
			team = next((team for team in teamlist if team.teamID == p[1]), None)
			if team:
				obj = TeamPointsUnit()
				obj.type = 1
				obj.league = team.league
				obj.leagueid = team.leagueid
				obj.season = team.season
				obj.teamName = team.teamName
				obj.teamID = team.teamID
				obj.ranking = p[0]
				obj.gamecount = p[2]
				obj.winCount = p[3]
				obj.drawCount = p[4]
				obj.loseCount = p[5]
				obj.goalcount = p[6]
				obj.losegoalcount = p[7]
				obj.goaloffset = p[8]
				obj.winRate = float(p[9])
				obj.drawRate = float(p[10])
				obj.loseRate = float(p[11])
				obj.avgGoal = p[12]
				obj.avgLostGoal = p[13]
				obj.points = p[14]
				team.homePoints = obj
		for p in guestJifenArr:
			team = next((team for team in teamlist if team.teamID == p[1]), None)
			if team:
				obj = TeamPointsUnit()
				obj.type = 2
				obj.league = team.league
				obj.leagueid = team.leagueid
				obj.season = team.season
				obj.teamName = team.teamName
				obj.teamID = team.teamID
				obj.ranking = p[0]
				obj.gamecount = p[2]
				obj.winCount = p[3]
				obj.drawCount = p[4]
				obj.loseCount = p[5]
				obj.goalcount = p[6]
				obj.losegoalcount = p[7]
				obj.goaloffset = p[8]
				obj.winRate = float(p[9])
				obj.drawRate = float(p[10])
				obj.loseRate = float(p[11])
				obj.avgGoal = p[12]
				obj.avgLostGoal = p[13]
				obj.points = p[14]
				team.awayPoints = obj
		for p in halfScoreArr:
			team = next((team for team in teamlist if team.teamID == p[1]), None)
			if team:
				obj = TeamPointsUnit()
				obj.type = 3
				obj.league = team.league
				obj.leagueid = team.leagueid
				obj.season = team.season
				obj.teamName = team.teamName
				obj.teamID = team.teamID
				obj.ranking = p[0]
				obj.gamecount = p[2]
				obj.winCount = p[3]
				obj.drawCount = p[4]
				obj.loseCount = p[5]
				obj.goalcount = p[6]
				obj.losegoalcount = p[7]
				obj.goaloffset = p[8]
				obj.winRate = float(p[9])
				obj.drawRate = float(p[10])
				obj.loseRate = float(p[11])
				obj.avgGoal = p[12]
				obj.avgLostGoal = p[13]
				obj.points = p[14]
				team.halfPoints = obj
		for p in halfHomeScoreArr:
			team = next((team for team in teamlist if team.teamID == p[1]), None)
			if team:
				obj = TeamPointsUnit()
				obj.type = 4
				obj.league = team.league
				obj.leagueid = team.leagueid
				obj.season = team.season
				obj.teamName = team.teamName
				obj.teamID = team.teamID
				obj.ranking = p[0]
				obj.gamecount = p[2]
				obj.winCount = p[3]
				obj.drawCount = p[4]
				obj.loseCount = p[5]
				obj.goalcount = p[6]
				obj.losegoalcount = p[7]
				obj.goaloffset = p[8]
				obj.winRate = float(p[9])
				obj.drawRate = float(p[10])
				obj.loseRate = float(p[11])
				obj.avgGoal = p[12]
				obj.avgLostGoal = p[13]
				obj.points = p[14]
				team.halfHomePoints = obj
		for p in halfGuestScoreArr:
			team = next((team for team in teamlist if team.teamID == p[1]), None)
			if team:
				obj = TeamPointsUnit()
				obj.type = 5
				obj.league = team.league
				obj.leagueid = team.leagueid
				obj.season = team.season
				obj.teamName = team.teamName
				obj.teamID = team.teamID
				obj.ranking = p[0]
				obj.gamecount = p[2]
				obj.winCount = p[3]
				obj.drawCount = p[4]
				obj.loseCount = p[5]
				obj.goalcount = p[6]
				obj.losegoalcount = p[7]
				obj.goaloffset = p[8]
				obj.winRate = float(p[9])
				obj.drawRate = float(p[10])
				obj.loseRate = float(p[11])
				obj.avgGoal = p[12]
				obj.avgLostGoal = p[13]
				obj.points = p[14]
				team.halfAwayPoints = obj

		if len(teamlist) == 0:
			print(Fore.RED + '没有数据 结束')
			return
		for t in teamlist:
			print(t, t.homePoints, t.awayPoints, t.halfPoints, t.halfHomePoints, t.halfAwayPoints)
			if t.homePoints is not None and t.homePoints.gamecount >= minCount:
				if writeSQL:
					mysql_insert_game_to_seasonjifen(t)
				else:
					print('不更新数据库')
				pass
			else:
				print(Fore.RED + '该队伍参赛比赛太少，没有价值')
				continue
	else:
		print(Fore.RED + f'parsePanlu出错:{url}')
		traceback.print_exc()

# 欧冠小组赛6场
def parsePanlu(season='2022-2023', leagueid=8, leaguename='德甲', minCount=3, alertThresholdValue=80, writeSQL= True):

	random_number = random.random()
	# print(Fore.GREEN + f"parsePanlu 正在进行{season} {random_number}")
	url = f'https://zq.titan007.com/jsData/letGoal/{season}/l{leagueid}.js?flesh={random_number}'
	HEADERS = {
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
		'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
		'Content-type': 'application/javascript',
		'referer': f'https://zq.titan007.com/cn/League/{leagueid}.html'
	}
	response = requests.get(url, headers=HEADERS, timeout=7)
	logger.debug(url,HEADERS)
	specialDic = {}
	if response.status_code == 200:
		js_code = response.text

		# 使用正则表达式提取变量值
		pattern = re.compile(r'var (\w+)\s*=\s*(.*?);', re.DOTALL)
		matches = pattern.findall(js_code)

		# 创建一个字典，用于存储变量名和对应的值
		variables = {}

		# 将提取的变量值转化为 Python 对象
		for match in matches:
			var_name, var_value = match
			try:
				# 尝试使用 ast 模块将字符串转化为 Python 对象
				var_value = ast.literal_eval(var_value)
				variables[var_name] = var_value
			except (ValueError, SyntaxError):
				# 转化失败时，将值保持为字符串
				variables[var_name] = var_value
				logger.error("转换失败",var_value)
		teamArr = variables.get('arrTeam', [])
		totoalPanluArr = variables.get('TotalPanLu', [])
		HomePanLuArr = variables.get('HomePanLu', [])
		awayPanLuArr = variables.get('GuestPanLu', [])
		TotalHalfPanLuArr = variables.get('TotalHalfPanLu', [])
		HomeHalfPanLuArr = variables.get('HomeHalfPanLu', [])
		GuestHalfPanLuArr = variables.get('GuestHalfPanLu', [])
		# 全场让球盘路数据统计
		addUpArr = variables.get('addUp', [])
		# 半场让球盘路数据统计
		addUpHalfArr = variables.get('addUpHalf', [])

		if len(teamArr) == 0:
			for var_name, var_value in variables.items():
				logger.error(f"数据出现异常 teamArr==0: {var_name}: {var_value}")
			return
		teamlist = []
		for t in teamArr:
			team = TeamPanLu()
			team.season = season
			team.belongLeagueName = leaguename
			team.belongLeagueID = leagueid
			team.teamID = t[0]
			team.teamName = t[1]
			teamlist.append(team)

		def handlePanluDetail(panluArr, panluType):
			for p in panluArr:
				oneteam = next((team for team in teamlist if team.teamID == p[1]), None)
				if oneteam:
					oneteam.ranking = p[0]
					detail = TeamPanLuDetail()
					detail.season = oneteam.season
					detail.belongLeagueName = oneteam.belongLeagueName
					detail.belongLeagueID = oneteam.belongLeagueID
					detail.teamID = oneteam.teamID
					detail.teamName = oneteam.teamName
					detail.type = panluType
					detail.numberOfGame = p[2]
					detail.upNumberOfGame = p[3]
					detail.drawNumberOfGame = p[4]
					detail.downNumberOfGame = p[5]
					detail.winNumberOfGame = p[6]
					detail.zouNumberOfGame = p[7]
					detail.loseNumberOfGame = p[8]
					# [9]是净值
					detail.offset = p[9]
					detail.winRate = p[10]
					detail.drawRate = p[11]
					detail.loseRate = p[12]
					oneteam.rounds = detail.numberOfGame
					luKey = ''
					if panluType == 1:
						oneteam.allDetail = detail
						luKey = "全部盘路"
					elif panluType == 2:
						oneteam.homeDetail = detail
						luKey = "主场盘路"
					elif panluType == 3:
						oneteam.awayDetail = detail
						luKey = "客场盘路"
					elif panluType == 4:
						oneteam.halfAllDetail = detail
						luKey = "半场盘路"
					elif panluType == 5:
						oneteam.halfHomeDetail = detail
						luKey = "半场主场盘路"
					elif panluType == 6:
						oneteam.halfAwayDetail = detail
						luKey = "半场客场盘路"
					else:
						pass

					logger.debug(f"赛季:{season} 联赛:{leaguename} {luKey}:{detail}")
					if detail.winRate >= alertThresholdValue or detail.loseRate >= alertThresholdValue:
						curlist = specialDic.get(luKey, None)
						if curlist is not None:
							curlist.append(detail)
							specialDic[luKey] = curlist
						else:
							specialDic[luKey] = [detail]

		handlePanluDetail(totoalPanluArr,1)
		handlePanluDetail(HomePanLuArr,2)
		handlePanluDetail(awayPanLuArr,3)
		handlePanluDetail(TotalHalfPanLuArr,4)
		handlePanluDetail(HomeHalfPanLuArr,5)
		handlePanluDetail(GuestHalfPanLuArr,6)

		winsutibetlist = addUpArr[6]
		for i in range(len(winsutibetlist) - 1):
			team = next((team for team in teamlist if team.teamID == winsutibetlist[i + 1]), None)
			if team:
				team.suitableWinBet = True

		losesutibetlist = addUpArr[7]
		for i in range(len(losesutibetlist) - 1):
			team = next((team for team in teamlist if team.teamID == losesutibetlist[i + 1]), None)
			if team:
				team.suitableLoseBet = True

		homewinsutibetlist = addUpArr[8]
		for i in range(len(homewinsutibetlist) - 1):
			team = next((team for team in teamlist if team.teamID == homewinsutibetlist[i + 1]), None)
			if team:
				team.suitableHomeWinBet = True

		homelosesutibetlist = addUpArr[9]
		for i in range(len(homelosesutibetlist) - 1):
			team = next((team for team in teamlist if team.teamID == homelosesutibetlist[i + 1]), None)
			if team:
				team.suitableHomeLoseBet = True

		awaywinsutibetlist = addUpArr[10]
		for i in range(len(awaywinsutibetlist) - 1):
			team = next((team for team in teamlist if team.teamID == awaywinsutibetlist[i + 1]), None)
			if team:
				team.suitableAwayWinBet = True

		awaylosesutibetlist = addUpArr[11]
		for i in range(len(awaylosesutibetlist) - 1):
			team = next((team for team in teamlist if team.teamID == awaylosesutibetlist[i + 1]), None)
			if team:
				team.suitableAwayLoseBet = True

		for t in teamlist:
			if (t.allDetail is not None and t.allDetail.numberOfGame >= minCount) or \
				(t.homeDetail is not None and t.homeDetail.numberOfGame >= minCount) or \
				(t.awayDetail is not None and t.awayDetail.numberOfGame >= minCount) or \
				(t.halfAllDetail is not None and t.halfAllDetail.numberOfGame >= minCount) or \
				(t.halfHomeDetail is not None and t.halfHomeDetail.numberOfGame >= minCount) or \
				(t.halfAwayDetail is not None and t.halfAwayDetail.numberOfGame >= minCount):
				if writeSQL:
					mysql_insert_game_to_seasonpanlu(t)
					logger.debug(f"更新数据库 {t}")
				else:
					logger.debug("不更新数据库")
			else:
				logger.info("该队伍参赛比赛太少，没有价值")
				continue
	else:
		logger.error(f'parsePanlu出错:{url}')
		traceback.print_exc()


	return specialDic

# 获取一个队伍的盘路历史
# lutype :0全场盘路 1主场盘路 2客场盘路 3半场盘路 4半场主场盘路 5半场客场盘路
def getOneTeamPanlu(season='2022-2023', teamid=46, leagueid=37, lutype=0):
	url = f"https://zq.titan007.com/cn/Team/HandicapDetail.aspx?sclassid={leagueid}&teamid={teamid}&matchseason={season}&halfOrAll={lutype}"
	HEADERS = {
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
		'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
		'Content-type': 'text/html; charset=utf-8',
		'Referer': f'https://zq.titan007.com/cn/SubLeague/{season}/{leagueid}_87.html'
	}
	webpage = requests.get(url, headers=HEADERS)
	webpage.encoding = 'utf-8'
	dom = etree.HTML(webpage.text)

	script_text = dom.xpath("//script[last()]/text()")[0]
	pattern = re.compile(r'var (\w+)\s*=\s*(.*?);', re.DOTALL)
	matches = pattern.findall(script_text)

	# 创建一个字典，用于存储变量名和对应的值
	variables = {}

	# 将提取的变量值转化为 Python 对象
	for match in matches:
		var_name, var_value = match
		try:
			# 尝试使用 ast 模块将字符串转化为 Python 对象
			var_value = ast.literal_eval(var_value)
			variables[var_name] = var_value
		except (ValueError, SyntaxError):
			# 转化失败时，将值保持为字符串
			variables[var_name] = var_value
	gamelist = variables.get("handicapDetail", [])
	gameobjlist = []
	wincount = 0
	losecount = 0
	if gamelist is None or len(gamelist) == 0:
		return
	for game in gamelist:
		# [2225177, 37, '#cc3300', '2023/05/08 22:00', 46, 64, '3-0', '2-0', '英冠', '英冠', 'ENG LCH', '伯恩利', '般尼', 'Burnley','卡迪夫城', '卡迪夫城', 'Cardiff City', '赢', '一球/球半|1/1.5', 'เบิร์นลี่ย์', 'คาร์ดิฟฟ์ซิตี้']
		gameobj = BaseFootballGame(gameid=game[0])
		gameobj.leaugeid = game[1]
		gameobj.beginTime = game[3]
		gameobj.homeTeamId = game[4]
		gameobj.friendTeamId = game[5]
		gameobj.allHome = int(game[6].split('-')[0])
		gameobj.allFriend = int(game[6].split('-')[1])
		gameobj.halfHome = int(game[7].split('-')[0])
		gameobj.halfFriend = int(game[7].split('-')[1])
		gameobj.homeTeam = game[11]
		gameobj.friendTeam = game[14]
		gameobj.panResult = game[17]
		gameobjlist.append(gameobj)

	count = 0
	gameobjlist.reverse()
	panlustrlist = []

	for gameobj in gameobjlist:
		if lutype == 1 or lutype == 4:
			if gameobj.homeTeamId != teamid:
				continue
		elif lutype == 2 or lutype == 5:
			if gameobj.friendTeamId != teamid:
				continue
		else:
			pass
		count += 1
		if gameobj.panResult == '赢':
			wincount += 1
		elif gameobj.panResult == '输':
			losecount += 1
		else:
			pass
		onet = f"{season}{gameobj.homeTeam}:{gameobj.friendTeam} {gameobj.panResult}/{wincount}/{losecount} 净胜{wincount - losecount} 胜率:{round(wincount / count, 2)} 输率:{round(losecount / count, 2)}"

		if count > 6 and (wincount/count > 0.7 or losecount/count > 0.7):
			onet = f"<span style=\"color:red;\">{onet}</span>"

		panlustrlist.append(onet)
		panlustrlist.append("\n")

	return panlustrlist

if __name__ == '__main__':
	game = FootballGame(2399250)
	# getOneGameOneCompangHandiChangeDetail(game, 1, year=2023)
	getOneGameHandiList(game)
	# qiutan_get_history_games()
	# parsePanlu(season='2021-2022',leagueid=36,leaguename='英超')
	# getOneGameOddList(game)
	# print(getOneTeamPanlu(season='2023-2024', teamid=20, leagueid=36, lutype=1))
	# parseJifen(season="2021-2022",leagueid=17,leaguename='荷乙',subleagueid=94)
	# parseJifen(season="2022-2023", leagueid=31, leaguename='西甲', writeFile=True)
	# getOneGameOddListFromLanjian()
