#!/usr/bin/env python
# -*- coding: utf-8 -*-


import time
from urllib2 import Request
import urllib2
from bs4 import BeautifulSoup
from DBHelper import *
from SoccerModels import *
from SoccerRound import *
import datetime

from SendMail import *
from SoccerRound import *

global AllGames
global AllBeginTimes



def anyaisegame(beginTimeStr, AllGames, AllBeginTimes):
    # global AllGames
    # global AllBeginTimes
    contentStr = ''
    for game in AllGames:
        if game.beginTime == beginTimeStr:
            game.oddCompanies = getOneGameODD(game)
            game.handiCompanies = getOneGameHandi(game)

            tempstr = getGameData(game)
            if tempstr != None:
                contentStr = contentStr + tempstr
                contentStr = contentStr + '\n'

            time.sleep(3)

    subjectstr = '时段足球分析'
    send_mail("%s %s" % (subjectstr, beginTimeStr), contentStr)
    del AllBeginTimes[0]
    if len(AllBeginTimes) > 0:
        runTask(anyaisegame, AllGames, AllBeginTimes)

def runTask(func, AllGames, AllBeginTimes):
# def runTask(func, day=0, hour=0, min=0, second=0):
    # get current time
    # now = datetime.now()
    # strnow = now.strftime('%Y-%m-%d %H:%M:%S')
    # print "now:", strnow
    # get net_run time
    # period = timedelta(days=0, hours=0, minutes=15, seconds=0)
    # next_time = now + period
    # strnext_time = next_time.strftime('%Y-%m-%d %H:%M:%S')
    # global AllGames
    # global AllBeginTimes

    timeStr = AllBeginTimes[0]
    print timeStr
    now = datetime.now()


    # period = timedelta(days=0, hours=0, minutes=15, seconds=0)
    # next_time = now - period
    # strnext_time = next_time.strftime('%Y-%m-%d %H:%M:%S')
    strnow = now.strftime('%Y-%m-%d %H:%M:%S')
    strnow = '2017-05-08 19:29'
    if timeStr < strnow:
        del AllBeginTimes[0]
        runTask(anyaisegame, AllGames, AllBeginTimes)
        return
    strnext_time = timeStr
    print "next run:", strnext_time
    while True:
        now = datetime.now()
        strnow = now.strftime('%Y-%m-%d %H:%M:%S')
        strnow = '2017-05-08 19:30'
        # if system time eq next_time run the specific task(hello func)
        if str(strnow) == str(strnext_time):
            print strnow
            func(str(strnow), AllGames, AllBeginTimes)
            break

