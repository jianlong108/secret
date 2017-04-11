#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import copy
import sys
from SoccerModels import *
import requests
from DBHelper import *
# http://112.91.160.46:8072/phone/txt/analysisheader/cn/1/25/1253496.txt?an=iosQiuTan&av=5.9&from=2&r=1490440206
# http://112.91.160.46:8072/phone/Handicap.aspx?ID=1252358&an=iosQiuTan&av=5.9&from=2&lang=0&r=1490449083

reload(sys)
sys.setdefaultencoding('utf-8')


'''
获取一场比赛的亚盘数据
'''


def getOneGameHandi(game):

    resultStr = ''

    try:
        handiURL = 'http://112.91.160.46:8072/phone/Handicap.aspx?ID=' + str(game.soccerID) + '&an=iosQiuTan&av=5.9&from=2&lang=0'
        print handiURL
    except:
        pass

    response = requests.get(handiURL)

    if response.ok:
        resultStr = response.content;
    else:
        pass

    if resultStr != '':
        array = resultStr.split('!')

        companys = []
        for unit in array:
            # print unit.decode('utf-8')
            company = LotteryCorporations()
            company.result = game.soccer
            company.homeSoccer = game.allHome
            company.friendSoccer = game.allFriend
            company.soccerGameId = game.soccerID
            unitArray = unit.split('^')

            company.companyTitle = unitArray[0].encode('utf-8')
            company.orignal_top = float(unitArray[2])
            company.orignal = float(unitArray[3])

            company.orignal_bottom = float(unitArray[4])

            company.now_top = float(unitArray[5])

            company.now = float(unitArray[6])
            company.now_bottom = float(unitArray[7])

            companys.append(company)

        return companys


'''
获取一场比赛的欧赔数据
'''
def getOneGameODD(game):
    resultStr = ''
    try:
        oddURL = 'http://112.91.160.46:8072/phone/1x2.aspx?ID=' + str(game.soccerID) + '&an=iosQiuTan&av=5.9&from=2&lang=0&subversion=1'
        print oddURL
    except:
        pass

    response = requests.get(oddURL)

    if response.ok:
        resultStr = response.content;
    else:
        pass


    if resultStr != '':
        array = resultStr.split('!')

        companys = []
        for unit in array:
            # print unit.decode('utf-8')
            company = LotteryCorporations()
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

            companys.append(company)

        return companys





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

                time.sleep(3)
                model.oddCompanies = getOneGameODD(model)
                model.handiCompanies = getOneGameHandi(model)
                return model
        except:
            return None

    else:
        return None


class MainSoccer:
    def __init__(self):
        self.contientList = []
        self.index = 0
        self.countryList = []
    def getContientModel(self, contientID):
        targetModel = None
        for model in self.contientList:
            if model.continentID == contientID:
                targetModel = model
                break
        return targetModel

    def getCountryModel(self, countryID):
        targetModel = None
        for model in self.countryList:
            if model.countryID == countryID:
                targetModel = model
                break
        return targetModel


    def switchModel(self, complexStr):
        if self.index == 0:
            array = complexStr.split('$$')

            contientStr = array[0]
            self.creatContientModel(contientStr)

            countryStr = array[1]
            self.creatCountryModel(countryStr)
        elif self.index == 1:
            array = complexStr.split('$$')

            countryStr = array[0]
            self.creatCountryModel(countryStr)

            leagueStr = array[1]
            self.creatLeagueModel(leagueStr)
        else:
            array = complexStr.split('$$')

            leagueStr = array[0]
            self.creatLeagueModel(leagueStr)

        self.index += 1

    def creatContientModel(self, complexStr):
        model = ContinentSoccer()
        array = complexStr.split('^')
        model.continentID = array[0]
        model.continentName = array[1]
        self.contientList.append(model)


    def creatCountryModel(self, complexStr):
        model = CountrySoccer()
        array = complexStr.split('^')
        model.countryID = array[0]
        model.belongtoContinentID = array[1]
        model.countryName = array[2]

        contientModel = self.getContientModel(model.belongtoContinentID)
        contientModel.countryList.append(model)
        self.countryList.append(model)

    def creatLeagueModel(self, complexStr):
        model = League()
        array = complexStr.split('^')
        model.leagueID = int(array[0])
        model.belongtoCountryID = int(array[1])
        model.leagueName = array[2]
        model.breifLeagueName = array[3]
        model.aviableSeasonStr = array[5]
        model.creatSeasonList()
        countryModel = self.getCountryModel(model.belongtoCountryID)
        if countryModel != None:
            countryModel.leagueList.append(model)


        if model.leagueID == 37 or model.leagueID == 39:
            print model.leagueName + '========='
            league = GetLeague(model)
            # 杯赛去请求杯赛接口,逻辑
            if '杯' in model.breifLeagueName:
                league.getCupDetails()
            #     否则全部视为联赛
            else:
                league.GetLeagueDetails()


        # insert_League(model)



    def getData(self):
        try:
            url = "http://121.10.245.46:8072/phone/InfoIndex.aspx?an=iosQiuTan&av=5.9" \
                  "&from=2&lang=0&r=1491480939"
            print url
        except:
            pass
        resultStr = ''
        response = requests.get(url)
        if response.ok:
            resultStr = response.content;
        else:
            pass

        if resultStr != '':
            allArray = resultStr.split('!')
            for complexStr in allArray:
                # print complexStr.decode('utf-8')
                # print '===='
                if '$$' in complexStr:
                    # 切换模型 生成
                    self.switchModel(complexStr)
                else:
                    unitArray = complexStr.split('^')

                    if len(unitArray) == 2:
                        self.creatContientModel(complexStr)
                    elif len(unitArray) == 3:
                        self.creatCountryModel(complexStr)
                    else:
                        self.creatLeagueModel(complexStr)



