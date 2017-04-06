#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import os

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
          '(soccer_ID INTEGER PRIMARY KEY AUTOINCREMENT,gameid INTEGER,result INTEGER,homeSoccer INTEGER,friendSoccer INTEGER,company VARCHAR(10),otodds REAL ,' \
          'orignalpan REAL,ododds REAL,ntodds REAL ,nowpan REAL,ndodds REAL)'
    c.execute(sql1)

    sql2 = 'create table if not exists ' + 'CompanyODD' + \
           '(soccer_ID INTEGER PRIMARY KEY AUTOINCREMENT,gameid INTEGER,result INTEGER,homeSoccer INTEGER,friendSoccer INTEGER,company VARCHAR(10),' \
           'ori_winODD REAL ,ori_drawODD REAL,ori_loseODD REAL,'\
            'winODD REAL ,drawODD REAL,loseODD REAL)'
    c.execute(sql2)

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
        params = (game.soccerID, game.leauge, game.beginTime, game.soccer, game.homeTeamLevel, game.homeTeam,
                     game.allHome, game.friendTeamLevel, game.friendTeam, game.allFriend)
        c.execute("INSERT INTO Games VALUES (NULL ,?,?,?,?,?,?,?,?,?,?)", params)

    conn.commit()
    c.close()
    conn.close()

'''
插入多条亚盘数据
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