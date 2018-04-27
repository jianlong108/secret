#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import time
# import pycurl
import StringIO

'''
获取联赛每轮的内容

leagueID: 联赛ID
leagueSubID: 联赛子ID
gameRound: 当前轮数
reason: 赛季
'''
def GetSeasonRoundstr(leagueID, leagueSubID, gameRound, reason):
    resultStr = ''

    try:
        if gameRound == 0:
            url = "http://ios.win007.com/phone/SaiCheng2.aspx?sclassid=" + str(
                leagueID).encode('utf-8') + "&season=" + reason + "&subid=" + str(
                leagueSubID).encode('utf-8') + "&apiversion=1&from=2"
        else:

            url = "http://ios.win007.com/phone/SaiCheng2.aspx?sclassid=" + str(
                    leagueID).encode('utf-8') + "&season=" + reason + "&subid=" + str(
                    leagueSubID).encode('utf-8') + "&round=" + str(gameRound).encode('utf-8') + "&apiversion=1&from=2"

        print '函数GetSeasonRoundstr' + url
    except Exception as e:
        print '函数GetSeasonRoundstr' + e

    response = requests.get(url)

    if response.ok:
        resultStr = response.content;
    else:
        pass
    return resultStr



'''
获取一场比赛的亚盘数据
'''
def GetOneGameHandiStr(gameid):

    try:
        handiURL = 'http://27.45.161.37:8072/phone/Handicap.aspx?ID=' + gameid + '&an=iosQiuTan&av=5.9&from=2&lang=0'
        print 'getOneGameHandi' + handiURL
    except Exception as e:
        print 'getOneGameHandi' + e

    # c = pycurl.Curl()
    #
    # c.setopt(pycurl.URL, handiURL)
    #
    # b = StringIO.StringIO()
    # c.setopt(pycurl.WRITEFUNCTION, b.write)
    # c.setopt(pycurl.FOLLOWLOCATION, 1)
    # c.setopt(pycurl.MAXREDIRS, 5)
    # c.perform()
    # resultStr = b.getvalue().encode('utf-8')
    return ''

'''
获取一场比赛的亚盘数据
'''
def GetOneGameOddStr(gameid):

    try:
        oddURL = 'http://27.45.161.37:8072/phone/1x2.aspx?ID=' + gameid + '&an=iosQiuTan&av=5.9&from=2&lang=0&subversion=1'
        print 'GetOneGameHandiStr' + oddURL
    except Exception as e:
        print 'GetOneGameHandiStr' + e
        pass

    # c = pycurl.Curl()
    #
    # c.setopt(pycurl.URL, oddURL)
    #
    # b = StringIO.StringIO()
    # c.setopt(pycurl.WRITEFUNCTION, b.write)
    # c.setopt(pycurl.FOLLOWLOCATION, 1)
    # c.setopt(pycurl.MAXREDIRS, 5)
    # c.perform()
    # resultStr = b.getvalue().decode('utf8')

    return ''

'''
获取昨日比赛的详细信息
'''
def GetYesterdaySoccerStr(timestr):
    try:
        url = "http://121.10.245.46:8072/phone/scheduleByDate.aspx?an=iosQiuTan&av=6.4&date=" + timestr + '&from=1&kind=3&r=1503367511&subversion=3'
        # 'http://121.10.245.46:8072/phone/scheduleByDate.aspx?an=iosQiuTan&av=6.4&date=2017-08-21&from=1&kind=3&r=1503367511&subversion=3'

        print 'getYesterdaySoccerStr' + url
    except Exception as e:
        print 'getYesterdaySoccerStr' + e
        pass
    # c = pycurl.Curl()
    #
    # c.setopt(pycurl.URL, url)
    #
    # b = StringIO.StringIO()
    # c.setopt(pycurl.WRITEFUNCTION, b.write)
    # c.setopt(pycurl.FOLLOWLOCATION, 1)
    # c.setopt(pycurl.MAXREDIRS, 5)
    # c.perform()
    # resultStr = b.getvalue().decode('utf8')
    return ''

def GetLeagueDetails(leagueid, season):

    orignalLeagueURL = 'http://ios.win007.com/phone/SaiCheng2.aspx?sclassid=' \
                            + leagueid + '&season=' + season + '&subid=0&apiversion=1&from=2'


    response = requests.get(orignalLeagueURL)

    if response.ok:
        resultStr = response.content;
    else:
        resultStr = ''

    return resultStr

def GetTodaySoccerStr(gameType):
    # type == 3 竞彩
    # type == 1 精简
    # type == 2 十四场
    url = ''
    try:
        url = "http://27.45.161.37:8071/phone/schedule_0_" + gameType + ".txt?an=iosQiuTan&av=6.2&from=2&r="+str(int(time.time()))
        print url
    except Exception as e:
        print 'GetTodaySoccerStr 请求接口出错'
        print e

    # curlInstance = pycurl.Curl()
    #
    # curlInstance.setopt(pycurl.URL, url)
    #
    # b = StringIO.StringIO()
    # curlInstance.setopt(pycurl.WRITEFUNCTION, b.write)
    # curlInstance.setopt(pycurl.FOLLOWLOCATION, 1)
    # curlInstance.setopt(pycurl.MAXREDIRS, 5)
    # curlInstance.perform()
    #
    # resultStr = b.getvalue().decode('utf8')
    response = requests.get(url)

    if response.ok:
        resultStr = response.content;
    else:
        resultStr = ''

    return resultStr


def GetYesterdaySoccerStr(timestr):
    try:
        url = "http://121.10.245.46:8072/phone/scheduleByDate.aspx?an=iosQiuTan&av=6.4&date=" + timestr + '&from=1&kind=3&r=1503367511&subversion=3'
        # 'http://121.10.245.46:8072/phone/scheduleByDate.aspx?an=iosQiuTan&av=6.4&date=2017-08-21&from=1&kind=3&r=1503367511&subversion=3'

        print url
    except:
        pass
    # c = pycurl.Curl()
    #
    # c.setopt(pycurl.URL, url)
    #
    # b = StringIO.StringIO()
    # c.setopt(pycurl.WRITEFUNCTION, b.write)
    # c.setopt(pycurl.FOLLOWLOCATION, 1)
    # c.setopt(pycurl.MAXREDIRS, 5)
    # c.perform()
    # resultStr = b.getvalue().decode('utf8')
    return ''
