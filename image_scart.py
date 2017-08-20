#!/usr/bin/env python
# -*- coding: utf-8 -*-


import BeautifulSoupHelper
# from biplist import *


class OneGirl:
    def __init__(self, name, url, firstImageUrl):
        self.name = name
        self.url = url
        self.firstImageUrl = firstImageUrl
        self.plsitDic = {}
        # self.getNumImages()

    def getNumImages(self):
        instance = BeautifulSoupHelper.SoupHelper(self.url)
        span = instance.gethtmllistwithlabel('span', attrs={'class': 'page-ch'})
        # html = HtmlParser.download(self.url)
        # soup = BeautifulSoup(html, 'html.parser', from_encoding='gb18030')
        # span = soup.find('span', attrs={'class': 'page-ch'})
        spanContent = span.get_text()
        num = spanContent[1:][:-1]
        if num.isdigit():
            self.num = int(num)
        else:
            self.num = 60
        return self.creatImageURLList()
        # oneGirlNumsComplete()

    def creatImageURLList(self):

        self.imageList = []
        if self.firstImageUrl.count('0.jpg') == 0:
            list = self.firstImageUrl.split(r'/')
            list.pop()
            oneurl = ''
            for tempstr in list:
                oneurl = oneurl + tempstr
                if str == '/':
                    oneurl = oneurl + '//'
                else:
                    oneurl = oneurl + '/'

            self.firstImageUrl = oneurl + ('0.jpg')
        else:
            pass

        for oneN in range(self.num):
            oneURL = self.firstImageUrl.replace('0.jpg', (str(oneN + 1) + '.jpg'))
            # if request.urlopen(oneUrl).getcode() == 200:
            self.imageList.append(oneURL)

        self.plsitDic[self.name] = self.imageList
        return self.plsitDic

class PageGirls:
    def __init__(self, name, url, website='http://www.mm131.com/'):
        self.name = name
        self.url = url
        self.website = website
        self.alreadyParseGirlNum = 0
        self.one_girl_list = []
        self.category_other_girls = []
        self.girList = []
        self.plist = {}
        self.parseronecategory(self.url)
        self.parserOtherPage()


    def parseronecategory(self, url):
        # url = "http://www.mm131.com/qingchun/"
        # html = HtmlParser.download(url)
        # mainSoup = BeautifulSoup(html, 'html.parser',from_encoding='gb18030')
        instance = BeautifulSoupHelper.SoupHelper(url)
        dlList = instance.gethtmllistwithlabel('dl', {'class': 'list-left public-box'})
        # dlList = mainSoup.find('dl', {'class': 'list-left public-box'})
        # dlList = HtmlParser.getHtmlListWithLabel(html, 'dl', {'class': 'list-left public-box'})

        for child in dlList.descendants:
            if str(type(child)) == "<class 'bs4.element.Tag'>":
                if child.get('src') is not None and child.get('alt') is not None:
                    # print(child.parent.get('href'))
                    one = OneGirl(child.get('alt'),child.parent.get('href') ,child.get('src'))
                    # print(child.get('alt'),child.get('src'))
                    self.one_girl_list.append(one)
                else:
                    if child.get('href') is not None and child.get_text() is not None:
                        # pass
                        # print(child.get('href'))
                        if child.get('href') != self.website and child.get('href') != self.url:
                            # print(child.get('href').find(self.website))
                            if child.get('href').find(self.website) == -1 and child.get_text() == '末页':
                                self.endPageHtml = self.url + child.get('href')
                            elif child.get('href').find(self.website) == -1 and child.get_text() == '下一页':
                                self.nextPageHtml = self.url + child.get('href')
                                # print(self.nextPageHtml)
        self.getGirlUrlList(url)


    def getGirlUrlList(self,url):
        for one in self.one_girl_list:
            oneplist = one.getNumImages()
            self.girList.append(oneplist)
        self.plist[url] = self.girList.copy()
        self.one_girl_list = []
        self.girList = []








    def parserOtherPage(self):
        self.otherCateoryPage = []
        for num in range(100):
            newHtml = self.nextPageHtml.replace('2.html', str(int(num)+3) + '.html')
            # print(newHtml)
            self.otherCateoryPage.append(newHtml)
            if newHtml == self.endPageHtml:
                # print(self.otherCateoryPage)
                break;

    def parseAllGirls(self):
        for html in self.otherCateoryPage:
            self.parserOneCategory(html)
        # writePlist(self.plist, "/Users/autohome/Desktop/channel.plist")

class ChannelGirl:
    def __init__(self,name,url):
        self.channelName = name
        self.channelURL = url
        self.channelEndPage = ''
        self.numPage = 0
        self.endPage = 'list_1_2.html'
        self.pagesHtmlList = {}

    def getAllPages(self):
        instance = BeautifulSoupHelper.SoupHelper(self.channelURL)
        aList = instance.gethtmllistwithlabel('a', {'class': 'page-en'}, fromencoding= 'gb2312')
        # html = HtmlParser.download(self.channelURL)
        # mainSoup = BeautifulSoup(html, 'html.parser',from_encoding='gb2312')
        # aList = mainSoup.find_all('a', {'class': 'page-en'})
        if len(aList)>0:
            self.numPage = int(aList[-1].get('href')[7:][:-5])
            self.endPage = aList[-1].get('href')
            self.channelEndPage = self.channelURL + aList[-1].get('href')
            # print(self.channelEndPage)
        tempstr = ''
        for num in range(self.numPage):
            if num == 0:
                continue
            tempstr = ''
            tempstr = self.endPage.replace((str(self.numPage)+'.html'),str(num + 1)+'.html')
            self.pagesHtmlList.append(self.channelURL+tempstr)

        # writePlist(main.channelList, "/Users/autohome/Desktop/channel.plist")


# one = OneGirl('gil','http://www.mm131.com/qingchun/2723.html')
# one.getNumImages()
class MainView:
    def __init__(self):
        self.url = "http://www.mm131.com/"
        self.channelList = []
        self.loclDic ={}
    def getAllCateogry(self):
        instance = BeautifulSoupHelper.SoupHelper(self.url)
        navHtml = instance.gethtmllistwithlabel('div', attrs={'class': 'nav'})
        # html = HtmlParser.download(self.url)
        # webSoup = HtmlParser.getSoup(html)
        # navHtml = webSoup.find('div', attrs={'class': 'nav'})
        for nav_child in navHtml.descendants:
            if str(type(nav_child)) == "<class 'bs4.element.Tag'>":
                if nav_child.get('href') != None:
                    tempDic = {}
                    # print(nav_child.get('href'),nav_child.get_text())
                    channel = ChannelGirl(nav_child.get_text(),nav_child.get('href'))
                    tempDic[nav_child.get_text()] = nav_child.get('href')
                    # channel.getAllPages()
                    self.channelList.append(tempDic)
                    self.loclDic[self.url] = self.channelList


def main():
    plsitDic = {}
    # main = MainView()
    # main.getAllCateogry()
    # writePlist(main.loclDic, "/Users/autohome/Desktop/channel.plist")
    page = PageGirls('清纯','http://www.mm131.com/qingchun/')
    page.parseAllGirls()


if __name__ == '__main__':
    main()


# def save_file( file_name, data):
#     if data == None:
#         return
#     # os.path.abspath('.')
#     path = os.path.join('/Users/autohome/Desktop', 'images')
#     if not os.path.exists(path):
#         os.mkdir(path=path)
#
#     if (not path.endswith("/")):
#         path = path + "/"
#     file = open(path + file_name, "wb")
#     file.write(data)
#     file.flush()
#     file.close()