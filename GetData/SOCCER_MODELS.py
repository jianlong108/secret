#!/usr/bin/env python
# -*- coding: utf-8 -*-

from BEAUTIFUL_SOUP_HELPER import *
import time
import blackboxprotobuf
import json
'''
博彩公司
'''
class BetCompany(object):
    def __init__(self,title = '', p_gameid = 0, p_companyid = '0'):
        self.isOdd = True
        # 公司id
        self.companyID = p_companyid
        # 公司名称
        self.companyTitle = title
        # 关联的比赛id
        self.soccerGameId = p_gameid
        # 关联的比赛比赛所属联赛
        self.league = ''
        self.leagueId = ''
        # 初盘 时间
        self.oriTimeStr = ''
        # 初盘 时间戳
        self.oriTimeStamp = 0.0
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

        # 是否是最高盘口
        self.lowest = False
        # 是否是最低盘口
        self.highest = False
        # 是否是最早开盘
        self.earlyest = False
        # 盘口翻转
        self.flip = False
        # 相似盘口的链接
        self.similerMatchURL = ''
        # 指数变化
        self.trendURL = ''
        # all统计
        self.allSamePanURL = ''
        # 主队统计
        self.homeSamePanURL = ''
        # 客队统计
        self.friendSamePanURL = ''

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


    def __str__(self, print_all=False):
        if print_all:
            return '\n'.join(['%s:%s' % item for item in self.__dict__.items()])
        else:
            if self.isOdd:
                return f"欧赔[公司]id:{self.soccerGameId} id:{self.companyID} 名称:{self.companyTitle} " \
                       f"初主:{self.orignal_winOdd}初平:{self.orignal_drawOdd} 初客:{self.orignal_loseOdd} 主:{self.winOdd} 平:{self.drawOdd} 客:{self.loseOdd}"
            else:
                return f"亚盘[公司]id:{self.soccerGameId} id:{self.companyID} 名称:{self.companyTitle} 初盘时间:{self.oriTimeStr} " \
                       f"时间戳:{self.oriTimeStamp}高:{self.highest} 低:{self.lowest} 早:{self.earlyest} 初上:{self.orignal_top} " \
                       f"初盘:{self.orignal_Handicap} 初下:{self.orignal_bottom} 终上:{self.now_top} 目前盘:{self.now_Handicap} 终下:{self.now_bottom}"


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
        if self.orignal_Handicap * self.now_Handicap < 0:
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

class BaseFootballGame(object):
    def __init__(self, gameid=0):
        # 比赛ID
        self.soccerID = gameid
        # 所属联赛
        self.leauge = ''
        self.leaugeid = 0
        # 赛季
        self.season = ''
        # 开赛时间
        self.beginTime = ''
        self.beginTimestamp = 0
        # 主队名称
        self.homeTeam = ''
        # 主队id
        self.homeTeamId = 0
        # 客队
        self.friendTeam = ''
        # 客队id
        self.friendTeamId = 0
        # 主队得分
        self.allHome = 0
        # 客队得分
        self.allFriend = 0
        # 半场主队得分
        self.halfHome = 0
        # 半场客队得分
        self.halfFriend = 0
        self.panResult = ''

class DisOrderGame(BaseFootballGame):
    def __init__(self, gameid=0):
        super.__init__(gameid=gameid)
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
        # self.topMax = 0.00
        # self.bottomMax = 0.00
        # self.topMaxCompany = ''
        # self.bottomMaxCompany = ''
        # self.topMin = 0.00
        # self.bottomMin = 0.00
        # self.topMinCompany = ''
        # self.bottomMinCompany = ''

