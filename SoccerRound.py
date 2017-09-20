#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from SoccerModels import *
import time
import pycurl
import StringIO

def GetRound(leaguename, leagueID, leagueSubID, gameRound, reason):
    resultStr = ''

    try:
        if gameRound == 0:
            url = "http://ios.win007.com/phone/SaiCheng2.aspx?sclassid=" + str(
                leagueID).encode('utf-8') + "&season=" + reason + "&subid=" + str(
                leagueSubID).encode('utf-8') + "&apiversion=1&from=2"
        else:

            url = "http://ios.win007.com/phone/SaiCheng2.aspx?sclassid=" + str(
                    leagueID).encode('utf-8') + "&season=" + reason + "&subid=" + str(
                    leagueSubID).encode('utf-8') + "&round=" + str(gameRound).encode('utf-8') + "&apiversion=1&from=2"

        print url
    except:
        pass

    response = requests.get(url)

    if response.ok:
        resultStr = response.content;
    else:
        pass

    games = []

    if resultStr != '':
        games = creatGameModelWithComplexStr(resultStr, leaguename)

    return games

def creatCupGameModelWithComplexStr(complexStr,leagueStr):
    array = complexStr.split('!')
    games = []
    for unit in array:
        print unit.decode('utf-8')
        if '$$' in unit:
            onegame = unit.split('$$')[1]
            model = creatCupGameModel(onegame, leagueStr)
            if model != None:
                games.append(model)

        else:
            model = creatCupGameModel(unit, leagueStr)
            if model != None:
                games.append(model)
    return games

def creatCupGameModel(gameStr,leagueStr):
    print gameStr
    if isinstance(gameStr, str):

        try:
            model = FootballGame()
            model.leauge = leagueStr

            if '$$' in gameStr:
                onestr = gameStr.split('$$')
                return creatGameModel(onestr[1], leagueStr)
            else:
                gameArray = gameStr.split('^')

                if int(gameArray[6]) != -1:
                    return None

                model.soccerID = int(gameArray[11])

                beginTime = gameArray[1].encode('utf-8')
                model.beginTime = beginTime[0:4] + '-' + beginTime[4:6] + '-' + beginTime[6:8] + '-' + beginTime[
                                                                                                       8:10] + ':' + beginTime[
                                                                                                                     10:12]
                model.homeTeam = gameArray[2].encode('utf-8')
                model.homeTeam2 = gameArray[3].encode('utf-8')
                model.friendTeam = gameArray[4].encode('utf-8')
                model.friendTeam2 = gameArray[5].encode('utf-8')

                model.allHome = int(gameArray[7])
                model.allFriend = int(gameArray[8])
                model.halfHome = int(gameArray[9])
                model.halfFriend = int(gameArray[10])
                if gameArray[11] != '':
                    model.homeTeamLevel = int(gameArray[11])

                time.sleep(1.5)
                model.oddCompanies = getOneGameODD(model)
                model.handiCompanies = getOneGameHandi(model)
                return model


        except:
            return None

    else:
        return None


def creatGameModelWithComplexStr(complexStr,leagueStr):
    array = complexStr.split('!')
    games = []
    for unit in array:
        print unit.decode('utf-8')
        if '$$' in unit:
            onegame = unit.split('$$')[1]
            model = creatGameModel(onegame, leagueStr)
            if model != None:
                games.append(model)

        else:
            model = creatGameModel(unit, leagueStr)
            if model != None:
                games.append(model)
    return games

def creatGameModel(gameStr,leagueStr):
    print gameStr
    if isinstance(gameStr, str):

        try:
            model = FootballGame()
            model.leauge = leagueStr

            if '$$' in gameStr:
                onestr = gameStr.split('$$')
                return creatGameModel(onestr[1], leagueStr)
            else:
                gameArray = gameStr.split('^')

                model.soccerID = int(gameArray[0])
                beginTime = gameArray[1].encode('utf-8')
                model.beginTime = beginTime[0:4] + '-' + beginTime[4:6] + '-' + beginTime[6:8] + '-' + beginTime[
                                                                                                       8:10] + ':' + beginTime[
                                                                                                                     10:12]
                model.homeTeam = gameArray[2].encode('utf-8')
                model.homeTeam2 = gameArray[3].encode('utf-8')
                model.friendTeam = gameArray[4].encode('utf-8')
                model.friendTeam2 = gameArray[5].encode('utf-8')
                if int(gameArray[6]) != -1:
                    return None
                model.allHome = int(gameArray[7])
                model.allFriend = int(gameArray[8])
                model.halfHome = int(gameArray[9])
                model.halfFriend = int(gameArray[10])
                if gameArray[11] != '':
                    model.homeTeamLevel = int(gameArray[11])

                if gameArray[12] != '':
                    model.friendTeamLevel = int(gameArray[12])

                time.sleep(1.5)
                model.oddCompanies = getOneGameODD(model)
                model.handiCompanies = getOneGameHandi(model)
                return model
        except:
            return None

    else:
        return None



