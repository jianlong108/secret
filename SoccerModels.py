#!/usr/bin/env python
# -*- coding: utf-8 -*-

from BeautifulSoupHelper import *

'''
终盘不统一模型
'''
class NowHandiDisunion:
    def __init__(self):
        self.AomenOri_Handi = 0.0
        self.AomenNow_Handi = 0.0
        self.AomenChange = 0
        self.maxHandi = 0.0
        self.countOfHandi = 0
        self.minHandi = 0.0
        self.homeSoccer = 0
        self.friengSoccer = 0
        self.result = -1

class CompanyChange:
    def __init__(self):
        self.name = ''
        self.ori_handi = 0.0
        self.now_handi = 0.0

        # 0 不变 1 升 2 降
        self.handi_change = -1

'''
博彩公司
'''
class BetCompany:
    def __init__(self,title = '',src = ''):
        self.companyID = 0
        self.soccerGameId = ''
        self.league = ''
        self.companyTitle = ''

        self.orignal_top = 0.0
        self.orignal_bottom = 0.0
        self.orignal_Handicap = 0.0


        self.now_top = 0.0
        self.now_bottom = 0.0
        self.now_Handicap = 0.0


        self.exchange_top = 0.0
        self.exchange_bottom = 0.0
        self.exchange_Handicap = 0.0

        self.homeWinningPercentage = ''
        self.friendWiningPercentage = ''

        # 相似盘口的链接
        self.similerMatchURL = ''


        # 胜赔
        self.winOdd = 0.00
        # 平赔
        self.drawOdd = 0.00
        # 负赔
        self.loseOdd = 0.00

        # 初胜赔
        self.orignal_winOdd = 0.00
        # 初平赔
        self.orignal_drawOdd = 0.00
        # 初负赔
        self.orignal_loseOdd = 0.00


        self.result = 0
        self.homeSoccer = 0
        self.friendSoccer = 0

        self.falldown = False
        self.rise = False
        self.lowest = False
        self.highest = False

        @property
        def homeWaterChange(self):
            if self.now_top - self.orignal_top > 0:
                return '升水'
            elif self.now_top - self.orignal_top == 0.00:
                return '不变'
            else:
                return '降水'

        @property
        def friendWaterChange(self):
            if self.now_bottom - self.orignal_bottom > 0:
                return '升水'
            elif self.now_bottom - self.orignal_bottom == 0.00:
                return '不变'
            else:
                return '降水'

        @property
        def handiChange(self):

            if self.orignal_Handicap * self.now_Handicap < 0.0:
                return '翻转'

            if self.orignal_Handicap >= 0:
                # 主让球
                if self.now_Handicap - self.orignal_Handicap > 0:
                    return '升'
                elif self.now_Handicap - self.orignal_Handicap == 0.0:
                    return '不变'
                else:
                    return '降'
            else:
                # 客让球
                if self.now_Handicap - self.orignal_Handicap < 0:
                    return '升'
                elif self.now_Handicap - self.orignal_Handicap == 0.0:
                    return '不变'
                else:
                    return '降'



    def getwiningpercentage(self):
        if self.similerMatchURL is None:
            return
        instance = SoupHelper(self.similerMatchURL)
        spanlist = instance.gethtmllistwithlabel('span', {'id': 'result'})
        if len(spanlist) == 0 or spanlist is None:
            return
        span = spanlist[0]
        divlist = getelementlistwithlabel(span,'div', {'align':'center'})
        div = divlist[0]

        tablelist = getelementlistwithlabel(div,'table',{'width':'750'})
        if len(tablelist) > 0:
            table = tablelist[0]
            self.homeWinningPercentage = gettextlistwithlabel(table)

        subdivlist = getelementlistwithlabel(div, 'div', {'align':'center'})
        if len(subdivlist) > 0:
            subdiv = subdivlist[0]
            self.friendWiningPercentage = gettextlistwithlabel(subdiv)

        print self.companyTitle + str(self.now_Handicap)
        print self.homeWinningPercentage
        print self.friendWiningPercentage


'''
单场比赛
'''
class FootballGame:
    def __init__(self):
        # 比赛ID
        self.soccerID = 0
        # 博彩公司列表
        self.oddCompanies = []
        self.handiCompanies = []
        # 所属联赛
        self.leauge = ''
        # 开赛时间
        self.beginTime = ''
        # 主队

        self.homeTeamLevel = 0
        self.friendTeamLevel = 0

        self.homeTeam = ''
        self.homeTeam2 = ''
        # 客队
        self.friendTeam = ''
        self.friendTeam2 = ''
        # 比分
        self.halfHome = 0
        self.halfFriend = 0
        self.allHome = 0
        self.allFriend = 0

        self.now_aomenHandi = 0
        self.now_aomenOdd = (0.0, 0.0, 0.0)

        self.orignal_aomenHandi = 0
        self.orignal_aomenOdd = (0.0, 0.0, 0.0)

        # 初盘的种类.
        self.orignalHandiList = []

        # 终盘的数量
        self.nowHandiList = []

        self.nowHandiDisUnionModel = None


    @property
    def soccer(self):
        if self.allFriend == self.allHome:
            return 1
        elif self.allFriend < self.allHome:
            return 3
        else:
            return 0

    @property
    def winhandi(self):
        num = self.allHome - self.allFriend -self.now_aomenHandi
        if num > 0:
            return '赢盘'
        elif num == 0:
            return '走盘'
        else:
            return '输盘'


'''
联赛
'''
class League:
    def __init__(self):
        # 联赛ID
        self.leagueID = 0
        # 联赛名称
        self.leagueName = ''
        # 联赛简称
        self.breifLeagueName = ''
        # 联赛所属国家ID
        self.belongtoCountryID = 0
        # 可支持查询的赛季列表
        self.aviableSeasonList = []
        # 球队数量
        self.teamNumber = 0
        # 当前轮数
        self.currentRound = 0
        # 球队
        self.teams = []
        # 当前赛季
        self.currentSeason = ''

        self.aviableSeasonStr = ''



        # 附加赛ID
        self.playOffs_ID = 0
        # 附加赛决赛ID
        self.final_playOffs_ID = 0
        #正赛ID
        self.leagueSubID = 0

    def creatSeasonList(self):
        array = self.aviableSeasonStr.split(',')
        self.aviableSeasonList = array

    # def get_aviableseasonstr(self):
    #     return self.aviableseasonstr
    #
    # def set_aviableseasonstr(self, value):
    #     array = value.splite(',')
    #     self.aviableSeasonList = array
    #
    # aviableSeasonStr = property(get_aviableseasonstr, set_aviableseasonstr)

'''
国家对应的数据模型
'''
class CountrySoccer:
    def __init__(self):
        # 国家ID
        self.countryID = 0
        # 所属洲
        self.belongtoContinentID = 0
        # 国家名称
        self.countryName = ''
        # 包含的联赛列表
        self.leagueList = []

'''
大洲对应的数据
'''
class ContinentSoccer:
    def __init__(self):
        # 洲名
        self.continentName = ''
        # 洲ID
        self.continentID = 0
        # 包含的国家
        self.countryList = []