'''
单场比赛
'''
class FootballGame(object):
    def __init__(self, gameid=0):
        # 比赛ID
        self.soccerID = gameid
        # 澳门是否开盘
        self.haveAomen = True
        # 博彩公司列表
        self.oddCompanies = []
        self.yapanCompanies = []
        # 所属联赛
        self.leauge = ''
        self.leaugeid = 0
        # 赛季
        self.season = ''
        # 轮次
        self.round = 0
        # 开赛时间
        self.beginTime = ''
        self.beginTimestamp = 0
        # 主队排名
        self.homeTeamLevel = 0
        self.homeTeamLevelStr = ''
        # 客队排名
        self.friendTeamLevel = 0
        self.friendTeamLevelStr = ''
        # 主队名称
        self.homeTeam = ''
        # 主队id
        self.homeTeamId = 0
        # 主队简称
        self.homeTeam2 = ''
        # 客队
        self.friendTeam = ''
        # 客队简称
        self.friendTeam2 = ''
        # 客队id
        self.friendTeamId = 0
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
        # 澳门初始盘口
        self.orignal_aomenHandi = 0
        self.now_365Handi = 0
        # 365初始盘口
        self.orignal_365Handi = 0
        self.aomenCompany = None
        self.aomenOddCompany = None

        self.earlyestCompany = None
        # 初盘的种类
        self.orignalHandiList = []
        # 终盘的种类
        self.nowHandiList = []

        self.historypanluStr = ''

    def __str__(self, print_all=False):
        if print_all:
            return '\n'.join(['%s:%s' % item for item in self.__dict__.items()])
        else:
            return f"id:{self.soccerID} 主:{self.homeTeam} 客:{self.friendTeam} 时间:{self.beginTime} 比分:{self.allHome}-{self.allFriend} 描述:{self.historypanluStr}"

    @property
    def handiIsFilp(self):
        count = 0
        for c in self.yapanCompanies:
            if c.flip:
                count += 1
        return count > 2

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
    def db_ori_pans(self):
        json_string = json.dumps(self.orignalHandiList)
        return json_string
        # str_list = [str(num) for num in self.orignalHandiList]
        # tmp = ','.join(str_list)
        # return '[' + tmp + ']'

    @property
    def db_now_pans(self):
        json_string = json.dumps(self.nowHandiList)
        return json_string
        # str_list = [str(num) for num in self.nowHandiList]
        # tmp = ','.join(str_list)
        # return '[' + tmp + ']'


    @property
    def winhandi(self):
        if self.now_aomenHandi >= 0:
            gap = self.allHome - self.allFriend - self.now_aomenHandi
            if gap > 0.1:
                return '赢'
            elif gap < 0:
                return '输'
            else:
                return '走'
        else:
            gap = self.allFriend - self.allHome + self.now_aomenHandi
            if gap > 0.1:
                return '输'
            elif gap < 0:
                return '赢'
            else:
                return '走'

    @property
    def oriWinhandi(self):
        if self.orignal_aomenHandi >= 0:
            gap = self.allHome - self.allFriend - self.orignal_aomenHandi
            if gap > 0.1:
                return '赢'
            elif gap < 0:
                return '输'
            else:
                return '走'
        else:
            gap = self.allFriend - self.allHome + self.orignal_aomenHandi
            if gap > 0.1:
                return '输'
            elif gap < 0:
                return '赢'
            else:
                return '走'
'''
终盘不统一模型
'''
class NowHandiDisunion(FootballGame):
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
        # 总轮次
        self.rounds = 0
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

'''
球队盘路
'''

class TeamPanLuDetail:
    def __init__(self):
        # 类型：1：总盘 2：主场 3：客场 4：半场盘 5：半场主 6：半场客
        self.type = 0
        self.season = ''
        self.teamName = ''
        self.teamID = ''
        self.belongLeagueName = ''
        self.belongLeagueID = 0
        # 差值
        self.offset = 0
        # 总场次
        self.numberOfGame = 0
        # 上
        self.upNumberOfGame = 0
        # 平
        self.drawNumberOfGame = 0
        # 下
        self.downNumberOfGame = 0
        # 赢
        self.winNumberOfGame = 0
        # 走
        self.zouNumberOfGame = 0
        # 输
        self.loseNumberOfGame = 0
        # 胜率
        self.winRate = 0
        # 平率
        self.drawRate = 0
        # 输率
        self.loseRate = 0
    def __str__(self, print_all=False):
        if print_all:
            return '\n'.join(['%s:%s' % item for item in self.__dict__.items()])
        else:
            return f"{self.teamName} 胜:{self.winRate} 平:{self.drawRate} 负:{self.loseRate}"

