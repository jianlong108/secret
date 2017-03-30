#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import copy
import sys
from SoccerModels import *

from HtmlParser import *
# http://112.91.160.46:8072/phone/txt/analysisheader/cn/1/25/1253496.txt?an=iosQiuTan&av=5.9&from=2&r=1490440206
# http://112.91.160.46:8072/phone/Handicap.aspx?ID=1252358&an=iosQiuTan&av=5.9&from=2&lang=0&r=1490449083

reload(sys)
sys.setdefaultencoding('utf-8')


def GetRound(leagueID, round, reason):
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


            if i == 0:
                if '1$$' in unit:
                    index = unit.index('1$$')+1
                    game.soccerID = unit[index:]
                elif '!' in unit:
                    index = unit.index('!') + 1
                    game.soccerID = unit[index:]
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

            else:
                pass

            i += 1
            if i == 13:
                i = 0
                games.append(copy.copy(game))
                game = None

        return games

class Game:
    '''
    获取一场比赛的欧赔数据
    '''
    def getOneGameODD(soccerId):

        try:
            url = 'http://112.91.160.46:8072/phone/1x2.aspx?ID=' + soccerId + '&an=iosQiuTan&av=5.9&from=2&lang=0&subversion=1'
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

                if i % 8 == 0:

                    company = LotteryCorporations()
                    company.soccerGameId = soccerId
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

    '''
    获取一场比赛的亚盘数据
    '''
    def getOneGameHandi(soccerId):
        try:
            url = 'http://112.91.160.46:8072/phone/Handicap.aspx?ID=' + soccerId + '&an=iosQiuTan&av=5.9&from=2&lang=0'
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
                # print unit.decode('utf-8')

                if i % 8 == 0:

                    company = LotteryCorporations()
                    company.soccerGameId = soccerId
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













#             英甲
English_C = League()
English_C.leagueName = '英甲'
English_C.teamNumber = 24
English_C.country = '英格兰'
create_database()
for game in GetRound(135, 1,'2016-2017'):
    print (game.soccerID,game.leauge,game.beginTime,game.soccer,game.homeTeamLevel,game.homeTeam,game.allHome,game.friendTeamLevel,game.friendTeam,game.allFriend)
    insert_Game((game.soccerID,game.leauge,game.beginTime,game.soccer,game.homeTeamLevel,game.homeTeam,game.allHome,game.friendTeamLevel,game.friendTeam,game.allFriend))
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




