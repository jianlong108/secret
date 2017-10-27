#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import os
import math

from SoccerModels import *
import sys

reload(sys)

sys.setdefaultencoding('utf8')

location = os.path.expanduser('~/Desktop/Soccer.db')

conn = sqlite3.connect(location)
c = conn.cursor()

def resultWithHandiAndPercent(handi,win,draw,lose):

    p_max = win
    if p_max < draw:
        p_max = draw

    if p_max < lose:
        p_max = lose


    if handi == 0:
        if p_max == win:
            return 3
        elif p_max == draw:
            return 1
        else:
            return 0
    elif handi < 0:
        if p_max == win or p_max == draw:
            return 0
        elif p_max == lose and p_max >= 50:
            return 3
        else:
            return 0
    else:
        if p_max == win and p_max > 50:
            return 3
        else:
            return 0


class ResultAnalyseGame(object):
    def __init__(self):
        self.soccerID = 0
        self.league = ''
        self.beginTime = ''
        self.resultOdd = -1
        self.resultHandi = -1
        self.homeTeam  = ''
        self.friendTeam = ''
        self.homeSoccer = -1
        self.friendSoccer = -1
        # 初盘混乱
        self.orignalHandiconfusion = 0
        # 澳门早开盘
        self.AomenFirst = 0
        # 盘口变化 0 不变 1 变盘
        self.handiDeeper = 0

        self.orignalHandiCompany = ''
        self.orignalHandi = 0.0
        self.orignalHandiQueryCount = 0
        self.percent_orignal_win_handi = ''
        self.percent_orignal_draw_handi = ''
        self.percent_orignal_lose_handi = ''
        self.percent_orignal_win_handi_odd = ''
        self.percent_orignal_draw_handi_odd = ''
        self.percent_orignal_lose_handi_odd = ''
        self.prediction_result_orignalHandi = -1

        self.orignalOddCompany = ''
        self.orignalOddQueryCount = 0
        self.percent_orignal_win_odd = ''
        self.percent_orignal_draw_odd = ''
        self.percent_orignal_lose_odd = ''
        self.prediction_result_orignalOdd = -1

        self.nowHandiCompany = ''
        self.nowHandi = 0.0
        self.nowHandiQueryCount = 0
        self.percent_now_win_handi = ''
        self.percent_now_draw_handi = ''
        self.percent_now_lose_handi = ''
        self.percent_now_win_handi_odd = ''
        self.percent_now_draw_handi_odd = ''
        self.percent_now_lose_handi_odd = ''
        self.prediction_result_nowHandi = -1

        self.nowOddCompany = ''
        self.nowOddQueryCount = 0
        self.percent_now_win_odd = ''
        self.percent_now_draw_odd = ''
        self.percent_now_lose_odd = ''
        self.prediction_result_nowOdd = -1

def create_result_database():
    global conn
    global c
    # 连接到SQLite数据库
    # 数据库文件是test.db
    # 如果文件不存在，会自动在当前目录创建:
    conn = sqlite3.connect(location)
    c = conn.cursor()

    sql0 = 'create table if not exists ' + 'ResultAnalyse' + \
          '(soccerID INTEGER PRIMARY KEY, league varchar(20), time VARCHAR(15), resultOdd INTEGER, resultHandi INTEGER,' \
          'confusion INTEGER, aomen INTEGER,deeper INTEGER,' \
          'homeTeam VARCHAR(20), homeSoccer INTEGER, friend VARCHAR(20), friendSoccer INTEGER,' \
          'ori_cpy_handi VARCHAR(20),ori_handi VARCHAR(10), ori_handi_count INTEGER, p_ori_win_handi VARCHAR(10),' \
          'p_ori_draw_handi VARCHAR(10), p_ori_lose_handi VARCHAR(10),' \
          'p_ori_win VARCHAR(10), p_ori_draw VARCHAR(10), p_ori_lose VARCHAR(10), reult_ori_handi INTEGER,' \
          'ori_cpy_odd VARCHAR(20), ori_odd_count INTEGER, p_ori_win_odd VARCHAR(10), p_ori_draw_odd VARCHAR(10), p_ori_lose_odd VARCHAR(10), reult_ori_odd INTEGER,' \
          'now_cpy_handi VARCHAR(20),now_handi VARCHAR(10), now_handi_count INTEGER, p_now_win_handi VARCHAR(10),' \
          'p_now_draw_handi VARCHAR(10), p_now_lose_handi VARCHAR(10),' \
          'p_now_win VARCHAR(10), p_now_draw VARCHAR(10), p_now_lose VARCHAR(10), reult_now_handi INTEGER,' \
          'now_cpy_odd VARCHAR(20), now_odd_count INTEGER, p_now_win_odd VARCHAR(10), p_now_draw_odd VARCHAR(10), p_now_lose_odd VARCHAR(10), reult_now_odd INTEGER)'

    # sql0 = 'drop table ResultAnalyse'
    c.execute(sql0)
    conn.commit()
    c.close()
    conn.close()


def create_database():
    global conn
    global c
    # 连接到SQLite数据库
    # 数据库文件是test.db
    # 如果文件不存在，会自动在当前目录创建:
    conn = sqlite3.connect(location)
    c = conn.cursor()

    # sql = 'create table if not exists ' + 'Soccer' + \
    #       '(soccer_ID INTEGER PRIMARY KEY AUTOINCREMENT,league varchar(20),soccer VARCHAR(5),gameurl VARCHAR (30),otodds VARCHAR(5) ,' \
    #       'orignalpan VARCHAR(5),ododds VARCHAR(5),ntodds VARCHAR(5) ,nowpan VARCHAR(5),ndodds VARCHAR(5))'
    # c.execute(sql)

    sql0 = 'create table if not exists ' + 'Games' + \
          '(soccer_ID INTEGER PRIMARY KEY AUTOINCREMENT,'\
            'soccerID INTEGER,league varchar(20),time VARCHAR(15),result INTEGER,' \
          'homeLevel INTEGER,home VARCHAR(20),homeSoccer INTEGER,'\
            'friendLevel INTEGER,friend VARCHAR(20) ,friendSoccer INTEGER)'

    c.execute(sql0)

    sql1 = 'create table if not exists ' + 'CompanyHandicap' + \
          '(rowid INTEGER PRIMARY KEY AUTOINCREMENT, soccerID INTEGER, gameid INTEGER,result INTEGER,homeSoccer INTEGER,friendSoccer INTEGER,company VARCHAR(10),otodds REAL ,' \
          'orignalpan REAL,ododds REAL,ntodds REAL ,nowpan REAL,ndodds REAL)'
    c.execute(sql1)

    sql2 = 'create table if not exists ' + 'CompanyODD' + \
           '(rowid INTEGER PRIMARY KEY AUTOINCREMENT, soccerID INTEGER , gameid INTEGER, result INTEGER,homeSoccer INTEGER,friendSoccer INTEGER,company VARCHAR(10),' \
           'ori_winODD REAL ,ori_drawODD REAL,ori_loseODD REAL,'\
            'winODD REAL ,drawODD REAL,loseODD REAL)'
    c.execute(sql2)

    sql3 = 'create table if not exists ' + 'League' + \
           '(league_ID INTEGER PRIMARY KEY AUTOINCREMENT,leagueID INTEGER,leagueName varchar(15),briefLeagueName varchar(15),season varchar(300))'
    c.execute(sql3)

    conn.commit()
    c.close()
    conn.close()