def getTodaySoccer(type):
    # type == 3 竞彩
    # type == 1 精简
    # type == 2 十四场
    type = int(type)
    try:
        url = "http://112.91.160.49:8071/phone/schedule_0_" + str(type) + ".txt?an=iosQiuTan&av=6.1&from=2&r="+str(int(time.time()))
        # url = "http://112.91.160.49:8071/phone/schedule_0_" + str(type) + ".txt?an=iosQiuTan&av=5.9&from=2&r=1494229747"


        print url
    except:
        pass
    resultStr = ''
    # req = urllib2.Request(url)
    # req.add_header("User-Agent", "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)")
    response = requests.get(url)
    # response = urllib2.urlopen(req)
    if response.ok:
        resultStr = response.content;
    else:
        pass

    AllGames = []
    AllBeginTimes = []
    resultStr = '20170622204820$$洲际杯^88^1!阿甲^2^1!欧青U21^1164^1!巴西甲^4^1!美职业^21^1$$1361101^88^0^20170622230000^^喀麦隆(中)^澳大利亚^0^0^^^0^0^0^0^0^周四001^^0^32^48^^^0^0^0^0^1^^0^0^2.25^9.5!1361102^88^0^20170623020000^^德国(中)^智利^0^0^^^0^0^0^0^0.25^周四002^^0^3^4^^^0^0^0^0^1^^0^0^2.75^9.5!1292524^2^0^20170623020000^^贝尔格拉诺^纽维尔老男孩^0^0^^^0^0^0^0^-0.75^周四003^^0^30^7^^^0^0^0^0^1^^0^0^2.25^9.5!1400328^1164^0^20170623024500^^波兰U21^英格兰U21^0^0^^^0^0^0^0^-0.75^周四004^^0^4^1^^^0^0^0^0^1^^0^0^2.75^!1356857^1164^0^20170623024500^^斯洛伐克U21(中)^瑞典U21^0^0^^^0^0^0^0^-0.25^周四005^^0^2^3^^^0^0^0^0^1^^0^0^2.75^10!1292532^2^0^20170623041000^^拉努斯^飓风队^0^0^^^0^0^0^0^1^周四006^^0^10^24^^^0^0^0^0^1^^0^0^2.25^9.5!1292521^2^0^20170623041000^^萨尔米安杜^帕特罗纳图^0^0^^^0^0^0^0^0^周四007^^0^26^23^^^0^0^0^0^1^^0^0^2.25^9.5!1292530^2^0^20170623062000^^泰格雷^拉斐拉竞技^0^0^^^0^0^0^0^0.5^周四008^^0^25^16^^^0^0^0^0^1^^0^0^2.25^9.5!1292534^2^0^20170623062000^^戈多伊克鲁斯^拉普拉塔大学生^0^0^^^0^0^0^0^0^周四009^^0^15^6^^^0^0^0^0^1^^0^0^2.25^9.5!1365190^4^0^20170623063000^^庞特普雷塔^克鲁塞罗^0^0^^^0^0^0^0^0^周四010^^0^11^10^^^0^0^0^0^1^^0^0^2.25^10!1365193^4^0^20170623063000^^科林蒂安^巴伊亚^0^0^^^0^0^0^0^1^周四011^^0^1^13^^^0^0^0^0^1^^0^0^2.5^11!1365191^4^0^20170623080000^^弗拉门戈^沙佩科恩斯^0^0^^^0^0^0^0^1^周四012^^0^9^7^^^1^0^0^0^1^^0^0^2.5^10.5!1365192^4^0^20170623080000^^格雷米奥^科里蒂巴^0^0^^^0^0^0^0^1^周四013^^0^2^4^^^0^0^0^0^1^^0^0^2.5^9.5!1292523^2^0^20170623083000^^圣塔菲联^阿根廷独立^0^0^^^0^0^0^0^-0.5^周四014^^0^20^8^^^0^0^0^0^1^^0^0^2.25^9!1292525^2^0^20170623083000^^图库曼竞技^萨斯菲尔德^0^0^^^0^0^0^0^0.25^周四015^^0^22^19^^^0^0^0^0^1^^0^0^2.25^9.5!1292529^2^-1^20170622083000^20170622093720^河床^阿尔多斯维^1^0^0^0^0^0^1^2^1.5^周三028^^1^3^27^^^0^0^6^7^1^^2^4^2.5^9.5!1365194^4^-1^20170622084500^20170622094600^米内罗竞技^累西腓体育^2^2^2^1^0^0^2^1^1^周三029^^1^15^17^^^0^0^3^2^1^^1^1^2.5^10!1365188^4^-1^20170622084500^20170622095006^巴拉纳竞技^圣保罗^1^0^1^0^0^0^3^3^0^周三030^^1^18^14^^^0^0^5^8^1^^5^5^2.25^10!1365196^4^-1^20170622084500^20170622095022^奥瓦^弗鲁米嫩塞^0^3^0^2^0^0^1^1^0^周三031^^1^20^11^^^0^0^5^4^1^^3^2^2.5^10.5!1344238^21^-1^20170622091000^20170622101301^科罗拉多急流^洛杉矶银河^1^3^1^1^0^0^1^2^0.25^周三032^^1^10^7^^^1^0^3^3^1^^2^1^2.75^9.5!1344239^21^-1^20170622103000^20170622114036^西雅图音速^奥兰多城^1^1^1^0^0^0^2^2^0.75^周三033^^1^8^4^^^1^0^4^4^1^^3^3^2.75^9.5'
    if resultStr != '':
        # print resultStr
        allArray = resultStr.split('$$')
        leagueStr = ''
        if type == 1:
            leagueStr = allArray[0]
        else:
            leagueStr = allArray[1]

        allLeague = leagueStr.split('!')
        dic = {}
        for league in allLeague:
            oneLeague = league.split('^')
            dic[oneLeague[1]] = oneLeague[0]

        gameStr = ''
        if type == 1:
            gameStr = allArray[1]
        else:
            gameStr = allArray[2]

        games = gameStr.split('!')
        contentStr = ''
        for game in games:
            onegame = FootballGame()
            oneGameArray = game.split('^')
            oneGameArray.remove('')
            onegame.soccerID = int(oneGameArray[0])
            onegame.leauge = dic.get(oneGameArray[1].encode('utf-8'))
            beginTime = oneGameArray[3].encode('utf-8')
            onegame.beginTime = beginTime[0:4] + '-' + beginTime[4:6] + '-' + beginTime[6:8] + ' ' + beginTime[8:10] + ':' + beginTime[10:12]


            briefTimeStr = beginTime[0:4] + '-' + beginTime[4:6] + '-' + beginTime[6:8] + ' ' + beginTime[8:10] + ':' + beginTime[10:12]
            if briefTimeStr not in AllBeginTimes:
                AllBeginTimes.append(briefTimeStr)

            if oneGameArray[4].isdigit() or oneGameArray[4] == '':
                onegame.homeTeam = oneGameArray[5].encode('utf-8')
                onegame.friendTeam = oneGameArray[6].encode('utf-8')
            else:
                onegame.homeTeam = oneGameArray[4].encode('utf-8')
                onegame.friendTeam = oneGameArray[5].encode('utf-8')

            AllGames.append(onegame)

            onegame.oddCompanies = getOneGameODD(onegame)
            onegame.handiCompanies = getOneGameHandi(onegame)
            # templist = getexchange(onegame.soccerID)
            tempstr = getGameData(onegame)
            if tempstr != None:
                contentStr = contentStr + tempstr
                contentStr = contentStr + '\n'
                # contentStr = contentStr.join(templist)
            time.sleep(3)

        i = datetime.now()

        if type == 1:
            subjectstr = '精简足球分析'
        elif type == 2:
            subjectstr = '十四场足球分析'
        else:
            subjectstr = '竞彩分析'

        send_mail("%s %s/%s/%s" % (subjectstr, i.year, i.month, i.day), contentStr)
        # if type == 1 or type == 3:
        #     runTask(anyaisegame, AllGames, AllBeginTimes)


# if sys.argv.__len__()==1:
#     sys.exit('\033[0;36;40m使用说明:\n1个参数:\n1:精简足球分析   2:十四场足球分析  3:竞彩分析\n事例: python TodaySoccer.pyc 1\033[0m')
#
# if __name__ == '__main__':
#     getTodaySoccer(sys.argv[1])
getTodaySoccer(3)




# getexchange(1255863)