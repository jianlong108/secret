#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import requests
from DBHelper import *
from SoccerRound import *
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

        else:
            return None


    def getOfficialLeague(self):

        for season in self.leagueModel.aviableSeasonList:

            # if self.leagueModel.leagueID == 23:
            #     if season in ['2007-2008']:
            #         print season
            #     else:
            #        continue
            # else:
            #     print season

            self.currentSeason = season
            self.GamesArray = []
            self.getCupDetails()
            self.getAllData()


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

            # print  resultStr
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

    def getAllData(self):
        for gameDic in self.GamesArray:
            gameID = gameDic['id']
            self.getGames(gameID)
            time.sleep(1)

        if len(self.allGames) > 0:
            insertGameList(self.allGames)

        time.sleep(2)


    def getGames(self, gameID):

        responseStr = ''
        url = 'http://ios.win007.com/phone/CupSaiCheng.aspx?ID=' + str(self.leagueModel.leagueID) + '&lang=0&Season=' + self.currentSeason + '&GroupId=' + str(gameID)
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
                    games = creatCupGameModelWithComplexStr(subGameStr, self.leagueModel.leagueName)
                    self.allGames.extend(games)



            elif '$$' in responseStr:
                # 小组赛
                array = responseStr.split('$$')
                subGameStr = array[2]
                if len(subGameStr) > 0:
                    games = creatCupGameModelWithComplexStr(subGameStr, self.leagueModel.leagueName)
                    self.allGames.extend(games)


            else:
                pass





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

            if ('联赛' in array[0]) and ('附加赛' in array[0]) and ('附加赛决赛' in array[0]):
                # 非顶级联赛 且 过往赛季
                leagueStr = array[0]
                leagueArray = leagueStr.split('!')
                officalStr = leagueArray[0]
                self.leagueSubID = int(officalStr.split('^')[0])
                self.countOfGounds = int(officalStr.split('^')[4])
                self.currentGound = int(officalStr.split('^')[5])

                additionalLeagueStr = leagueArray[1]
                additionalArray = additionalLeagueStr.split('^')
                self.addtionalSubID = int(additionalArray[0])

                finalLeagueStr = leagueArray[2]
                finalArray = finalLeagueStr.split('^')
                self.finalSubID = int(finalArray[0])



            elif '联赛' in array[0]:
                # 非顶级联赛 正在进行赛季
                header = array[0]
                print '非顶级联赛 正在进行赛季' + 'header' + header

                leagueArray = header.split('^')
                self.leagueSubID = int(leagueArray[0])
                self.countOfGounds = int(leagueArray[4])
                self.currentGound = int(leagueArray[5])


            else:
                # 顶级联赛
                header = array[0]
                print '顶级联赛' + 'header' + header
                headerArray = header.split('^')
                self.countOfGounds = int(headerArray[0])
                self.currentGound = int(headerArray[1])


    def getAllData(self):
        if self.finalSubID != 0:
            self.getAddtionalFinalLeague()
            pass
        if self.addtionalSubID != 0:
            pass
            self.getAddtionalLeague()

        self.getLeagueGame()


    def getAddtionalLeague(self):
        games = GetRound(self.leagueModel.breifLeagueName, self.leagueModel.leagueID, self.addtionalSubID, 0,
                         self.currentSeason)
        print '获取附加赛数据' + self.currentSeason + str(len(games))
        self.allGames.extend(games)

    def getAddtionalFinalLeague(self):

        games = GetRound(self.leagueModel.breifLeagueName, self.leagueModel.leagueID, self.finalSubID, 0,
                         self.currentSeason)
        print '获取附加赛决赛数据' + self.currentSeason + str(len(games))
        self.allGames.extend(games)

    def getLeagueGame(self):
        while (self.currentGound <= self.countOfGounds and self.currentGound >= 1):
            # if self.currentGound > 3:
            #     self.currentGound -= 1
            #     continue

            games = GetRound(self.leagueModel.breifLeagueName, self.leagueModel.leagueID, self.leagueSubID,
                             self.currentGound,
                             self.currentSeason)

            self.allGames.extend(games)
            print '获取正赛数据 ' + self.currentSeason +' '+str(self.currentGound) + ' '+ str(len(games))
            self.currentGound -= 1
            if len(self.allGames) != 0:
                insertGameList(self.allGames)

            # self.currentGound = self.countOfGounds
            del self.allGames[:]

            time.sleep(3)
            if self.currentGound == 0:

                # if len(self.allGames) != 0:
                #     insertGameList(self.allGames)
                #
                self.currentGound = self.countOfGounds
                # del self.allGames[:]
                break
                time.sleep(10)

    def getOfficialLeague(self):

        for season in self.leagueModel.aviableSeasonList:

            # if self.leagueModel.leagueID == 23:
            #     if season in ['2007-2008']:
            #         print season
            #     else:
            #        continue
            # else:
            #     print season



            if season != self.currentSeason:
                self.currentGound = self.countOfGounds

            self.currentSeason = season
            print '================'

            self.GetLeagueDetails()
            self.getAllData()

if __name__ == '__main__':
    leagueArray = getLeagueDetail(17)
    leagueModel = League()
    if leagueArray != None:
        leagueModel.leagueID = leagueArray[1]
        leagueModel.leagueName = leagueArray[2]
        leagueModel.breifLeagueName = leagueArray[3]
        leagueModel.aviableSeasonStr = leagueArray[4]
        leagueModel.creatSeasonList()

        # 杯赛去请求杯赛接口,逻辑
        if '杯' in leagueModel.breifLeagueName:
            cup = GetCup(leagueModel)
            cup.getOfficialLeague()
        #     否则全部视为联赛
        else:
            league = GetLeague(leagueModel)
            league.getOfficialLeague()

    else:
        pass