'''
插入一个比赛分析 数据
'''
def insert_Result_Analyse_list(resultList):
    global conn
    global c
    # conn = sqlite3.connect(location)
    c = conn.cursor()
    for reslut in resultList:
        if isinstance(reslut, ResultAnalyseGame) is True:

            params = (reslut.soccerID, reslut.league.decode('utf-8'), reslut.beginTime.decode('utf-8'),reslut.resultOdd,reslut.resultHandi,
                      reslut.orignalHandiconfusion,reslut.AomenFirst,reslut.handiDeeper,
                      reslut.homeTeam.decode('utf-8'), reslut.homeSoccer, reslut.friendTeam.decode('utf-8'), reslut.friendSoccer,
                      reslut.orignalHandiCompany.decode('utf-8'),reslut.orignalHandi,reslut.orignalHandiQueryCount,reslut.percent_orignal_win_handi.decode('utf-8'),reslut.percent_orignal_draw_handi.decode('utf-8'),reslut.percent_orignal_lose_handi.decode('utf-8'),
                      reslut.percent_orignal_win_handi_odd.decode('utf-8'),reslut.percent_orignal_draw_handi_odd.decode('utf-8'),reslut.percent_orignal_lose_handi_odd.decode('utf-8'),reslut.prediction_result_orignalHandi,
                      reslut.orignalOddCompany.decode('utf-8'), reslut.orignalOddQueryCount, reslut.percent_orignal_win_odd.decode('utf-8'), reslut.percent_orignal_draw_odd.decode('utf-8'),reslut.percent_orignal_lose_odd.decode('utf-8'), reslut.prediction_result_orignalOdd,
                      reslut.nowHandiCompany.decode('utf-8'), reslut.nowHandi, reslut.nowHandiQueryCount,reslut.percent_now_win_handi.decode('utf-8'), reslut.percent_now_draw_handi.decode('utf-8'),reslut.percent_now_lose_handi.decode('utf-8'),
                      reslut.percent_now_win_handi_odd.decode('utf-8'), reslut.percent_now_draw_handi_odd.decode('utf-8'),reslut.percent_now_lose_handi_odd.decode('utf-8'), reslut.prediction_result_nowHandi,
                      reslut.nowOddCompany.decode('utf-8'), reslut.nowOddQueryCount, reslut.percent_now_win_odd.decode('utf-8'),reslut.percent_now_draw_odd.decode('utf-8'), reslut.percent_now_lose_odd.decode('utf-8'),reslut.prediction_result_nowOdd,
                      )
            try:
                c.execute("INSERT INTO ResultAnalyse VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", params)
            except sqlite3.IntegrityError as e:
                print e
                print reslut.soccerID
        else:
            pass

    conn.commit()
    c.close()
    conn.close()

'''
插入一个联赛 数据
'''
def insert_League(league):
    global conn
    global c
    # conn = sqlite3.connect(location)
    c = conn.cursor()

    params = (league.leagueID, league.leagueName.decode('utf-8'), league.breifLeagueName.decode('utf-8'), league.aviableSeasonStr.decode('utf-8'))
    c.execute("INSERT INTO League VALUES (NULL ,?,?,?,?)", params)
    # c.execute(sql)
    conn.commit()
    c.close()
    conn.close()

'''
插入一条 比赛 数据
'''
def insert_Game(game):
    global conn
    global c
    conn = sqlite3.connect(location)
    c = conn.cursor()

    params = (game.soccerID, game.leauge, game.beginTime, game.soccer, game.homeTeamLevel, game.homeTeam,
              game.allHome, game.friendTeamLevel, game.friendTeam, game.allFriend)
    c.execute("INSERT INTO Games VALUES (NULL ,?,?,?,?,?,?,?,?,?,?)", params)
    conn.commit()
    c.close()
    conn.close()

'''
插入比赛列表
'''
def insertGameList(games):
    global conn
    global c

    conn = sqlite3.connect(location)
    c = conn.cursor()

    for game in games:
        params = (game.soccerID, game.leauge.decode('utf-8'), game.beginTime.decode('utf-8'), game.soccer, game.homeTeamLevel, game.homeTeam.decode('utf-8'),
                     game.allHome, game.friendTeamLevel, game.friendTeam.decode('utf-8'), game.allFriend)
        c.execute("INSERT INTO Games VALUES (NULL ,?,?,?,?,?,?,?,?,?,?)", params)

        handi = game.handiCompanies
        if handi is None:
            pass
        else:
            for company  in handi:
                if isinstance(company, BetCompany):
                    params1 = (
                    game.soccerID, company.soccerGameId, company.result, company.homeSoccer, company.friendSoccer,
                    company.companyTitle.decode('utf-8'),
                    company.orignal_top, company.orignal_Handicap, company.orignal_bottom, company.now_top, company.now_Handicap,
                    company.now_bottom)

                    c.execute("INSERT INTO CompanyHandicap VALUES (NULL ,? ,?,?,?,?,?,?,?,?,?,?,?)", params1)




        odd  = game.oddCompanies
        if odd == None:
            pass
        else:
            for company in odd:
                params = (game.soccerID, company.soccerGameId, company.result, company.homeSoccer, company.friendSoccer,
                          company.companyTitle.decode('utf-8'),
                          company.orignal_winOdd, company.orignal_drawOdd,
                          company.orignal_loseOdd, company.winOdd, company.drawOdd, company.loseOdd)
                c.execute("INSERT INTO CompanyODD VALUES (NULL ,?,?,?,?,?,?,?,?,?,?,?,?)", params)


    conn.commit()
    c.close()
    conn.close()

