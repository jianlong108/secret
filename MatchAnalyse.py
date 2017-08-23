#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import re
from SoccerGame import SoccerGame
import datetime
import BeautifulSoupHelper
import time

def main():
    date_list = []
    begin_date = datetime.datetime.strptime("2017-08-22", "%Y-%m-%d")
    end_date = datetime.datetime.strptime("2017-08-22", "%Y-%m-%d")
    # print begin_date,end_date.__class__

    while begin_date <= end_date:
        date_str = begin_date.strftime("%Y-%m-%d")
        date_list.append(date_str)
        begin_date += datetime.timedelta(days=1)


    for dateStr in date_list:
        url = "http://www.310win.com/buy/JingCai.aspx?typeID=105&oddstype=2&date=" + dateStr
        print url
        instance = BeautifulSoupHelper.SoupHelper(url)
        matchtable = instance.gethtmllistwithlabel('table', {'id': 'MatchTable'})
        # matchtable 类型是数组类型
        table = matchtable[0]
        allGameList = []
        for tr in table.children:
            if BeautifulSoupHelper.isTagClass(tr):
                if tr.get('matchid') is not None:
                    game = SoccerGame('http://www.310win.com')
                    game.leauge = tr.get('gamename').encode('utf-8')

                    for td in tr.descendants:
                        if BeautifulSoupHelper.isTagClass(td):

                            if td.get('onmouseout') == "hide('WinOdds')":
                                # 获得比分
                                game.soccer = td.get_text().encode("UTF-8")
                            elif td.get_text().encode("UTF-8") == '亚':
                                # 获得比赛的亚盘 分析地址
                                game.handiurl = game.url + td.get('href').encode("UTF-8")
                            elif td.get_text().encode("UTF-8") == '欧':
                                # 获得比赛的欧赔 分析地址
                                game.oddurl = game.url + td.get('href').encode("UTF-8")
                    allGameList.append(game)


        # game = allGameList[0]
        for game in allGameList:
            if isinstance(game, SoccerGame):
                print(game.soccer)
                game.gethandidata()
                time.sleep(0.5)


            # game.getodddata()
        # for soccer in allGameList:
        #     soccer.parserHtml()
        #     soccer.beginCaculte()


    # urllist = []
    # for a in newImgList:
    #     print(a)
    #     match = re.findall(r'(/[^# ]*html)', str(a))
    #     url = 'http://www.310win.com/' + match[0]
    #     urllist.append(url)
    #     soup = BeautifulSoup(HtmlParser.download(url), 'html.parser')
    #     list = soup.find_all('tr')
    #
    # soccerList = []
    # for url in urllist:
    #     soccer = SoccerGame(url)
    #     soccer.parserHtml()
    #     soccer.beginCaculte()
    #     soccer.canSaveLocal()
    #     soccerList.append(soccer)



if __name__ == "__main__":
    main()
    # pass
