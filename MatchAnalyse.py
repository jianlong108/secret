#!/usr/bin/env python
# -*- coding: utf-8 -*-

from SoccerGame import SoccerGame
import datetime
import BEAUTIFUL_SOUP_HELPER
import time
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

'''
根据指定日期 获取每个公司的历史盘口胜率
'''

def main():
    date_list = []
    begin_date = datetime.datetime.strptime("2017-08-25", "%Y-%m-%d")
    end_date = datetime.datetime.strptime("2017-08-25", "%Y-%m-%d")
    # print begin_date,end_date.__class__

    while begin_date <= end_date:
        date_str = begin_date.strftime("%Y-%m-%d")
        date_list.append(date_str)
        begin_date += datetime.timedelta(days=1)


    for dateStr in date_list:
        url = "http://www.310win.com/buy/JingCai.aspx?typeID=105&oddstype=2&date=" + dateStr
        print url
        instance = BEAUTIFUL_SOUP_HELPER.SoupHelper(url)
        matchtable = instance.gethtmllistwithlabel('table', {'id': 'MatchTable'})
        # matchtable 类型是数组类型
        table = matchtable[0]
        allGameList = []
        for tr in table.children:
            if BEAUTIFUL_SOUP_HELPER.isTagClass(tr):
                if tr.get('matchid') is not None:
                    game = SoccerGame('http://www.310win.com')
                    game.leauge = tr.get('gamename').encode('utf-8')

                    if BEAUTIFUL_SOUP_HELPER.getelementlistwithlabel(tr, 'a', {'id': True}):
                        alist = BEAUTIFUL_SOUP_HELPER.getelementlistwithlabel(tr, 'a')
                        game.hometeam = alist[1].get_text().encode('utf-8')
                        home_a_id = alist[1].get('id').encode('utf-8')
                        game.matchid = (home_a_id.split('_')[1]).encode('utf-8')
                        game.guestteam = alist[2].get_text().encode('utf-8')

                    for td in tr.descendants:
                        if BEAUTIFUL_SOUP_HELPER.isTagClass(td):



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


        for game in allGameList:
            if isinstance(game, SoccerGame):
                print(game.soccer,game.hometeam,game.guestteam,game.matchid)
                game.gethandidata()
                time.sleep(1.5)





if __name__ == "__main__":
    main()
    # pass