'''
插入多条亚赔数据
'''
def insertGameHandiList(games):
    global conn
    global c

    conn = sqlite3.connect(location)
    c = conn.cursor()

    for company in games:
        if isinstance(company, BetCompany):
            params = (
            company.soccerGameId, company.result, company.homeSoccer, company.friendSoccer, company.companyTitle,
            company.orignal_top, company.orignal_Handicap, company.orignal_bottom, company.now_top, company.now_Handicap,
            company.now_bottom)

            c.execute("INSERT INTO CompanyHandicap VALUES (NULL ,?,?,?,?,?,?,?,?,?,?,?)", params)



    conn.commit()
    c.close()
    conn.close()

'''
插入多条欧赔数据
'''
def insertGameODDList(games):
    global conn
    global c

    conn = sqlite3.connect(location)
    c = conn.cursor()

    for company in games:
        params = (company.soccerGameId, company.result, company.homeSoccer, company.friendSoccer,company.companyTitle, company.orignal_winOdd, company.orignal_drawOdd,
         company.orignal_loseOdd, company.winOdd, company.drawOdd, company.loseOdd)
        c.execute("INSERT INTO CompanyODD VALUES (NULL ,?,?,?,?,?,?,?,?,?,?,?)", params)

    conn.commit()
    c.close()
    conn.close()



'''
插入单条亚盘数据
'''
def insert_Handi(company):
    global conn
    global c

    conn = sqlite3.connect(location)
    c = conn.cursor()
    if isinstance(company, BetCompany):
        params = (company.soccerGameId, company.result, company.homeSoccer, company.friendSoccer, company.companyTitle,
                  company.orignal_top, company.orignal_Handicap, company.orignal_bottom, company.now_top, company.now_Handicap,
                  company.now_bottom)
        c.execute("INSERT INTO CompanyHandicap VALUES (NULL ,?,?,?,?,?,?,?,?,?,?,?)", params)

    # c.execute(sql)
    conn.commit()
    c.close()
    conn.close()

'''
插入单条欧赔数据
'''
def insert_ODD(company):
    global conn
    global c

    conn = sqlite3.connect(location)
    c = conn.cursor()

    params = (company.soccerGameId, company.result, company.homeSoccer, company.friendSoccer, company.companyTitle,
              company.orignal_winOdd, company.orignal_drawOdd,
              company.orignal_loseOdd, company.winOdd, company.drawOdd, company.loseOdd)
    c.execute("INSERT INTO CompanyODD VALUES (NULL ,?,?,?,?,?,?,?,?,?,?,?)", params)
    # c.execute(sql)
    conn.commit()
    c.close()
    conn.close()

'''
获取初始欧赔的概率
'''
def getOrignalODDProbability(game, isYesterday = False, resultGame = None):
    contentstr = ''
    resultTuple = None
    if isinstance(game, FootballGame):

        if game.oddCompanies is None:
            if isYesterday:
                return resultTuple
            else:
                return contentstr
        global conn
        global c

        conn = sqlite3.connect(location)
        c = conn.cursor()

        # 将比赛开始时间 对阵双方信息 录入
        titlestr = ''.join(
            [str(game.beginTime), ':', game.leauge, ':', game.homeTeam, 'vs', game.friendTeam, ' id: ',
             str(game.soccerID)])
        # contentstr += titlestr
        print titlestr

        # 总场次
        totalcount = 0

        # 欧赔 胜场数
        win_count = 0
        unit_win_count = 0
        # 欧赔 平场数
        draw_count = 0
        unit_draw_count = 0

        # 欧赔 输场数
        lose_count = 0
        unit_lose_count = 0

        maxIndex = 0
        resultSet = []

        for oneCompany in game.oddCompanies:
            if isinstance(oneCompany ,BetCompany):
                c.execute("SELECT * FROM Games WHERE soccerID IN "
                          "(select soccerID from CompanyODD where company == ? and ori_winODD == ? "
                          "and ori_drawODD == ? and ori_loseODD >= ? ) AND league == ?",
                          (oneCompany.companyTitle.decode('utf-8'), oneCompany.orignal_winOdd, oneCompany.orignal_drawOdd,
                           oneCompany.orignal_loseOdd, game.leauge.decode('utf-8')))
                r = c.fetchall()
                totalcount += len(r)
                unit_totalcount = len(r)
                for result in r:
                    if result[4] == 3:
                        win_count += 1
                        unit_win_count += 1
                    elif result[4] == 1:
                        draw_count += 1
                        unit_draw_count += 1
                    else:
                        lose_count += 1
                        unit_lose_count += 1


                if unit_totalcount > 0:

                    unitTuple = (
                    unit_totalcount, oneCompany.companyTitle, str(oneCompany.orignal_winOdd), str(oneCompany.orignal_drawOdd),
                    str(oneCompany.orignal_drawOdd),
                    str(float(unit_win_count) / float(unit_totalcount) * 100)[:5],
                    str(float(unit_draw_count) / float(unit_totalcount) * 100)[:5],
                    str(float(unit_lose_count) / float(unit_totalcount) * 100)[:5])

                    resultSet.append(unitTuple)


                unit_win_count = 0
                unit_draw_count = 0
                unit_lose_count = 0

        if len(resultSet) > 0:
            maxCount = (resultSet[0])[0]
            for oneTuple in resultSet:
                if maxCount < oneTuple[0]:
                    maxCount = oneTuple[0]
                    maxIndex = resultSet.index(oneTuple)
            resultTuple = resultSet[maxIndex]
            # 对比赛模型数据进行赋值
            if resultGame is not None and isinstance(resultGame, ResultAnalyseGame):
                resultGame.orignalOddQueryCount = maxCount
                resultGame.orignalOddCompany = resultTuple[1]
                resultGame.percent_orignal_win_odd = resultTuple[5]
                resultGame.percent_orignal_draw_odd = resultTuple[6]
                resultGame.percent_orignal_lose_odd = resultTuple[7]
                resultGame.prediction_result_orignalOdd = resultWithHandiAndPercent(resultGame.orignalHandi, float(
                    resultGame.percent_orignal_win_odd), float(resultGame.percent_orignal_draw_odd), float(
                    resultGame.percent_orignal_lose_odd))

                # 赋值结束
            for oneTuple in resultSet:
                index = resultSet.index(oneTuple)
                if maxIndex == index:
                    bgcolor = 'red'
                    textColor = 'white'
                else:
                    bgcolor = 'white'
                    textColor = 'black'

                tempResultStr = "<tr bgcolor=\"%s\" style=\"color:%s\"><td>%s</td> <td>%s</td><td>%s</td><td>%s</td>" \
                                "<td>%s</td><td>%s</td><td>%s</td><td>%s</td>" % (bgcolor, textColor, oneTuple[1],
                                                                                  str(oneTuple[0]),
                                                                                  oneTuple[2],
                                                                                  oneTuple[3],
                                                                                  oneTuple[4],
                                                                                  oneTuple[5],
                                                                                  oneTuple[6],
                                                                                  oneTuple[7])

                contentstr += tempResultStr

        if totalcount == 0:
            if isYesterday:
                return resultTuple
            else:
                return contentstr

        odd_winPercent = float(win_count) / float(totalcount) * 100
        odd_drawPercent = float(draw_count) / float(totalcount) * 100
        odd_losePercent = float(lose_count) / float(totalcount) * 100
        contentstr += "<tr bgcolor=\"white\"><td>%s</td> <td>%s</td><td>%s</td><td>%s</td>" \
                      "<td>%s</td><td>%s</td><td>%s</td><td>%s</td>" % ('总数',
                                                                        str(totalcount),
                                                                        '',
                                                                        '',
                                                                        '',

                                                                        str(odd_winPercent)[:5],
                                                                        str(odd_drawPercent)[:5],
                                                                        str(odd_losePercent)[:5])

    else:
        pass
    if isYesterday:
        return resultTuple
    else:
        return contentstr

