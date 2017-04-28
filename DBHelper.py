#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import os
import math
from decimal import Decimal
import sys
reload(sys)
sys.setdefaultencoding('utf8')

location = os.path.expanduser('~/Desktop/Soccer.db')

global conn
global c

def create_database():

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
插入单条联赛数据
'''
def insert_League(league):
    conn = sqlite3.connect(location)
    c = conn.cursor()
    params = (league.leagueID, league.leagueName.decode('utf-8'), league.breifLeagueName.decode('utf-8'), league.aviableSeasonStr.decode('utf-8'))
    c.execute("INSERT INTO League VALUES (NULL ,?,?,?,?)", params)
    # c.execute(sql)
    conn.commit()
    c.close()
    conn.close()

def insert_Game(game):
    conn = sqlite3.connect(location)
    c = conn.cursor()
    params = (game.soccerID, game.leauge, game.beginTime, game.soccer, game.homeTeamLevel, game.homeTeam,
              game.allHome, game.friendTeamLevel, game.friendTeam, game.allFriend)
    c.execute("INSERT INTO Games VALUES (NULL ,?,?,?,?,?,?,?,?,?,?)", params)
    # c.execute(sql)
    conn.commit()
    c.close()
    conn.close()


def insertGameList(games):
    conn = sqlite3.connect(location)
    c = conn.cursor()

    for game in games:
        params = (game.soccerID, game.leauge.decode('utf-8'), game.beginTime.decode('utf-8'), game.soccer, game.homeTeamLevel, game.homeTeam.decode('utf-8'),
                     game.allHome, game.friendTeamLevel, game.friendTeam.decode('utf-8'), game.allFriend)
        c.execute("INSERT INTO Games VALUES (NULL ,?,?,?,?,?,?,?,?,?,?)", params)

        handi = game.handiCompanies
        if handi == None:
            pass
        else:
            for company in handi:
                params1 = (game.soccerID, company.soccerGameId, company.result, company.homeSoccer, company.friendSoccer,
                           company.companyTitle.decode('utf-8'),
                           company.orignal_top, company.orignal, company.orignal_bottom, company.now_top, company.now,
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
插入多条欧赔数据
'''
def insertGameHandiList(games):
    conn = sqlite3.connect(location)
    c = conn.cursor()

    for company in games:
        params = (company.soccerGameId, company.result, company.homeSoccer, company.friendSoccer,company.companyTitle,company.orignal_top,company.orignal,company.orignal_bottom,company.now_top,company.now,company.now_bottom)
        c.execute("INSERT INTO CompanyHandicap VALUES (NULL ,?,?,?,?,?,?,?,?,?,?,?)", params)

    conn.commit()
    c.close()
    conn.close()

'''
插入多条欧赔数据
'''
def insertGameODDList(games):
    conn = sqlite3.connect(location)
    c = conn.cursor()

    for company in games:
        params = (company.soccerGameId, company.result, company.homeSoccer, company.friendSoccer,company.companyTitle, company.orignal_winOdd, company.orignal_drawOdd,
         company.orignal_loseOdd, company.winOdd, company.drawOdd, company.loseOdd)
        c.execute("INSERT INTO CompanyODD VALUES (NULL ,?,?,?,?,?,?,?,?,?,?,?)", params)

    conn.commit()
    c.close()
    conn.close()


def insert_record(params):
    conn = sqlite3.connect(location)
    c = conn.cursor()
    # sql = 'insert into ' + table_name + '(num, league,soccer,gameurl,otodds,orignalpan,ododds,ntodds,nowpan,ndodds) values (NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s)'%(game.leauge,game.soccer,game.url,company.orignal_top,company.orignal,company.orignal_bottom,company.now_top,company.now,company.now_bottom)

    c.execute("INSERT INTO Soccer VALUES (NULL ,?,?,?,?,?,?,?,?,?)", params)
    # c.execute(sql)
    conn.commit()
    c.close()
    conn.close()


