#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import copy
import requests
from SoccerModels import *
# http://112.91.160.46:8072/phone/txt/analysisheader/cn/1/25/1253496.txt?an=iosQiuTan&av=5.9&from=2&r=1490440206
# http://112.91.160.46:8072/phone/Handicap.aspx?ID=1252358&an=iosQiuTan&av=5.9&from=2&lang=0&r=1490449083
def GetRound(leagueID,round):
    resultStr = ''
    try:
        url = "http://ios.win007.com/phone/SaiCheng2.aspx?sclassid="+ '39'+ "&season="+"2016-2017"+"&subid="+str(leagueID)+"&round="+str(round)+"&apiversion=1&from=2"
        print url
    except :
        pass

    response = requests.get(url)

    if response.ok:
        resultStr = response.content;
    else:
        pass

    if resultStr != '':
        array = resultStr.split('^')
        # 移除前六个元素
        array = array[6:]
        i = 0
        games = []
        game = None
        for unit in array:
            print unit.decode('utf-8')

            if game == None:
                game = FootballGame()
            else:
                pass

            if i == 0:
                if '1$$' in unit:
                    game.soccerID = unit[3:]
                elif '!' in unit:
                    game.soccerID = unit[1:]
                else:
                    game.soccerID = unit

            elif i == 1:
                game.beginTime = unit
            elif i == 2:
                game.homeTeam = unit
            elif i == 3:
                game.homeTeam2 = unit
            elif i == 4:
                game.friendTeam = unit
            elif i == 5:
                game.friendTeam2 = unit
            elif i == 6:
                pass
            elif i == 7:
                game.allHome = unit
            elif i == 8:
                game.allFriend = unit
            elif i == 9:
                game.halfHome = unit
            elif i == 10:
                game.halfFriend = unit
            elif i == 11:
                # 主队排名
                pass
            elif i == 12:
                # 客队排名
                pass
            elif i == 13:
                i = 0
                games.append(copy.copy(game))
                game = None
            else:
                pass

            i += 1

        print len(games)

def getOneGameHandi(soccerId):

    try:
        url = 'http://112.91.160.46:8072/phone/Handicap.aspx?ID='+soccerId+'&an=iosQiuTan&av=5.9&from=2&lang=0'
        print url
    except:
        pass

    response = requests.get(url)

    if response.ok:
        resultStr = response.content;
    else:
        pass

    if resultStr != '':
        array = resultStr.split('^')
        # 移除前六个元素
        # array = array[6:]
        i = 0
        company = None
        companys = []
        for unit in array:
            print unit.decode('utf-8')

            if company == None:
                company = LotteryCorporations()
                company.soccerID = soccerId
            else:
                pass

            if i == 0:
                if '!' in unit:
                    company.companyTitle = unit[1:]
                else:
                    company.companyTitle = unit

            elif i == 1:
                pass
            elif i == 2:
                company.orignal_top = float(unit)
            elif i == 3:
                company.orignal = float(unit)
            elif i == 4:
                company.orignal_bottom = float(unit)
            elif i == 5:
                company.now_top = float(unit)
            elif i == 6:
                company.now = float(unit)
            elif i == 7:
                company.now_bottom = float(unit)
            elif i == 8:
                i = 0
                companys.append(copy.copy(company))
                company = None
            else:
                pass

            i += 1

        return companys




#             英甲
English_C = League()
English_C.leagueName = '英甲'
English_C.teamNumber = 24
English_C.country = '英格兰'
# GetRound(135, 1)
print getOneGameHandi('1252360')
i = 51
while (i<=46):
    GetRound(135, i)
    i += 1
    time.sleep(1)