class TeamPanLu:
    def __init__(self):
        self.season = ''
        self.teamName = ''
        self.teamID = ''
        self.belongLeagueName = ''
        self.belongLeagueID = 0
        self.suitableWinBet = False
        self.suitableLoseBet = False
        self.suitableHomeWinBet = False
        self.suitableHomeLoseBet = False
        self.suitableAwayWinBet = False
        self.suitableAwayLoseBet = False
        self.allDetail = None
        self.homeDetail = None
        self.awayDetail = None
        self.halfAllDetail = None
        self.halfHomeDetail = None
        self.halfAwayDetail = None
        self.ranking = 0
        self.homeRanking = 0
        self.awayRanking = 0
        self.halfRanking = 0
        self.halfHomeRanking = 0
        self.halfAwayRanking = 0
        self.jifenRanking = 0
        self.rounds = 0
        self.halfWinPan = 0
        self.halfDrawPan = 0
        self.halfLosePan = 0
        self.winPan = 0
        self.drawPan = 0
        self.losePan = 0
        self.homeWinPan = 0
        self.homeDrawPan = 0
        self.homeLosePan = 0
        self.awayWinPan = 0
        self.awayDrawPan = 0
        self.awayLosePan = 0
        self.winRate = 0.0
        self.drawRate = 0.0
        self.loseRate = 0.0
        self.homeWinPanRate = 0.0
        self.homeDrawPanRate = 0.0
        self.homeLosePanRate = 0.0
        self.awayWinPanRate = 0.0
        self.awayDrawPanRate = 0.0
        self.awayLosePanRate = 0.0
        self.halfWinPan = 0
        self.halfDrawPan = 0
        self.halfLosePan = 0
        self.halfHomeWinPan = 0
        self.halfHomeDrawPan = 0
        self.halfHomeLosePan = 0
        self.halfAwayWinPan = 0
        self.halfAwayDrawPan = 0
        self.halfAwayLosePan = 0
        self.halfWinRate = 0.0
        self.halfDrawRate = 0.0
        self.halfLoseRate = 0.0
        self.halfHomeWinPanRate = 0.0
        self.halfHomeDrawPanRate = 0.0
        self.halfHomeLosePanRate = 0.0
        self.halfAwayWinPanRate = 0.0
        self.halfAwayDrawPanRate = 0.0
        self.halfAwayLosePanRate = 0.0

        self.isWinest = False
        self.isLosest = False
        self.isHomeWinest = False
        self.isHomeLosest = False
        self.isAwayWinest = False
        self.isAwayLosest = False
        self.isHalfWinest = False
        self.isHalfLosest = False
        self.isHalfHomeWinest = False
        self.isHalfHomeLosest = False
        self.isHalfAwayWinest = False
        self.isHalfAwayLosest = False

    def __str__(self, print_all=False):
        if print_all:
            return '\n'.join(['%s:%s' % item for item in self.__dict__.items()])
        else:
            return f"赛季:{self.season} 球队id:{self.teamID}:{self.teamName}"
