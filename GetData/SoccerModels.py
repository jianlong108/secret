#!/usr/bin/env python
# -*- coding: utf-8 -*-

from BeautifulSoupHelper import *

'''
博彩公司
'''
class BetCompany(object):
    def __init__(self,title = '',src = ''):
        # 公司id
        self.companyID = 0
        # 公司名称
        self.companyTitle = title
        # 比赛id
        self.soccerGameId = ''
        # 比赛所属联赛
        self.league = ''
        # 初盘 主队水位
        self.orignal_top = 0.00
        # 初盘 客队水位
        self.orignal_bottom = 0.00
        # 初盘 盘口
        self.orignal_Handicap = 0.00
        # 终盘 主队水位
        self.now_top = 0.00
        # 终盘 客队水位
        self.now_bottom = 0.00
        # 终盘 盘口
        self.now_Handicap = 0.00

        # *********begin************
        # ********暂时不用**********
        # ************************
        # 欧亚转换后的 主队水位
        self.exchange_top = 0.00
        # 欧亚转换后的 客队水位
        self.exchange_bottom = 0.00
        # 欧亚转换后的 盘口
        self.exchange_Handicap = 0.00
        #
        self.homeWinningPercentage = ''
        self.friendWiningPercentage = ''
        # **********end***********
        # ************************

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

        # 结果 310
        self.result = -1

        # 主队得分
        self.homeSoccer = -1
        # 客队得分
        self.friendSoccer = -1

        # 是否是最高盘口
        self.lowest = False
        # 是否是最低盘口
        self.highest = False

    @property
    def resultStr(self):
        if self.now_Handicap >= 0:
            if self.homeSoccer - self.friendSoccer - self.now_Handicap > 0:
                return '赢'
            elif self.homeSoccer - self.friendSoccer - self.now_Handicap == 0.0:
                return '走'
            else:
                return '输'
        else:
            if self.friendSoccer - self.homeSoccer - self.now_Handicap > 0:
                return '赢'
            elif self.friendSoccer - self.homeSoccer - self.now_Handicap == 0.0:
                return '走'
            else:
                return '输'

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
class FootballGame(object):
    def __init__(self):
        # 比赛ID
        self.soccerID = 0
        # 博彩公司列表
        self.oddCompanies = []
        self.handiCompanies = []
        # 所属联赛
        self.leauge = ''
        self.leaugeid = 0
        # 开赛时间
        self.beginTime = ''
        # 主队排名
        self.homeTeamLevel = 0
        # 客队排名
        self.friendTeamLevel = 0
        # 主队名称
        self.homeTeam = ''
        # 主队简称
        self.homeTeam2 = ''
        # 客队
        self.friendTeam = ''
        # 客队简称
        self.friendTeam2 = ''
        # 半场主队得分
        self.halfHome = 0
        # 半场客队得分
        self.halfFriend = 0
        # 主队得分
        self.allHome = 0
        # 客队得分
        self.allFriend = 0
        # 澳门即时盘口
        self.now_aomenHandi = 0
        # 澳门即时欧赔
        self.now_aomenOdd = (0.0, 0.0, 0.0)
        # 澳门初始盘口
        self.orignal_aomenHandi = 0
        # 澳门初始欧赔
        self.orignal_aomenOdd = (0.0, 0.0, 0.0)

        # 初盘的种类
        self.orignalHandiList = []

        # 终盘的种类
        self.nowHandiList = []

        # 终盘不统一
        self.ori_maxHandi = 10
        self.ori_minHandi = 10
        self.ori_maxHandiCompany = ''
        self.ori_minHandiCompany = ''
        self.ori_topMax = 0.00
        self.ori_bottomMax = 0.00
        self.ori_topMaxCompany = ''
        self.ori_bottomMaxCompany = ''
        self.ori_topMin = 0.00
        self.ori_bottomMin = 0.00
        self.ori_topMinCompany = ''
        self.ori_bottomMinCompany = ''

        self.maxHandi = 10
        self.minHandi = 10
        self.maxHandiCompany = ''
        self.minHandiCompany = ''
        self.topMax = 0.00
        self.bottomMax = 0.00
        self.topMaxCompany = ''
        self.bottomMaxCompany = ''
        self.topMin = 0.00
        self.bottomMin = 0.00
        self.topMinCompany = ''
        self.bottomMinCompany = ''

    @property
    def nowHandiDisUnion(self):
        if len(self.nowHandiList) > 1:
            return 1
        else:
            return 0

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
        if self.now_aomenHandi >= 0:
            if self.allHome - self.allFriend - self.now_aomenHandi > 0:
                return '赢'
            elif self.allHome - self.allFriend - self.now_aomenHandi == 0.0:
                return '走'
            else:
                return '输'
        else:
            if self.allFriend - self.allHome - self.now_aomenHandi > 0:
                return '赢'
            elif self.allFriend - self.allHome - self.now_aomenHandi == 0.0:
                return '走'
            else:
                return '输'

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

        # 0 不变 1 升 2 降 3反转
        # self.handi_change = -1
    @property
    def handi_change(self):
        if self.ori_handi * self.now_handi == 0.0:
            if self.now_handi - self.ori_handi == 0.0:
                return 1
            else:
                return
        elif self.ori_handi * self.now_handi < 0.0:
            return 3
        else:
            return 0

