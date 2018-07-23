#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from urllib2 import Request
import re
from SoccerGame import SoccerGame
import datetime





class GetURL:
    usedurl = ''
    html = ''
    def __init__(self,url):
        self.usedurl = url
        self.html = self.download(url)

    def download(self,url):
        print("downloading", url)
        try:
            html = Request.urlopen(url).read()
        except Request.URLError as e:
            print("download error")
            html = None
        return html

    def getHtmlListWithLabel(self, label):
        soup = BeautifulSoup(self.html, "html.parser")
        trList = []
        tr_ni = soup.find_all(label)
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
            elementmodel = SoccerGame.ElementModel(getRangeWithStr(imgLabel_str, 'alt="', '"'), src)
            imgList.append(elementmodel)

        return imgList


def getRangeWithStr(Str,start,end):
    # start_index = str(Str).find(start)
    # end_index = str(Str).find(end)
    # return str(Str)[start_index:end_index]
    match = re.findall('[\u4e00-\u9fa5]*[\u4e00-\u9fa5]', str(Str))
    # print(type(match))
    return str(match)



# url = "http://www.mm131.com/qingchun/"
def main():
    url = "http://www.310win.com/buy/jingcai.aspx?typeID=102&oddstype=2&date=" + str(datetime.date.today())
    instance = GetURL(url)
    imgList = instance.getHtmlListWithLabel('a')
    newImgList = instance.filterList(imgList, '>亚<')

    urllist = []
    for a in newImgList:
        print(a)
        match = re.findall(r'(/[^# ]*html)', str(a))
        url = 'http://www.310win.com/' + match[0]
        urllist.append(url)

    soccerList = []
    for url in urllist:
        soccer = SoccerGame(url)
        soccer.parserHtml()
        soccer.beginCaculte()
        soccer.canSaveLocal()
        soccerList.append(soccer)

if __name__ == "__main__":
    main()





