#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from NETWORKS_TOOLS import get_resultstr_with_url
from SOCCER_MODELS import BetCompany,FootballGame

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

        print(url)
    except BaseException as e:
        print(e)


    resultStr = get_resultstr_with_url(url)
    games = []

    if resultStr != '':
        games = creatGameModelWithComplexStr(resultStr, leaguename)

    return games

def creatCupGameModelWithComplexStr(complexStr,leagueStr,isCup = False):
    array = complexStr.split('!')
    games = []
    for unit in array:
        print(unit.decode('utf-8'))
        if '$$' in unit:
            onegame = unit.split('$$')[1]
            model = creatCupGameModel(onegame, leagueStr,isCup)
            if model is not None:
                games.append(model)

        else:
            model = creatCupGameModel(unit, leagueStr,isCup)
            if model is not None:
                games.append(model)
    return games

def creatCupGameModel(gameStr,leagueStr,isCup = False):
    print(gameStr + isCup)
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
                model.yapanCompanies = getOneGameHandi(model)
                return model


        except BaseException as e:
            print(e)
            return None

    else:
        return None


def creatGameModelWithComplexStr(complexStr,leagueStr):
    array = complexStr.split('!')
    games = []
    for unit in array:
        print(unit.decode('utf-8'))
        if '$$' in unit:
            onegame = unit.split('$$')[1]
            model = creatGameModel(onegame, leagueStr)
            if model is not None:
                games.append(model)

        else:
            model = creatGameModel(unit, leagueStr)
            if model is not None:
                games.append(model)
    return games

def creatGameModel(gameStr,leagueStr,isCup=False):

    if isinstance(gameStr, str):

        try:
            model = FootballGame()
            model.leauge = leagueStr

            if '$$' in gameStr:
                onestr = gameStr.split('$$')
                return creatGameModel(onestr[1], leagueStr)
            else:
                gameArray = gameStr.split('^')
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
                if isCup:
                    model.soccerID = int(gameArray[11])

                    if gameArray[13] != '':
                        model.homeTeamLevel = int(gameArray[13])

                    if gameArray[14] != '':
                        model.friendTeamLevel = int(gameArray[14])
                else:
                    model.soccerID = int(gameArray[0])

                    if gameArray[11] != '':
                        model.homeTeamLevel = int(gameArray[11])

                    if gameArray[12] != '':
                        model.friendTeamLevel = int(gameArray[12])


                time.sleep(1.5)
                model.oddCompanies = getOneGameODD(model)
                model.yapanCompanies = getOneGameHandi(model)
                return model
        except BaseException as e:
            print(e)
            return None

    else:
        return None



