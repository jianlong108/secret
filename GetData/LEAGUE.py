#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time

from DBHELPER import (insert_game_list_to_db, insertNewGameList, GET_LEAGUE_DETAIL_FROM_DB,
                      InsertLeagueJiFenALL, InsertLeagueDaXiao, InsertLeaguePanLu,
                      get_team_history_panlu_fromdb_with_teamid,insert_game_to_db)

from MySQLHelper import mysql_insert_game_to_season_games
from SOCCER_ROUND import GetRound,creatCupGameModelWithComplexStr
from NETWORKS_TOOLS import get_resultstr_with_url
from SendMail import MailHelper
import functools

from GetData.GET_GAME_PAN_ODD_DATA import *
from loguru import logger
import re

from GetData.TIME_TOOL import get_current_timestr_YMDHms


def is_valid_format(season):
    pattern = re.compile(r'^\d{4}-\d{4}$')
    return bool(pattern.match(season))



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
        resultStr = get_resultstr_with_url(self.orignalCupURL)

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
            insert_game_list_to_db(self.allGames)
            self.allGames = []

        time.sleep(2)


    def getGames(self, gameID,season):

        responseStr = ''
        url = 'http://ios.win007.com/phone/CupSaiCheng.aspx?ID=' + str(self.leagueModel.leagueID) + '&lang=0&Season=' + season + '&GroupId=' + str(gameID)
        responseStr = get_resultstr_with_url(url)

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
            # 获取积分数据的URL
            self.jifenURL = ''
            # 联赛结束时的积分排名
            self.teamPointsArr = []
            # 获取联赛盘路的URL
            self.panLuURL = ''
            # 联赛结束时的盘路排名
            self.DaXiaoURL = ''
            self.teamPanLuArr = []
            self.teamDaXiaoArr = []
            self.leagueID = ''
            self.currentSeason = ''

            self.leagueSubID = 0
            self.countOfGounds = 0
            self.currentGound = 1

            self.addtionalSubID = 0
            self.finalSubID = 0

            self.superLeague = True
            self.allGames = []
            self.allSubLeagues = []
            self.abortSeasonList = []
            self.middleSeasonTuple = ('2010-2011',1,)
            self.httpHost = ''

        else:
            return None

    # pointskind = 0总积分 1.半场积分2.主场积分3.客场积分
    def GetLeagueJiFen(self,pointskind = '0',season = '2017-2018'):
        resultStr = ''
        # url = f"http://api.letarrow.com/ios/Phone/FBDataBase/LeaguePoints.aspx?lang=0&pointsKind=0&sclassid=36&season=2023-2024&subid=0&from=48&_t=1702645393"
        self.jifenURL = 'http://%s:8072/phone/Jifen2.aspx?an=iosQiuTan&av=6.5&from=2&pointsKind=%s&r=1532144326&sclassid=%s&season=%s&subVersion=2&subid=0' % (self.httpHost,pointskind,str(self.leagueModel.leagueID).encode('utf-8'), self.currentSeason)
        print('获取联赛: %s 赛季: %s 积分数据 url %s' % (str(self.leagueModel.leagueID).encode('utf-8'), season, self.jifenURL))

        resultStr = get_resultstr_with_url(self.jifenURL)

        if resultStr != '':

            array = resultStr.split('$$')
            if len(array) > 2:
                jifenDataStr = array[2]
                teamDataArr = jifenDataStr.split('!')
                for teamDataStr in teamDataArr:
                    if len(teamDataStr) > 0:
                        temp_TeamPoints = TeamPoints()
                        self.teamPointsArr.append(temp_TeamPoints)
                        teamPointArr = teamDataStr.split('^')
                        # 1^24^切尔西^車路士^38^30^3^5^85^33^93^0^0^^^0
                        temp_TeamPoints.season = season
                        temp_TeamPoints.league = self.leagueModel.breifLeagueName
                        temp_TeamPoints.ranking = int(teamPointArr[0])
                        temp_TeamPoints.teamID = int(teamPointArr[1])
                        temp_TeamPoints.teamName = teamPointArr[2]
                        temp_TeamPoints.seasonRound = int(teamPointArr[4])
                        temp_TeamPoints.winCount = int(teamPointArr[5])
                        temp_TeamPoints.drawCount = int(teamPointArr[6])
                        temp_TeamPoints.loseCount = int(teamPointArr[7])
                        temp_TeamPoints.getScore = int(teamPointArr[8])
                        temp_TeamPoints.loseScore = int(teamPointArr[9])
                        temp_TeamPoints.points = int(teamPointArr[10])

    # 根据球队id 获取对应球队的积分排名
    def GetJifenRanking(self,teamID):
        if len(self.teamPointsArr) <= 0:
            return -1

        for teamPoints in self.teamPointsArr:
            if isinstance(teamPoints,TeamPoints):
                if teamPoints.teamID == teamID:
                    return teamPoints.ranking
                else:
                    return -1
            else:
                return -1

    def GetLeaguePanlu(self, season = '2017-2018'):
        #api.letarrow.com
        resultStr = ''
        self.panLuURL = 'http://ios.win007.com/phone/Panlu.aspx?id=%s&season=%s&apiversion=1&from=2' % (str(self.leagueModel.leagueID).encode('utf-8'), season)
        print('获取联赛: %s 赛季: %s 盘路数据 url %s' % (
        str(self.leagueModel.leagueID).encode('utf-8'), season, self.panLuURL))

        resultStr = get_resultstr_with_url(self.panLuURL)

        if resultStr != '':

            array = resultStr.split('!')
            for teamDataStr in array:
                if len(teamDataStr) > 0:
                    temp_TeamPanLu = TeamPanLu()
                    self.teamPanLuArr.append(temp_TeamPanLu)
                    teamPointArr = teamDataStr.split('^')
                    # 1^46^伯恩利^般尼^38^8^7^23^21^4^13^8
                    temp_TeamPanLu.rankIng = int(teamPointArr[0])
                    temp_TeamPanLu.teamID = int(teamPointArr[1])
                    temp_TeamPanLu.jifenRanking = self.GetJifenRanking(temp_TeamPanLu.teamID)
                    temp_TeamPanLu.teamName = teamPointArr[2]
                    temp_TeamPanLu.rounds = int(teamPointArr[4])
                    temp_TeamPanLu.halfWinPan = int(teamPointArr[5])
                    temp_TeamPanLu.halfDrawPan = int(teamPointArr[6])
                    temp_TeamPanLu.halfLosePan = int(teamPointArr[7])
                    temp_TeamPanLu.winPan = int(teamPointArr[8])
                    temp_TeamPanLu.drawPan = int(teamPointArr[9])
                    temp_TeamPanLu.losePan = int(teamPointArr[10])
                    temp_TeamPanLu.netEarningCounts = int(teamPointArr[11])
                    temp_TeamPanLu.belongLeagueName = self.leagueModel.breifLeagueName
                    temp_TeamPanLu.season = season

    def GetLeagueDaXiao(self, season = '2017-2018'):
        resultStr = ''
        self.DaXiaoURL = 'http://ios.win007.com/phone/Daxiao.aspx?id=%s&season=%s&apiversion=1&from=2' % (str(self.leagueModel.leagueID).encode('utf-8'), season)
        print('获取联赛: %s 赛季: %s 大小球数据 url %s' % (
        str(self.leagueModel.leagueID).encode('utf-8'), season, self.DaXiaoURL))

        resultStr = get_resultstr_with_url(self.DaXiaoURL)

        if resultStr != '':

            array = resultStr.split('!')
            for teamDataStr in array:
                if len(teamDataStr) > 0:
                    temp_TeamPanLu = TeamPanLu()
                    self.teamDaXiaoArr.append(temp_TeamPanLu)
                    teamPointArr = teamDataStr.split('^')

                        # 1^39^上海绿地申花^上海绿地申花^30^19^1^10^63.3%^3.3%^33.3%
                    temp_TeamPanLu.rankIng = int(teamPointArr[0])
                    temp_TeamPanLu.teamID = int(teamPointArr[1])
                    temp_TeamPanLu.jifenRanking = self.GetJifenRanking(temp_TeamPanLu.teamID)
                    temp_TeamPanLu.teamName = teamPointArr[2]
                    temp_TeamPanLu.rounds = int(teamPointArr[4])
                    temp_TeamPanLu.winPan = int(teamPointArr[5])
                    temp_TeamPanLu.drawPan = int(teamPointArr[6])
                    temp_TeamPanLu.losePan = int(teamPointArr[7])
                    temp_TeamPanLu.winRate = teamPointArr[8]
                    temp_TeamPanLu.drawRate = teamPointArr[9]
                    temp_TeamPanLu.loseRate = teamPointArr[10]
                    temp_TeamPanLu.belongLeagueName = self.leagueModel.breifLeagueName
                    temp_TeamPanLu.season = season

    # 获取此联赛是否包含附加赛,晋级赛之类的赛事
    def GetLeagueDetails(self):
        self.orignalLeagueURL = 'http://ios.win007.com/phone/SaiCheng2.aspx?sclassid=' \
                                + str(self.leagueModel.leagueID).encode(
            'utf-8') + '&season=' + self.currentSeason + '&subid=0&apiversion=1&from=2'
        resultStr = get_resultstr_with_url(self.orignalLeagueURL)

        if resultStr != '':

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
            self.GetLeagueDetails()
            self.getAllData()
            self.allSubLeagues = []
            if len(self.allGames) != 0:
                insertNewGameList(self.allGames)
            self.allGames  = []

    # 获取联赛的基本数据:积分榜,赢盘榜,大小球榜
    def Get_basic_league_data(self):
        for season in self.leagueModel.aviableSeasonList:
            if season in self.abortSeasonList:
                continue
            else:
                self.currentSeason = season
            # 获取联赛积分榜
            self.GetLeagueJiFen(pointskind = 0,season= season)
            # 获取赢盘榜
            self.GetLeaguePanlu(season = season)
            self.GetLeagueDaXiao(season = season)

            InsertLeagueJiFenALL(self.teamPointsArr)
            InsertLeaguePanLu(self.teamPanLuArr)
            InsertLeagueDaXiao(self.teamDaXiaoArr)
            self.teamPointsArr = []
            self.teamDaXiaoArr = []
            self.teamPanLuArr = []


