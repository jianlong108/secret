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

def getTodaySoccer(type):
    # type == 3 精彩
    # type == 1 精简
    # type == 2 十四场
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
            onegame.beginTime = beginTime[0:4] + '-' + beginTime[4:6] + '-' + beginTime[6:8] + '-' + beginTime[
                                                                                                     8:10] + ':' + beginTime[
                                                                                                                   10:12]
            if oneGameArray[4].isdigit() or oneGameArray[4] == '':
                onegame.homeTeam = oneGameArray[5].encode('utf-8')
                onegame.friendTeam = oneGameArray[6].encode('utf-8')
            else:
                onegame.homeTeam = oneGameArray[4].encode('utf-8')
                onegame.friendTeam = oneGameArray[5].encode('utf-8')
            onegame.oddCompanies = getOneGameODD(onegame)
            onegame.handiCompanies = getOneGameHandi(onegame)
            Games.append(onegame)
            tempstr = getGameData(onegame)
            if tempstr != None:
                contentStr = contentStr + tempstr
                contentStr = contentStr + '\n'

            time.sleep(3)

        i = datetime.datetime.now()

        subjectstr = ''

        if type == 1:
            subjectstr = '精简足球分析'
        elif type == 2:
            subjectstr = '十四场足球分析'
        else:
            subjectstr = '竞彩分析'

        send_mail("%s %s/%s/%s" % (subjectstr, i.year, i.month, i.day), contentStr)



if sys.argv.__len__()==1:
    sys.exit('\033[0;36;40m使用说明:\n1个参数:\n1:精简足球分析   2:十四场足球分析  3:竞彩分析\n事例: python TodaySoccer.pyc 1\033[0m')

if __name__ == '__main__':
    getTodaySoccer(2)

# print float(Decimal(1.345).quantize(Decimal('0.0')))



