#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import datetime
import time
import SoccerOrignalPanTime
from GetData.DBHELPER import (ResultAnalyseGame,getHandiProbability,getOrignalODDProbability,
                              getnowODDProbability,getnowHandiProbability)
from NetWorkTools import get_resultstr_with_url
from SOCCER_MODELS import FootballGame
from GetData.SOCCER_ROUND import getOneGameODD,getOneGameHandi




"""
全局变量定义
"""

AllGames = []
AllResultAnalyseGames = []
AllBeginTimes = []

'''
主函数
'''
def getYesterdaySoccer(timestr):
    url = ''
    try:
        url = "http://61.143.225.85:8072/phone/scheduleByDate.aspx?an=iosQiuTan&av=6.4&date=" + timestr + '&from=1&kind=3&r=1503367511&subversion=3'
# http://61.143.225.85:8072/phone/scheduleByDate.aspx?an=iosQiuTan&av=6.5&date=2018-08-21&from=2&kind=0&r=1535094647&subversion=2
        print url
    except BaseException as e:
        print e
        pass

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
            # leaguelistfile.write('%s:%s\n'%(oneLeague[1],oneLeague[0]))
        leaguelist = leaguelistfile.readlines()
        # return
        if type == 1:
            gameStr = allArray[1]
        else:
            gameStr = allArray[2]

        games = gameStr.split('!')
        contentStr = "<!DOCTYPE html><html lang=\"en\"><head><meta charset=\"UTF-8\"><title>初盘预测</title></head><body>"

        for game in games:
            tempstr_utf_8 =  game.encode('utf-8')
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

                if flag is False:
                    continue

                beginTime = oneGameArray[3].encode('utf-8')
                onegame.beginTime = beginTime[0:4] + '-' + beginTime[4:6] + '-' + beginTime[6:8] + ' ' + beginTime[8:10] + ':' + beginTime[10:12]
                # 比赛结果模型 赋值开赛时间
                resultGame.beginTime = onegame.beginTime
                # 赋值结束

                briefTimeStr = beginTime[0:4] + '-' + beginTime[4:6] + '-' + beginTime[6:8] + ' ' + beginTime[8:10] + ':' + beginTime[10:12]
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
                handiOffset = onegame.now_aomenHandi - onegame.orignal_aomenHandi
                if handiOffset == 0:
                    resultGame.handiDeeper = 0
                else:
                    resultGame.handiDeeper = 1


                # 比赛结果模型 比赛结果赋值
                offset = onegame.allHome - onegame.allFriend - onegame.now_aomenHandi
                if offset == 0:
                    resultGame.resultHandi = 1
                elif offset > 0:
                    resultGame.resultHandi = 3
                else:
                    resultGame.resultHandi = 0

                if onegame.allHome == onegame.allFriend:
                    resultGame.resultOdd = 1
                elif onegame.allHome > onegame.allFriend:
                    resultGame.resultOdd = 3
                else:
                    resultGame.resultOdd = 0
                # 赋值结束

                titlestr = ''.join(
                    [str(onegame.beginTime), ':', onegame.leauge, ':', onegame.homeTeam, 'vs', onegame.friendTeam,
                     ' id: ',
                     str(onegame.soccerID), '澳盘: ', str(onegame.orignal_aomenHandi), ' -> ',
                     str(onegame.now_aomenHandi)])
                contentStr += "<h3 style=\"color:red;\">%s</h3>" % (titlestr,)

                # 获取开盘时间
                flag = SoccerOrignalPanTime.gethandiTime(onegame.soccerID)
                if flag:
                    # contentStr += '澳盘开盘早\n'.join([str(onegame.beginTime), ':', onegame.leauge, ':', onegame.homeTeam, 'vs', onegame.friendTeam])
                    contentStr += "<h4 style=\"color:red;\" align=\"center\">澳盘开盘早</h4>"
                    resultGame.AomenFirst = 1
                # 获取初始盘口数量
                if len(onegame.orignalHandiList) > 2:
                    contentStr += "<h4 style=\"color:red;\" align=\"center\">初盘混乱</h4>"
                    resultGame.orignalHandiconfusion = 1
                    # contentStr += '初盘混乱\n'
                    # contentStr += ''.join(
                    #     [str(onegame.beginTime), ':', onegame.leauge, ':', onegame.homeTeam, 'vs', onegame.friendTeam])

                contentStr += "<table bgcolor=\"black\"cellspacing=\"1px\"width=\"375px\" align=\"center\">" \
                              "<caption style=\"color:red;\"><h5>亚盘</h5></caption><tr bgcolor=#663399><th>博彩公司</th><th>盘口</th><th>数量</th><th>赢盘</th><th>走盘</th><th>输盘</th><th>胜</th><th>平</th><th>负</th></tr> "
                tempHandistr = getHandiProbability(onegame,False,resultGame)
                if tempHandistr is not None:
                    contentStr += tempHandistr
                    # contentStr += '\n'

                tempNowHandistr = getnowHandiProbability(onegame,False,resultGame)
                if tempNowHandistr is not None:
                    contentStr += tempNowHandistr

                contentStr += '</table>'
                contentStr += "<table bgcolor=\"black\"cellspacing=\"1px\"width=\"375px\" align=\"center\"><caption style=\"color:red;\"><h5>欧赔</h5></caption>" \
                              "<tr bgcolor=\"white\" ><td>博彩公司</td> <td>数量</td><td>胜</td><td>平</td><td>负</td><td>胜率</td><td>平率</td><td>负率</td>"
                tempOddstr = getOrignalODDProbability(onegame,False,resultGame)
                if tempOddstr is not None:
                    contentStr += tempOddstr
                    # contentStr += '\n'

                tempNowOddstr = getnowODDProbability(onegame,False,resultGame)
                if tempNowOddstr is not None:
                    contentStr += tempNowOddstr
                contentStr += '</table>'

                time.sleep(3)



                # Ori_Handi_result = getHandiProbability(onegame,True)
                # Now_Handi_result = getnowHandiProbability(onegame,True)
                # Ori_Odd_result = getOrignalODDProbability(onegame,True)
                # Now_Odd_result = getnowODDProbability(onegame,True)
                #
                result_locationstr = os.path.join('/Users/mi/Desktop', '%s-result.txt' % (timestr,))
                result_leaguelistfile = open(result_locationstr, 'a')

                if onegame.allHome - onegame.allFriend - onegame.now_aomenHandi > 0:
                    result = '赢'
                elif onegame.allHome - onegame.allFriend - onegame.now_aomenHandi == 0:
                    result = '输'
                else:
                    result = '走'

                if len(onegame.nowHandiList) > 1:
                    result_leaguelistfile.write('%s: %s %s vs %s %d:%d 盘口:%s 澳初:%s 即:%s %s\n'%
                                                (onegame.beginTime, onegame.leauge ,onegame.homeTeam,
                                                 onegame.friendTeam,onegame.allHome,onegame.allFriend,
                                                 str(onegame.nowHandiList),str(onegame.orignal_aomenHandi),
                                                 str(onegame.now_aomenHandi),result
                                                                                                                  ))


            time.sleep(1.5)

        # insertGameList(AllGames)
        # insert_Result_Analyse_list(AllResultAnalyseGames)

        # i = datetime.now()
        # send_mail("%s %s/%s/%s" % ('往日比赛分析', i.year, i.month, i.day), contentStr, 'html')


def main():
    days = 365
    while days > 0:
        now = datetime.datetime.strptime('2018-08-21', '%Y-%m-%d')
        aDay = now - datetime.timedelta(days=days)

        aDaystr = aDay.strftime('%Y-%m-%d')
        getYesterdaySoccer(aDaystr)
        days -= 1


if __name__ == '__main__':
    main()