def GetLeagueDetailFromDB(leagueid = -1,getDataType = 0 ,isCup = False):
    if leagueid < 0:
        return
    leagueArray = GET_LEAGUE_DETAIL_FROM_DB(leagueid)
    leagueModel = League()
    if leagueArray is not None:
        leagueModel.leagueID = leagueArray[0]
        leagueModel.leagueName = leagueArray[1].encode('utf-8')
        leagueModel.breifLeagueName = leagueArray[2].encode('utf-8')
        leagueModel.aviableSeasonStr = leagueArray[5].encode('utf-8')
        if '2018-2019' in leagueModel.aviableSeasonList:
            leagueModel.aviableSeasonList.remove('2018-2019')
        elif '2018' in leagueModel.aviableSeasonList:
            leagueModel.aviableSeasonList.remove('2018')


        httpHomeStr = get_resultstr_with_url('http://119.29.29.29/d?ttl=1&dn=txt.city007.net')
        httpHomeList = httpHomeStr.split(';')
        host = httpHomeList[0]

        # 杯赛去请求杯赛接口,逻辑
        if isCup == 0:
            cup = GetCup(leagueModel)
            cup.cupName = leagueModel.breifLeagueName
            cup.getOfficialLeague()
        #     否则全部视为联赛
        else:
            league = GetLeague(leagueModel)
            league.httpHost = host
            if getDataType == 0:
                league.getOfficialLeague()
            elif getDataType == 1:
                league.Get_basic_league_data()
            elif getDataType == 2:
                header = leagueModel.aviableSeasonList
                league.GetLeaguePanlu('2018-2019')
                currentSeason = '2018-2019'
                if not len(league.teamPanLuArr) > 0:
                    league.GetLeaguePanlu('2018')
                    currentSeason = '2018'
                team_panlu_list = []
                header.insert(0,currentSeason)
                header.insert(0,'联赛')
                header.insert(0, '球队')
                # header = ['球队', '联赛',
                #           '2018-2019', '2017-2018', '2016-2017', '2015-2016', '2014-2015', '2013-2014',
                #           '2012-2013', '2011-2012', '2010-2011', '2009-2010', '2008-2009', '2007-2008',
                #           '2006-2007',
                #           '2005-2006', '2004-2005', '2003-2004']

                for teamPanlu in league.teamPanLuArr:
                    if isinstance(teamPanlu, TeamPanLu):
                        # 插入当前赛季
                        one_team_data = [teamPanlu.teamName.decode('utf-8'), leagueModel.breifLeagueName.decode('utf-8'),
                                         str(teamPanlu.winPan * 100 / teamPanlu.rounds), '', '', '', '', '', '', '', '', '',
                                         '', '',
                                         '', '', '', '']

                        gamelist = get_team_history_panlu_fromdb_with_teamid(teamPanlu.teamID, leagueModel.breifLeagueName)

                        for tempGameTuple in gamelist:
                            if tempGameTuple[0] in header:
                                index = header.index(tempGameTuple[0])
                                winCount = tempGameTuple[3]
                                rounds = tempGameTuple[2]
                                if rounds == 0:
                                    continue
                                rate = str(winCount * 100 / rounds)
                                one_team_data.insert(index, rate)

                        team_panlu_list.append(one_team_data)

                # write_excel(team_panlu_list)


