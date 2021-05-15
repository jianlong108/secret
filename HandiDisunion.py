#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from GetData.DBHELPER import *
from GetData.SOCCER_ROUND import *
from SendMail import send_mail

AllGames = []
AllBeginTimes = []
AllResultAnalyseGames = []

def getTodaySoccer(gameType):
    # type == 3 竞彩
    # type == 1 精简
    # type == 2 十四场
    url = ''
    resultStr = ''
    gameType = int(gameType)
    try:
        url = "http://61.143.225.85:8072/phone/schedule_0_" + str(gameType) + ".txt?an=iosQiuTan&av=2.4&from=2&r="+str(int(time.time()))
        print url
    except Exception as e:
        print '请求接口出错' + url
        print e

    if url != '':
        resultStr = get_resultstr_with_url(url)

    global AllGames
    global AllBeginTimes

    if resultStr != '':
        # print resultStr
        allArray = resultStr.split('$$')

        if gameType == 1:
            leagueStr = allArray[0]
        else:
            leagueStr = allArray[1]

        allLeague = leagueStr.split('!')
        dic = {}
        for league in allLeague:
            oneLeague = league.split('^')
            dic[oneLeague[1]] = oneLeague[0].encode('utf-8')

        if gameType == 1:
            gameStr = allArray[1]
        else:
            gameStr = allArray[2]

        games = gameStr.split('!')
        # firstobject = games[0]
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

            if len(onegame.nowHandiList) > 1:
                getHandiDisunion(onegame)

            # 获取开盘时间
            # flag = getHandiOrignalTime.gethandiTime(onegame.soccerID)
            # if flag:
            #     contentStr += "<h4 style=\"color:red;\" align=\"center\">澳盘开盘早</h4>"
            # 获取初始盘口数量
            # if len(onegame.orignalHandiList) > 2:
            #     contentStr += "<h4 style=\"color:red;\" align=\"center\">初盘混乱</h4>"
                # contentStr += '初盘混乱\n'
                # contentStr += ''.join(
                #     [str(onegame.beginTime), ':', onegame.leauge, ':', onegame.homeTeam, 'vs', onegame.friendTeam])

            # contentStr += "<table bgcolor=\"black\"cellspacing=\"1px\"width=\"375px\" align=\"center\">" \
            #               "<caption style=\"color:red;\"><h5>亚盘</h5></caption><tr bgcolor=#663399><th>博彩公司</th><th>盘口</th><th>数量</th><th>赢盘</th><th>走盘</th><th>输盘</th><th>胜</th><th>平</th><th>负</th></tr> "
            # tempHandistr = getHandiProbability(onegame)
            # if tempHandistr is not None:
            #     contentStr += tempHandistr
            #     # contentStr += '\n'
            #
            #
            # tempNowHandistr = getnowHandiProbability(onegame)
            # if tempNowHandistr is not None:
            #     contentStr += "<tr bgcolor=#888888><th>即时盘口</th><th>%s</th><th></th><th></th><th></th><th></th><th></th><th></th><th></th></tr> "%(str(len(onegame.nowHandiList)))
            #     contentStr += tempNowHandistr
            #     contentStr += '</table>'
            # else:
            #     contentStr += '</table>'
            #
            #
            # contentStr += '</table>'
            # contentStr += "<table bgcolor=\"black\"cellspacing=\"1px\"width=\"375px\" align=\"center\"><caption style=\"color:red;\"><h5>欧赔</h5></caption>" \
            #               "<tr bgcolor=\"white\" ><td>博彩公司</td> <td>数量</td><td>胜</td><td>平</td><td>负</td><td>胜率</td><td>平率</td><td>负率</td>"
            # tempOddstr = getOrignalODDProbability(onegame)
            # if tempOddstr is not None:
            #     contentStr += tempOddstr
            #     # contentStr += '\n'
            #
            # tempNowOddstr = getnowODDProbability(onegame)
            #
            # if tempNowOddstr is not None:
            #     contentStr += "<tr bgcolor=#888888 ><td>即时欧赔</td> <td></td><td></td><td></td><td></td><td></td><td></td><td></td>"
            #     contentStr += tempNowOddstr
            #     contentStr += '</table>'
            # else:
            #     contentStr += '</table>'

            time.sleep(3)

        i = datetime.datetime.now()

        if gameType == 1:
            subjectstr = '精简足球分析'
        elif gameType == 2:
            subjectstr = '十四场足球分析'
        else:
            subjectstr = '初盘分析'

        subjectstr += '  盘口不一致'
        send_mail("%s %s/%s/%s" % (subjectstr, i.year, i.month, i.day), contentStr,'html')

