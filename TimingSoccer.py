#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
实时性的分析每个时段的比赛.做到临场分析
'''

from DBHelper import *
import exchangeODD
import threading
from SendMail import *
from SoccerRound import *
from datetime import datetime,timedelta

import pycurl
import StringIO

AllGames = []
AllBeginTimes = []
exitflag = 1




def getTodaySoccer(type = 3):
    # type == 3 竞彩
    # type == 1 精简
    # type == 2 十四场

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
            onegame.leauge = dic.get(oneGameArray[1].encode('utf-8')).encode('utf-8')
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
    getHandiProbability(game)

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
        timerAnalys(self.name, 60, len(AllBeginTimes))
        print "Exiting " + self.name


def timerAnalys(threadName, delay, counter):
    global AllBeginTimes
    global AllGames
    global exitflag
    while exitflag:

        now = datetime.now()
        offset_half_hour = timedelta(minutes=-30)
        offset_three_hour = timedelta(hours=-3)

        offset_one_hour = timedelta(hours=-1)
        now_offset_halfHour = now - offset_half_hour
        now_offset_threehour = now - offset_three_hour
        now_offset_onehour = now - offset_one_hour
        nowstr = now.strftime('%Y-%m-%d %H:%M')
        nowstr_offset_threeHour = now_offset_threehour.strftime('%Y-%m-%d %H:%M')
        nowstr_offset_halfHour = now_offset_halfHour.strftime('%Y-%m-%d %H:%M')
        nowstr_offset_oneHour = now_offset_onehour.strftime('%Y-%m-%d %H:%M')
        if nowstr_offset_halfHour == '2017-10-28 13:30':
            nowstr_offset_halfHour = '2017-10-28 13:00'
        print nowstr_offset_halfHour

        allCacluateTimeList = [nowstr_offset_threeHour,nowstr_offset_oneHour,nowstr_offset_halfHour]

        canCaclute = False
        timeStrList = []
        for timestr in allCacluateTimeList:
            if timestr in AllBeginTimes:
                canCaclute = True
                timeStrList.append(timestr)

        if canCaclute:
            for timeStr in timeStrList:
                resultstr = "<!DOCTYPE html><html lang=\"en\"><head><meta charset=\"UTF-8\"><title>临场预测</title></head><body>"
                for onegame in AllGames:
                    if isinstance(onegame, FootballGame):

                        if onegame.beginTime == timeStr:
                            # gameThread(2, '比赛线程', game)
                            onegame.oddCompanies = getOneGameODD(onegame)
                            onegame.handiCompanies = getOneGameHandi(onegame)
                            titlestr = ''.join(
                                [str(onegame.beginTime), ':', onegame.leauge, ':', onegame.homeTeam, 'vs',
                                 onegame.friendTeam, ' id: ',
                                 str(onegame.soccerID), '澳盘: ', str(onegame.orignal_aomenHandi), ' -> ',
                                 str(onegame.now_aomenHandi)])
                            resultstr += "<h3 style=\"color:red;\">%s</h3>" % (titlestr,)
                            # 获取初始盘口数量
                            if len(onegame.orignalHandiList) > 2:
                                resultstr += "<h4 style=\"color:red;\" align=\"center\">初盘混乱</h4>"

                            orignalHandiStr = getHandiProbability(onegame)
                            orignalOddStr = getOrignalODDProbability(onegame)
                            nowOddStr = getnowODDProbability(onegame)

                            nowHandistr = getnowHandiProbability(onegame)
                            if orignalHandiStr is not None:
                                resultstr += "<table bgcolor=\"black\"cellspacing=\"1px\"width=\"375px\" align=\"center\">" \
                                             "<caption style=\"color:red;\"><h5>亚盘</h5></caption><tr bgcolor=#663399><th>博彩公司</th><th>盘口</th><th>数量</th><th>赢盘</th><th>走盘</th><th>输盘</th><th>胜</th><th>平</th><th>负</th></tr> "

                                resultstr += orignalHandiStr

                            if nowHandistr is not None:
                                resultstr += "<tr bgcolor=#888888><th>即时盘口</th><th>%s</th><th></th><th></th><th></th><th></th><th></th><th></th><th></th></tr> " % (str(len(onegame.nowHandiList)))

                                resultstr += nowHandistr
                                resultstr += '</table>'
                            else:
                                resultstr += '</table>'

                            if orignalOddStr is not None:
                                resultstr += "<table bgcolor=\"black\"cellspacing=\"1px\"width=\"375px\" align=\"center\">" \
                                             "<caption style=\"color:red;\"><h5>欧赔</h5></caption><tr bgcolor=#663399 ><td>博彩公司</td> <td>数量</td><td>胜</td><td>平</td><td>负</td><td>胜率</td><td>平率</td><td>负率</td>"

                                resultstr += orignalOddStr

                            if nowOddStr is not None:
                                resultstr += "<tr bgcolor=#888888 ><td>即时欧赔</td> <td></td><td></td><td></td><td></td><td></td><td></td><td></td>"
                                resultstr += nowOddStr
                                resultstr += '</table>'
                            else:
                                resultstr += '</table>'

                            resultstr += "<table bgcolor=\"black\"cellspacing=\"1px\"width=\"375px\" align=\"center\">" \
                                         "<caption style=\"color:red;\"><h5>欧亚转换</h5></caption><tr bgcolor=#663399 ><td>博彩公司</td> <td>转换后</td><td>主</td><td>盘口</td><td>客</td><td>实际</td><td>主</td><td>盘口</td><td>客</td>"
                            resultstr += exchangeODD.getexchange(onegame.soccerID)
                            resultstr += '</table>'
                if resultstr != '' or resultstr is not None:
                    a = datetime.strptime(timeStr, '%Y-%m-%d %H:%M')
                    b = now
                    c = a - b
                    offsetTimeNum = c.seconds / 3600.0

                    send_mail("<<临场%s小时>> 开赛时间:%s " % (str(round(offsetTimeNum, 1)), timeStr,), resultstr, 'html')




        time.sleep(delay)
        if counter == 0:
            exitflag = 0
        print "%s: %s" % (threadName, time.ctime(time.time()))



# if sys.argv.__len__()==1:
#     sys.exit('\033[0;36;40m使用说明:\n1个参数:\n1:精简足球分析   2:十四场足球分析  3:竞彩分析\n事例: python TodaySoccer.pyc 1\033[0m')

if __name__ == '__main__':
    getTodaySoccer(sys.argv[1])
    # getTodaySoccer(3)
    thread1 = TimeingThread(1, "实时分析", 1)
    thread1.start()