'''
获取即时欧赔的概率
'''
def getnowODDProbability(game, isYesterday = False, resultGame = None):
    if isinstance(game, FootballGame):
        contentstr = ''
        resultTuple = (0, 0, 0)
        if game.oddCompanies is None:
            if isYesterday:
                return resultTuple
            else:
                return contentstr
        global conn
        global c

        conn = sqlite3.connect(location)
        c = conn.cursor()

        # 将比赛开始时间 对阵双方信息 录入
        titlestr = ''.join(
            [str(game.beginTime), ':', game.leauge, ':', game.homeTeam, 'vs', game.friendTeam, ' id: ',
             str(game.soccerID)])
        # contentstr += titlestr
        print titlestr

        # 总场次
        totalcount = 0

        # 欧赔 胜场数
        win_count = 0
        unit_win_count = 0
        # 欧赔 平场数
        draw_count = 0
        unit_draw_count = 0

        # 欧赔 输场数
        lose_count = 0
        unit_lose_count = 0

        maxIndex = 0
        resultSet = []

        for oneCompany in game.oddCompanies:
            if isinstance(oneCompany ,BetCompany):
                c.execute("SELECT * FROM Games WHERE soccerID IN "
                          "(select soccerID from CompanyODD where company == ? and winODD == ? "
                          "and drawODD == ? and loseODD >= ? ) AND league == ?",
                          (oneCompany.companyTitle.decode('utf-8'), oneCompany.winOdd, oneCompany.drawOdd,
                           oneCompany.loseOdd, game.leauge.decode('utf-8')))
                r = c.fetchall()
                totalcount += len(r)
                unit_totalcount = len(r)
                for result in r:
                    if result[4] == 3:
                        win_count += 1
                        unit_win_count += 1
                    elif result[4] == 1:
                        draw_count += 1
                        unit_draw_count += 1
                    else:
                        lose_count += 1
                        unit_lose_count += 1


                if unit_totalcount > 0:

                    # contentstr += "<tr bgcolor=\"white\" ><td>%s</td> <td>%s</td><td>%s</td><td>%s</td>" \
                    #               "<td>%s</td><td>%s</td><td>%s</td><td>%s</td>" % (oneCompany.companyTitle,
                    #                                                                 str(unit_totalcount),
                    #                                                                 str(oneCompany.winOdd),
                    #                                                                 str(oneCompany.drawOdd),
                    #                                                                 str(oneCompany.loseOdd),
                    #
                    #                                                                 str(float(unit_win_count) / float(
                    #                                                                     unit_totalcount) * 100)[:5],
                    #                                                                 str(float(unit_draw_count) / float(
                    #                                                                     unit_totalcount) * 100)[:5],
                    #                                                                 str(float(unit_lose_count) / float(
                    #                                                                     unit_totalcount) * 100)[:5])
                    unitTuple = (unit_totalcount, oneCompany.companyTitle, str(oneCompany.winOdd),str(oneCompany.drawOdd),str(oneCompany.loseOdd),
                                 str(float(unit_win_count) / float(unit_totalcount) * 100)[:5],
                                 str(float(unit_draw_count) / float(unit_totalcount) * 100)[:5],
                                 str(float(unit_lose_count) / float(unit_totalcount) * 100)[:5])
                    resultSet.append(unitTuple)

                unit_win_count = 0
                unit_draw_count = 0
                unit_lose_count = 0
        if len(resultSet) > 0:
            maxCount = (resultSet[0])[0]
            for oneTuple in resultSet:
                if maxCount < oneTuple[0]:
                    maxCount = oneTuple[0]
                    maxIndex = resultSet.index(oneTuple)
            resultTuple = resultSet[maxIndex]
            # 对比赛模型数据进行赋值
            if resultGame is not None and isinstance(resultGame, ResultAnalyseGame):
                resultGame.nowOddQueryCount = maxCount
                resultGame.nowOddCompany = resultTuple[1]
                resultGame.percent_now_win_odd = resultTuple[5]
                resultGame.percent_now_draw_odd = resultTuple[6]
                resultGame.percent_now_lose_odd = resultTuple[7]
                resultGame.prediction_result_nowOdd = resultWithHandiAndPercent(resultGame.nowHandi, float(
                    resultGame.percent_now_win_odd), float(resultGame.percent_now_draw_odd), float(
                    resultGame.percent_now_lose_odd))

            # 赋值结束
            for oneTuple in resultSet:
                index = resultSet.index(oneTuple)
                if maxIndex == index:
                    bgcolor = 'red'
                    textColor = 'white'
                else:
                    bgcolor = 'white'
                    textColor = 'black'

                tempResultStr = "<tr bgcolor=\"%s\" style=\"color:%s\"><td>%s</td> <td>%s</td><td>%s</td><td>%s</td>" \
                                "<td>%s</td><td>%s</td><td>%s</td><td>%s</td>" % (bgcolor, textColor, oneTuple[1],
                                                                                  str(oneTuple[0]),
                                                                                  oneTuple[2],
                                                                                  oneTuple[3],
                                                                                  oneTuple[4],
                                                                                  oneTuple[5],
                                                                                  oneTuple[6],
                                                                                  oneTuple[7])

                contentstr += tempResultStr

        if totalcount == 0:
            if isYesterday:
                return resultTuple
            else:
                return contentstr

        odd_winPercent = float(win_count) / float(totalcount) * 100
        odd_drawPercent = float(draw_count) / float(totalcount) * 100
        odd_losePercent = float(lose_count) / float(totalcount) * 100
        contentstr += "<tr bgcolor=\"white\" ><td>%s</td> <td>%s</td><td>%s</td><td>%s</td>" \
                      "<td>%s</td><td>%s</td><td>%s</td><td>%s</td>" % ('总数',
                                                                        str(totalcount),
                                                                        '',
                                                                        '',
                                                                        '',

                                                                        str(odd_winPercent)[:5],
                                                                        str(odd_drawPercent)[:5],
                                                                        str(odd_losePercent)[:5])

    else:
        pass
    if isYesterday:
        return resultTuple
    else:
        return contentstr