'''
联赛
'''
class League:
    def __init__(self):
        # 联赛ID
        self.leagueID = 0
        self.subLeagueID = 0
        # 联赛名称
        self.leagueName = ''
        # 联赛简称
        self.breifLeagueName = ''
        # 联赛所属国家ID
        self.belongtoCountryID = 0
        self.belongtoCountryName = ''
        self.belongtoContinentName = ''
        # 可支持查询的赛季列表
        # self.aviableSeasonList = []
        # 球队数量
        self.teamNumber = 0
        # 当前轮数
        self.currentRound = 0
        # 球队
        self.teams = []
        # 当前赛季
        self.currentSeason = ''
        self._aviableSeasonList = []
        self.aviableSeasonStr = ''
        # 附加赛ID
        self.playOffs_ID = 0
        # 附加赛决赛ID
        self.final_playOffs_ID = 0
        #正赛ID
        self.leagueSubID = 0

    @property
    def aviableSeasonList(self):
        if len(self._aviableSeasonList) > 0:
            return self._aviableSeasonList
        else:
            self._aviableSeasonList = self.aviableSeasonStr.split(',')
            return self._aviableSeasonList

'''
国家对应的数据模型
'''
class CountrySoccer:
    def __init__(self):
        # 国家ID
        self.countryID = 0
        # 所属洲
        self.belongtoContinentID = 0
        self.belongtoContinentName = ''
        # 国家名称
        self.countryName = ''

'''
大洲对应的数据
'''
class ContinentSoccer:
    def __init__(self):
        # 洲名
        self.continentName = ''
        # 洲ID
        self.continentID = 0

class TeamPanLu:
    def __init__(self):
        self.season = ''
        self.teamName = ''
        self.teamID = ''
        self.belongLeagueName = ''
        self.rankIng = 0
        self.jifenRanking = 0
        self.rounds = 0
        self.halfWinPan = 0
        self.halfDrawPan = 0
        self.halfLosePan = 0
        self.winPan = 0
        self.drawPan = 0
        self.losePan = 0
        self.winRate = ''
        self.drawRate = ''
        self.loseRate = ''
        # 净盈利场数
        self.netEarningCounts = 0

# 球队积分模型
class TeamPoints:
    def __init__(self):
        # 所属联赛
        self.league = ''
        # 当前赛季
        self.season = ''
        # 赛季总轮数
        self.seasonRound = 0
        # 球队名称
        self.teamName = ''
        self.teamID = 0
        # 排名
        self.ranking = 0
        self.halfRanking = 0
        self.homeRanking = 0
        self.friendRanking = 0
        # 获胜的场次数量
        self.winCount = 0
        self.halfWinCount = 0
        self.homeWinCount = 0
        self.friendWinCount = 0
        # 平掉的场次数量
        self.drawCount = 0
        self.halfDrawCount = 0
        self.homeDrawCount = 0
        self.friendDrawCount = 0
        # 输掉的场次数量
        self.loseCount = 0
        self.halfLoseCount = 0
        self.homeLoseCount = 0
        self.friendLoseCount = 0
        # 进球数
        self.getScore = 0
        self.homeGetScore = 0
        self.friendGetScore = 0
        self.halfGetScore = 0
        # 失球数
        self.loseScore = 0
        self.halfLoseScore = 0
        self.homeLoseScore = 0
        self.friendLoseScore = 0
        # 赛季积分
        self.points = 0
        # 赛季半场积分
        self.halfPoints = 0
        # 主场积分
        self.homePoints = 0
        # 客场积分
        self.friendPoints = 0