def getSeasonGamelist(season, leagueid=36, league='英超', maxround= 38):
    cur_round = maxround
    if season == '2023-2024':
        cur_round = 16
    while cur_round > 0:
        print(f"获取联赛数据 {league} 赛季:{season} 轮次:{cur_round}")
        games = getRoundGames(season=season, leagueid=leagueid, league=league, round=cur_round)
        for game in games:
            game.season = season
            getOneGameHandiList(game)
            time.sleep(3)
            getOneGameOddList(game)
            time.sleep(3)
            mysql_insert_game_to_season_games(game)
        # insert_game_list_to_db(games)
        time.sleep(3)
        cur_round -= 1


# 0 代表最新一轮； >=1 实际赛程
def getRoundGames(season='2023-2024', leagueid=36, league='英超', round = 0):
    round_game_url = f"http://api.letarrow.com/ios/Phone/FBDataBase/LeagueSchedules.aspx?lang=0&round={round}&sclassid={leagueid}&season={season}&subid=0&from=48&_t={str(int(time.time()))}"
    round_game_headers = {
    'User-Agent': 'QTimesApp/3.0 (Letarrow.QTimes; build:39; iOS 17.1.0) Alamofire/5.4.',
    'cookie': 'aiappfrom=48'
    }
    try:
        round_game_response = requests.get(round_game_url, headers=round_game_headers)
        if round_game_response.ok:
            round_game_content_type = round_game_response.headers.get('Content-Type')
            # print(content_type)
            if 'application/x-protobuf' == round_game_content_type:
                round_game_resultStr = round_game_response.content
                obj = GameParserFromProtobuf(oristr=round_game_resultStr, league_id=leagueid, league_name=league)
                obj.parser()
                return obj.games
    except Exception as a_e:
        print('获取联赛数据', url, a_e)
        traceback.print_exc()
        return []


