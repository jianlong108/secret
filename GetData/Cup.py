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
from GetData.SOCCER_MODELS import *
from GetData.GET_GAME_PAN_ODD_DATA import *
from colorama import Fore, init
import re
import ast

def getSubCupSeasonGamelist(season='2022-2023', leagueID=103, leaguename='欧冠',subid='',subname=''):
	s_headers = {
		'User-Agent': 'QTimesApp/3.0 (Letarrow.QTimes; build:39; iOS 17.1.0) Alamofire/5.4.',
		'cookie': 'aiappfrom=48'
	}
	suburl = f"http://api.letarrow.com/ios/Phone/FBDataBase/CupInfo.aspx?groupid={subid}&id={leagueID}&lang=0&season={season}&from=48&_t={str(int(time.time()))}"
	sub_response = requests.get(suburl, headers=s_headers)
	sub_content_type = sub_response.headers.get('Content-Type')
	gameobjlist = []
	if sub_response.ok and 'application/x-protobuf' == sub_content_type:
		subResultStr = sub_response.content
		print(suburl)
		message, subtypedef = blackboxprotobuf.protobuf_to_json(subResultStr)
		pro_gamedic = json.loads(message)
		maybe_gamelist = pro_gamedic.get('3', {}).get('3', None)
		if maybe_gamelist is None:
			print(Fore.RED + f"{pro_gamedic}")
			return []

		gamediclist = []
		if isinstance(maybe_gamelist, list):
			for groupdic in maybe_gamelist:
				groupgamelist = groupdic.get('2', [])
				gamediclist.extend(groupgamelist)
		else:
			gamelist = maybe_gamelist.get('2', None)
			if isinstance(gamelist, dict):
				gamediclist.append(gamelist)
			elif isinstance(gamelist, list):
				gamediclist.extend(gamelist)
		for onegamedic in gamediclist:
			game_id = int(onegamedic.get('1', '0'))
			gameobj = FootballGame(gameid=game_id)
			gameobj.season = season
			gameobj.leauge = leaguename + subname
			gameobj.leaugeid = leagueID
			gameobj.beginTimestamp = int(onegamedic.get('2', '0'))
			time_struct = time.localtime(gameobj.beginTimestamp)
			gameobj.beginTime = time.strftime("%Y-%m-%d %H:%M:%S", time_struct)
			gameobj.homeTeamId = int(onegamedic.get('3', '0'))
			gameobj.friendTeamId = int(onegamedic.get('4', '0'))
			gameobj.homeTeam = onegamedic.get('5', '')
			gameobj.friendTeam = onegamedic.get('6', '')
			gameobj.allHome = int(onegamedic.get('8', '0'))
			gameobj.allFriend = int(onegamedic.get('9', '0'))
			gameobj.halfHome = int(onegamedic.get('10', '0'))
			gameobj.halfFriend = int(onegamedic.get('11', '0'))
			gameobjlist.append(gameobj)

	print(f'{season} {subname}:采集到比赛数:{len(gameobjlist)}')
	for gameobj in gameobjlist:
		getOneGameHandiList(gameobj)
		time.sleep(2)
		getOneGameOddList(gameobj)
		time.sleep(3)
		mysql_insert_game_to_season_games(gameobj)
	return gameobjlist

def getCupSeasonGamelist(season='2022-2023', leagueID=103, leaguename='欧冠'):
	c_headers = {
		'User-Agent': 'QTimesApp/3.0 (Letarrow.QTimes; build:39; iOS 17.1.0) Alamofire/5.4.',
		'cookie': 'aiappfrom=48'
	}
	timestr = str(int(time.time()))
	t_gameobjlist = []
	url = f"http://api.letarrow.com/ios/Phone/FBDataBase/CupInfo.aspx?id={leagueID}&lang=0&season={season}&from=48&_t={timestr}"
	try:
		response = requests.get(url, headers=c_headers)
		content_type = response.headers.get('Content-Type')
		if response.ok and 'application/x-protobuf' == content_type:
			resultStr = response.content
			temp_message, typedef = blackboxprotobuf.protobuf_to_json(resultStr)
			p = os.path.expanduser(f'~/Desktop/{season}欧冠.json')
			with open(p, 'w+') as f:
				f.write(temp_message)
				f.close()
			protobufdic = json.loads(temp_message)
			gamecateList = protobufdic.get("3", {}).get("1", [])
			for one in gamecateList:
				cateName = one.get("2", {}).get("2", "")
				subid= one.get("1", "")
				if cateName != "" and subid != "" and cateName in ['分组赛']:#,'十六强','半准决赛','准决赛','决赛']:
					print(cateName, subid)
					l = getSubCupSeasonGamelist(season=season, leagueID=leagueID, leaguename=leaguename,subid=subid,subname=cateName)
					t_gameobjlist.extend(l)
	except Exception as e:
		print('获取杯赛数据', url, e)
	finally:
		print(f'{season}:采集到比赛数:{len(t_gameobjlist)}')



if __name__ == '__main__':
	_league_id = 103
	_sub_league_id = None
	_league_name = '欧冠'
	getCupSeasonGamelist('2022-2023', _league_id, _league_name)
	exit(0)
	headers = {
		'User-Agent': 'QTimesApp/3.0 (Letarrow.QTimes; build:39; iOS 17.1.0) Alamofire/5.4.',
		'cookie': 'aiappfrom=48'
	}
	url = f"http://api.letarrow.com/pcf/bfmatch/api/database/v1/leaguedetail?kind=1&lang=0&sid={_league_id}&_t={str(int(time.time()))}"
	try:
		response = requests.get(url, headers=headers)
		if response.ok:
			content_type = response.headers.get('Content-Type')
			if 'application/x-protobuf' == content_type:
				resultStr = response.content
				print(url, resultStr)
				temp_message, typedef = blackboxprotobuf.protobuf_to_json(resultStr)
				print(temp_message)
				leaguedic = json.loads(temp_message)
				league_id = int(leaguedic.get('1', '0'))
				if league_id != _league_id:
					raise ValueError("杯赛id异常")

				leaguename = leaguedic.get('2', '')
				seasons = leaguedic.get('4', [])
				for s in seasons:
					if s != '2022-2023':
						continue
					getCupSeasonGamelist(s, league_id, _league_name)
					# parsePanlu(season=s, leagueid=league_id, leaguename=_league_name)
					# parseJifen(season=s,leagueid=league_id,leaguename=_league_name,subleagueid=_sub_league_id)
					time.sleep(5)
	except Exception as e:
		print('获取杯赛数据异常:', e, url)


