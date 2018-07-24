#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import time
from DBHelper import *
from SoccerRound import *
from NetWorkTools import *
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
            self.jifenURL = ''
            self.leagueID = '37'
            self.currentSeason = '2016-2017'

            self.leagueSubID = 0
            self.countOfGounds = 0
            self.currentGound = 1

            self.addtionalSubID = 0
            self.finalSubID = 0

            self.superLeague = True
            self.teamPointsArr = []
            self.allGames = []
            self.allSubLeagues = []
            self.abortSeasonList = []
            self.middleSeasonTuple = ('2010-2011',1,)
        else:
            return None

    # pointskind = 0总积分 1.半场积分2.主场积分3.客场积分
    def GetLeagueJiFen(self,pointskind = '0'):
        resultStr = ''
        self.jifenURL = 'http://27.45.161.46:8072/phone/Jifen2.aspx?an=iosQiuTan&av=6.5&from=2&pointsKind=%s&r=1532144326&sclassid=%s&season=%s&subVersion=2&subid=0' % (pointskind,str(self.leagueModel.leagueID).encode('utf-8'), self.currentSeason)
        print '获取联赛: %s 赛季: %s 积分数据 url %s' % (str(self.leagueModel.leagueID).encode('utf-8'), self.currentSeason, self.jifenURL)

        response = requests.get(self.jifenURL)

        if response.ok:
            resultStr = response.content
        else:
            pass

        if resultStr != '':
            print resultStr

            array = resultStr.split('$$')
            if len(array) > 2:
                jifenDataStr = array[2]
                teamDataArr = jifenDataStr.split('!')
                for teamDataStr in teamDataArr:
                    if len(teamDataStr) > 0:
                        temp_TeamPoints = TeamPoints()
                        self.teamPointsArr.append(temp_TeamPoints)
                        teamPointArr = teamDataStr.split('^')
                        try:
                            # 1^24^切尔西^車路士^38^30^3^5^85^33^93^0^0^^^0
                            temp_TeamPoints.ranking = int(teamPointArr[0])
                            temp_TeamPoints.teamID = int(teamPointArr[1])
                            temp_TeamPoints.teamName = teamPointArr[2].encode('utf-8')
                            temp_TeamPoints.seasonRound = int(teamPointArr[4])
                            temp_TeamPoints.winCount = int(teamPointArr[5])
                            temp_TeamPoints.drawCount = int(teamPointArr[6])
                            temp_TeamPoints.loseCount = int(teamPointArr[7])
                            temp_TeamPoints.getScore = int(teamPointArr[8])
                            temp_TeamPoints.loseScore = int(teamPointArr[9])
                            temp_TeamPoints.points = int(teamPointArr[10])
                            temp_TeamPoints.league = self.leagueModel.breifLeagueName.encode('utf-8')
                            temp_TeamPoints.season = self.currentSeason.encode('utf-8')
                        except BaseException, e:
                            print '解析比赛积分出错'
                            print e

    # 获取此联赛是否包含附加赛,晋级赛之类的赛事
    def GetLeagueDetails(self):

        resultStr = GetLeagueDetails(str(self.leagueModel.leagueID).encode('utf-8'),self.currentSeason)

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

    # 获取某个联赛,某一轮的比赛数据
    def getLeagueGame(self, leagueSubID = 0, countRound = 0, currentRound = 0):
        if countRound == 0 and currentRound == 0:
            games = GetRound(self.leagueModel.breifLeagueName, self.leagueModel.leagueID, leagueSubID,
                             countRound,
                             self.currentSeason)
            self.allGames.extend(games)
            return
        else:
            while (currentRound > 0):
                if self.currentSeason == self.middleSeasonTuple[0]:
                    if currentRound > self.middleSeasonTuple[1]:
                        currentRound -= 1
                    else:
                        games = GetRound(self.leagueModel.breifLeagueName, self.leagueModel.leagueID, leagueSubID,
                                         currentRound,
                                         self.currentSeason)
                        # if len(games) == 0:
                        #     games = GetRound(self.leagueModel.breifLeagueName, self.leagueModel.leagueID, leagueSubID,
                        #                      currentRound,
                        #                      self.currentSeason)
                        self.allGames.extend(games)
                        print '获取正赛数据 ' + self.currentSeason + ' ' + str(currentRound) + ' ' + str(len(games))
                        currentRound -= 1
                        # if len(self.allGames) != 0:
                        #     insertNewGameList(self.allGames)
                        # del self.allGames[:]

                        time.sleep(3)
                else:
                    games = GetRound(self.leagueModel.breifLeagueName, self.leagueModel.leagueID, leagueSubID,
                                     currentRound,
                                     self.currentSeason)
                    self.allGames.extend(games)
                    print '获取正赛数据 ' + self.currentSeason + ' ' + str(currentRound) + ' ' + str(len(games))
                    currentRound -= 1
                    # if len(self.allGames) != 0:
                    #     insertNewGameList(self.allGames)
                    # del self.allGames[:]

                    time.sleep(3)

    def getOfficialLeague(self):

        for season in self.leagueModel.aviableSeasonList:

            if season in self.abortSeasonList:
                continue
            if season != self.currentSeason:
                self.currentGound = self.countOfGounds

            self.currentSeason = season
            self.GetLeagueJiFen(0)
            time.sleep(3)

        InsertLeagueJiFenALL(self.teamPointsArr)
            # self.GetLeagueDetails()
            # self.getAllData()
            # self.allSubLeagues = []
            # if len(self.allGames) != 0:
            #     insertNewGameList(self.allGames)
            # self.allGames  = []


def GetLeagueDetailFromDB(leagueid = -1,isCup = False):
    if leagueid < 0:
        print '联赛id 非法'
        return
    leagueArray = GET_LEAGUE_DETAIL_FROM_DB(leagueid)
    leagueModel = League()
    if leagueArray is not None:
        leagueModel.leagueID = leagueArray[0]
        leagueModel.leagueName = leagueArray[1].encode('utf-8')
        leagueModel.breifLeagueName = leagueArray[2].encode('utf-8')
        leagueModel.aviableSeasonStr = leagueArray[5].encode('utf-8')
        print leagueModel.aviableSeasonList
        leagueModel.aviableSeasonList.remove('2018-2019')

        # 杯赛去请求杯赛接口,逻辑
        print isCup
        if isCup == 0:
            print '请求杯赛接口'
            cup = GetCup(leagueModel)
            cup.cupName = leagueModel.breifLeagueName
            cup.getOfficialLeague()
        #     否则全部视为联赛
        else:
            print '请求联赛接口'
            league = GetLeague(leagueModel)
            league.getOfficialLeague()


# if sys.argv.__len__()==1:
#     sys.exit('\033[0;36;40m使用说明:\n2个参数:\n1:联赛id\n2:是否是杯赛.事例: python League.pyc 144 True\033[0m')
#
# if __name__ == '__main__':
#     leagueid = sys.argv[1]
#     isCup = sys.argv[2]
#     getLeagueData(leagueid,isCup)


GetLeagueDetailFromDB(36,1)