def getYesterdaySoccer(timestr):
    url = ''
    resultStr = ''
    try:
        url = "http://121.10.245.46:8072/phone/scheduleByDate.aspx?an=iosQiuTan&av=6.4&date=" + timestr + '&from=1&kind=3&r=1503367511&subversion=3'
        # 'http://121.10.245.46:8072/phone/scheduleByDate.aspx?an=iosQiuTan&av=6.4&date=2017-08-21&from=1&kind=3&r=1503367511&subversion=3'
        print url
    except BaseException as e:
        print e
        pass
    if url != '':
        resultStr = get_resultstr_with_url(url)

    global AllGames
    global AllBeginTimes
    global AllResultAnalyseGames

    if resultStr != '':
        allArray = resultStr.split('$$')
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
        if type == 1:
            gameStr = allArray[1]
        else:
            gameStr = allArray[2]

        games = gameStr.split('!')
        contentStr = "<!DOCTYPE html><html lang=\"en\"><head><meta charset=\"UTF-8\"><title>初盘预测</title></head><body>"

        for game in games:
            tempstr_utf_8 = game.encode('utf-8')
            resultGame = ResultAnalyseGame()
            onegame = FootballGame()
            oneGameArray = tempstr_utf_8.split('^')
            '''
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
            '''

            try:
                onegame.soccerID = int(oneGameArray[0])
                onegame.leauge = dic.get(oneGameArray[1].encode('utf-8'))
                # 比赛结果模型 赋值soccerID.联赛
                resultGame.soccerID = onegame.soccerID
                resultGame.league = onegame.leauge
                # 赋值结束
                flag = False
                for leaguestr in leaguelist:
                    if onegame.leauge in leaguestr:
                        flag = True
                    # if onegame.leauge == '英超':
                    #     flag = True

                if flag is False:
                    continue

                beginTime = oneGameArray[3].encode('utf-8')
                onegame.beginTime = beginTime[0:4] + '-' + beginTime[4:6] + '-' + beginTime[6:8] + ' ' + beginTime[
                                                                                                         8:10] + ':' + beginTime[
                                                                                                                       10:12]
                # 比赛结果模型 赋值开赛时间
                resultGame.beginTime = onegame.beginTime
                # 赋值结束

                briefTimeStr = beginTime[0:4] + '-' + beginTime[4:6] + '-' + beginTime[6:8] + ' ' + beginTime[
                                                                                                    8:10] + ':' + beginTime[
                                                                                                                  10:12]
                if briefTimeStr not in AllBeginTimes:
                    AllBeginTimes.append(briefTimeStr)

                onegame.homeTeam = oneGameArray[5]
                onegame.friendTeam = oneGameArray[6]
                onegame.allHome = int(oneGameArray[7])
                onegame.allFriend = int(oneGameArray[8])
                # 比赛结果模型 赋值主客队,比分
                resultGame.homeTeam = onegame.homeTeam
                resultGame.friendTeam = onegame.friendTeam
                resultGame.homeSoccer = onegame.allHome
                resultGame.friendSoccer = onegame.allFriend
                # 赋值结束
                onegame.halfHome = int(oneGameArray[9])
                onegame.halfFriend = int(oneGameArray[10])

                if oneGameArray[15] != '' and oneGameArray[15] is not None:
                    onegame.bet365Handi = float(oneGameArray[15])
            except ValueError as e:
                onegame = None
                print  e

            except BaseException, e:
                onegame = None
                print e
            else:
                AllGames.append(onegame)
                # 比赛结果模型 添加到数组
                AllResultAnalyseGames.append(resultGame)
                # 赋值结束

                onegame.oddCompanies = getOneGameODD(onegame)
                onegame.handiCompanies = getOneGameHandi(onegame)
                getHandiDisunion(onegame)
                # handiOffset = onegame.now_aomenHandi - onegame.orignal_aomenHandi
                # if handiOffset == 0:
                #     resultGame.handiDeeper = 0
                # else:
                #     resultGame.handiDeeper = 1

                # 比赛结果模型 比赛结果赋值
                # offset = onegame.allHome - onegame.allFriend - onegame.now_aomenHandi
                # if offset == 0:
                #     resultGame.resultHandi = 1
                # elif offset > 0:
                #     resultGame.resultHandi = 3
                # else:
                #     resultGame.resultHandi = 0
                #
                # if onegame.allHome == onegame.allFriend:
                #     resultGame.resultOdd = 1
                # elif onegame.allHome > onegame.allFriend:
                #     resultGame.resultOdd = 3
                # else:
                #     resultGame.resultOdd = 0
                # 赋值结束

                # titlestr = ''.join(
                #     [str(onegame.beginTime), ':', onegame.leauge, ':', onegame.homeTeam, 'vs', onegame.friendTeam,
                #      ' id: ',
                #      str(onegame.soccerID), '澳盘: ', str(onegame.orignal_aomenHandi), ' -> ',
                #      str(onegame.now_aomenHandi)])
                # contentStr += "<h3 style=\"color:red;\">%s</h3>" % (titlestr,)

                # 获取开盘时间
                # flag = getHandiOrignalTime.gethandiTime(onegame.soccerID)
                # if flag:
                    # contentStr += '澳盘开盘早\n'.join([str(onegame.beginTime), ':', onegame.leauge, ':', onegame.homeTeam, 'vs', onegame.friendTeam])
                    # contentStr += "<h4 style=\"color:red;\" align=\"center\">澳盘开盘早</h4>"
                    # resultGame.AomenFirst = 1
                # 获取初始盘口数量
                # if len(onegame.orignalHandiList) > 2:
                #     contentStr += "<h4 style=\"color:red;\" align=\"center\">初盘混乱</h4>"
                #     resultGame.orignalHandiconfusion = 1
                    # contentStr += '初盘混乱\n'
                    # contentStr += ''.join(
                    #     [str(onegame.beginTime), ':', onegame.leauge, ':', onegame.homeTeam, 'vs', onegame.friendTeam])

                # contentStr += "<table bgcolor=\"black\"cellspacing=\"1px\"width=\"375px\" align=\"center\">" \
                #               "<caption style=\"color:red;\"><h5>亚盘</h5></caption><tr bgcolor=#663399><th>博彩公司</th><th>盘口</th><th>数量</th><th>赢盘</th><th>走盘</th><th>输盘</th><th>胜</th><th>平</th><th>负</th></tr> "
                # tempHandistr = getHandiProbability(onegame, False, resultGame)
                # if tempHandistr is not None:
                #     contentStr += tempHandistr
                    # contentStr += '\n'

                # tempNowHandistr = getnowHandiProbability(onegame, False, resultGame)
                # if tempNowHandistr is not None:
                #     contentStr += tempNowHandistr
                #
                # contentStr += '</table>'
                # contentStr += "<table bgcolor=\"black\"cellspacing=\"1px\"width=\"375px\" align=\"center\"><caption style=\"color:red;\"><h5>欧赔</h5></caption>" \
                #               "<tr bgcolor=\"white\" ><td>博彩公司</td> <td>数量</td><td>胜</td><td>平</td><td>负</td><td>胜率</td><td>平率</td><td>负率</td>"
                # tempOddstr = getOrignalODDProbability(onegame, False, resultGame)
                # if tempOddstr is not None:
                #     contentStr += tempOddstr
                    # contentStr += '\n'

                # tempNowOddstr = getnowODDProbability(onegame, False, resultGame)
                # if tempNowOddstr is not None:
                #     contentStr += tempNowOddstr
                # contentStr += '</table>'
                #
                # time.sleep(3)

                # Ori_Handi_result = getHandiProbability(onegame,True)
                # Now_Handi_result = getnowHandiProbability(onegame,True)
                # Ori_Odd_result = getOrignalODDProbability(onegame,True)
                # Now_Odd_result = getnowODDProbability(onegame,True)
                #
                # result_locationstr = os.path.join('/Users/mi/Desktop', '%s-result.txt' % (timestr,))
                # result_leaguelistfile = open(result_locationstr, 'a')
                #
                # if onegame.allHome - onegame.allFriend - onegame.now_aomenHandi > 0:
                #     result = '赢'
                # elif onegame.allHome - onegame.allFriend - onegame.now_aomenHandi == 0:
                #     result = '输'
                # else:
                #     result = '走'

                # if (len(onegame.nowHandiList) > 1):
                #     result_leaguelistfile.write('%s: %s %s vs %s %d:%d 盘口:%s 澳初:%s 即:%s %s\n' %
                #                                 (onegame.beginTime, onegame.leauge, onegame.homeTeam,
                #                                  onegame.friendTeam, onegame.allHome, onegame.allFriend,
                #                                  str(onegame.nowHandiList), str(onegame.orignal_aomenHandi),
                #                                  str(onegame.now_aomenHandi), result
                #                                  ))

            time.sleep(1.5)

            # insertGameList(AllGames)
            # insert_Result_Analyse_list(AllResultAnalyseGames)

            # i = datetime.now()
            # send_mail("%s %s/%s/%s" % ('往日比赛分析', i.year, i.month, i.day), contentStr, 'html')

def main():
    now = datetime.datetime.now()
    aDay = datetime.timedelta(days=-1)
    now = now + aDay
    yesterdaystr = now.strftime('%Y-%m-%d')

    getYesterdaySoccer(yesterdaystr)



# if sys.argv.__len__()==1:
#     sys.exit('\033[0;36;40m使用说明:\n1个参数:\n1:精简足球分析   2:十四场足球分析  3:竞彩分析\n事例: python TodaySoccer.pyc 1\033[0m')
#
if __name__ == '__main__':
#     getTodaySoccer(sys.argv[1])
    getTodaySoccer(3)
# getYesterdaySoccer('2017-11-10')