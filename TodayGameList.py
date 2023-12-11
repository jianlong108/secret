#!/usr/bin/env python
# -*- coding: utf-8 -*-


from GetData.SOCCER_MODELS import FootballGame,BetCompany
from colorama import Fore,init
import requests
from lxml import etree
import time
from numpy import *
import math
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

# result1=html.xpath('//li[@class="item-1"]//text()') #获取li下所有子孙节点的内容
# result=html.xpath('//li/a/@href')  #获取a的href属性
def gethandiTime(gameObj):
    if not isinstance(gameObj, FootballGame):
        print("传参不正确", gameObj.__class__.__name__)
        return
    # url = 'http://www.310win.com/info/1x2exchange.aspx?id=' + str(soccerid) + '&cids=,' + str(companyid) + ',&type=3'
    # url = 'http://www.310win.com/handicap/' + str(soccerid) + '.html'
    # http://www.310win.com/handicap/2478509.html
    url = f"https://vip.titan007.com/AsianOdds_n.aspx?id={gameObj.soccerID}"
    HEADERS = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
    }
    webpage = requests.get(url, headers=HEADERS)
    webpage.encoding = 'utf-8'
    # soup = BeautifulSoup(webpage.content, "html.parser")
    dom = etree.HTML(webpage.text)
    table_dom = dom.xpath('//table[@id="odds"]')[0]
    # print(type(table_dom), table_dom)
    tr_list = table_dom.xpath('//tr')
    companies = []
    earlyest_timestamp = 0
    earlyest_company = None
    ori_pan_list = []
    now_pan_list = []
    max_handi = 0.0
    max_company = None

    min_handi = 0.0
    min_company = None

    #一般第一个公司就是澳门，判断如果第一个不是澳门 代表澳门没有开盘
    firstCompany = None
    for tr_dom in tr_list:
        #真TMB坑，需要加个点 https://blog.csdn.net/weixin_44749897/article/details/93637740
        span_dom_right = tr_dom.xpath('.//td[2]/span/@companyid')
        if span_dom_right is not None and len(span_dom_right) > 0:
            # print(type(span_dom_right), span_dom_right)
            name = tr_dom.xpath('.//td[1]//text()')[0]
            # name = [str(s) for s in name]
            name = ''.join([str(s) for s in name])
            companyid = tr_dom.xpath('.//td[2]/span/@companyid')[0]
            companyid = ''.join([str(s) for s in companyid])

            oriTime = tr_dom.xpath('.//td[3]/@title')[0]
            oriTime = ''.join([str(s) for s in oriTime])

            orihomeshui = tr_dom.xpath('.//td[3]//text()')[0]
            orihomeshui = ''.join([str(s) for s in orihomeshui])

            oripan = tr_dom.xpath('.//td[4]/@goals')[0]
            oripan = ''.join([str(s) for s in oripan])

            oriawayshui = tr_dom.xpath('.//td[5]//text()')[0]
            oriawayshui = ''.join([str(s) for s in oriawayshui])


            nowhomeshui = tr_dom.xpath('.//td[6]//text()')[0]
            nowhomeshui = ''.join([str(s) for s in nowhomeshui])

            nowpan = tr_dom.xpath('.//td[7]/@goals')[0]
            nowpan = ''.join([str(s) for s in nowpan])

            nowawayshui = tr_dom.xpath('.//td[8]//text()')[0]
            nowawayshui = ''.join([str(s) for s in nowawayshui])
            company = BetCompany(p_gameid=gameObj.soccerID, p_companyid=companyid)
            if firstCompany is None:
                firstCompany = company
                if companyid != '1':
                    gameObj.haveAomen = False
                    return
            company.companyTitle = name
            time_s = time.strptime(oriTime, '%Y-%m-%d %H:%M')
            company.oriTimeStr = oriTime
            company.oriTimeStamp = time.mktime(time_s)
            if earlyest_company is None:
                earlyest_company = company
                earlyest_timestamp = company.oriTimeStamp

            if earlyest_company is not None and company.oriTimeStamp < earlyest_timestamp:
                earlyest_timestamp = company.oriTimeStamp
                earlyest_company = company

            company.orignal_Handicap = float(oripan)
            company.orignal_top = orihomeshui
            company.orignal_bottom = oriawayshui
            company.now_Handicap = float(nowpan)
            if max_company is None:
                max_company = company
                max_handi = float(oripan)
            if max_company is not None and math.fabs(float(oripan)) > math.fabs(max_handi):
                max_handi = float(oripan)
                max_company = company

            if min_company is None:
                min_company = company
                min_handi = float(oripan)
            if min_company is not None and math.fabs(float(oripan)) < math.fabs(min_handi):
                min_handi = float(oripan)
                min_company = company

            if float(oripan) not in ori_pan_list:
                ori_pan_list.append(float(oripan))

            if float(nowpan) not in now_pan_list:
                now_pan_list.append(float(nowpan))
            company.flip = (float(nowpan) * float(oripan)) < 0
            company.now_top = nowhomeshui
            company.now_bottom = nowawayshui
            company.similerMatchURL = f"https://vip.titan007.com/history/SearchSameAsian.aspx?id={gameObj.soccerID}&companyid={companyid}&l=0&goal={oripan}"
            company.allSamePanURL = f"https://vip.titan007.com/count/goalCount.aspx?t=1&sid={gameObj.soccerID}&cid=1&l=0"
            company.trendURL = f"https://vip.titan007.com/changeDetail/handicap.aspx?id={gameObj.soccerID}&companyID={companyid}&l=0"
            company.homeSamePanURL = f"https://vip.titan007.com/history/SearchAsianByTeamID.aspx?id={gameObj.soccerID}&companyid={companyid}&l=0&teamid={gameObj.homeTeamId}"
            company.similerMatchURL = f"https://vip.titan007.com/history/SearchAsianByTeamID.aspx?id={gameObj.soccerID}&companyid={companyid}&l=0&teamid={gameObj.friendTeamId}"
            companies.append(company)
            # print(name, type(name),companyid, type(companyid), oriTime, type(oriTime), orihomeshui, type(orihomeshui), oripan, type(oripan),oriawayshui, type(oriawayshui),nowhomeshui, type(nowhomeshui),nowpan, type(nowpan),nowawayshui,type(nowawayshui))
            # company.print_self()
    if earlyest_company:
        earlyest_company.earlyest = True
        gameObj.earlyestCompany = earlyest_company
    gameObj.yapanCompanies = companies
    gameObj.orignalHandiList = ori_pan_list
    gameObj.nowHandiList = now_pan_list
    gameObj.maxHandi = max_handi
    gameObj.maxHandiCompany = max_company
    gameObj.minHandi = min_handi
    gameObj.minHandiCompany = min_company


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
        'User-Agent': 'QTimesApp/3.0 (Letarrow.QTimes; build:39; iOS 17.1.0) Alamofire/5.4.',
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
                # print "比赛已经开始或结束"
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
            gethandiTime(gameobj)
            if not gameobj.haveAomen:
                continue
            can_insert_db = False
            print('---------')
            if gameobj.handiIsFilp:
                print(Fore.GREEN + "盘口翻转",gameobj)
                can_insert_db = True
            if gameobj.earlyestCompany is not None and gameobj.earlyestCompany.companyID == '1':
                print(Fore.YELLOW + "澳盘开盘早", gameobj.earlyestCompany)
                can_insert_db = True

            if len(gameobj.orignalHandiList) > 2:
                if gameobj.maxHandiCompany.companyID != '1' and mean(gameobj.orignalHandiList) > mean(
                        gameobj.nowHandiList):
                    print(Fore.BLUE + "初盘混乱 后续降盘 澳盘不是最大盘", gameobj)
                    can_insert_db = True

                if gameobj.maxHandiCompany.companyID != '1' and mean(gameobj.orignalHandiList) < mean(
                        gameobj.nowHandiList):
                    print(Fore.BLUE + "初盘混乱 后续升盘 澳盘不是最大盘", gameobj)
                    can_insert_db = True
            if can_insert_db:
                if gameobj.now_aomenHandi > 0 and gameobj.now_aomenHandi > gameobj.orignal_aomenHandi:
                    print(Fore.RED + gameobj)
            time.sleep(5)


if __name__ == '__main__':
    getTodaySoccer(1)