def compare_game_begintime(x,y):
    if x.beginTimestamp > y.beginTimestamp:
        return 1
    elif x.beginTimestamp < y.beginTimestamp:
        return -1
    else:
        return 0

def compare_game(x,y):
    if x.beginTimestamp > y.beginTimestamp:
        return 1
    elif x.beginTimestamp < y.beginTimestamp:
        return -1
    else:
        return 0

# 如果没有连接本地数据库，就不能更新，故增加了这个属性进行控制
def updateCurrentSeasonPanlu(par_write_SQL = True):
    league_dic = {"8":"德甲","9":"德乙","11":"法甲","12":"法乙",
               "16":"荷甲","17":"荷乙","23":"葡超","27":"瑞超",
                "29":"苏超","31":"西甲","33":"西乙","36":"英超",
               "37":"英冠","39":"英甲","34":"意甲","40":"意乙"}
    round_dic = {}
    # round_dic = {"德甲":"25","德乙":"25","法甲":"25","法乙":"28",
    #            "荷甲":"25","荷乙":"29","葡超":"25","瑞超":"27",
    #             "苏超":"19","西甲":"28","西乙":"30","英超":"28",
    #            "英冠":"39","英甲":"41","意甲":"28","意乙":"29"}
    furture_game_list = []
    try:
        for key,value in league_dic.items():
            specialDic = parsePanlu(season='2023-2024', leagueid=key, leaguename=value,writeSQL=par_write_SQL)
            if specialDic is None:
                specialDic = parsePanlu(season='2023-2024', leagueid=key, leaguename=value,writeSQL=par_write_SQL)
                if specialDic is None:
                    time.sleep(3)
                    print(value,'没有specialDic')
                    continue
            time.sleep(3)
            roundnum = 0
            if value in round_dic:
                roundnum = int(round_dic[value]) - 1
            if roundnum < 0:
                roundnum = 0
            games = getRoundGames(season='2023-2024', leagueid=key, league=value, round=str(roundnum))
            if len(games) == 0:
                games = getRoundGames(season='2023-2024', leagueid=key, league=value, round=str(roundnum))
                if len(games) == 0:
                    time.sleep(3)
                    print(value,'没有games')
                    continue
            homelist = specialDic.get("主场盘路", [])
            awaylist = specialDic.get("客场盘路", [])
            halfhomelist = specialDic.get("半场主场盘路", [])
            halfawaylist = specialDic.get("半场客场盘路", [])
            print(value)
            for g in games:
                getOneGameHandiList(g)
                for detail in homelist:
                    if detail.teamName == g.homeTeam:
                        g.historypanluStr = g.historypanluStr + "{}主场盘路:{}".format(value,detail)
                        furture_game_list.append(g)
                    else:
                        pass

                for detail in awaylist:
                    if detail.teamName == g.friendTeam:
                        g.historypanluStr = g.historypanluStr + "{}客场盘路:{}".format(value,detail)
                        furture_game_list.append(g)
                    else:
                        pass

                for detail in halfhomelist:
                    if detail.teamName == g.homeTeam:
                        g.historypanluStr = g.historypanluStr + "{}半场主场盘路:{}".format(value,detail)
                        furture_game_list.append(g)
                    else:
                        pass

                for detail in halfawaylist:
                    if detail.teamName == g.friendTeam:
                        g.historypanluStr = g.historypanluStr + "{}半场客场盘路:{}".format(value,detail)
                        furture_game_list.append(g)
                    else:
                        pass
            time.sleep(5)
    except BaseException as oneE:
        print('updateCurrentSeasonPanlu', oneE)
        traceback.print_exc()

    furture_game_list.sort(key=functools.cmp_to_key(compare_game_begintime))
    for g in furture_game_list:
        print(g)



