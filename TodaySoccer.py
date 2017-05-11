#!/usr/bin/env python
# -*- coding: utf-8 -*-


import time
from urllib2 import Request
import urllib2
from bs4 import BeautifulSoup
from DBHelper import *
from SoccerModels import *
from SoccerRound import *
import datetime

from SendMail import *
from SoccerRound import *

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
    # type == 3 精彩
    # type == 1 精简
    # type == 2 十四场
    type = int(type)
    try:
        url = "http://112.91.160.49:8071/phone/schedule_0_" + str(type) + ".txt?an=iosQiuTan&av=5.9&from=2&r="+str(int(time.time()))
        # url = "http://112.91.160.49:8071/phone/schedule_0_" + str(type) + ".txt?an=iosQiuTan&av=5.9&from=2&r=1494229747"


        print url
    except:
        pass
    resultStr = ''
    # req = urllib2.Request(url)
    # req.add_header("User-Agent", "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)")
    response = requests.get(url)
    # response = urllib2.urlopen(req)
    if response.ok:
        resultStr = response.content;
    else:
        pass

    AllGames = []
    AllBeginTimes = []
    resultStr = '芬超^13^1!欧罗巴杯^113^1!瑞典甲^122^1!南球杯^263^1!南美超杯^270^1!芬甲^212^1!丹麦甲^127^1!秘鲁甲^242^1!白俄超^230^1!立陶甲^217^1!哥伦甲^250^1!保超^131^1!委內超^391^1!哥斯甲^504^1!玻利甲^593^1!巴西杯^186^1!墨西联^140^1!阿乙^423^1!美公开赛^483^1!厄瓜甲^596^1$$1379126^131^0^20170511220000^^格纳火车头^比林^0^0^^^0^0^0^0^-0.25^^^0^4^1^^^0^0^0^0^0^^0^0^2.25^!1364590^230^0^20170511230000^^索利戈尔斯克矿工^FC斯拉维亚^0^0^^^0^0^0^0^1.5^^^0^4^14^^^0^0^0^0^1^^0^0^2.5^9.5!1364959^217^0^20170511230000^^苏杜瓦^乌田纳^0^0^^^0^0^0^0^1.5^^^0^2^5^^^0^0^0^0^0^^0^0^2.75^!1357040^13^0^20170511233000^^赫尔辛基^埃尔维斯^0^0^^^0^0^0^0^1.25^^^0^1^2^^^0^0^0^0^1^^0^0^2.5^8.5!1352473^212^0^20170511233000^^哈卡^EIF埃克纳斯^0^0^^^0^0^0^0^0.5^^^0^10^7^^^0^0^0^0^0^^0^0^3^!1364589^230^0^20170511233000^^兹霍迪诺^库鲁马卡西^0^0^^^0^0^0^0^0.5^^^0^5^11^^^0^0^0^0^1^^0^0^2^9.5!1256068^127^0^20170511235900^^AB哥本哈根^希尔星格^0^0^^^0^0^0^0^-0.75^^^0^12^3^^^0^0^0^0^1^^0^0^2.75^9.5!1256069^127^0^20170511235900^^霍布罗^维积利^0^0^^^0^0^0^0^1^^^0^1^7^^^0^0^0^0^1^^0^0^2.75^10!1256070^127^0^20170511235900^^阿玛盖尔^纳斯特维德^0^0^^^0^0^0^0^0.25^^^0^8^11^^^0^0^0^0^1^^0^0^2.5^9.5!1256071^127^0^20170511235900^^LFA尼克宾^罗斯基德^0^0^^^0^0^0^0^-0.25^^^0^9^5^^^0^0^0^0^0^^0^0^2.5^!1256072^127^0^20170511235900^^靴尔科治^弗雷德里西亚^0^0^^^0^0^0^0^0.25^^^0^6^10^^^0^0^0^0^1^^0^0^2.5^9.5!1256073^127^0^20170511235900^^文德斯尔^斯基夫^0^0^^^0^0^0^0^0.75^^^0^4^2^^^0^0^0^0^1^^0^0^2.5^9.5!1364588^230^0^20170511235900^^利文哥特奴^纳夫田^0^0^^^0^0^0^0^1.25^^^0^7^16^^^0^0^0^0^1^^0^0^2.5^9.5!1364591^230^0^20170512003000^^戈洛迪亚^德内普^0^0^^^0^0^0^0^0.25^^^0^9^6^^^0^0^0^0^1^^0^0^2^10!1379125^131^0^20170512003000^^贝尔罗^內夫托西米克^0^0^^^0^0^0^0^0.75^^^0^2^3^^^0^0^0^0^0^^0^0^2.25^!1336878^122^0^20170512010000^^奥尔格里特^哥德堡盖斯^0^0^^^0^0^0^0^0.25^^^0^10^9^^^0^0^0^0^1^^0^0^2.5^10.5!1364960^217^0^20170512010000^^施登巴斯^考诺萨基列斯^0^0^^^0^0^0^0^0.5^^^0^7^8^^^0^0^0^0^0^^0^0^2.25^!1381863^113^0^20170512030500^^曼彻斯特联^塞尔塔^0^0^^^0^0^0^0^1^^^0^6^12^^^1^0^0^0^1^^0^0^2.75^10!1381864^113^0^20170512030500^^里昂^阿贾克斯^0^0^^^0^0^0^0^0.75^^^0^4^2^^^1^0^0^0^1^^0^0^3^10!1363911^263^0^20170512061500^^萨兰迪兵工厂^胡安奥里奇^0^0^^^0^0^0^0^1.25^^^0^30^8^^^0^0^0^0^1^^0^0^2.5^10!1363912^263^0^20170512061500^^卡拉卡斯^波特诺山丘^0^0^^^0^0^0^0^-0.25^^^0^7^4^^^0^0^0^0^1^^0^0^2.25^9.5!1349718^250^0^20170512070000^^托利马体育^佩雷拉金鹰^0^0^^^0^0^0^0^0.5^^^0^13^17^^^0^0^0^0^1^^0^0^2.25^8.5!1348184^391^0^20170512070000^^莫纳加斯^拉腊体育^0^0^^^0^0^0^0^0.5^^^0^9^13^^^0^0^0^0^0^^0^0^2.5^!1386900^140^0^20170512083000^^莫雷利亚^提华纳^0^0^^^0^0^0^0^0^^^0^8^1^^^0^0^0^0^1^^0^0^2.5^9.5!1363909^263^0^20170512084500^^丹奴比奥(中)^累西腓体育^0^0^^^0^0^0^0^0.25^^^0^11^3^^^0^0^0^0^1^^0^0^2.25^9.5!1363910^263^0^20170512084500^^圣保罗^防卫者^0^0^^^0^0^0^0^0.75^^^0^5^14^^^0^0^0^0^1^^0^0^2.25^9.5!1349717^250^0^20170512090000^^国民竞技^锡帕基拉老虎^0^0^^^0^0^0^0^1^^^0^1^15^^^0^0^0^0^0^^0^0^2.5^!1351931^242^-1^20170511080000^20170511090748^梅尔加^英提加斯^2^2^0^2^0^0^2^7^1^^^0^1^5^^^0^0^11^2^1^^6^0^2.5^10!1357581^593^-1^20170511080000^20170511090331^奥利恩特^史庄格斯^3^1^1^1^0^0^2^4^0^^^0^4^2^^^0^0^4^6^1^^3^0^2.75^10!1302626^423^-1^20170511080000^20170511085830^克鲁塞罗德尔诺特^维拉多尔米尼^1^2^1^1^0^0^2^4^0.25^^^0^22^21^^^0^0^6^1^1^^3^0^2.25^9!1302629^423^-1^20170511080000^20170511090509^联合队^吉列尔莫布朗^2^0^1^0^1^1^2^1^0.25^^^0^6^2^^^0^0^5^1^1^^2^0^2.25^9!1302634^423^-1^20170511080000^20170511090352^瓜勒瓜伊楚^博卡联合^1^1^0^0^0^0^1^4^0.25^^^0^20^19^^^0^0^8^3^1^^3^2^2^9.5!1302628^423^-1^20170511080500^20170511090956^查卡里塔青年^布朗安德奎^1^2^1^1^0^0^1^6^0.5^^^0^4^10^^^0^0^2^3^1^^0^2^2^9!1302630^423^-1^20170511080500^20170511091547^阿根廷青年人^全男孩竞技^5^1^1^0^0^0^1^2^1^^^0^1^11^^^0^0^0^6^1^^0^3^2^9!1302633^423^-1^20170511081500^20170511091759^洛斯安第斯^科尔多瓦中央SDE^1^1^1^0^0^0^0^3^0.25^^^0^9^8^^^0^0^5^3^1^^3^2^2^9!1348310^596^-1^20170511081500^20170511092158^瓜亚基尔^利加大学^3^1^2^0^0^1^2^5^1^^^0^6^9^^^0^0^8^3^1^^4^1^2.25^9!1386898^140^-1^20170511083000^20170511093200^泰格雷斯^蒙特瑞^4^1^2^0^0^1^1^7^0.25^^^1^7^2^^^0^0^5^7^1^^4^3^2.5^10!1302627^423^-1^20170511083000^20170511093534^图库曼圣马丁^巴拉纳竞技会^4^2^1^1^0^0^1^2^0.75^^^0^12^23^^^0^0^5^6^1^^1^6^2.25^10!1386882^483^-1^20170511083000^20170511093300^塔尔萨体育会^OKC能量U23^1^1^0^1^0^0^1^1^^^^0^^1^90,1-1;;1,1-1;2-4;2^^0^0^2^1^1^^0^0^^!1363913^263^-1^20170511084500^20170511095200^智利大学^科林蒂安^1^2^0^1^2^0^5^1^0.25^^^0^2^2^^^0^0^4^1^1^^3^1^2.25^10!1363914^263^-1^20170511084500^20170511095000^蒙得维的(中)^弗鲁米嫩塞^1^0^1^0^0^0^4^3^-0.5^^^0^14^4^^^0^0^6^1^1^^5^1^2.25^10!1376858^270^-1^20170511084500^20170511094800^国民竞技^沙佩科恩斯^4^1^2^0^0^1^3^5^1.25^^^0^1^1^^^0^0^3^7^1^^2^3^2.5^9!1383790^186^-1^20170511084500^20170511095100^圣十字^巴拉纳竞技^0^0^0^0^0^0^2^4^0.25^^^0^4^8^^^0^0^6^4^1^^5^3^2.25^10!1383793^186^-1^20170511084500^20170511094932^帕桑度^桑托斯^1^3^0^1^0^0^0^1^-0.75^^^0^38^3^^^0^0^4^6^1^^2^1^2.5^11!1349721^250^-1^20170511090000^20170511101143^巴兰基亚青年^布卡拉曼格^3^1^2^1^0^0^1^2^0.75^^^1^18^10^^^0^0^4^5^1^^2^2^2.25^9!1385303^504^-1^20170511100000^20170511110429^希雷迪亚诺^萨普里萨^0^1^0^0^0^0^1^3^0.5^^^0^1^3^^^0^0^4^6^1^^3^2^2.5^10!1386899^140^-1^20170511103000^20170511114022^桑托斯拉古纳^托卢卡^1^4^0^1^0^0^1^3^0.25^^^1^5^4^^^0^0^9^7^1^^3^7^2.5^10!1386877^483^-12^20170511080000^^芝加哥火焰P^格兰德急流^0^0^0^0^0^0^0^0^0.25^^^0^^57^^^0^0^0^0^0^^0^0^2.75^'
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
            dic[oneLeague[1]] = oneLeague[0]

        gameStr = ''
        if type == 1:
            gameStr = allArray[1]
        else:
            gameStr = allArray[2]

        games = gameStr.split('!')
        contentStr = ''
        for game in games:
            onegame = FootballGame()
            oneGameArray = game.split('^')
            oneGameArray.remove('')
            onegame.soccerID = int(oneGameArray[0])
            onegame.leauge = dic.get(oneGameArray[1].encode('utf-8'))
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

            onegame.oddCompanies = getOneGameODD(onegame)
            onegame.handiCompanies = getOneGameHandi(onegame)
            # templist = getexchange(onegame.soccerID)
            tempstr = getGameData(onegame)
            if tempstr != None:
                contentStr = contentStr + tempstr
                contentStr = contentStr + '\n'
                # contentStr = contentStr.join(templist)
            time.sleep(3)

        i = datetime.now()

        if type == 1:
            subjectstr = '精简足球分析'
        elif type == 2:
            subjectstr = '十四场足球分析'
        else:
            subjectstr = '竞彩分析'

        send_mail("%s %s/%s/%s" % (subjectstr, i.year, i.month, i.day), contentStr)
        # if type == 1 or type == 3:
        #     runTask(anyaisegame, AllGames, AllBeginTimes)


# if sys.argv.__len__()==1:
#     sys.exit('\033[0;36;40m使用说明:\n1个参数:\n1:精简足球分析   2:十四场足球分析  3:竞彩分析\n事例: python TodaySoccer.pyc 1\033[0m')
#
# if __name__ == '__main__':
#     getTodaySoccer(sys.argv[1])
getTodaySoccer(1)




# getexchange(1255863)