class GetLeague:
    def __init__(self, model):
        if isinstance(model, League):
            self.leagueModel = model
            self.orignalLeagueURL = ''
            self.orignalCupURL = ''
            self.leagueID = '37'
            self.currentSeason = '2016-2017'

            self.leagueSubID = 0
            self.countOfGounds = 0
            self.currentGound = 1

            self.addtionalSubID = 0
            self.finalSubID = 0

            self.superLeague = True

            self.allGames = []
        else:
            return None

    def getCupDetails(self):
        resultStr = ''

        self.orignalCupURL = 'http://ios.win007.com/phone/CupSaiCheng.aspx?ID=' + str(self.leagueModel.leagueID).encode(
            'utf-8') + '&lang=0&Season=' + self.currentSeason
        print self.orignalCupURL
        response = requests.get(self.orignalCupURL)

        if response.ok:
            resultStr = response.content;
        else:
            pass

        # 1.非顶级联赛;正在进行的赛季
        if resultStr != '':

            print  resultStr
            if '$$$$' in resultStr:
                # 以往赛季
                array = resultStr.split('$$$$')
                subGameStr = array[0]
                if len(subGameStr) > 0:
                    for subStr in subGameStr.split('!'):
                        if len(subStr) > 0:
                            gameIDArray = subStr.split('^')
                            gameIDArray[0]

            else:
                # 当前赛季
                array = resultStr.split('$$')
                subGameStr = array[2]
                if len(subGameStr) > 0:
                    for subStr in subGameStr.split('!'):
                        pass




    def GetLeagueDetails(self):
        resultStr = ''


        self.orignalLeagueURL = 'http://ios.win007.com/phone/SaiCheng2.aspx?sclassid=' \
                                    + str(self.leagueModel.leagueID).encode('utf-8') + '&season=' + self.currentSeason + '&subid=0&apiversion=1&from=2'
        print self.orignalLeagueURL
        response = requests.get(self.orignalLeagueURL)

        if response.ok:
            resultStr = response.content;
        else:
            pass

        if resultStr != '':

            print  resultStr
            array = resultStr.split('$$')

            if ('联赛' in array[0]) and ('附加赛' in array[0]) and ('附加赛决赛' in array[0]):
                # 非顶级联赛 且 过往赛季
                leagueStr = array[0]
                leagueArray = leagueStr.split('^')
                self.leagueSubID = int(leagueArray[0])
                self.countOfGounds = int(leagueArray[4])
                self.currentGound = int(leagueArray[5])

                additionalLeagueStr = array[1]
                additionalArray = additionalLeagueStr.split('^')
                self.addtionalSubID = int(additionalArray[0])

                finalLeagueStr = array[2]
                finalArray = finalLeagueStr.split('^')
                self.finalSubID = int(finalArray[0])

                self.getOfficialLeague()
                self.getAddtionalLeague()
                self.getAddtionalFinalLeague()

                self.superLeague = False


            elif '联赛' in array[0]:
                # 非顶级联赛 正在进行赛季
                header = array[0]
                print '非顶级联赛 正在进行赛季' + 'header' + header

                leagueArray = header.split('^')
                self.leagueSubID = int(leagueArray[0])
                self.countOfGounds = int(leagueArray[4])
                self.currentGound = int(leagueArray[5])

                self.getOfficialLeague()

            else:
                # 顶级联赛
                header = array[0]
                print '顶级联赛' + 'header' + header
                headerArray = header.split('^')
                self.countOfGounds = int(headerArray[0])
                self.currentGound = int(headerArray[1])

                self.getOfficialLeague()



    def getAddtionalLeague(self):
        games = GetRound(self.leagueModel.breifLeagueName, self.leagueModel.leagueID, self.leagueSubID, 0,
                         self.currentSeason)
        self.allGames.extend(games)

    def getAddtionalFinalLeague(self):
        games = GetRound(self.leagueModel.breifLeagueName, self.leagueModel.leagueID, self.leagueSubID, 0,
                         self.currentSeason)
        self.allGames.extend(games)

    def getOfficialLeague(self):

        for season in self.leagueModel.aviableSeasonList:

            if self.leagueModel.leagueID == 37:
                if season == '2012-2013' or season == '2013-2014' or season == '2014-2015' or season == '2015-2016' or season == '2016-2017':
                    continue
                else:
                   print season
            else:
                print season



            if season != self.currentSeason:
                self.currentGound = self.countOfGounds




            self.currentSeason = season
            print '================'



            while(self.currentGound <= self.countOfGounds and self.currentGound >= 1):

                games = GetRound(self.leagueModel.breifLeagueName, self.leagueModel.leagueID, self.leagueSubID, self.currentGound,
                                 season)

                self.allGames.extend(games)
                self.currentGound -= 1

                time.sleep(3)
                if self.currentGound == 0:
                    print len(self.allGames)
                    if len(self.allGames) != 0:
                        insertGameList(self.allGames)

                    self.currentGound = self.countOfGounds
                    del self.allGames[:]
                    break
                    time.sleep(10)

















create_database()
main = MainSoccer()
main.getData()
# main = GetLeague()
# main.GetLeagueDetails(37, '2015-2016')






