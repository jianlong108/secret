#!/usr/bin/env python
# -*- coding: utf-8 -*-


import time
import requests
from DBHelper import *
from SoccerModels import *
from SoccerRound import *
import datetime

from SendMail import *
from SoccerRound import *

AllGames = []
AllBeginTimes = []

def anyaisegame(beginTimeStr):
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
        runTask(anyaisegame,AllBeginTimes[0])

def runTask(func):
# def runTask(func, day=0, hour=0, min=0, second=0):
    # get current time
    # now = datetime.now()
    # strnow = now.strftime('%Y-%m-%d %H:%M:%S')
    # print "now:", strnow
    # get net_run time
    # period = timedelta(days=0, hours=0, minutes=15, seconds=0)
    # next_time = now + period
    # strnext_time = next_time.strftime('%Y-%m-%d %H:%M:%S')
    timeStr = '2017-05-08 00:30'
    print timeStr
    now = datetime.now()


    # period = timedelta(days=0, hours=0, minutes=15, seconds=0)
    # next_time = now - period
    # strnext_time = next_time.strftime('%Y-%m-%d %H:%M:%S')
    strnow = now.strftime('%Y-%m-%d %H:%M:%S')
    if timeStr < strnow:
        del AllBeginTimes[0]
        runTask(anyaisegame)
        return
    strnext_time = timeStr
    print "next run:", strnext_time
    while True:
        now = datetime.now()
        strnow = now.strftime('%Y-%m-%d %H:%M:%S')
        # if system time eq next_time run the specific task(hello func)
        if str(strnow) == str(strnext_time):
            print strnow
            func(str(strnow))
            break

def getTodaySoccer(type):
    # type == 3 精彩
    # type == 1 精简
    # type == 2 十四场
    type = int(type)
    try:
        url = "http://112.91.160.49:8071/phone/schedule_0_" + str(type) + ".txt?an=iosQiuTan&av=5.9&from=2&r="+str(int(time.time()))
        print url
    except:
        pass
    resultStr = ''
    response = requests.get(url)
    if response.ok:
        resultStr = response.content;
    else:
        pass
    Games = []
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

            # onegame.oddCompanies = getOneGameODD(onegame)
            # onegame.handiCompanies = getOneGameHandi(onegame)
            # Games.append(onegame)
            # tempstr = getGameData(onegame)
            # if tempstr != None:
            #     contentStr = contentStr + tempstr
            #     contentStr = contentStr + '\n'
            #
            # time.sleep(3)

        # i = datetime.now()

        subjectstr = ''

        # if type == 1:
        #     subjectstr = '精简足球分析'
        # elif type == 2:
        #     subjectstr = '十四场足球分析'
        # else:
        #     subjectstr = '竞彩分析'
        #
        # send_mail("%s %s/%s/%s" % (subjectstr, i.year, i.month, i.day), contentStr)

        runTask(anyaisegame)


# if sys.argv.__len__()==1:
#     sys.exit('\033[0;36;40m使用说明:\n1个参数:\n1:精简足球分析   2:十四场足球分析  3:竞彩分析\n事例: python TodaySoccer.pyc 1\033[0m')
#
# if __name__ == '__main__':
#     getTodaySoccer(sys.argv[1])
getTodaySoccer(3)