def getLeagueHistoryPanluFrom5Round(p_league_id = 36, p_league_name = '英超', p_season = '2023-2024'):
    """
        获取联赛 前5轮的历史盘路
        :param p_league_id:
        :param p_league_name:
        :param p_season:
    """
    for i in range(1, 6):
        games = getRoundGames(season=p_season, league=p_league_name, leagueid=p_league_id, round=1)
        for g in games:
            getOneGameHandiList(g)
    # furture_game_list = []
    # try:
    #     specialDic = parsePanlu(season='2023-2024', leagueid=p_league_id, leaguename=p_league_name,writeSQL=False)
    #     if specialDic is None:
    #         specialDic = parsePanlu(season='2023-2024', leagueid=p_league_id, leaguename=p_league_name,writeSQL=False)
    #         if specialDic is None:
    #             time.sleep(3)
    #             print('{}没有获取到盘路情况' % {p_league_name})
    #             return
    #     time.sleep(3)
    #     roundnum = 27
    #     games = getRoundGames(season='2023-2024', leagueid=p_league_id, league=p_league_name, round=str(roundnum))
    #     if len(games) == 0:
    #         games = getRoundGames(season='2023-2024', leagueid=p_league_id, league=p_league_name, round=str(roundnum))
    #         if len(games) == 0:
    #             time.sleep(3)
    #             print('{}第{}轮没有获取到games' % {p_league_name,roundnum})
    #             return
    #     homelist = specialDic.get("主场盘路", [])
    #     awaylist = specialDic.get("客场盘路", [])
    #     halfhomelist = specialDic.get("半场主场盘路", [])
    #     halfawaylist = specialDic.get("半场客场盘路", [])
    #     print('正在获取{} 第{}轮的比赛情况'.format(p_league_name,roundnum))
    #     for g in games:
    #         getOneGameHandiList(g)
    #         for detail in homelist:
    #             if detail.teamName == g.homeTeam:
    #                 # 主队 赢盘率高，期望 输
    #                 g.historypanluStr = g.historypanluStr + "{}主场盘路:{} 期望:{}盘".format(p_league_name,detail,'输'if detail.winRate>detail.loseRate else "赢")
    #                 furture_game_list.append(g)
    #             else:
    #                 pass
    #
    #         for detail in awaylist:
    #             if detail.teamName == g.friendTeam:
    #                 # 客队 赢盘率高 期望 主队赢盘
    #                 g.historypanluStr = g.historypanluStr + "{}客场盘路:{} 期望:{}盘".format(p_league_name,detail,'赢'if detail.winRate>detail.loseRate else "输")
    #                 furture_game_list.append(g)
    #             else:
    #                 pass
    #
    #         for detail in halfhomelist:
    #             if detail.teamName == g.homeTeam:
    #                 g.historypanluStr = g.historypanluStr + "{}半场主场盘路:{} 期望:{}盘".format(p_league_name,detail,'输'if detail.winRate>detail.loseRate else "赢")
    #                 furture_game_list.append(g)
    #             else:
    #                 pass
    #
    #         for detail in halfawaylist:
    #             if detail.teamName == g.friendTeam:
    #                 g.historypanluStr = g.historypanluStr + "{}半场客场盘路:{} 期望:{}盘".format(p_league_name,detail,'赢'if detail.winRate>detail.loseRate else "输")
    #                 furture_game_list.append(g)
    #             else:
    #                 pass
    #     time.sleep(5)
    # except BaseException as oneE:
    #     print('updateCurrentSeasonPanlu', oneE)
    #     traceback.print_exc()
    #
    # furture_game_list.sort(key=functools.cmp_to_key(compare_game))
    # for g in furture_game_list:
    #     print(g, f"终盘:{g.now_365Handi}赛果：", g.win365Handi, f"初盘:{g.orignal_365Handi}赛果：", g.ori365Winhandi)


