#!/usr/bin/env python
# -*- coding: utf-8 -*-

from GetData.SOCCER_MODELS import FootballGame
import requests
import time
from numpy import *
import blackboxprotobuf
import json
from colorama import Fore,init
from MySQLHelper import mysql_insert_game_to_disorder
from GetData.GET_PAN_LIST import getOneGameHandiList,qiutan_get_history_games
from datetime import datetime, timedelta


init(autoreset=True)

# {
#     "1": "2464799",
#     "2": "192",
#     "3": "1",
#     "4": "1701252000",
#     "5": "1701255842",
#     "6": {
#         "1": "3584",//teamid
#         "2": "杰志",
#         "3": "2",//排名
#         "4": "1",//全场得分
# "5"："0",//半场得分
# "6"："0", 红牌
#         "7": "3",黄牌
#         "8": "7",角球
#         "10": {
#             "2": "香港超2"
#         },
#         "11": {
#
#         }
#     },
#     "7": {
#         "1": "484",
#         "2": "全北现代",
#         "3": "4",
#         "4": "2",
#         "5": "2",
#         "6": "1",
#         "7": "2",
#         "8": "4",
#         "10": {
#             "2": "韩K联4"
#         },
#         "11": {
#             "1": "2"
#         }
#     },
#     "8": {
#         "1": "1064346583",
#         "2": "3208642560",
#         "3": "1061326684"
#     },
#     "9": {
#         "1": "1063675494",
#         "2": "1077936128",
#         "3": "1061997773"
#     },
#     "17": {
#         "1": "1081711002",
#         "2": "1081081856",
#         "3": "1070302495"
#     },
#     "18": "56"
# }

def getDisorderSoccerDay(daystr = '2023-11-25'):
    # http://api.letarrow.com/ios/phone/scheduleByDate.aspx?date=2023-11-29&lang=0&leagueList=1&subversion=3&from=48&_t=1701354305

    # kind 0 全部
    # kind 1 胜负
    # kind 2 竟足
    # kind 3 单场
    url = f"http://api.letarrow.com/ios/phone/scheduleByDate.aspx?date={daystr}&kind=0&lang=0&subversion=3&from=48&_t={str(int(time.time()))}"
    print(url)

    headers = {
        'User-Agent': 'QTimesApp/3.0 (Letarrow.QTimes; build:39; iOS 17.1.0) Alamofire/5.4.',
        'cookie': 'aiappfrom=48'
    }
    response = requests.get(url,headers=headers)
    if response.ok:
        content_type = response.headers.get('Content-Type')
        # print(content_type)
        if 'application/x-protobuf' == content_type:
            resultStr = response.content
            # print(url, resultStr)
            temp_message, typedef = blackboxprotobuf.protobuf_to_json(resultStr)
            # print(temp_message)
            protobufdic = json.loads(temp_message)
            leaguedic = protobufdic.get('3', {})
            gamelist = leaguedic.get('1', [])
            seasonlist = leaguedic.get('2', [])
            if len(gamelist) == 0 or len(seasonlist) == 0:
                print("不存在合法数据")
                return 108
            importantseasonidlist = []
            importantseasoniddic = {}
            gameobjlist = []
            for season in seasonlist:
                if season.get('3', '') == '':
                    continue
                importantseasonidlist.append(season.get('1',''))
                importantseasoniddic[season.get('1','')] = season.get('2','')

            for game in gamelist:
                seasonid = game.get('2', '')
                if seasonid not in importantseasonidlist:
                    continue
                print(game.get('6', {}).get('2',''), 'vs', game.get('7', {}).get('2',''))
                game_id = game.get('1', '0')
                leagueidstr = game.get('2', '0')
                leaguename = importantseasoniddic.get(leagueidstr, '')
                if game_id == '0' or leagueidstr == '0' or leaguename == '':
                    continue

                hometeamdic = game.get('6', {})
                if hometeamdic == {}:
                    continue

                friendteamdic = game.get('7', {})
                if friendteamdic == {}:
                    continue
                gameobj = FootballGame(gameid=int(game_id))
                gameobj.leauge = leaguename
                gameobj.leaugeid = int(leagueidstr)
                # gameobj.round = round
                gameobj.beginTimestamp = int(game.get('4', '0'))
                time_struct = time.localtime(gameobj.beginTimestamp)
                gameobj.beginTime = time.strftime("%Y-%m-%d %H:%M:%S", time_struct)
                gameobj.homeTeamId = int(hometeamdic.get('1', '0'))
                gameobj.friendTeamId = int(friendteamdic.get('1', '0'))
                gameobj.homeTeam = hometeamdic.get('2', '')
                gameobj.friendTeam = friendteamdic.get('2', '')
                gameobj.homeTeamLevel = int(hometeamdic.get('3', '0'))
                gameobj.friendTeamLevel = int(friendteamdic.get('3', '0'))
                gameobj.allHome = int(hometeamdic.get('4', '0'))
                gameobj.allFriend = int(friendteamdic.get('4', '0'))
                gameobj.halfHome = int(hometeamdic.get('5', '0'))
                gameobj.halfFriend = int(friendteamdic.get('5', '0'))
                gameobjlist.append(gameobj)
            return 0, gameobjlist
        else:
            return 0,[]
    else:
        print(response)
        return 404, []


def try_insert_db_disordergames(gameobj):
    can_insert_db = False
    if gameobj.handiIsFilp:
        print(Fore.GREEN + "盘口翻转", gameobj)
        can_insert_db = True
    if gameobj.earlyestCompany is not None and gameobj.earlyestCompany.companyID == '1':
        print(Fore.YELLOW + "澳盘开盘早", gameobj.earlyestCompany)
        can_insert_db = True

    if len(gameobj.orignalHandiList) > 2:
        if gameobj.maxHandiCompany.companyID != '1' and mean(gameobj.orignalHandiList) > mean(
                gameobj.nowHandiList):
            print(Fore.BLUE + "初盘混乱 后续降盘 澳盘不是最大盘", gameobj)
            can_insert_db = True

        if gameobj.maxHandiCompany.companyID != '1' and mean(gameobj.orignalHandiList) < mean(
                gameobj.nowHandiList):
            print(Fore.BLUE + "初盘混乱 后续升盘 澳盘不是最大盘", gameobj)
            can_insert_db = True
    if can_insert_db:
        mysql_insert_game_to_disorder(gameobj)


def get_previous_dates_games(start_date_str, num_days):
    # 将字符串日期解析为 datetime 对象
    start_date = datetime.strptime(start_date_str, '%Y%m%d')

    # 逐个获取之前的日期
    for i in range(num_days):
        current_date = start_date - timedelta(days=i)
        daystr = current_date.strftime('%Y%m%d')
        print(Fore.RED + f"目前的日期:{daystr}")
        code,game_list = qiutan_get_history_games(daystr)
        for gameobj in game_list:
            print(Fore.LIGHTGREEN_EX + f"{gameobj}")
            getOneGameHandiList(gameobj)
            try_insert_db_disordergames(gameobj)
            time.sleep(3)
        time.sleep(3)



if __name__ == '__main__':
    # 从 20231209 开始往前打印 5 天的日期
    get_previous_dates_games('20230831', 31)
    # code,gamelist = getDisorderSoccerDay('2023-12-07')
    # if code == 0:
    #     for gameobj in gamelist:
    #         print(gameobj)
    #         getOneGameHandiList(gameobj)
    #         try_insert_db_disordergames(gameobj)
    #         time.sleep(5)
