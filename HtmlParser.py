#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
# from urllib2 import Request
import requests
import sqlite3




def download(url):
    # print("downloading", url)
    try:
        html = requests.urlopen(url).read()
    except requests.URLError as e:
        print("download error")
        html = None
    return html


def getHtmlListWithLabel(html, label,attrs={}):

    soup = BeautifulSoup(html, "html.parser")

    trList = []
    if attrs != {}:
        tr_ni = soup.find_all(label,attrs=attrs)
    else:
        tr_ni = soup.find_all(label)

    trList.extend(tr_ni)
    return trList

def getSoup(html):

    soup = BeautifulSoup(html, "html.parser")

    return soup

def filterList(list, label):
    tempList = []
    tempList.extend(list)
    for ele in list:
        value = str(ele).find(label)
        if value < 0:
            tempList.remove(ele)

    return tempList

location = '/Users/mi/Desktop/Soccer.db'
def create_database():
    global conn
    global c

    # 连接到SQLite数据库
    # 数据库文件是test.db
    # 如果文件不存在，会自动在当前目录创建:
    conn = sqlite3.connect(location)
    c = conn.cursor()

    sql = 'create table if not exists ' + 'Soccer' + \
          '(soccer_ID INTEGER PRIMARY KEY AUTOINCREMENT,league varchar(20),soccer VARCHAR(5),gameurl VARCHAR (30),otodds VARCHAR(5) ,' \
          'orignalpan VARCHAR(5),ododds VARCHAR(5),ntodds VARCHAR(5) ,nowpan VARCHAR(5),ndodds VARCHAR(5))'
    c.execute(sql)
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