global_league_arr = [
    {"1":8, "2":"德甲" , "3":"2024-2025","4":38,"5":8},
    {"1":9, "2":"德乙" , "3":"2024-2025","4":38,"5":8},
    {"1":11, "2":"法甲", "3":"2024-2025","4":38,"5":8},
    {"1":12, "2":"法乙", "3":"2024-2025","4":38,"5":8},
    {"1":16, "2":"荷甲", "3":"2024-2025","4":38,"5":8},
    {"1":17, "2":"荷乙", "3":"2024-2025","4":38,"5":8},
    {"1":23, "2":"葡超", "3":"2024-2025","4":38,"5":8},
    {"1":27, "2":"瑞超", "3":"2024-2025","4":38,"5":8},
    {"1":29, "2":"苏超", "3":"2024-2025","4":38,"5":8},
    {"1":31, "2":"西甲", "3":"2024-2025","4":38,"5":8},
    {"1":33, "2":"西乙", "3":"2024-2025","4":38,"5":8},
    {"1":36, "2":"英超", "3":"2024-2025","4":38,"5":8},
    {"1":37, "2":"英冠", "3":"2024-2025","4":38,"5":8},
    {"1":39, "2":"英甲", "3":"2024-2025","4":38,"5":8},
    {"1":34, "2":"意甲", "3":"2024-2025","4":38,"5":8},
    {"1":40, "2":"意乙", "3":"2024-2025","4":38,"5":8},
    {"1":25, "2":"日职联", "3":"2024"   ,"4":38, "5":8},
    {"1":60, "2":"中超", "3":"2024"     ,"4":38,"5":8}
]

class GetLeagueGameObject:
    # 类属性定义
    # maxround = 34
    def __init__(self, lid, lname):
        self.leagueid = int(lid)
        self.leaguename = lname
        self.maxround = 34
        self.currentSeason = '2024'
        self.subleague = None

    def seasonIsvaild(self, curSeason):
        return True

class GetCurrentSeasonPanluObject(GetLeagueGameObject):
    def seasonIsvaild(self, curSeason):
        return self.currentSeason == curSeason

