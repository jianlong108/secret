#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import time
# import requests
from DBHelper import *
from SoccerRound import *
import sys
# http://112.91.160.46:8072/phone/txt/analysisheader/cn/1/25/1253496.txt?an=iosQiuTan&av=5.9&from=2&r=1490440206
# http://112.91.160.46:8072/phone/Handicap.aspx?ID=1252358&an=iosQiuTan&av=5.9&from=2&lang=0&r=1490449083

reload(sys)
sys.setdefaultencoding('utf-8')



class GetCup:
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

            self.GamesArray = []
            self.finalGame = None
            self.cupName = ''



    def getOfficialLeague(self):

        for season in self.leagueModel.aviableSeasonList:
            self.currentSeason = season
            self.GamesArray = []
            self.getCupDetails(season)
            self.getAllData(season)

    # 获取指定赛季的详情数据
    def getCupDetails(self,season):

        resultStr = ''

        self.orignalCupURL = 'http://ios.win007.com/phone/CupSaiCheng.aspx?ID=' + str(self.leagueModel.leagueID).encode(
            'utf-8') + '&lang=0&Season=' + season
        print self.orignalCupURL
        response = requests.get(self.orignalCupURL)

        if response.ok:
            resultStr = response.content
        else:
            pass

        # 1.非顶级联赛;正在进行的赛季
        if resultStr != '':

            if '$$$$' in resultStr:
                # 非小组赛
                array = resultStr.split('$$$$')
                subGameStr = array[0]

                if len(subGameStr) > 0:
                    for subStr in subGameStr.split('!'):
                        if len(subStr) > 0:
                            gameIDArray = subStr.split('^')
                            newDic = {}
                            if len(gameIDArray) > 2:
                                newDic['id'] = gameIDArray[0]
                                newDic['dec'] = gameIDArray[1]
                                newDic['bool'] = gameIDArray[2]

                            if len(newDic) > 0:
                                self.GamesArray.append(newDic)



            elif '$$' in resultStr:
                # 小组赛
                array = resultStr.split('$$')
                subGameStr = array[0]
                if len(subGameStr) > 0:
                    for subStr in subGameStr.split('!'):
                        if len(subStr) > 0:
                            gameIDArray = subStr.split('^')
                            newDic = {}
                            if len(gameIDArray) > 2:
                                newDic['id'] = gameIDArray[0]
                                newDic['dec'] = gameIDArray[1]
                                newDic['bool'] = gameIDArray[2]

                            if len(newDic) > 0:
                                self.GamesArray.append(newDic)

            else:
                pass

    # 获取指定赛季的所有数据
    def getAllData(self,season):
        for gameDic in self.GamesArray:
            gameID = gameDic['id']
            self.getGames(gameID,season)
            time.sleep(1)

        if len(self.allGames) > 0:
            insertGameList(self.allGames)
            self.allGames = []

        time.sleep(2)


    def getGames(self, gameID,season):

        responseStr = ''
        url = 'http://ios.win007.com/phone/CupSaiCheng.aspx?ID=' + str(self.leagueModel.leagueID) + '&lang=0&Season=' + season + '&GroupId=' + str(gameID)
        print url
        response = requests.get(url)
        if response.ok:
            responseStr = response.content
        else:
            pass

        if responseStr != '':
            if '$$$$' in responseStr:
                # 非小组赛
                array = responseStr.split('$$$$')
                subGameStr = array[1]

                if len(subGameStr) > 0:
                    games = creatCupGameModelWithComplexStr(subGameStr, self.leagueModel.breifLeagueName)
                    self.allGames.extend(games)



            elif '$$' in responseStr:
                # 小组赛
                array = responseStr.split('$$')
                subGameStr = array[2]
                if len(subGameStr) > 0:
                    games = creatCupGameModelWithComplexStr(subGameStr, self.leagueModel.breifLeagueName)
                    self.allGames.extend(games)


            else:
                pass

