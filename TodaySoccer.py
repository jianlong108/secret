#!/usr/bin/env python
# -*- coding: utf-8 -*-



from DBHelper import *

import datetime

from SendMail import *
from SoccerRound import *

import pycurl
import StringIO
import getHandiOrignalTime

global AllGames
global AllBeginTimes



def anyaisegame(beginTimeStr, AllGames, AllBeginTimes):
    # global AllGames
    # global AllBeginTimes
    contentStr = ''
    for game in AllGames:
        if game.beginTime == beginTimeStr:
            game.oddCompanies = getOneGameODD(game)
            game.handiCompanies = getOneGameHandi(game)

            tempstr = getGameData(game)
            if tempstr != None:
                contentStr = contentStr + tempstr
                contentStr = contentStr + '\n'

            time.sleep(3)

    subjectstr = '时段足球分析'
    send_mail("%s %s" % (subjectstr, beginTimeStr), contentStr)
    del AllBeginTimes[0]
    if len(AllBeginTimes) > 0:
        runTask(anyaisegame, AllGames, AllBeginTimes)

def runTask(func, AllGames, AllBeginTimes):
# def runTask(func, day=0, hour=0, min=0, second=0):
    # get current time
    # now = datetime.now()
    # strnow = now.strftime('%Y-%m-%d %H:%M:%S')
    # print "now:", strnow
    # get net_run time
    # period = timedelta(days=0, hours=0, minutes=15, seconds=0)
    # next_time = now + period
    # strnext_time = next_time.strftime('%Y-%m-%d %H:%M:%S')
    # global AllGames
    # global AllBeginTimes

    timeStr = AllBeginTimes[0]
    print timeStr
    now = datetime.now()


    # period = timedelta(days=0, hours=0, minutes=15, seconds=0)
    # next_time = now - period
    # strnext_time = next_time.strftime('%Y-%m-%d %H:%M:%S')
    strnow = now.strftime('%Y-%m-%d %H:%M:%S')
    strnow = '2017-05-08 19:29'
    if timeStr < strnow:
        del AllBeginTimes[0]
        runTask(anyaisegame, AllGames, AllBeginTimes)
        return
    strnext_time = timeStr
    print "next run:", strnext_time
    while True:
        now = datetime.now()
        strnow = now.strftime('%Y-%m-%d %H:%M:%S')
        strnow = '2017-05-08 19:30'
        # if system time eq next_time run the specific task(hello func)
        if str(strnow) == str(strnext_time):
            print strnow
            func(str(strnow), AllGames, AllBeginTimes)
            break