def getAllSeasonPanlu(spSeasonid=0):
    logger.add("/Users/jl/Desktop/soccer/{}_getLeaguePanlu.txt".format(get_current_timestr_YMDHms()))
    headers = {
        'User-Agent': 'QTimesApp/3.0 (Letarrow.QTimes; build:39; iOS 17.1.0) Alamofire/5.4.',
        'cookie': 'aiappfrom=48'
    }
    _allLeagueNextRoundGamedic = {}
    try:
        for season in global_league_arr:
            league_id_in_dic = season.get("1", 0)
            league_name_in_dic = season.get("2", "")
            season_in_dic = season.get("3", "")
            if spSeasonid != 0 and league_id_in_dic != 0 and spSeasonid != league_id_in_dic:
                continue
            logger.debug(f"开始获取当前赛季盘路--{league_id_in_dic} {league_name_in_dic}")
            getPanluObj = GetCurrentSeasonPanluObject(lid=league_id_in_dic, lname=league_name_in_dic)
            getPanluObj.currentSeason = season_in_dic
            getPanluObj.maxround = 38
            timestr = str(int(time.time()))
            url = f"http://api.letarrow.com/pcf/bfmatch/api/database/v1/leaguedetail?kind=1&lang=0&sid={getPanluObj.leagueid}&_t={timestr}"
            response = requests.get(url, headers=headers)
            if response.ok and response.headers.get('Content-Type', '') == 'application/x-protobuf':
                resultStr = response.content
                temp_message, typedef = blackboxprotobuf.protobuf_to_json(resultStr)
                # logger.info("protobuf解析后: {}".format(temp_message))
                leaguedic = json.loads(temp_message)
                league_id = int(leaguedic.get('1', '0'))
                if league_id != getPanluObj.leagueid:
                    raise ValueError(f"联赛id异常 {league_id} != {getPanluObj.leagueid}")
                leaguename = leaguedic.get('2', '')

                for s in leaguedic.get('4', []):
                    if not getPanluObj.seasonIsvaild(s):
                        logger.debug(f"{s} 校验不通过 continue")
                        continue
                    specialDic = parsePanlu(season=s, leagueid=league_id, leaguename=leaguename,minCount=5)
                    time.sleep(1)
                    allgames = getNextRoundGames(league_id, cur_season=season_in_dic)
                    for game in allgames:
                        body = f"{season_in_dic}:{leaguename} | {game}"
                        gameHtmlContent = body
                        for (k, v) in specialDic.items():
                            if not isinstance(v, list):
                                continue
                            for tmpDetail in v:
                                if not isinstance(tmpDetail, TeamPanLuDetail):
                                    continue
                                if gameAndPanluDetailIsMatch(game, tmpDetail):
                                    if "<ul>" not in gameHtmlContent:
                                        gameHtmlContent += "<ul>"
                                    body += f"\n {k} {tmpDetail}"
                                    gameHtmlContent += f"<li> {k} : {tmpDetail} </li>"
                        # 对所有 符号条件的比赛 根据开赛时间 加以颜色标识
                        color = "black"
                        if "<ul>" in gameHtmlContent:
                            gameHtmlContent += "</ul>"
                            if game.beginTimestamp > time.time():
                                hour = (game.beginTimestamp - time.time()) / 3600
                                # 增加颜色区分，便于
                                if hour > 72:
                                    color = "chocolate"
                                elif  hour > 60:
                                    color = "orangered"
                                elif  hour > 48:
                                    color = "purple"
                                elif hour > 24:
                                    color = "green"
                                elif hour > 12:
                                    color = "blue"
                                else:
                                    color = "red"
                            else:
                                color = "gray"
                        gameHtmlContent = f"<p style=\"color: {color};\">{gameHtmlContent}</p>"
                        _allLeagueNextRoundGamedic[game] = gameHtmlContent

                        logger.info(body)
                    time.sleep(3)

            else:
                raise Exception('请求{}:出错'.format(url))
    except Exception as e:
        logger.error(e)
    finally:
        html_content = """
                       <html>
                       <head></head>
                       <body>
                       """

        html_content_end = """
                       </body>
                       </html>
                       """
        sorted_games = dict(sorted(_allLeagueNextRoundGamedic.items(), key=lambda item: item[0].beginTimestamp))

        # 打印排序后的字典
        for game, game_html_content in sorted_games.items():
            html_content += game_html_content
        html_content += html_content_end
        if html_content != "":
            mailobj = MailHelper()
            # mailobj.sendMailWithPlainText(get_current_timestr_YMDHms(), mailBody)
            mailobj.sendMailWithHtml(f'{get_current_timestr_YMDHms()}:盘路分析', html_content)

# 获取当前轮次的比赛
def getNextRoundGames(leagueid, cur_season='2024-2025', roundnum=0):
    headers = {
        'User-Agent': 'QTimesApp/3.0 (Letarrow.QTimes; build:39; iOS 17.1.0) Alamofire/5.4.',
        'cookie': 'aiappfrom=48'
    }
    allgameObjs = []
    try:
        timestr = str(int(time.time()))
        url = f"http://api.letarrow.com/ios/Phone/FBDataBase/LeagueSchedules.aspx?lang=0&round={roundnum}&sclassid={leagueid}&season={cur_season}&subid=0&from=48&_t={timestr}"
        response = requests.get(url, headers=headers)
        if response.ok and response.headers.get('Content-Type') == 'application/x-protobuf':
            resultStr = response.content
            temp_message, typedef = blackboxprotobuf.protobuf_to_json(resultStr)

            leaguedic = json.loads(temp_message)
            threeDic = leaguedic.get('3', {})
            # '1': {'1': '1778', '2': '联赛', '3': '1', '4': '1'}
            leagueinfo = threeDic.get('1', {})
            # '2': {'1': '34', '2': '5', '3': '5'}
            roundinfo = threeDic.get('2', {})
            roundcount = roundinfo.get('1', '0')
            curround = roundinfo.get('2', '0')
            # '3': [{'1': '2639227', '2': '1726855200', '3': '5961', '4': '393', '5': '马蒂格', '6': '格勒诺布尔', '12': '14', '13': '8'}, {'.......
            allgames = threeDic.get('3', [])

            for gameinfo in allgames:
                gameid = gameinfo.get('1','0')
                if gameid == '0':
                    continue
                gameobj = BaseGame(gameid=int(gameid))
                gameobj.round = int(curround)
                gameobj.beginTimestamp = int(gameinfo.get('2','0'))
                gameobj.homeTeamId = int(gameinfo.get('3', '0'))
                gameobj.homeTeam = gameinfo.get('5','')
                gameobj.friendTeamId = int(gameinfo.get('4', '0'))
                gameobj.friendTeam = gameinfo.get('6','')
                gameobj.homeTeamLevel = int(gameinfo.get('12','0'))
                gameobj.friendTeamLevel = int(gameinfo.get('13','0'))
                allgameObjs.append(gameobj)
                logger.debug(gameobj)
        else:
            raise Exception('请求{}:出错'.format(response.status_code))
    except Exception as e:
        print(e)
    finally:
        return allgameObjs

