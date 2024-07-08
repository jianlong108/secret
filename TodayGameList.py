#!/usr/bin/env python
# -*- coding: utf-8 -*-


from GetData.SOCCER_MODELS import FootballGame,BetCompany
from colorama import Fore,init
import requests
import time
from numpy import *
from GetData.GET_GAME_PAN_ODD_DATA import getOneGameHandiList,getOneGameOddList
from SendMail import MailHelper
from GetData.TIME_TOOL import get_current_timestr_YMDHms

'''
找出今天澳*最早开盘的比赛
response.text：
欧冠杯^103^1^^53^欧洲赛事^192
!英冠^37^1^^1^英格兰^1
!意乙^40^1^^2^意大利^2
!法乙^12^1^^5^法国^5
!苏超^29^1^^7^苏格兰^7
!阿甲^2^1^^38^阿根廷^49
!巴西甲^4^1^^39^巴西^50
!亚冠杯^192^1^^56^亚洲赛事^193
!英甲^39^1^^1^英格兰^1
!英乙^35^1^^1^英格兰^1
!亚协杯^350^1^^56^亚洲赛事^193
!苏冠^150^1^^7^苏格兰^7
!俄杯^153^1^^18^俄罗斯^18
!威超^135^1^^30^威尔士^29
!乌拉甲^240^1^^40^乌拉圭^51
!埃及超^303^1^^70^埃及^74
!阿尔巴超^315^1^^60^阿尔巴尼亚^66
!南非超^308^1^^99^南非^100
!摩洛超^321^1^^74^摩洛哥^78
!阿美超^469^1^^91^阿美尼亚^41
!格鲁甲^563^1^^96^格鲁吉亚^46
!玻利甲^593^1^^80^玻利维亚^84
!肯尼超^1456^1^^117^肯尼亚^117
!牙买超^1409^1^^114^牙买加^114

$$2464791^192^0^20231128180000^^仁川联队^横滨水手^0^0^^^0^0^0^0^0^^^0^6^2^^^0^0^0^0^1^^0^0^2.5^10^56^1^1^0^^^497^196
!2464792^192^0^20231128180000^^川崎前锋^柔佛^0^0^^^0^0^0^0^1.25^^^0^9^1^^^0^0^0^0^1^^0^0^3^8.5^56^1^1^0^^^1989^3629
!2464793^192^0^20231128180000^^巴吞联^蔚山现代^0^0^^^0^0^0^0^-0.75^^^0^2^1^^^0^0^0^0^1^^0^0^3^9^56^1^1^0^^^9960^480
'''

init(autoreset=True)


