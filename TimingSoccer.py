#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
实时性的分析每个时段的比赛.做到临场分析
'''

from DBHelper import *

import threading
from SendMail import *
from SoccerRound import *

import pycurl
import StringIO
import SendMail

AllGames = []
AllBeginTimes = []
exitflag = 0




def getTodaySoccer(type):
    # type == 3 竞彩
    # type == 1 精简
    # type == 2 十四场
    type = int(type)
    try:
        url = "http://27.45.161.37:8071/phone/schedule_0_" + str(type) + ".txt?an=iosQiuTan&av=6.2&from=2&r=" + str(
            int(time.time()))
        # url = "http://112.91.160.49:8071/phone/schedule_0_" + str(type) + ".txt?an=iosQiuTan&av=5.9&from=2&r=1494229747"


        print url
    except:
        pass
    c = pycurl.Curl()

    c.setopt(pycurl.URL, url)

    b = StringIO.StringIO()
    c.setopt(pycurl.WRITEFUNCTION, b.write)
    c.setopt(pycurl.FOLLOWLOCATION, 1)
    c.setopt(pycurl.MAXREDIRS, 5)
    c.perform()
    resultStr = b.getvalue().decode('utf8')

    global AllGames
    global AllBeginTimes

    if resultStr != '':
        # print resultStr
        allArray = resultStr.split('$$')
        leagueStr = ''
        if type == 1:
            leagueStr = allArray[0]
        else:
            leagueStr = allArray[1]

        allLeague = leagueStr.split('!')
        dic = {}
        locationstr = os.path.join(os.path.abspath('.'), 'league.txt')
        leaguelistfile = open(locationstr, 'r+')
        for league in allLeague:
            oneLeague = league.split('^')
            dic[oneLeague[1]] = oneLeague[0]
        leaguelist = leaguelistfile.readlines()
        for league in allLeague:
            oneLeague = league.split('^')
            dic[oneLeague[1]] = oneLeague[0]

        if type == 1:
            gameStr = allArray[1]
        else:
            gameStr = allArray[2]

        games = gameStr.split('!')
        for game in games:
            onegame = FootballGame()
            oneGameArray = game.split('^')
            oneGameArray.remove('')
            onegame.soccerID = int(oneGameArray[0])
            onegame.leauge = dic.get(oneGameArray[1].encode('utf-8'))
            beginTime = oneGameArray[3].encode('utf-8')
            onegame.beginTime = beginTime[0:4] + '-' + beginTime[4:6] + '-' + beginTime[6:8] + ' ' + beginTime[
                                                                                                     8:10] + ':' + beginTime[
                                                                                                                   10:12]

            briefTimeStr = beginTime[0:4] + '-' + beginTime[4:6] + '-' + beginTime[6:8] + ' ' + beginTime[
                                                                                                8:10] + ':' + beginTime[
                                                                                                              10:12]
            if briefTimeStr not in AllBeginTimes:
                AllBeginTimes.append(briefTimeStr)

            if oneGameArray[4].isdigit() or oneGameArray[4] == '':
                onegame.homeTeam = oneGameArray[5].encode('utf-8')
                onegame.friendTeam = oneGameArray[6].encode('utf-8')
            else:
                onegame.homeTeam = oneGameArray[4].encode('utf-8')
                onegame.friendTeam = oneGameArray[5].encode('utf-8')

            AllGames.append(onegame)


def getgame(game):
    print '开始分析比赛'
    getOneGameODD(game)
    getOneGameHandi(game)
    getGameData(game)

class gameThread(threading.Thread):
    def __init__(self, threadID, name, game):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.game = game
    def run(self):
        print "Starting " + self.name
        # 定时300秒 执行一次
        getgame(self.game)
        print "Exiting " + self.name

class TimeingThread(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        print "Starting " + self.name
        # 定时300秒 执行一次
        timerAnalys(self.name, 300, len(AllBeginTimes))
        print "Exiting " + self.name


def timerAnalys(threadName, delay, counter):
    global AllBeginTimes
    global AllGames
    global exitflag
    while counter:

        now = datetime.now()
        nowstr = now.strftime('%Y-%m-%d %H:%M')
        print nowstr
        if nowstr in AllBeginTimes:
            if AllBeginTimes.index(nowstr) == AllBeginTimes.count() - 1:
                exitflag = 1
            print nowstr
            resultstr = ''
            for game in AllGames:
                if isinstance(game, FootballGame):

                    if game.beginTime == nowstr:
                        # gameThread(2, '比赛线程', game)
                        game.oddCompanies = getOneGameODD(game)
                        game.handiCompanies = getOneGameHandi(game)
                        resultstr +=  getGameData(game)
            if resultstr != '' or resultstr is not None:
                send_mail('临场分析', resultstr)

        time.sleep(delay)
        print "%s: %s" % (threadName, time.ctime(time.time()))
        counter -= 1

        if exitflag:
            threading.Thread.exit()

getTodaySoccer(3)

thread1 = TimeingThread(1, "实时分析", 1)
thread1.start()