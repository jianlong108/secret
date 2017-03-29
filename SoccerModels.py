#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
博彩公司
'''
class BetCompany:
    def __init__(self,title,src):
        self.companyTitle = ''
        self.orignal_top = ''
        self.orignal_bottom = ''
        self.orignal_Handicap = 0.0
        self.now_top = ''
        self.now_bottom = ''
        self.now_Handicap = 0.0
        self.orignal = ''
        self.now = ''

        # 胜赔
        self.winOdd = 0.00
        # 平赔
        self.drawOdd = 0.00
        # 负赔
        self.loseOdd = 0.00

        self.falldown = False
        self.rise = False
        self.lowest = False
        self.highest = False

class LotteryCorporations:
    def __init__(self):
        self.soccerGameId = ''
        self.companyTitle = ''
        self.orignal_top = 0.0
        self.orignal_bottom = 0.0
        self.orignal_Handicap = 0.0
        self.now_top = 0.0
        self.now_bottom = 0.0
        self.now_Handicap = 0.0
        self.orignal = 0.0
        self.now = 0.0

        # 胜赔
        self.winOdd = 0.00
        # 平赔
        self.drawOdd = 0.00
        # 负赔
        self.loseOdd = 0.00

        self.falldown = False
        self.rise = False
        self.lowest = False
        self.highest = False


'''
单场比赛
'''
class FootballGame:
    def __init__(self):
        # 比赛ID
        self.soccerID = 0
        # 博彩公司列表
        self.betcompanyList = []
        # 所属联赛
        self.leauge = ''
        # 开赛时间
        self.beginTime = ''
        # 主队
        self.homeTeam = ''
        self.homeTeam2 = ''
        # 客队
        self.friendTeam = ''
        self.friendTeam2 = ''
        # 比分
        self.soccer = ''
        self.halfHome = 0
        self.halfFriend = 0
        self.allHome = 0
        self.allFriend = 0

'''
联赛
'''
class League:
    def __init__(self):
        # 联赛ID
        self.leagueID = 0
        # 联赛名称
        self.leagueName = ''
        # 联赛所属国家
        self.country = ''
        # 球队数量
        self.teamNumber = 0
        # 当前轮数
        self.currentRound = 0
        # 球队
        self.teams = []
        # 当前赛季
        self.currentSeason = ''