def getTodaySoccer(soccer_type = 0):
    typeStr = ''
    if isinstance(soccer_type,int):
        typeStr = str(soccer_type)
    # type == 3 竞彩
    # type == 1 精简
    # type == 2 十四场
    # url = "http://61.143.224.166:8071/phone/schedule_0_" + typeStr + ".txt?an=iosQiuTan&av=2.4&from=2&r=" + str(int(time.time()))
    # url = "http://112.91.160.49:8071/phone/schedule_0_" + str(type) + ".txt?an=iosQiuTan&av=5.9&from=2&r=1494229747"

    # http://txt.letarrow.com/phone/schedule_0_1.txt?from=48&_t=1701143016
    url = f"http://txt.letarrow.com/phone/schedule_0_{typeStr}.txt?from=48&_t={str(int(time.time()))}"
    # print(url)

    headers = {
        'User-Agent': 'QTimesApp/3.4 (Letarrow.QTimes; build:42; iOS 17.5.1) Alamofire/5.4.3',
        'cookie': 'aiappfrom=48'
    }
    response = requests.get(url,headers=headers)
    if response.ok:
        resultStr = response.content.decode('utf-8')
    print(resultStr)

    if resultStr != '':

        allArray = resultStr.split('$$')
        if soccer_type == 1:
            leagueStr = allArray[0]
        else:
            leagueStr = allArray[1]

        allLeague = leagueStr.split('!')
        dic = {}
        for league in allLeague:
            oneLeague = league.split('^')
            dic[oneLeague[1]] = oneLeague[0]

        if soccer_type == 1:
            gameStr = allArray[1]
        else:
            gameStr = allArray[2]

        games = gameStr.split('!')
        # 2464792^192^0^20231128180000^^川崎前锋^柔佛^0^0^^^0^0^0^0^1.25^^^0^9^1^^^0^0^0^0^1^^0^0^3^8.5^56^1^1^0^^^1989^3629
        # 比赛^联赛^是否开赛^开赛日期

        # time_s = time.strptime('201809301100', '%Y%m%d%H%M')
        # time.struct_time(tm_year=2018, tm_mon=9, tm_mday=30, tm_hour=11, tm_min=0, tm_sec=0, tm_wday=6, tm_yday=273, tm_isdst=-1) 1538276400.0
        # print(time_s, time.mktime(time_s))
        # 2018-09-30 11:00:00
        # print(time.strftime("%Y-%m-%d %H:%M:%S", time_s))
        mailBody = ""
        for game in games:
            # if game is not firstobject:
            #     continue;
            gameobj = FootballGame()
            oneGameArray = game.split('^')
            oneGameArray.remove('')

            teamidlist = game.split('^^^')
            teamidstr = teamidlist[-1]
            teamid_str_list = teamidstr.split('^')
            gameobj.homeTeamId = int(teamid_str_list[0])
            gameobj.friendTeamId = int(teamid_str_list[1])
            gameing = int(oneGameArray[2])
            if gameing != 0:
                continue
            gameobj.soccerID = int(oneGameArray[0])
            gameobj.leauge = dic.get(oneGameArray[1])
            gameobj.leaugeid = oneGameArray[1]
            beginTime_str = oneGameArray[3]
            time_stru = time.strptime(beginTime_str, '%Y%m%d%H%M%S')
            gameobj.beginTime = time.strftime("%Y-%m-%d %H:%M:%S", time_stru)
            gameobj.beginTimestamp = time.mktime(time_stru)

            if oneGameArray[4].isdigit() or oneGameArray[4] == '':
                gameobj.homeTeam = oneGameArray[5]
                gameobj.friendTeam = oneGameArray[6]
            else:
                gameobj.homeTeam = oneGameArray[4]
                gameobj.friendTeam = oneGameArray[5]

            # print(f"ID:{gameObj.soccerID} 时间:{gameObj.beginTime} 联赛:{gameObj.leauge} 主队:id:{gameObj.homeTeamId} {gameObj.homeTeam} 客队:id:{gameObj.friendTeamId} {gameObj.friendTeam}")
            getOneGameHandiList(gameobj)

            if not gameobj.haveAomen:
                continue
            can_insert_db = False
            print('---------')
            if gameobj.handiIsFilp:
                mailBody += f"盘口翻转:{gameobj}"
                mailBody += "\n"
                mailBody += "\n"
                print(Fore.GREEN + f"盘口翻转:{gameobj}")
                can_insert_db = True
            if gameobj.earlyestCompany is not None and gameobj.earlyestCompany.companyID == '1':
                print(Fore.YELLOW + f"澳盘开盘早:{gameobj.earlyestCompany}")
                mailBody += f"澳盘开盘早:{gameobj.earlyestCompany}"
                mailBody += "\n"
                mailBody += "\n"
                can_insert_db = True

            # if len(gameobj.orignalHandiList) > 2:
            if len(gameobj.fix_orignalHandiList) > 2:
                print(gameobj.fix_orignalHandiList)
                for company in gameobj.yapanCompanies:
                    mailBody += f"name:{company.companyTitle} {company.early_fix_change}"
                    mailBody += "\n"

                if gameobj.maxHandiCompany.companyID != '1' and mean(gameobj.orignalHandiList) > mean(
                        gameobj.nowHandiList):
                    mailBody += f"初盘混乱 后续降盘 澳盘不是最大盘 出下盘:{gameobj}"
                    mailBody += "\n"
                    mailBody += "\n"
                    print(Fore.BLUE + f"初盘混乱 后续降盘 澳盘不是最大盘 出下盘:{gameobj}")
                    can_insert_db = True

                if gameobj.maxHandiCompany.companyID != '1' and mean(gameobj.orignalHandiList) < mean(
                        gameobj.nowHandiList):
                    mailBody += f"初盘混乱 后续升盘 澳盘不是最大盘  出下盘, {gameobj}"
                    mailBody += "\n"
                    mailBody += "\n"
                    print(Fore.BLUE + f"初盘混乱 后续升盘 澳盘不是最大盘  出下盘, {gameobj}")
                    can_insert_db = True
            if can_insert_db:
                if gameobj.now_aomenHandi > 0 and gameobj.now_aomenHandi > gameobj.orignal_aomenHandi:
                    mailBody += f"澳门终盘主队强，且澳门升盘：{gameobj}"
                    mailBody += "\n"
                    mailBody += "\n"
                    print(Fore.RED + f"澳门终盘主队强，且澳门升盘：{gameobj}")
            time.sleep(3)
            oddmailstr = getOneGameOddList(gameobj)
            if oddmailstr != "":
                mailBody += oddmailstr
            time.sleep(3)
        if mailBody != "":
            mailobj = MailHelper()
            mailobj.sendMailWithPlainText(get_current_timestr_YMDHms(), mailBody)

if __name__ == '__main__':
    getTodaySoccer(1)