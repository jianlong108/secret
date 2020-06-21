#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pylint: disable=no-member
from BEAUTIFUL_SOUP_HELPER import SoupHelper
import json
import os


class OneGirl:
    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.pageList = [url]
        self.plsitDic = {}
        self.getImagePages()

    def getImagePages(self):
        instance = SoupHelper(self.url)
        pageListContainer = instance.getOneTagObjWithClass('div','pagelist')
        aList = pageListContainer.find_all('a')
        for a in aList:
            # print a.get('href').encode('utf-8')
            self.pageList.append(a.get('href').encode('utf-8'))
        # print self.pageList

    def getAllImages(self):
        self.imageList = []
        for onePage in self.pageList:
            soupObj = SoupHelper(onePage)
            imgContainer = soupObj.getOneTagObjWithId("post_content")
            ele = imgContainer.find_all('img')
            for img in ele:
                # print img.get('src').encode('utf-8')
                self.imageList.append(img.get('src').encode('utf-8'))
        # print self.imageList

    def writeToJsonFile(self):
        resultDir = os.getcwd()
        resultJsonPath = os.path.join(resultDir,"{}.json".format(self.name))
        print resultJsonPath
        with open(resultJsonPath,"w") as f:
            json.dump({self.name:self.imageList},f)

class ChannelPageGirls:
    def __init__(self, name, url='http://www.taotuxp.com/xinggan/page/110'):
        self.name = name
        self.url = url
        self.pageList = []
        self.parserAllPages(url)
        self.parserOnePageChannel(self.url)


    def parserOnePageChannel(self, url):
        instance = SoupHelper(url)
        ulElement = instance.getOneTagObjWithId('post_container')
        # for child in ulElement.descendants:
        for child in ulElement.find_all('li'):
            thumbnailEle = child.find('div',{'class':'thumbnail'})
            print thumbnailEle.find('a').get('href')


    def parserAllPages(self,url):
        instance = SoupHelper(url)
        divElement = instance.getOneTagObjWithClass('div','pagination')
        if not divElement:
            print url + ' 不合法'
            print self.pageList
            return
        pageList = divElement.find_all('a')
        lastPage = None
        foundNextPageFlag = False
        for child in pageList:
            pageUrl = child.get('href').encode('utf-8')
            # print pageUrl
            if not pageUrl in self.pageList:
                self.pageList.append(pageUrl)
            if child.get_text().encode('utf-8') != '下一页':
                lastPage = pageUrl
            else:
                foundNextPageFlag = True
        # print lastPage
        if foundNextPageFlag == True:
            self.parserAllPages(lastPage)
        else:
            print self.pageList

def main():
    channelPage = ChannelPageGirls('性感','http://www.taotuxp.com/xinggan/page/110')
    # channelPage.get

    # girlObj = OneGirl('极品妹子周研希透视内衣若隐若现写真','http://www.taotuxp.com/252555.html')
    # girlObj.getAllImages()
    # girlObj.writeToJsonFile()

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