'''
获取初盘的概率
'''
def getHandiProbability(game, isYesterday = False, resultGame = None):
    if isinstance(game, FootballGame):
        contentstr = ''
        resultTuple = (0,0,0)
        if game.handiCompanies is None:
            if isYesterday:
                return resultTuple
            else:
                return contentstr

        global conn
        global c

        conn = sqlite3.connect(location)
        c = conn.cursor()

        # 将比赛开始时间 对阵双方信息 录入
        titlestr = ''.join(
            [str(game.beginTime), ':', game.leauge, ':', game.homeTeam, 'vs', game.friendTeam, ' id: ',
             str(game.soccerID), '澳盘: ',str(game.orignal_aomenHandi), ' -> ',str(game.now_aomenHandi)])
        # contentstr += titlestr
        print titlestr

        # 总场次
        totalcount = 0

        # 亚盘 胜场数
        handi_win_count = 0
        win_count = 0
        unit_handi_win_count= 0
        unit_win_count = 0
        # 亚盘 平场数
        handi_draw_count = 0
        draw_count = 0
        unit_handi_draw_count= 0
        unit_draw_count = 0

        # 亚盘 输场数
        handi_lose_count = 0
        lose_count = 0
        unit_handi_lose_count= 0
        unit_lose_count = 0
        maxIndex = 0
        resultSet = []
        for oneCompany in game.handiCompanies:
            if isinstance(oneCompany ,BetCompany):
                c.execute("SELECT * FROM Games WHERE soccerID IN "
                          "(select soccerID from CompanyHandicap where company == ? and orignalpan == ? "
                          "and otodds == ? and ododds >= ? ) AND league == ?",
                          (oneCompany.companyTitle.decode('utf-8'), oneCompany.orignal_Handicap, oneCompany.orignal_top,
                           oneCompany.orignal_bottom, game.leauge.decode('utf-8')))
                r = c.fetchall()
                totalcount += len(r)
                unit_totalcount = len(r)
                for result in r:
                    if result[4] == 3:
                        win_count += 1
                        unit_win_count += 1
                    elif result[4] == 1:
                        draw_count += 1
                        unit_draw_count += 1
                    else:
                        lose_count += 1
                        unit_lose_count += 1

                    offset = int(result[7]) - int(result[10]) - float(oneCompany.orignal_Handicap)
                    if offset > 0.0:
                        handi_win_count += 1
                        unit_handi_win_count += 1
                    elif offset == 0.0:
                        handi_draw_count += 1
                        unit_handi_draw_count += 1
                    else:
                        handi_lose_count += 1
                        unit_handi_lose_count += 1

                if unit_totalcount > 0:

                    # tempResultStr = "<tr bgcolor=\"white\" ><td>%s</td><td>%s</td> <td>%s</td><td>%s</td><td>%s</td>" \
                    #               "<td>%s</td><td>%s</td><td>%s</td><td>%s</td>" % (oneCompany.companyTitle,
                    #                                                                 oneCompany.orignal_Handicap,
                    #                                                                 str(unit_totalcount),
                    #                                                                 str(float(unit_handi_win_count) / float(unit_totalcount) * 100)[:5],
                    #                                                                 str(float(unit_handi_draw_count) / float(unit_totalcount) * 100)[:5],
                    #                                                                 str(float(unit_handi_lose_count) / float(unit_totalcount) * 100)[:5],
                    #                                                                 str(float(unit_win_count) / float(unit_totalcount) * 100)[:5],
                    #                                                                 str(float(unit_draw_count) / float(unit_totalcount) * 100)[:5],
                    #                                                                 str(float(unit_lose_count) / float(unit_totalcount) * 100)[:5])
                    # contentstr += tempResultStr
                    unitTuple = (unit_totalcount,oneCompany.companyTitle,oneCompany.orignal_Handicap,
                                 str(float(unit_handi_win_count) / float(unit_totalcount) * 100)[:5],
                                 str(float(unit_handi_draw_count) / float(unit_totalcount) * 100)[:5],
                                 str(float(unit_handi_lose_count) / float(unit_totalcount) * 100)[:5],
                                 str(float(unit_win_count) / float(unit_totalcount) * 100)[:5],
                                 str(float(unit_draw_count) / float(unit_totalcount) * 100)[:5],
                                 str(float(unit_lose_count) / float(unit_totalcount) * 100)[:5])
                    resultSet.append(unitTuple)

                unit_handi_win_count = 0
                unit_win_count = 0
                unit_handi_draw_count = 0
                unit_draw_count = 0
                unit_handi_lose_count = 0
                unit_lose_count = 0

        if len(resultSet) > 0:
            maxCount = (resultSet[0])[0]
            for oneTuple in resultSet:
                if maxCount < oneTuple[0]:
                    maxCount = oneTuple[0]
                    maxIndex = resultSet.index(oneTuple)
            resultTuple = resultSet[maxIndex]
            # 对比赛模型数据进行赋值
            if resultGame is not None and isinstance(resultGame, ResultAnalyseGame):
                resultGame.orignalHandiQueryCount = maxCount
                resultGame.orignalHandiCompany = resultTuple[1]
                resultGame.orignalHandi = resultTuple[2]
                resultGame.percent_orignal_win_handi = resultTuple[3]
                resultGame.percent_orignal_draw_handi = resultTuple[4]
                resultGame.percent_orignal_lose_handi = resultTuple[5]
                resultGame.percent_orignal_win_handi_odd = resultTuple[6]
                resultGame.percent_orignal_draw_handi_odd = resultTuple[7]
                resultGame.percent_orignal_lose_handi_odd = resultTuple[8]
                resultGame.prediction_result_orignalHandi = resultWithHandiAndPercent(resultGame.orignalHandi, float(resultGame.percent_orignal_win_handi_odd), float(resultGame.percent_orignal_draw_handi_odd), float(resultGame.percent_orignal_lose_handi_odd))

            # 赋值结束
            for oneTuple in resultSet:
                index = resultSet.index(oneTuple)
                if maxIndex == index:
                    bgcolor = 'red'
                    textColor = 'white'
                else:
                    bgcolor = 'white'
                    textColor = 'black'
                tempResultStr = "<tr bgcolor=\"%s\" style=\"color:%s\"><td>%s</td><td>%s</td> <td>%s</td><td>%s</td><td>%s</td>" \
                                "<td>%s</td><td>%s</td><td>%s</td><td>%s</td>" % (bgcolor, textColor, oneTuple[1],
                                                                                  oneTuple[2],
                                                                                  str(oneTuple[0]),
                                                                                  oneTuple[3],
                                                                                  oneTuple[4],
                                                                                  oneTuple[5],
                                                                                  oneTuple[6],
                                                                                  oneTuple[7],
                                                                                  oneTuple[8])
                contentstr += tempResultStr

        if totalcount == 0:
            if isYesterday:
                return resultTuple
            else:
                return contentstr


        handi_winPercent = float(handi_win_count) / float(totalcount) * 100
        handi_drawPercent = float(handi_draw_count) / float(totalcount) * 100
        handi_losePercent = float(handi_lose_count) / float(totalcount) * 100
        odd_winPercent = float(win_count) / float(totalcount) * 100
        odd_drawPercent = float(draw_count) / float(totalcount) * 100
        odd_losePercent = float(lose_count) / float(totalcount) * 100
        contentstr += "<tr bgcolor = \"white\"><td>%s</td><td>%s</td> <td>%s</td><td>%s</td><td>%s</td>" \
                      "<td>%s</td><td>%s</td><td>%s</td><td>%s</td>" % ('总数',
                                                                        '',
                                                                        str(totalcount),
                                                                        str(handi_winPercent)[:5],
                                                                        str(handi_drawPercent)[:5],
                                                                        str(handi_losePercent)[:5],
                                                                        str(odd_winPercent)[:5],
                                                                        str(odd_drawPercent)[:5],
                                                                        str(odd_losePercent)[:5])

    else:
        pass

    if isYesterday:
        return resultTuple
    else:
        return contentstr