def getTodaySoccer(type):
    # type == 3 竞彩
    # type == 1 精简
    # type == 2 十四场
    type = int(type)
    try:
        url = "http://27.45.161.37:8071/phone/schedule_0_" + str(type) + ".txt?an=iosQiuTan&av=6.2&from=2&r="+str(int(time.time()))
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

    AllGames = []
    AllBeginTimes = []

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
        for league in allLeague:
            oneLeague = league.split('^')
            dic[oneLeague[1]] = oneLeague[0].encode('utf-8')

        gameStr = ''
        if type == 1:
            gameStr = allArray[1]
        else:
            gameStr = allArray[2]

        games = gameStr.split('!')
        firstobject = games[0]
        contentStr = "<!DOCTYPE html><html lang=\"en\"><head><meta charset=\"UTF-8\"><title>初盘预测</title></head><body>"
        for game in games:
            # if game is not firstobject:
            #     continue;
            onegame = FootballGame()
            oneGameArray = game.split('^')
            oneGameArray.remove('')
            onegame.soccerID = int(oneGameArray[0])
            onegame.leauge = dic.get(oneGameArray[1])
            beginTime = oneGameArray[3].encode('utf-8')
            onegame.beginTime = beginTime[0:4] + '-' + beginTime[4:6] + '-' + beginTime[6:8] + ' ' + beginTime[8:10] + ':' + beginTime[10:12]


            briefTimeStr = beginTime[0:4] + '-' + beginTime[4:6] + '-' + beginTime[6:8] + ' ' + beginTime[8:10] + ':' + beginTime[10:12]
            if briefTimeStr not in AllBeginTimes:
                AllBeginTimes.append(briefTimeStr)

            if oneGameArray[4].isdigit() or oneGameArray[4] == '':
                onegame.homeTeam = oneGameArray[5].encode('utf-8')
                onegame.friendTeam = oneGameArray[6].encode('utf-8')
            else:
                onegame.homeTeam = oneGameArray[4].encode('utf-8')
                onegame.friendTeam = oneGameArray[5].encode('utf-8')
            AllGames.append(onegame)
            # 获取欧赔,亚盘数据
            onegame.oddCompanies = getOneGameODD(onegame)
            onegame.handiCompanies = getOneGameHandi(onegame)

            titlestr = ''.join([str(onegame.beginTime), ':', onegame.leauge, ':', onegame.homeTeam, 'vs', onegame.friendTeam, ' id: ',
                     str(onegame.soccerID), '澳盘: ', str(onegame.orignal_aomenHandi), ' -> ', str(onegame.now_aomenHandi)])
            contentStr += "<h3 style=\"color:red;\">%s</h3>" % (titlestr,)

            # 获取开盘时间
            flag = getHandiOrignalTime.gethandiTime(onegame.soccerID)
            if flag:
                # contentStr += '澳盘开盘早\n'.join([str(onegame.beginTime), ':', onegame.leauge, ':', onegame.homeTeam, 'vs', onegame.friendTeam])
                contentStr += "<h4 style=\"color:red;\" align=\"center\">澳盘开盘早</h4>"
            # 获取初始盘口数量
            if len(onegame.orignalHandiList) > 2:
                contentStr += "<h4 style=\"color:red;\" align=\"center\">初盘混乱</h4>"
                # contentStr += '初盘混乱\n'
                # contentStr += ''.join(
                #     [str(onegame.beginTime), ':', onegame.leauge, ':', onegame.homeTeam, 'vs', onegame.friendTeam])

            contentStr += "<table bgcolor=\"black\"cellspacing=\"1px\"width=\"375px\" align=\"center\">" \
                          "<caption style=\"color:red;\"><h5>亚盘</h5></caption><tr bgcolor=#663399><th>博彩公司</th><th>盘口</th><th>数量</th><th>赢盘</th><th>走盘</th><th>输盘</th><th>胜</th><th>平</th><th>负</th></tr> "
            tempHandistr = getHandiProbability(onegame)
            if tempHandistr is not None:
                contentStr += tempHandistr
                # contentStr += '\n'


            tempNowHandistr = getnowHandiProbability(onegame)
            if tempNowHandistr is not None:
                contentStr += "<tr bgcolor=#888888><th>即时盘口</th><th>%s</th><th></th><th></th><th></th><th></th><th></th><th></th><th></th></tr> "%(str(len(onegame.nowHandiList)))
                contentStr += tempNowHandistr
                contentStr += '</table>'
            else:
                contentStr += '</table>'


            contentStr += '</table>'
            contentStr += "<table bgcolor=\"black\"cellspacing=\"1px\"width=\"375px\" align=\"center\"><caption style=\"color:red;\"><h5>欧赔</h5></caption>" \
                          "<tr bgcolor=\"white\" ><td>博彩公司</td> <td>数量</td><td>胜</td><td>平</td><td>负</td><td>胜率</td><td>平率</td><td>负率</td>"
            tempOddstr = getOrignalODDProbability(onegame)
            if tempOddstr is not None:
                contentStr += tempOddstr
                # contentStr += '\n'

            tempNowOddstr = getnowODDProbability(onegame)

            if tempNowOddstr is not None:
                contentStr += "<tr bgcolor=#888888 ><td>即时欧赔</td> <td></td><td></td><td></td><td></td><td></td><td></td><td></td>"
                contentStr += tempNowOddstr
                contentStr += '</table>'
            else:
                contentStr += '</table>'

            time.sleep(3)

        i = datetime.now()

        if type == 1:
            subjectstr = '精简足球分析'
        elif type == 2:
            subjectstr = '十四场足球分析'
        else:
            subjectstr = '初盘分析'

        send_mail("%s %s/%s/%s" % (subjectstr, i.year, i.month, i.day), contentStr,'html')
        # if type == 1 or type == 3:
        #     runTask(anyaisegame, AllGames, AllBeginTimes)


# if sys.argv.__len__()==1:
#     sys.exit('\033[0;36;40m使用说明:\n1个参数:\n1:精简足球分析   2:十四场足球分析  3:竞彩分析\n事例: python TodaySoccer.pyc 1\033[0m')
#
# if __name__ == '__main__':
#     getTodaySoccer(sys.argv[1])
getTodaySoccer(1)
