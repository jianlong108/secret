#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
# from urllib2 import request
import requests

import re
from SoccerGame import SoccerGame
import HtmlParser
import datetime
import calendar




class GetURL:
    usedurl = ''
    html = ''
    def __init__(self,url):
        self.usedurl = url
        self.html = self.download(url)

    def download(self,url):
        print("downloading", url)

        # try:
        #     # html = requests.urlopen(url).read()
        #     html = requests.get(url)
        #     print(html)
        # except requests.URLError as e:
        #     print("download error")
        #     html = None
        html = requests.get(url)
        return html.content

    def getHtmlListWithLabel(self, label, options={}):
        soup = BeautifulSoup(self.html,"html.parser",from_encoding='gb18030')
        trList = []
        tr_ni = soup.find_all(label,attrs=options)
        trList.extend(tr_ni)
        return trList

    def filterList(self,list,label):
        tempList = []
        tempList.extend(list)
        for ele in list:
            value = str(ele).find(label)
            if value<0:
                tempList.remove(ele)

        return tempList

    def creatImageUrlList(self,list):
        imgList = []
        for imgLabel in list:
            imgLabel_str = str(imgLabel)
            src = re.findall('[a-zA-z]+://[^\s]*jpg', imgLabel_str)
            # elementmodel = SoccerGame.ElementModel(getRangeWithStr(imgLabel_str,'alt="','"'),src)
            # imgList.append(elementmodel)

        return imgList

def main():
    date_list = []
    begin_date = datetime.datetime.strptime("2017-05-09", "%Y-%m-%d")
    end_date = datetime.datetime.strptime("2017-05-09", "%Y-%m-%d")
    while begin_date <= end_date:
        date_str = begin_date.strftime("%Y-%m-%d")
        date_list.append(date_str)
        begin_date += datetime.timedelta(days=1)

    for dateStr in date_list:
        print dateStr
        url = "http://www.310win.com/buy/JingCai.aspx?typeID=105&oddstype=2&date=" + dateStr
        instance = GetURL(url)
        # HtmlParser.create_database()
        # imgList = instance.getHtmlListWithLabel('a')
        # newImgList = instance.filterList(imgList, '>亚<')
        gameList = instance.getHtmlListWithLabel('table', {'class': 'socai'})
        table = gameList[0]
        allGameList = []
        for tr in table.children:
            if str(type(tr)) == "<class 'bs4.element.Tag'>":
                if tr.get('id') != None:
                    # print(tr.get('gamename'))
                    game = SoccerGame('http://www.310win.com/')
                    game.leauge = tr.get('gamename')
                    for td in tr.descendants:
                        if str(type(td)) == "<class 'bs4.element.Tag'>":
                            # print(td)
                            if td.get('onmouseout') == "hide('WinOdds')":
                                # print(td.get_text())
                                game.soccer = td.get_text()
                            elif td.get_text() == u'亚':
                                # print(td.get('href'))
                                game.url = game.url + td.get('href')
                    allGameList.append(game)
                    # print(game.leauge,game.soccer,game.url)

        for soccer in allGameList:
            soccer.parserHtml()
            soccer.beginCaculte()




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
