#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import os
from SOCCER_MODELS import FootballGame
from SOCCER_ROUND import getOneGameODD,getOneGameHandi
from DBHELPER import DB_InsertDisorderGameList
from NetWorkTools import get_resultstr_with_url

def ReadData_from_local_file():
    # codeFilePaths = os.path.abspath('.')

    desktoppath = os.path.join(os.path.expanduser("~"), 'Desktop')
    # currentpath = os.getcwd()
    # paths = os.path.split(codeFilePaths)
    gameidpath = os.path.join(desktoppath, 'gameid.txt')
    gamelistfile = open(gameidpath, 'r+')
    gameidlist = gamelistfile.readlines()

    httpHomeStr = get_resultstr_with_url('http://119.29.29.29/d?ttl=1&dn=txt.city007.net')
    httpHomeList = httpHomeStr.split(';')
    host = httpHomeList[0]

    gamelist = []
    for gameid in gameidlist:
        print gameid
        game = GetGameBriefWithGameid(gameid[:-1])
        # game.oddCompanies = getOneGameODD(host,game)
        game.handiCompanies = getOneGameHandi(host,game)
        gamelist.append(game)
        if len(gamelist) > 0 :
            DB_InsertDisorderGameList(gamelist)
            gamelist = []
        time.sleep(3)



def GetGameBriefWithGameid(gameid):
    # http://61.143.225.85:8072/phone/txt/analysisheader/cn/2/36/23608.txt
    firstNum = gameid[0]
    secondNum = gameid[:2]

    url = ''
    try:
        url = 'http://61.143.225.85:8072/phone/txt/analysisheader/cn/%s/%s/%s.txt' % (firstNum,secondNum,gameid)
        print url
    except BaseException as e:
        print e

    if url != '':
        result = get_resultstr_with_url(url)
        if result != '':
            game = FootballGame()
            game.soccerID = int(gameid)

            gameList = result.split('^')
            game.homeTeam = gameList[0]
            game.friendTeam = gameList[1]
            beginTime = gameList[5].encode('utf-8')
            game.beginTime = beginTime[0:4] + '-' + beginTime[4:6] + '-' + beginTime[6:8] + ' ' + beginTime[
                                                                                                     8:10] + ':' + beginTime[
                                                                                                                   10:12] + ':' + beginTime[
                                                                                                                                  12:14]

            game.homeTeamLevel = gameList[6]
            game.friendTeamLevel = gameList[7]
            game.allHome = int(gameList[10])
            game.allFriend = int(gameList[11])
            game.leaugeid = gameList[13]
            game.leauge = gameList[15]

            return game
        else:
            return None
    else:
        return None


ReadData_from_local_file()
