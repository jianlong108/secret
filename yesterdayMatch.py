#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from datetime import timedelta

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

from SendMail import *
from SoccerRound import *

import pycurl
import StringIO
from DBHelper import *

global AllGames
global AllBeginTimes


def unicodeTostr(onestr):
    str(onestr).encode('utf-8')

def getYesterdaySoccer(timestr):
    try:
        url = "http://121.10.245.46:8072/phone/scheduleByDate.aspx?an=iosQiuTan&av=6.4&date=" + timestr + '&from=1&kind=3&r=1503367511&subversion=3'
# 'http://121.10.245.46:8072/phone/scheduleByDate.aspx?an=iosQiuTan&av=6.4&date=2017-08-21&from=1&kind=3&r=1503367511&subversion=3'

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
        location = os.path.expanduser('~/Desktop/league.txt')
        leaguelistfile = open(location, 'r+')
        for league in allLeague:
            oneLeague = league.split('^')
            dic[oneLeague[1]] = oneLeague[0]
            # leaguelistfile.write('%s:%s\n'%(oneLeague[1],oneLeague[0]))
        leaguelist = leaguelistfile.readlines()
        # return
        gameStr = ''
        if type == 1:
            gameStr = allArray[1]
        else:
            gameStr = allArray[2]

        games = gameStr.split('!')
        contentStr = ''
        for game in games:
            tempstr_utf_8 =  game.encode('utf-8')
            onegame = FootballGame()
            oneGameArray = tempstr_utf_8.split('^')
            # 0.soccerid
            # 1.联赛id
            # 2. - 1
            # 3.开赛时间
            # 4.下半场开赛时间
            # 5.主队
            # 6.客队
            # 7.主队比分
            # 8.客队比分
            # 9.主队半场比分
            # 10.客队半场比分
            # 11.主队红牌个数
            # 12.客队红牌个数
            # 13.主队黄牌个数
            # 14.客队黄牌个数
            # 15.盘口
            # 赔率
            # 16 胜
            # 17 平
            # 18 负

            onegame.soccerID = int(oneGameArray[0])
            onegame.leauge = dic.get(oneGameArray[1].encode('utf-8'))
            flag = False
            for leaguestr in leaguelist:
                if onegame.leauge in leaguestr:
                    flag = True

            if flag is False:
                continue

            beginTime = oneGameArray[3].encode('utf-8')
            onegame.beginTime = beginTime[0:4] + '-' + beginTime[4:6] + '-' + beginTime[6:8] + ' ' + beginTime[
                                                                                                     8:10] + ':' + beginTime[
                                                                                                                   10:12]

            briefTimeStr = beginTime[0:4] + '-' + beginTime[4:6] + '-' + beginTime[6:8] + ' ' + beginTime[
                                                                                                8:10] + ':' + beginTime[
                                                                                                              10:12]
            if briefTimeStr not in AllBeginTimes:
                AllBeginTimes.append(briefTimeStr)

            onegame.homeTeam = oneGameArray[5]
            onegame.friendTeam = oneGameArray[6]
            onegame.allHome = int(oneGameArray[7])
            onegame.allFriend = int(oneGameArray[8])
            onegame.halfHome = int(oneGameArray[9])
            onegame.halfFriend = int(oneGameArray[10])

            if oneGameArray[15] !='' and oneGameArray[15] is not None:
                onegame.bet365Handi = float(oneGameArray[15])


            AllGames.append(onegame)
            onegame.oddCompanies = getOneGameODD(onegame)
            onegame.handiCompanies = getOneGameHandi(onegame)
            print onegame.leauge +' ' + onegame.homeTeam +' '+ onegame.friendTeam +' '+ str(onegame.soccer)

            time.sleep(1.5)

        insertGameList(AllGames)



def main():
    now = datetime.now()
    aDay = timedelta(days=-1)
    now = now + aDay
    yesterdaystr = now.strftime('%Y-%m-%d')
    getYesterdaySoccer('2017-08-23')
# if sys.argv.__len__()==1:
#     sys.exit('\033[0;36;40m使用说明:\n1个参数:\n1:精简足球分析   2:十四场足球分析  3:竞彩分析\n事例: python TodaySoccer.pyc 1\033[0m')
#
# if __name__ == '__main__':
#     getYesterdaySoccer(sys.argv[1])

main()
