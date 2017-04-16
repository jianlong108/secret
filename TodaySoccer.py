#!/usr/bin/env python
# -*- coding: utf-8 -*-


import time
import requests
from DBHelper import *
from SoccerModels import *
from SoccerRound import *

from SoccerRound import *

def getTodaySoccer():
    try:
        url = "http://112.91.160.49:8071/phone/schedule_0_3.txt?an=iosQiuTan&av=5.9&from=2&r="+str(int(time.time()))
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
        allArray = resultStr.split('$$')

        leagueStr = allArray[1]
        allLeague = leagueStr.split('!')
        dic = {}
        for league in allLeague:
            oneLeague = league.split('^')
            dic[oneLeague[1]] = oneLeague[0]

        gameStr = allArray[2]
        games = gameStr.split('!')
        for game in games:
            onegame = FootballGame()
            oneGameArray = game.split('^')
            oneGameArray.remove('')
            onegame.soccerID = int(oneGameArray[0])
            onegame.leauge = dic.get(oneGameArray[1].encode('utf-8'))
            onegame.beginTime = oneGameArray[3].encode('utf-8')
            if oneGameArray[4].isdigit() or oneGameArray[4] == '':
                onegame.homeTeam = oneGameArray[5].encode('utf-8')
                onegame.friendTeam = oneGameArray[6].encode('utf-8')
            else:
                onegame.homeTeam = oneGameArray[4].encode('utf-8')
                onegame.friendTeam = oneGameArray[5].encode('utf-8')

            onegame.oddCompanies = getOneGameODD(onegame)
            onegame.handiCompanies = getOneGameHandi(onegame)
            Games.append(onegame)
            getGameData(onegame)
            time.sleep(3)





getTodaySoccer()

# print float(Decimal(1.345).quantize(Decimal('0.0')))