'''
插入单条亚盘数据
'''
def insert_Handi(company):
    conn = sqlite3.connect(location)
    c = conn.cursor()
    params = (company.soccerGameId, company.result, company.homeSoccer, company.friendSoccer, company.companyTitle,
              company.orignal_top, company.orignal, company.orignal_bottom, company.now_top, company.now,
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

def getGameData(game,contentStr):
    if isinstance(contentStr, str) == False:
        return
    conn = sqlite3.connect(location)
    c = conn.cursor()
    winCount = 0
    drawCount = 0
    loseCount = 0
    num = 0
    if game.handiCompanies == None:
        return

    for oneCompany in game.handiCompanies:

        # 亚盘
        c.execute("select * from CompanyHandicap where company == ? and orignalpan == ? and nowpan == ? and ntodds >= ? and ntodds < ? and ndodds >= ? and ndodds < ? AND otodds >= ? AND otodds < ? AND ododds >= ? AND ododds < ?", (oneCompany.companyTitle.decode('utf-8'), oneCompany.orignal, oneCompany.now, switchData(oneCompany.now_bottom)[0], switchData(oneCompany.now_bottom)[1], switchData(oneCompany.now_top)[0], switchData(oneCompany.now_top)[1], switchData(oneCompany.orignal_top)[0], switchData(oneCompany.orignal_top)[1], switchData(oneCompany.orignal_bottom)[0], switchData(oneCompany.orignal_bottom)[1]))
        r = c.fetchall()
        num += len(r)
        for result in r:

           if result[3] == 3:
               winCount += 1
           elif result[3] == 1:
               drawCount += 1
           else:
               loseCount += 1

    if num > 0:
        contentStr + str(game.beginTime) + ':' + game.leauge +':'+ game.homeTeam + 'vs' + game.friendTeam
        contentStr + ' 胜:' + str(float(winCount)/float(num) * 100)[:5]+'/100' + ' 平:' + str(float(drawCount)/float(num) * 100)[:5]+'/100' + ' 负:' + str(float(loseCount)/float(num) * 100)[:5]+'/100'
        print str(game.beginTime) + ':' + game.leauge +':'+ game.homeTeam + 'vs' + game.friendTeam
        print ' 胜:' + str(float(winCount)/float(num) * 100)[:5]+'/100' + ' 平:' + str(float(drawCount)/float(num) * 100)[:5]+'/100' + ' 负:' + str(float(loseCount)/float(num) * 100)[:5]+'/100'
    # 欧赔
    winCount = 0
    drawCount = 0
    loseCount = 0
    num = 0
    if len(game.oddCompanies) <= 0:
        return
    for oneOdd in game.oddCompanies:
        c.execute(
            "select * from CompanyODD where company == ? and ori_winODD >= ? and ori_winODD <= ? and ori_drawODD >= ? and ori_drawODD <= ? and ori_loseODD >= ? and ori_loseODD <= ? and winODD >= ? and winODD <= ? AND drawODD >= ? and drawODD <= ? AND loseODD >= ? and loseODD <= ?",
            (oneCompany.companyTitle.decode('utf-8'), switchODDData(oneOdd.orignal_winOdd)[0], switchODDData(oneOdd.orignal_winOdd)[1], switchODDData(oneOdd.orignal_drawOdd)[0], switchODDData(oneOdd.orignal_drawOdd)[1], switchODDData(oneOdd.orignal_loseOdd)[0], switchODDData(oneOdd.orignal_loseOdd)[1], switchODDData(oneOdd.winOdd)[0], switchODDData(oneOdd.winOdd)[1], switchODDData(oneOdd.drawOdd)[0], switchODDData(oneOdd.drawOdd)[1], switchODDData(oneOdd.loseOdd)[0], switchODDData(oneOdd.loseOdd)[1])
             )
        r = c.fetchall()
        num += len(r)
        for result in r:
            if result[3] == 3:
                winCount += 1
            elif result[3] == 1:
                drawCount += 1
            else:
                loseCount += 1

    if num > 0:
        contentStr + ' 胜:' + str(float(winCount) / float(num) * 100)[
                                                               :5] + '/100' + ' 平:' + str(
            float(drawCount) / float(num) * 100)[:5] + '/100' + ' 负:' + str(float(loseCount) / float(num) * 100)[
                                                                        :5] + '/100'
        print ' 胜:' + str(float(winCount) / float(num) * 100)[
                                                               :5] + '/100' + ' 平:' + str(
            float(drawCount) / float(num) * 100)[:5] + '/100' + ' 负:' + str(float(loseCount) / float(num) * 100)[
                                                                        :5] + '/100'
        print '\n'

    contentStr + '-------------------------------------------'

    c.close()
    conn.close()

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