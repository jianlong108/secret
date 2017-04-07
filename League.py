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
        array = resultStr.split('^')
        # 移除前六个元素
        # array = array[6:]
        i = 0
        company = None
        companys = []
        for unit in array:
            # print unit.decode('utf-8')

            if i % 8 == 0:

                company = LotteryCorporations()
                company.result = game.soccer
                company.homeSoccer = game.allHome
                company.friendSoccer = game.allFriend
                company.soccerGameId = game.soccerID
                # if isinstance(unit, unicode):
                #     print 'unit 是 Unicode'
                # else:
                #     print 'unit 是 str'

                if '!' in unit:
                    index = unit.index('!') + 1
                    company.companyTitle = unit[index:].decode('utf-8')
                else:
                    company.companyTitle = unit.decode('utf-8')

            elif i % 8 == 1:
                pass
            elif i % 8 == 2:
                company.orignal_top = float(unit)
            elif i % 8 == 3:
                company.orignal = float(unit)
            elif i % 8 == 4:
                company.orignal_bottom = float(unit)
            elif i % 8 == 5:
                company.now_top = float(unit)
            elif i % 8 == 6:
                company.now = float(unit)
            elif i % 8 == 7:
                company.now_bottom = float(unit)

            else:
                pass

            i += 1
            if i % 8 == 0:
                companys.append(copy.copy(company))
                company = None

        return companys


'''
获取一场比赛的欧赔数据
'''
def getOneGameODD(game):

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
        array = resultStr.split('^')
        # 移除前六个元素
        # array = array[6:]
        i = 0
        company = None
        companys = []
        for unit in array:
            print unit.decode('utf-8')

            if i % 8 == 0:

                company = LotteryCorporations()
                company.result = game.soccer
                company.homeSoccer = game.allHome
                company.friendSoccer = game.allFriend
                company.soccerGameId = game.soccerID
                # if isinstance(unit, unicode):
                #     print 'unit 是 Unicode'
                # else:
                #     print 'unit 是 str'

                if '!' in unit:
                    index = unit.index('!') + 1
                    company.companyTitle = unit[index:].decode('utf-8')
                else:
                    company.companyTitle = unit.decode('utf-8')

            elif i % 8 == 1:
                pass
            elif i % 8 == 2:
                company.orignal_winOdd = float(unit)
            elif i % 8 == 3:
                company.orignal_drawOdd = float(unit)
            elif i % 8 == 4:
                company.orignal_loseOdd = float(unit)
            elif i % 8 == 5:
                company.winOdd = float(unit)
            elif i % 8 == 6:
                company.drawOdd = float(unit)
            elif i % 8 == 7:
                company.loseOdd = float(unit)

            else:
                pass

            i += 1
            if i % 8 == 0:
                companys.append(copy.copy(company))
                company = None

        return companys





def GetRound(league,leagueID, round, reason):
    resultStr = ''
    try:
        url = "http://ios.win007.com/phone/SaiCheng2.aspx?sclassid=" + '39' + "&season=" + reason + "&subid=" + str(
            leagueID) + "&round=" + str(round) + "&apiversion=1&from=2"

        print url
    except:
        pass

    response = requests.get(url)

    if response.ok:
        resultStr = response.content;
    else:
        pass

    if resultStr != '':
        array = resultStr.split('!')
        i = 0
        games = []
        game = None
        for unit in array:
            print unit.decode('utf-8')

            if game == None:
                game = FootballGame()
                game.leauge = league.decode('utf-8')

            if i == 0:
                if '1$$' in unit:
                    index = unit.index('1$$')+3
                    game.soccerID = unit[index:].decode('utf-8')
                elif '!' in unit:
                    index = unit.index('!') + 1
                    game.soccerID = unit[index:].decode('utf-8')
                else:
                    game.soccerID = unit.decode('utf-8')

            elif i == 1:
                game.beginTime = unit.decode('utf-8')
            elif i == 2:
                game.homeTeam = unit.decode('utf-8')
            elif i == 3:
                game.homeTeam2 = unit.decode('utf-8')
            elif i == 4:
                game.friendTeam = unit.decode('utf-8')
            elif i == 5:
                game.friendTeam2 = unit.decode('utf-8')
            elif i == 6:
                pass
            elif i == 7:
                game.allHome = int(unit)
            elif i == 8:
                game.allFriend = int(unit)
            elif i == 9:
                game.halfHome = int(unit)
            elif i == 10:
                game.halfFriend = int(unit)
            elif i == 11:
                # 主队排名
                game.homeTeamLevel = int(unit)
            elif i == 12:
                # 客队排名
                game.friendTeamLevel = int(unit)

            else:
                pass

            i += 1
            if i == 13:
                i = 0
                games.append(copy.copy(game))

                game = None

        return games