'''
获取即时盘口的概率
'''
def getnowHandiProbability(game, isYesterday = False, resultGame = None):
    contentstr = ''
    resultTuple = (0, 0, 0)
    if isinstance(game, FootballGame):
        if game.handiCompanies is None:
            if isYesterday:
                return resultTuple
            else:
                return contentstr
        global conn
        global c

        conn = sqlite3.connect(location)
        c = conn.cursor()

        # 总场次
        totalcount = 0

        # 亚盘 胜场数
        handi_win_count = 0
        win_count = 0
        unit_handi_win_count= 0
        unit_win_count = 0
        # 亚盘 平场数
        handi_draw_count = 0
        draw_count = 0
        unit_handi_draw_count= 0
        unit_draw_count = 0

        # 亚盘 输场数
        handi_lose_count = 0
        lose_count = 0
        unit_handi_lose_count= 0
        unit_lose_count = 0

        maxIndex = 0
        resultSet = []
        for oneCompany in game.handiCompanies:
            if isinstance(oneCompany ,BetCompany):
                c.execute("SELECT * FROM Games WHERE soccerID IN "
                          "(select soccerID from CompanyHandicap where company == ? and nowpan == ? "
                          "and ntodds == ? and ndodds >= ? ) AND league == ?",
                          (oneCompany.companyTitle.decode('utf-8'), oneCompany.now_Handicap, oneCompany.now_top,
                           oneCompany.now_bottom, game.leauge.decode('utf-8')))
                r = c.fetchall()
                totalcount += len(r)
                unit_totalcount = len(r)
                for result in r:
                    if result[4] == 3:
                        win_count += 1
                        unit_win_count += 1
                    elif result[4] == 1:
                        draw_count += 1
                        unit_draw_count += 1
                    else:
                        lose_count += 1
                        unit_lose_count += 1

                    offset = int(result[7]) - int(result[10]) - float(oneCompany.now_Handicap)
                    if offset > 0.0:
                        handi_win_count += 1
                        unit_handi_win_count += 1
                    elif offset == 0.0:
                        handi_draw_count += 1
                        unit_handi_draw_count += 1
                    else:
                        handi_lose_count += 1
                        unit_handi_lose_count += 1

                if unit_totalcount > 0:
                    # contentstr += "<tr bgcolor=\"white\" ><td>%s</td><td>%s</td> <td>%s</td><td>%s</td><td>%s</td>" \
                    #               "<td>%s</td><td>%s</td><td>%s</td><td>%s</td>" % (oneCompany.companyTitle,
                    #                                                                 oneCompany.now_Handicap,
                    #                                                                 str(unit_totalcount),
                    #                                                                 str(float(
                    #                                                                     unit_handi_win_count) / float(
                    #                                                                     unit_totalcount) * 100)[:5],
                    #                                                                 str(float(
                    #                                                                     unit_handi_draw_count) / float(
                    #                                                                     unit_totalcount) * 100)[:5],
                    #                                                                 str(float(
                    #                                                                     unit_handi_lose_count) / float(
                    #                                                                     unit_totalcount) * 100)[:5],
                    #                                                                 str(float(unit_win_count) / float(
                    #                                                                     unit_totalcount) * 100)[:5],
                    #                                                                 str(float(unit_draw_count) / float(
                    #                                                                     unit_totalcount) * 100)[:5],
                    #                                                                 str(float(unit_lose_count) / float(
                    #                                                                     unit_totalcount) * 100)[:5])
                    unitTuple = (unit_totalcount, oneCompany.companyTitle, oneCompany.now_Handicap,
                                 str(float(unit_handi_win_count) / float(unit_totalcount) * 100)[:5],
                                 str(float(unit_handi_draw_count) / float(unit_totalcount) * 100)[:5],
                                 str(float(unit_handi_lose_count) / float(unit_totalcount) * 100)[:5],
                                 str(float(unit_win_count) / float(unit_totalcount) * 100)[:5],
                                 str(float(unit_draw_count) / float(unit_totalcount) * 100)[:5],
                                 str(float(unit_lose_count) / float(unit_totalcount) * 100)[:5])
                    resultSet.append(unitTuple)

                unit_handi_win_count = 0
                unit_win_count = 0
                unit_handi_draw_count = 0
                unit_draw_count = 0
                unit_handi_lose_count = 0
                unit_lose_count = 0

        if len(resultSet) > 0:
            maxCount = (resultSet[0])[0]
            for oneTuple in resultSet:
                if maxCount < oneTuple[0]:
                    maxCount = oneTuple[0]
                    maxIndex = resultSet.index(oneTuple)
            resultTuple = resultSet[maxIndex]
            # 对比赛模型数据进行赋值
            if resultGame is not None and isinstance(resultGame, ResultAnalyseGame):
                resultGame.nowHandiQueryCount = maxCount
                resultGame.nowHandiCompany = resultTuple[1]
                resultGame.nowHandi = resultTuple[2]
                resultGame.percent_now_win_handi = resultTuple[3]
                resultGame.percent_now_draw_handi = resultTuple[4]
                resultGame.percent_now_lose_handi = resultTuple[5]
                resultGame.percent_now_win_handi_odd = resultTuple[6]
                resultGame.percent_now_draw_handi_odd = resultTuple[7]
                resultGame.percent_now_lose_handi_odd = resultTuple[8]
                resultGame.prediction_result_nowHandi = resultWithHandiAndPercent(resultGame.nowHandi, float(
                    resultGame.percent_now_win_handi_odd), float(resultGame.percent_now_draw_handi_odd), float(
                    resultGame.percent_now_lose_handi_odd))

                # 赋值结束
            for oneTuple in resultSet:
                index = resultSet.index(oneTuple)
                if maxIndex == index:
                    bgcolor = 'red'
                    textColor = 'white'
                else:
                    bgcolor = 'white'
                    textColor = 'black'
                tempResultStr = "<tr bgcolor=\"%s\" style=\"color:%s\"><td>%s</td><td>%s</td> <td>%s</td><td>%s</td><td>%s</td>" \
                                "<td>%s</td><td>%s</td><td>%s</td><td>%s</td>" % (bgcolor, textColor, oneTuple[1],
                                                                                  oneTuple[2],
                                                                                  str(oneTuple[0]),
                                                                                  oneTuple[3],
                                                                                  oneTuple[4],
                                                                                  oneTuple[5],
                                                                                  oneTuple[6],
                                                                                  oneTuple[7],
                                                                                  oneTuple[8])
                contentstr += tempResultStr

        if totalcount == 0:
            if isYesterday:
                return resultTuple
            else:
                return contentstr


        handi_winPercent = float(handi_win_count) / float(totalcount) * 100
        handi_drawPercent = float(handi_draw_count) / float(totalcount) * 100
        handi_losePercent = float(handi_lose_count) / float(totalcount) * 100
        contentstr += "<tr bgcolor=\"white\"><td>%s</td><td>%s</td> <td>%s</td><td>%s</td><td>%s</td>" \
                      "<td>%s</td><td>%s</td><td>%s</td><td>%s</td>" % ('终盘概率',
                                                                        '总数',
                                                                        str(totalcount),
                                                                        str(handi_winPercent)[:5],
                                                                        str(handi_drawPercent)[:5],
                                                                        str(handi_losePercent)[:5],
                                                                        str(float(win_count) / float(totalcount) * 100)[
                                                                        :5],
                                                                        str(float(draw_count) / float(
                                                                            totalcount) * 100)[:5],
                                                                        str(float(lose_count) / float(
                                                                            totalcount) * 100)[:5])

    else:
        pass
    if isYesterday:
        return resultTuple
    else:
        return contentstr

