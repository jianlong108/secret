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

        # insert_League(model)

        if model.leagueID == 8 or model.leagueID == 9 or model.leagueID == 11 or model.leagueID == 12:
            print model.leagueName + '========='
            league = GetLeague(model)
            # 杯赛去请求杯赛接口,逻辑
            if '杯' in model.breifLeagueName:
                league.getCupDetails()
            #     否则全部视为联赛
            else:
                league.getOfficialLeague()






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
            if self.currentGound > 32:
                self.currentGound -= 1
                continue

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

            # if self.leagueModel.leagueID == 31:
            #     if season in ['2012-2013']:
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


















create_database()
main = MainSoccer()
main.getData()
# main = GetLeague()
# main.GetLeagueDetails(37, '2015-2016')