'''
获取一场比赛的亚盘数据
'''
def getOneGameHandi(host, game):

    resultStr = ''
    url = ''
    try:
        # url = 'http://xxx:8072/phone/Handicap.aspx?ID=' + str(game.soccerID) + '&an=iosQiuTan&av=5.9&from=2&lang=0'

        url = '%s/phone/Handicap.aspx?ID=%s&an=iosQiuTan&av=7.1&from=2&lang=0&subversion=1' % (host, str(game.soccerID))
    except BaseException as e:
        print(e)

    if url != '':
        resultStr = get_resultstr_with_url(url)

    if resultStr != '':
        array = resultStr.split('!')

        if isinstance(game, FootballGame):
            companys = []
            temp_maxHandi = -10
            temp_minHandi = -10
            temp_maxHandiCompany = ''
            temp_minHandiCompany = ''
            temp_topMax = 0.00
            temp_bottomMax = 0.00
            temp_topMaxCompany = ''
            temp_bottomMaxCompany = ''
            temp_topMin = 10.00
            temp_bottomMin = 10.00
            temp_topMinCompany = ''
            temp_bottomMinCompany = ''

            temp_ori_maxHandi = -10
            temp_ori_minHandi = -10
            temp_ori_maxHandiCompany = ''
            temp_ori_minHandiCompany = ''
            temp_ori_topMax = 0.00
            temp_ori_bottomMax = 0.00
            temp_ori_topMaxCompany = ''
            temp_ori_bottomMaxCompany = ''
            temp_ori_topMin = 10.00
            temp_ori_bottomMin = 10.00
            temp_ori_topMinCompany = ''
            temp_ori_bottomMinCompany = ''
            for unit in array:
                company = BetCompany()
                company.result = game.soccer
                company.league = game.leauge
                company.homeSoccer = game.allHome
                company.friendSoccer = game.allFriend
                company.soccerGameId = game.soccerID
                unitArray = unit.split('^')

                try:
                    company.companyTitle = unitArray[0]
                    company.companyID = int(unitArray[1])
                    company.orignal_top = float(unitArray[2])
                    company.orignal_Handicap = float(unitArray[3])
                    # 获取初盘种类
                    if company.orignal_Handicap not in game.orignalHandiList:
                        game.orignalHandiList.append(company.orignal_Handicap)
                    company.orignal_bottom = float(unitArray[4])

                    company.now_top = float(unitArray[5])
                    company.now_Handicap = float(unitArray[6])
                    company.now_bottom = float(unitArray[7])
                    # 获取终盘种类
                    if company.now_Handicap not in game.nowHandiList:
                        game.nowHandiList.append(company.now_Handicap)


                except (IndexError, ValueError) as e:
                    print(e, unitArray)

                except Exception as e:
                    print(e)


                if company.companyTitle == '澳门':
                    game.orignal_aomenHandi = company.orignal_Handicap
                    game.now_aomenHandi = company.now_Handicap
                companys.append(company)

                if temp_maxHandi == -10 or abs(temp_maxHandi) < abs(company.now_Handicap):
                    temp_maxHandi = company.now_Handicap
                    temp_maxHandiCompany = company.companyTitle

                if temp_minHandi == -10 or abs(temp_minHandi) > abs(company.now_Handicap):
                    temp_minHandi = company.now_Handicap
                    temp_minHandiCompany = company.companyTitle

                if temp_topMax < company.now_top:
                    temp_topMax = company.now_top
                    temp_topMaxCompany = company.companyTitle

                if temp_bottomMax < company.now_bottom:
                    temp_bottomMax = company.now_bottom
                    temp_bottomMaxCompany = company.companyTitle

                if (temp_topMin > company.now_top) and (company.now_top > 0.00):
                    temp_topMin = company.now_top
                    temp_topMinCompany = company.companyTitle

                if temp_bottomMin > company.now_bottom:
                    temp_bottomMin = company.now_bottom
                    temp_bottomMinCompany = company.companyTitle

                if temp_ori_maxHandi == -10 or abs(temp_ori_maxHandi) < abs(company.orignal_Handicap):
                    temp_ori_maxHandi = company.orignal_Handicap
                    temp_ori_maxHandiCompany = company.companyTitle

                if temp_ori_minHandi == -10 or abs(temp_ori_minHandi) > abs(company.orignal_Handicap):
                    temp_ori_minHandi = company.orignal_Handicap
                    temp_ori_minHandiCompany = company.companyTitle

                if temp_ori_topMax < company.orignal_top:
                    temp_ori_topMax = company.orignal_top
                    temp_ori_topMaxCompany = company.companyTitle

                if temp_ori_bottomMax < company.orignal_bottom:
                    temp_ori_bottomMax = company.orignal_bottom
                    temp_ori_bottomMaxCompany = company.companyTitle

                if temp_ori_topMin > company.orignal_top:
                    temp_ori_topMin = company.orignal_top
                    temp_ori_topMinCompany = company.companyTitle

                if temp_ori_bottomMin > company.orignal_bottom:
                    temp_ori_bottomMin = company.orignal_bottom
                    temp_ori_bottomMinCompany = company.companyTitle

            if temp_maxHandiCompany != '澳门' and temp_maxHandi == game.now_aomenOdd:
                temp_maxHandiCompany = '澳门'

            if temp_ori_maxHandiCompany != '澳门' and temp_ori_maxHandi == game.orignal_aomenHandi:
                temp_ori_maxHandiCompany = '澳门'

            game.maxHandi = temp_maxHandi
            game.maxHandiCompany = temp_maxHandiCompany
            game.minHandi = temp_minHandi
            game.minHandiCompany = temp_minHandiCompany
            game.topMax = temp_topMax
            game.bottomMax = temp_bottomMax
            game.topMaxCompany = temp_topMaxCompany
            game.bottomMaxCompany = temp_bottomMaxCompany
            game.topMin = temp_topMin
            game.topMinCompany = temp_topMinCompany
            game.bottomMin = temp_bottomMin
            game.bottomMinCompany = temp_bottomMinCompany

            game.ori_maxHandi = temp_ori_maxHandi
            game.ori_maxHandiCompany = temp_ori_maxHandiCompany
            game.ori_minHandi = temp_ori_minHandi
            game.ori_minHandiCompany = temp_ori_minHandiCompany
            game.ori_topMax = temp_ori_topMax
            game.ori_bottomMax = temp_ori_bottomMax
            game.ori_topMaxCompany = temp_ori_topMaxCompany
            game.ori_bottomMaxCompany = temp_ori_bottomMaxCompany
            game.ori_topMin = temp_ori_topMin
            game.ori_topMinCompany = temp_ori_topMinCompany
            game.ori_bottomMin = temp_ori_bottomMin
            game.ori_bottomMinCompany = temp_ori_bottomMinCompany

            return companys
        else:
            return []

    else:
        return []


'''
获取一场比赛的欧赔数据
'''
def getOneGameODD(host,game):
    resultStr = ''
    url = ''
    try:
        # url = 'http://xxx:8072/phone/1x2.aspx?ID=' + str(game.soccerID) + '&an=iosQiuTan&av=5.9&from=2&lang=0&subversion=1'
        url = '%s/phone/1x2.aspx?ID=%s&an=iosQiuTan&av=5.9&from=2&lang=0&subversion=1' % (host, str(game.soccerID))

    except BaseException as e:
        print(e)

    if url != '':
        resultStr = get_resultstr_with_url(url)

    if resultStr != '':
        array = resultStr.split('!')

        companys = []
        for unit in array:
            # print unit.decode('utf-8')
            company = BetCompany()
            company.league = game.leauge
            company.result = game.soccer
            company.homeSoccer = game.allHome
            company.friendSoccer = game.allFriend
            company.soccerGameId = game.soccerID
            unitArray = unit.split('^')

            try:
                company.companyTitle = unitArray[0].encode('utf-8')
                company.orignal_winOdd = float(unitArray[2])
                company.orignal_drawOdd = float(unitArray[3])

                company.orignal_loseOdd = float(unitArray[4])

                company.winOdd = float(unitArray[5])

                company.drawOdd = float(unitArray[6])
                company.loseOdd = float(unitArray[7])
            except IndexError as e:
                print(e, unitArray)

            companys.append(company)
            if company.companyTitle == '澳门':
                game.orignal_aomenOdd = (company.orignal_winOdd, company.orignal_drawOdd, company.orignal_loseOdd)
                game.now_aomenOdd = (company.winOdd, company.drawOdd, company.loseOdd)

        return companys
    else:
        return []