'''
分析一场比赛的数据
'''
def getGameData(game):

    contentstr = ''

    global conn
    global c

    conn = sqlite3.connect(location)
    c = conn.cursor()

    # 将比赛开始时间 对阵双方信息 录入
    contentstr = contentstr.join([str(game.beginTime), ':', game.leauge, ':', game.homeTeam, 'vs', game.friendTeam, ' id: ', str(game.soccerID)])
    contentstr += '\n'
    print str(game.beginTime) + ':' + game.leauge + ':' + game.homeTeam + 'vs' + game.friendTeam  +'  '+str(game.allHome)+ ' : ' + str(game.allFriend) + ' ' + str(game.soccerID)

    # 获取亚盘数据
    handituple = getHandi(game ,c)
    contentstr += handituple[0]
    contentstr += '\n'
    oddtuple = getOdd(game ,c)
    contentstr += oddtuple[0]
    contentstr += '\n'

    c.close()
    conn.close()
    return contentstr


def getHandi(game, c):
    contentstr = ''
    allHandiGames = []

    # 如果这场比赛没有亚盘数据,就返回
    if game.handiCompanies is None:
        return (contentstr, allHandiGames)


    # 查询到的总数
    num = 0

    # 亚盘 胜场数
    handi_win_count = 0
    win_count = 0

    # 亚盘 平场数
    handi_draw_count = 0
    draw_count = 0

    # 亚盘 输场数
    handi_lose_count = 0
    lose_count = 0

    for oneCompany in game.handiCompanies:
        if isinstance(oneCompany, BetCompany):
            c.execute("SELECT * FROM Games WHERE soccerID IN "
                      "(select soccerID from CompanyHandicap where company == ? and orignalpan == ? "
                      "and nowpan == ? and ntodds >= ? and ntodds < ? and ndodds >= ? and ndodds < ? AND otodds >= ? "
                      "AND otodds < ? AND ododds >= ? AND ododds < ?) AND league == ?",
                      (oneCompany.companyTitle.decode('utf-8'), oneCompany.orignal_Handicap, oneCompany.now_Handicap,
                       switchData(oneCompany.now_bottom)[0],
                       switchData(oneCompany.now_bottom)[1], switchData(oneCompany.now_top)[0],
                       switchData(oneCompany.now_top)[1], switchData(oneCompany.orignal_top)[0],
                       switchData(oneCompany.orignal_top)[1], switchData(oneCompany.orignal_bottom)[0],
                       switchData(oneCompany.orignal_bottom)[1], game.leauge.decode('utf-8')))
            r = c.fetchall()
            num += len(r)
            for result in r:
                allHandiGames.append(result)
                if result[4] == 3:
                    win_count += 1
                elif result[4] == 1:
                    draw_count += 1
                else:
                    lose_count += 1

                if int(result[7]) - int(result[10]) - float(oneCompany.now_Handicap) > 0.0:
                    handi_win_count += 1
                elif int(result[7]) - int(result[10]) - float(oneCompany.now_Handicap) == 0.0:
                    handi_draw_count += 1
                else:
                    handi_lose_count += 1




    if num > 0:

        tempstr_one = ''.join(['  亚 ->',str(game.winhandi),'总数: ',str(num),'  盘口:',str(game.bet365Handi), '赢盘: ', str(float(handi_win_count) / float(num) * 100)[:5], '/100', ' 走盘:',
                               str(float(handi_draw_count) / float(num) * 100)[:5], '/100', '输盘',
                               str(float(handi_lose_count) / float(num) * 100)[:5], '/100  '])
        tempstr_two = ''.join(['  亚: ', str(game.soccer),'胜: ', str(float(win_count) / float(num) * 100)[:5], '/100', ' 平:',
                               str(float(draw_count) / float(num) * 100)[:5], '/100', '负',
                               str(float(lose_count) / float(num) * 100)[:5], '/100'])

        if float(handi_win_count) / float(num) > 0.55 or float(handi_draw_count) / float(num) > 0.55 or float(handi_lose_count) / float(num) > 0.55:
            contentstr += tempstr_one
            contentstr += '\n'
            contentstr += tempstr_two

            # 终端的字符颜色是用转义序列控制的，是文本模式下的系统显示功能，和具体的语言无 关。
            # 转义序列是以 ESC 开头,可以用 \033 完成相同的工作（ESC 的 ASCII 码用十进制表 示就是 27， = 用八进制表示的 33）
            print "\033[1;31;40m%s\033[0m" % tempstr_one
            print "\033[1;31;40m%s\033[0m" % tempstr_two
        else:
            print '忽略' + tempstr_one

            print '忽略' + tempstr_two
            # 当概率小于55%.就不通过邮件发送
            # contentstr += ('忽略' + tempstr_one)
            # contentstr += '\n'
            # contentstr += ('忽略' + tempstr_two)
    else:
        print '无亚盘数据'
        contentstr = contentstr + '无亚盘数据'

    return (contentstr, )