# 1主场 2客场 3半场 4半场主 5半场客
class TeamPointsUnit:
    def __init__(self):
        self.type = 0
        # 所属联赛
        self.league = ''
        self.leagueid = 0
        # 当前赛季
        self.season = ''
        # 球队名称
        self.teamName = ''
        self.teamID = 0
        self.ranking = 0
        self.gamecount = 0
        self.winCount = 0
        self.drawCount = 0
        self.loseCount = 0
        self.goalcount = 0
        self.losegoalcount = 0
        self.goaloffset = 0
        self.winRate = 0
        self.drawRate = 0
        self.loseRate = 0
        self.avgGoal = 0.0
        self.avgLostGoal = 0.0
        self.points = 0
    def __str__(self, print_all=False):
        if print_all:
            return '\n'.join(['%s:%s' % item for item in self.__dict__.items()])
        else:
            return f"赛季:{self.season} 球队id:{self.teamID}:{self.teamName} 积分:{self.points}/{self.winCount}/{self.drawCount}/{self.loseCount}"

# 球队积分模型
class TeamPoints:
    def __init__(self):
        # 所属联赛
        self.league = ''
        self.leagueid = 0
        # 当前赛季
        self.season = ''
        # 球队名称
        self.teamName = ''
        self.teamID = 0
        # 排名
        self.ranking = 0
        self.gamecount = 0
        self.winCount = 0
        self.drawCount = 0
        self.loseCount = 0
        self.goalcount = 0
        self.losegoalcount = 0
        self.goaloffset = 0
        self.winRate = 0.0
        self.drawRate = 0.0
        self.loseRate = 0.0
        self.avgGoal = 0.0
        self.avgLostGoal = 0.0
        self.points = 0
        self.homePoints = None
        self.awayPoints = None
        self.halfPoints = None
        self.halfHomePoints = None
        self.halfAwayPoints = None
    def __str__(self, print_all=False):
        if print_all:
            return '\n'.join(['%s:%s' % item for item in self.__dict__.items()])
        else:
            return f"赛季:{self.season} 球队id:{self.teamID}:{self.teamName} 积分:{self.points}/{self.winCount}/{self.drawCount}/{self.loseCount}"


class GameParserFromProtobuf(object):
    def __init__(self, oristr = None, league_id=0, league_name=''):
        self.ori_str = oristr
        self.leagueid = league_id
        self.leaguename = league_name
        self.games = []

    def parser(self):
        try:
            resultStr = self.ori_str
            # print(resultStr)
            # messagetype = {'3': {'type': 'message', 'message_typedef': {'2': {'type': 'message', 'message_typedef': {'1': {'type': 'int', 'name': ''}, '2': {'type': 'int', 'name': ''}}, 'name': ''}, '3': {'type': 'message', 'message_typedef': {'1': {'type': 'int', 'name': ''}, '2': {'type': 'int', 'name': ''}, '3': {'type': 'int', 'name': ''}, '4': {'type': 'int', 'name': ''}, '5': {'type': 'bytes', 'name': ''}, '6': {'type': 'bytes', 'name': ''}, '7': {'type': 'int', 'name': ''}, '8': {'type': 'int', 'name': ''}, '9': {'type': 'int', 'name': ''}, '11': {'type': 'int', 'name': ''}, '12': {'type': 'int', 'name': ''}, '13': {'type': 'int', 'name': ''}, '10': {'type': 'int', 'name': ''}}, 'name': ''}}, 'name': ''}}
            temp_message, typedef = blackboxprotobuf.protobuf_to_json(resultStr)
            # print(temp_message)
            # print(typedef)
            dic = json.loads(temp_message)
            contentdic = dic.get('3')
            # round 排名
            rounddic = contentdic.get('2')
            # 总round
            rounds = int(rounddic.get('1', '0'))
            # 当前round
            round = int(rounddic.get('2', '0'))
            # 比赛列表
            games = contentdic.get('3')
            for gamedic in games:
                game_id = int(gamedic.get('1', '0'))
                if game_id == 0:
                    continue
                gameobj = FootballGame(gameid=game_id)
                gameobj.leauge = self.leaguename
                gameobj.leaugeid = self.leagueid
                gameobj.round = round
                gameobj.beginTimestamp = int(gamedic.get('2', '0'))
                time_struct = time.localtime(gameobj.beginTimestamp)
                gameobj.beginTime = time.strftime("%Y-%m-%d %H:%M:%S", time_struct)
                gameobj.homeTeamId = int(gamedic.get('3', '0'))
                gameobj.friendTeamId = int(gamedic.get('4', '0'))
                gameobj.homeTeam = gamedic.get('5', '')
                gameobj.friendTeam = gamedic.get('6', '')
                gameobj.allHome = int(gamedic.get('8', '0'))
                gameobj.allFriend = int(gamedic.get('9', '0'))
                gameobj.halfHome = int(gamedic.get('10', '0'))
                gameobj.halfFriend = int(gamedic.get('11', '0'))
                gameobj.homeTeamLevel = int(gamedic.get('12', '0'))
                gameobj.friendTeamLevel = int(gamedic.get('13', '0'))
                self.games.append(gameobj)
        except Exception as e:
            print(e,dic)