# 获取联赛数据
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
            self.allSubLeagues = []
        else:
            return None






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

            print resultStr

            array = resultStr.split('$$')
            if '!' in array[0]:
                leagueStr = array[0]
                subLeagueArray = leagueStr.split('!')
                for subLeagueStr in subLeagueArray:
                    if len(subLeagueStr) > 0:
                        gameIDArray = subLeagueStr.split('^')
                        newDic = {}
                        if len(gameIDArray) > 2:
                            newDic['id'] = gameIDArray[0]
                            newDic['dec'] = gameIDArray[1]
                            newDic['subdec'] = gameIDArray[2]
                            newDic['flag'] = gameIDArray[3]
                            newDic['count'] = gameIDArray[4]
                            newDic['round'] = gameIDArray[5]

                        if len(newDic) > 0:
                            self.allSubLeagues.append(newDic)
            else:
                print '不包含附加赛' + 'header' + array[0]
                gameIDArray = array[0].split('^')
                newDic = {}
                if len(gameIDArray) > 3:
                    newDic['id'] = gameIDArray[0]
                    newDic['dec'] = gameIDArray[1]
                    newDic['subdec'] = gameIDArray[2]
                    newDic['flag'] = gameIDArray[3]
                    newDic['count'] = gameIDArray[4]
                    newDic['round'] = gameIDArray[5]

                else:
                    newDic['count'] = gameIDArray[0]
                    newDic['round'] = gameIDArray[1]

                if len(newDic) > 0:
                    self.allSubLeagues.append(newDic)


    def getAllData(self):
        for leagueDic in self.allSubLeagues:
            leagueId = 0
            leagueDec = ''
            if 'id' in leagueDic:
                leagueId = leagueDic['id']
                leagueDec = leagueDic['dec']
                flag = leagueDic['flag']

                countOfRound = leagueDic['count']
                currentRound = leagueDic['round']
            else:
                countOfRound = leagueDic['count']
                currentRound = leagueDic['round']

            self.getLeagueGame(leagueId, int(countOfRound), int(currentRound))

    def getLeagueGame(self, leagueSubID = 0, countRound = 0, currentRound = 0):
        if countRound == 0 and currentRound == 0:
            games = GetRound(self.leagueModel.breifLeagueName, self.leagueModel.leagueID, leagueSubID,
                             countRound,
                             self.currentSeason)
            self.allGames.extend(games)
            return
        else:
            while (currentRound > 0):

                games = GetRound(self.leagueModel.breifLeagueName, self.leagueModel.leagueID, leagueSubID,
                                 currentRound,
                                 self.currentSeason)
                self.allGames.extend(games)
                print '获取正赛数据 ' + self.currentSeason + ' ' + str(currentRound) + ' ' + str(len(games))
                currentRound -= 1
                # if len(self.allGames) != 0:
                #     insertGameList(self.allGames)
                # del self.allGames[:]

                time.sleep(3)


    def getOfficialLeague(self):

        for season in self.leagueModel.aviableSeasonList:


            if season != self.currentSeason:
                self.currentGound = self.countOfGounds

            self.currentSeason = season

            self.GetLeagueDetails()
            self.getAllData()
            self.allSubLeagues = []
            if len(self.allGames) != 0:
                insertGameList(self.allGames)
            self.allGames  = []


def getLeagueData(leagueid = -1,isCup = False):
    if leagueid < 0:
        print '联赛id 非法'
    leagueArray = getLeagueDetail(leagueid)
    leagueModel = League()
    if leagueArray is not None:
        leagueModel.leagueID = leagueArray[1]
        leagueModel.leagueName = leagueArray[2].encode('utf-8')
        leagueModel.breifLeagueName = leagueArray[3].encode('utf-8')
        leagueModel.aviableSeasonStr = leagueArray[4].encode('utf-8')
        leagueModel.creatSeasonList()

        # 杯赛去请求杯赛接口,逻辑
        if isCup:
            cup = GetCup(leagueModel)
            cup.cupName = leagueModel.breifLeagueName
            cup.getOfficialLeague()
        #     否则全部视为联赛
        else:
            league = GetLeague(leagueModel)
            league.getOfficialLeague()


if sys.argv.__len__()==1:
    sys.exit('\033[0;36;40m使用说明:\n2个参数:\n1:联赛id\n2:是否是杯赛.事例: python League.pyc 36 True\033[0m')

if __name__ == '__main__':
    leagueid = sys.argv[1]
    isCup = sys.argv[2]
    getLeagueData(leagueid, isCup)