class MainSoccer:
    def __init__(self):
        self.contientList = []
        self.index = 0
        self.countryList = []
    def getContientModel(self,contientID):
        targetModel = None
        for model in self.contientList:
            if model.continentID == contientID:
                targetModel = model
                break
        return targetModel

    def getCountryModel(self,countryID):
        targetModel = None
        for model in self.countryList:
            if model.countryID == countryID:
                targetModel = model
                break
        return targetModel


    def switchModel(self,complexStr):
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

    def creatContientModel(self,complexStr):
        model = ContinentSoccer()
        array = complexStr.split('^')
        model.continentID = array[0]
        model.continentName = array[1]
        self.contientList.append(model)


    def creatCountryModel(self,complexStr):
        model = CountrySoccer()
        array = complexStr.split('^')
        model.countryID = array[0]
        model.belongtoContinentID = array[1]
        model.countryName = array[2]

        contientModel = self.getContientModel(model.belongtoContinentID)
        contientModel.countryList.append(model)
        self.countryList.append(model)

    def creatLeagueModel(self,complexStr):
        model = League()
        array = complexStr.split('^')
        model.leagueID = array[0]
        model.belongtoCountryID = array[1]
        model.leagueName = array[2]
        model.breifLeagueName = array[3]
        model.aviableseasonstr = array[5]

        countryModel = self.getCountryModel(model.belongtoCountryID)
        countryModel.leagueList.append(model)

        insert_League(model)



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





# create_database()
# main = MainSoccer()
# main.getData()




resultStr = ''
try:
    url = 'http://ios.win007.com/phone/SaiCheng2.aspx?sclassid=39&season=2016-2017&subid=0&apiversion=1&from=2'

    print url
except:
    pass

response = requests.get(url)

if response.ok:
    resultStr = response.content;
else:
    pass

if resultStr != '':
    array = resultStr.split('!')
    for str in array:
        print str.decode('utf-8')







#             英甲
# English_C = League()
# English_C.leagueName = '英甲'
# English_C.teamNumber = 24
# English_C.country = '英格兰'
# create_database()
# for game in GetRound('英甲',135, 1,'2016-2017'):
#     time.sleep(1)
#
#     print (game.soccerID,game.leauge,game.beginTime,game.soccer,game.homeTeamLevel,game.homeTeam,game.allHome,game.friendTeamLevel,game.friendTeam,game.allFriend)
#     insert_Game(game)
#
#     companys = getOneGameODD(game)
#     insertGameODDList(companys)
#
#     companyHandis = getOneGameHandi(game)
#     insertGameHandiList(companyHandis)
# print getOneGameODD('1252359')


# for company in getOneGameHandi('1252360'):
#     print (company.soccerGameId,company.companyTitle,company.orignal_top,company.orignal,company.orignal_bottom,company.now_top,company.now,company.now_bottom)
#     insert_Handi((company.soccerGameId,company.companyTitle,company.orignal_top,company.orignal,company.orignal_bottom,company.now_top,company.now,company.now_bottom))
# for company in getOneGameODD('1252360'):
#     print (company.soccerGameId,company.companyTitle,company.orignal_winOdd,company.orignal_drawOdd,company.orignal_loseOdd,company.winOdd,company.drawOdd,company.loseOdd)
#     insert_ODD((company.soccerGameId,company.companyTitle,company.orignal_winOdd,company.orignal_drawOdd,company.orignal_loseOdd,company.winOdd,company.drawOdd,company.loseOdd))

# i = 51
# while (i<=46):
#     GetRound(135, i,'2016-2017')
#     i += 1
#     time.sleep(1)




