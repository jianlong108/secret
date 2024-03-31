#!/usr/bin/env python
# -*- coding: utf-8 -*-

from DBHELPER import (insert_game_list_to_db, insertNewGameList, GET_LEAGUE_DETAIL_FROM_DB,
                      InsertLeagueJiFenALL, InsertLeagueDaXiao, InsertLeaguePanLu,
                      get_team_history_panlu_fromdb_with_teamid,insert_game_to_db)
from SOCCER_ROUND import GetRound,creatCupGameModelWithComplexStr
from NETWORKS_TOOLS import get_resultstr_with_url
import functools

from GetData.GET_GAME_PAN_ODD_DATA import *

import re


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


def getSeasonGamelist(season, leagueid=36, league='英超'):
    headers = {
    'User-Agent': 'QTimesApp/3.0 (Letarrow.QTimes; build:39; iOS 17.1.0) Alamofire/5.4.',
    'cookie': 'aiappfrom=48'
    }
    round = 38
    if season == '2023-2024':
        round = 16
    while round > 0:
        timestr = str(int(time.time()))
        url = f"http://api.letarrow.com/ios/Phone/FBDataBase/LeagueSchedules.aspx?lang=2&round={round}&sclassid={leagueid}&season={season}&subid=0&from=48&_t={timestr}"
        try:
            response = requests.get(url, headers=headers)
            if response.ok:
                content_type = response.headers.get('Content-Type')
                # print(content_type)
                if 'application/x-protobuf' == content_type:
                    resultStr = response.content
                    print(url, resultStr)
                    obj = GameParserFromProtobuf(oristr=resultStr, league_id=leagueid, league_name=league)
                    obj.parser()
                    for game in obj.games:
                        game.season = season
                        getOneGameHandiList(game)
                        time.sleep(3)
                        getOneGameOddList(game)
                        time.sleep(3)
                    insert_game_list_to_db(obj.games)
        except Exception as e:
            print('获取联赛数据', url, e)
        time.sleep(3)
        round -= 1

def getRoundGames(season, leagueid=36, league='英超', round = 0):
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


def compare_game(x,y):
    if x.beginTimestamp > y.beginTimestamp:
        return 1
    elif x.beginTimestamp < y.beginTimestamp:
        return -1
    else:
        return 0

# 如果没有连接本地数据库，就不能更新，故增加了这个属性进行控制
def updateCurrentSeasonPanlu(func_write_SQL = True):
    league_dic = {"8":"德甲","9":"德乙","11":"法甲","12":"法乙",
               "16":"荷甲","17":"荷乙","23":"葡超","27":"瑞超",
                "29":"苏超","31":"西甲","33":"西乙","36":"英超",
               "37":"英冠","39":"英甲","34":"意甲","40":"意乙",
                "700":"泰超"}
    furture_game_list = []
    try:
        for key,value in league_dic.items():
            specialDic = parsePanlu(season='2023-2024', leagueid=key, leaguename=value,writeSQL=func_write_SQL)
            if specialDic is None:
                specialDic = parsePanlu(season='2023-2024', leagueid=key, leaguename=value,writeSQL=func_write_SQL)
                if specialDic is None:
                    time.sleep(3)
                    print(value,'没有specialDic')
                    continue
            time.sleep(3)
            games = getRoundGames(season='2023-2024', leagueid=key, league=value)
            if len(games) == 0:
                games = getRoundGames(season='2023-2024', leagueid=key, league=value)
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

    furture_game_list.sort(key=functools.cmp_to_key(compare_game))
    for g in furture_game_list:
        print(g)

if __name__ == '__main__':
    updateCurrentSeasonPanlu(func_write_SQL=False)
    exit(0)
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
    #
    _league_id = 700
    _sub_league_id = None
    _league_name = '泰超'
    headers = {
        'User-Agent': 'QTimesApp/3.0 (Letarrow.QTimes; build:39; iOS 17.1.0) Alamofire/5.4.',
        'cookie': 'aiappfrom=48'
    }
    timestr = str(int(time.time()))
    url = f"http://api.letarrow.com/pcf/bfmatch/api/database/v1/leaguedetail?kind=1&lang=0&sid={_league_id}&_t={timestr}"
    try:
        response = requests.get(url, headers=headers)
        if response.ok:
            content_type = response.headers.get('Content-Type')
            # print(content_type)
            if 'application/x-protobuf' == content_type:
                resultStr = response.content
                print(url, resultStr)
                temp_message, typedef = blackboxprotobuf.protobuf_to_json(resultStr)
                print(temp_message)
                leaguedic = json.loads(temp_message)
                league_id = int(leaguedic.get('1', '0'))
                if league_id != _league_id:
                    raise ValueError("联赛id异常")

                leaguename = leaguedic.get('2', '')
                seasons = leaguedic.get('4', [])
                for s in seasons:

                    # getSeasonGamelist(s, league_id, _league_name)
                    parsePanlu(season=s,leagueid=league_id,leaguename=_league_name)
                    # parseJifen(season=s,leagueid=league_id,leaguename=_league_name,subleagueid=_sub_league_id)
                    time.sleep(8)

    except Exception as e:
        print('获取联赛数据', url, e)