class GameParserFromPlainText(object):
    def __init__(self, contentStr = ''):
        self.oriDataStr = contentStr

        self.leagueDic = {}
        self.games = []

    def parse(self):
        if len(self.oriDataStr) < 1:
            return

        allArray = self.oriDataStr.split('$$')
        # if soccer_type == 1:
        leagueStr = allArray[0]
        # else:
        #     leagueStr = allArray[1]

        allLeague = leagueStr.split('!')
        for league in allLeague:
            oneLeague = league.split('^')
            if len(oneLeague) > 1:
                self.leagueDic[oneLeague[1]] = oneLeague[0]
        # if soccer_type == 1:
            gameStr = allArray[1]
        # else:
        #     gameStr = allArray[2]

        games = gameStr.split('!')
        # 2464792^192^0^20231128180000^^川崎前锋^柔佛^0^0^^^0^0^0^0^1.25^^^0^9^1^^^0^0^0^0^1^^0^0^3^8.5^56^1^1^0^^^1989^3629
        # 比赛^联赛^是否开赛^开赛日期

        # time_s = time.strptime('201809301100', '%Y%m%d%H%M')
        # time.struct_time(tm_year=2018, tm_mon=9, tm_mday=30, tm_hour=11, tm_min=0, tm_sec=0, tm_wday=6, tm_yday=273, tm_isdst=-1) 1538276400.0
        # print(time_s, time.mktime(time_s))
        # 2018-09-30 11:00:00
        # print(time.strftime("%Y-%m-%d %H:%M:%S", time_s))
        for game in games:
            gameObj = FootballGame()
            oneGameArray = game.split('^')
            oneGameArray.remove('')

            teamidlist = game.split('^^^')
            teamidstr = teamidlist[-1]
            teamid_str_list = teamidstr.split('^')
            gameObj.homeTeamId = int(teamid_str_list[0])
            gameObj.friendTeamId = int(teamid_str_list[1])
            gameing = int(oneGameArray[2])
            if gameing != 0:
                # print "比赛已经开始或结束"
                continue
            gameObj.soccerID = int(oneGameArray[0])
            gameObj.leauge = self.leagueDic.get(oneGameArray[1])
            gameObj.leaugeid = oneGameArray[1]
            beginTime_str = oneGameArray[3]
            time_stru = time.strptime(beginTime_str, '%Y%m%d%H%M%S')
            gameObj.beginTime = time.strftime("%Y-%m-%d %H:%M:%S", time_stru)
            gameObj.beginTimestamp = time.mktime(time_stru)

            if oneGameArray[4].isdigit() or oneGameArray[4] == '':
                gameObj.homeTeam = oneGameArray[5]
                gameObj.friendTeam = oneGameArray[6]
            else:
                gameObj.homeTeam = oneGameArray[4]
                gameObj.friendTeam = oneGameArray[5]
            self.games.append(gameObj)