'''
获取一场比赛的亚盘数据
'''
def getOneGameHandi(game):

    resultStr = ''

    try:
        handiURL = 'http://27.45.161.37:8072/phone/Handicap.aspx?ID=' + str(game.soccerID) + '&an=iosQiuTan&av=5.9&from=2&lang=0'
        # print handiURL
    except:
        pass

    c = pycurl.Curl()

    c.setopt(pycurl.URL, handiURL)

    b = StringIO.StringIO()
    c.setopt(pycurl.WRITEFUNCTION, b.write)
    c.setopt(pycurl.FOLLOWLOCATION, 1)
    c.setopt(pycurl.MAXREDIRS, 5)
    c.perform()
    resultStr = b.getvalue().encode('utf-8')

    if resultStr != '':
        array = resultStr.split('!')

        if isinstance(game, FootballGame):
            companys = []
            for unit in array:
                company = BetCompany()
                company.result = game.soccer
                company.league = game.leauge
                company.homeSoccer = game.allHome
                company.friendSoccer = game.allFriend
                company.soccerGameId = game.soccerID
                unitArray = unit.split('^')

                company.companyTitle = unitArray[0]
                company.companyID = int(unitArray[1])
                company.orignal_top = float(unitArray[2])
                company.orignal_Handicap = float(unitArray[3])
                if company.orignal_Handicap not in game.orignalHandiList:
                    game.orignalHandiList.append(company.orignal_Handicap)
                company.orignal_bottom = float(unitArray[4])
                company.now_top = float(unitArray[5])
                company.now_Handicap = float(unitArray[6])
                company.now_bottom = float(unitArray[7])
                if company.companyTitle == '澳门':
                    game.orignal_aomenHandi = company.orignal_Handicap
                    game.now_aomenHandi = company.now_Handicap
                companys.append(company)
            return companys
        else:
            return []



    else:
        return []


'''
获取一场比赛的欧赔数据
'''
def getOneGameODD(game):
    resultStr = ''
    try:
        oddURL = 'http://27.45.161.37:8072/phone/1x2.aspx?ID=' + str(game.soccerID) + '&an=iosQiuTan&av=5.9&from=2&lang=0&subversion=1'
        # print oddURL
    except:
        pass

    c = pycurl.Curl()

    c.setopt(pycurl.URL, oddURL)

    b = StringIO.StringIO()
    c.setopt(pycurl.WRITEFUNCTION, b.write)
    c.setopt(pycurl.FOLLOWLOCATION, 1)
    c.setopt(pycurl.MAXREDIRS, 5)
    c.perform()
    resultStr = b.getvalue().decode('utf8')

    if resultStr != '':
        array = resultStr.split('!')

        companys = []
        for unit in array:
            # print unit.decode('utf-8')
            company = BetCompany()
            company.league = game.leauge;
            company.result = game.soccer
            company.homeSoccer = game.allHome
            company.friendSoccer = game.allFriend
            company.soccerGameId = game.soccerID
            unitArray = unit.split('^')

            company.companyTitle = unitArray[0].encode('utf-8')
            company.orignal_winOdd = float(unitArray[2])
            company.orignal_drawOdd = float(unitArray[3])

            company.orignal_loseOdd = float(unitArray[4])

            company.winOdd = float(unitArray[5])

            company.drawOdd = float(unitArray[6])
            company.loseOdd = float(unitArray[7])
            if company.companyTitle in ['竞彩官方', '10BET', 'bet 365', 'bwin', 'Interwetten', 'SB', '澳门', '立博', '威廉希尔', '香港马会', '伟德']:
                companys.append(company)
                if company.companyTitle == '澳门':
                    game.orignal_aomenOdd = (company.orignal_winOdd, company.orignal_drawOdd, company.orignal_loseOdd)
                    game.now_aomenOdd = (company.winOdd, company.drawOdd, company.loseOdd)

        return companys
    else:
        return []