def gameAndPanluDetailIsMatch(gameObj, panluDeatil):
    if not isinstance(gameObj, BaseGame):
        return False
    if not isinstance(panluDeatil, TeamPanLuDetail):
        return False
    # 类型：1：总盘 2：主场 3：客场 4：半场盘 5：半场主 6：半场客
    if panluDeatil.type == 1 or panluDeatil.type == 4:
        if gameObj.homeTeamId == panluDeatil.teamID or gameObj.friendTeamId == panluDeatil.teamID:
            return True
        else:
            return False
    elif panluDeatil.type == 2 or panluDeatil.type == 5:
        if gameObj.homeTeamId == panluDeatil.teamID:
            return True
        else:
            return False
    elif panluDeatil.type == 3 or panluDeatil.type == 6:
        if gameObj.friendTeamId == panluDeatil.teamID:
            return True
        else:
            return False
    else:
        return False


if __name__ == '__main__':
    getAllSeasonPanlu()
    exit(0)
    # logger.add("/Users/jl/Desktop/soccer/{}getLeague.log".format(get_current_timestr_YMDHms()))
    # updateCurrentSeasonPanlu(par_write_SQL=False)
    # getLeagueHistoryPanluFrom5Round()
    # exit(0)
    #英超 联赛 盘路 积分 已完成 36
    #英冠 盘路  已完成 37
    #德甲 盘路  已完成 8
    #德乙 盘路  已完成 9
    #意甲 盘路  已完成 34
    #西甲 盘路  已完成 31
    #法甲 盘路  已完成 11
    #法乙 盘路 联赛  已完成 12
    #意乙 盘路 已完成 40
    #西乙 盘路 已完成 33
    #葡超 盘路 已完成 23
    #荷甲 盘路 已完成 16
    #荷乙 盘路 积分 已完成 17/94
    #苏超 盘路 完成 29
    # 瑞超 盘路 完成 27
    getPanluObj = GetCurrentSeasonPanluObject(lid=12, lname='英超')
    getPanluObj.currentSeason = '2024-2025'
    getPanluObj.maxround = 38
    headers = {
        'User-Agent': 'QTimesApp/3.0 (Letarrow.QTimes; build:39; iOS 17.1.0) Alamofire/5.4.',
        'cookie': 'aiappfrom=48'
    }
    timestr = str(int(time.time()))
    url = f"http://api.letarrow.com/pcf/bfmatch/api/database/v1/leaguedetail?kind=1&lang=0&sid={getPanluObj.leagueid}&_t={timestr}"
    try:
        response = requests.get(url, headers=headers)
        if response.ok:
            content_type = response.headers.get('Content-Type')
            logger.info("{}  type: {}".format(url,content_type))
            if 'application/x-protobuf' == content_type:
                resultStr = response.content
                temp_message, typedef = blackboxprotobuf.protobuf_to_json(resultStr)
                logger.info("protobuf解析后: {}".format(temp_message))
                leaguedic = json.loads(temp_message)
                league_id = int(leaguedic.get('1', '0'))
                if league_id != getPanluObj.leagueid:
                    raise ValueError(f"联赛id异常 {league_id} != {getPanluObj.leagueid}")

                leaguename = leaguedic.get('2', '')
                seasons = leaguedic.get('4', [])
                for s in seasons:
                    if not getPanluObj.seasonIsvaild(s):
                        logger.debug(f"{s} 校验不通过 continue")
                        continue
                    # getSeasonGamelist(s, league_id, leaguename, getleaguegameobj.maxround)
                    parsePanlu(season=s,leagueid=league_id,leaguename=leaguename)
                    # parseJifen(season=s,leagueid=league_id,leaguename=leaguename,subleagueid=_sub_league_id)
                    time.sleep(3)
        else:
            raise Exception('请求{}:出错'.format(url))
    except Exception as e:
        logger.error(e)