def getOdd(game, c):
    contentstr = ''
    # 欧赔
    wincount = 0
    drawcount = 0
    losecount = 0
    num = 0
    allOddGames = []
    if len(game.oddCompanies) <= 0:
        return (contentstr, allOddGames)


    for oneOdd in game.oddCompanies:
        c.execute(
            "SELECT * FROM Games WHERE soccerID IN "
            "(select soccerID from CompanyODD where company == ? and ori_winODD >= ? and ori_winODD <= ? "
            "and ori_drawODD >= ? and ori_drawODD <= ? and ori_loseODD >= ? and ori_loseODD <= ? "
            "and winODD >= ? and winODD <= ? AND drawODD >= ? and drawODD <= ? AND loseODD >= ? "
            "and loseODD <= ?) AND league == ?",
            (oneOdd.companyTitle.decode('utf-8'), switchODDData(oneOdd.orignal_winOdd)[0],
             switchODDData(oneOdd.orignal_winOdd)[1], switchODDData(oneOdd.orignal_drawOdd)[0],
             switchODDData(oneOdd.orignal_drawOdd)[1], switchODDData(oneOdd.orignal_loseOdd)[0],
             switchODDData(oneOdd.orignal_loseOdd)[1], switchODDData(oneOdd.winOdd)[0], switchODDData(oneOdd.winOdd)[1],
             switchODDData(oneOdd.drawOdd)[0], switchODDData(oneOdd.drawOdd)[1], switchODDData(oneOdd.loseOdd)[0],
             switchODDData(oneOdd.loseOdd)[1],game.leauge.decode('utf-8'))
        )
        r = c.fetchall()
        num += len(r)
        for result in r:
            allOddGames.append(result)
            if result[4] == 3:
                wincount += 1
            elif result[4] == 1:
                drawcount += 1
            else:
                losecount += 1

    if num > 0:
        tempstr = ''.join(['  欧: ', '总数: ',str(num), '胜: ', str(float(wincount) / float(num) * 100)[:5], '/100', ' 平:',
                           str(float(drawcount) / float(num) * 100)[:5], '/100', '负',
                           str(float(losecount) / float(num) * 100)[:5], '/100'])

        if float(wincount) / float(num) > 0.55 or float(drawcount) / float(num) > 0.55 or float(losecount) / float(
                num) > 0.55:

            contentstr = contentstr + tempstr

            print "\033[1;31;40m%s\033[0m" % tempstr
            print '\n'
        else:
            print '忽略' + tempstr
            # contentstr = contentstr + '忽略' + tempstr
    else:
        print '无欧赔数据'
        contentstr = contentstr + '无欧赔数据'

    return (contentstr, )



def switchData(num):
    if num<0.5:
        return (0, 0)
    elif num >= 0.5 and num < 0.6:
        return (0.5, 0.6)
    elif num >= 0.6 and num < 0.7:
        return (0.6, 0.7)
    elif num >= 0.7 and num < 0.8:
        return (0.7, 0.8)
    elif num >= 0.8 and num < 0.9:
        return (0.8, 0.9)
    elif num >= 0.9 and num < 1.0:
        return (0.9, 1.0)
    elif num >= 1.0 and num < 1.1:
        return (1.0, 1.1)
    elif num >= 1.1 and num < 1.2:
        return (1.1, 1.2)
    elif num >= 1.2 and num < 1.3:
        return (1.2, 1.3)
    elif num >= 1.3 and num < 1.4:
        return (1.3, 1.4)
    elif num >= 1.4 and num < 1.5:
        return (1.4, 1.5)
    elif num >= 1.5 and num < 1.6:
        return (1.5, 1.6)
    elif num >= 1.6 and num < 1.7:
        return (1.6, 1.7)
    else:
        return (0,0)


def switchODDData(num):
    maxNum = math.ceil(num)
    minNum = int(num)

    middle = (maxNum + minNum)/2
    if num > middle:
        return (middle, maxNum)
    else:
        return (minNum, middle)

'''
根据联赛id 获取联赛对应的详细信息
'''
def getLeagueDetail(tempLeagueID):
    global conn
    global c

    conn = sqlite3.connect(location)
    c = conn.cursor()

    c.execute("SELECT * FROM League WHERE leagueID == ?", (tempLeagueID, ))
    r = c.fetchall()
    if len(r) > 0:
        return r[0]
    else:
        return None

    conn.commit()
    c.close()
    conn.close()





create_result_database()