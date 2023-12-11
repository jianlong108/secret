#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from bs4.element import Tag
from NETWORKS_TOOLS import get_htmlcontent_with_url

class SoupHelper(object):
    def __init__(self, url, htmldecode = 'utf-8'):
        self.html_url = url
        self.html_content = None
        self.html_contetn_decode = htmldecode
        self.download(url)
        self.soupObj = None

    def download(self,url):
        try:
            self.html_content =  get_htmlcontent_with_url(url, self.html_contetn_decode)
            if self.html_content is None:
                print('SoupHelper init 解析出错')
            return self.html_content
        except EnvironmentError as e:
            print(e)
        except BaseException as e:
            print(e)

    def getOneTagObjWithClass(self,tagName,clsName):
        try:
            if not self.soupObj:
                self.soupObj = BeautifulSoup(self.html_content,"html.parser")
                # print self.soupObj
            return self.soupObj.find(tagName,{'class':clsName})
        except Exception as e:
            print(e)
            return None

    def getOneTagObjWithId(self,identifier):
        try:
            if not self.soupObj:
                self.soupObj = BeautifulSoup(self.html_content,"html.parser")
                # print self.soupObj
            return self.soupObj.find(id=identifier)
        except Exception as e:
            print(e)
            return None

    def gethtmllistwithlabel(self, label, options ={}, fromencoding = 'gb18030'):
        try:
            if self.html_content is None:
                return None
            if not self.soupObj:
                self.soupObj = BeautifulSoup(self.html_content,"html.parser")
                # self.soupObj = BeautifulSoup(self.html_content,"html.parser",from_encoding= self.html_contetn_decode)
            elementlist = []
            templist = self.soupObj.find_all(label,attrs=options)
            elementlist.extend(templist)
            return elementlist
        except Exception as e:
            print(e)
            return None

    # def isTagClass(obj):
    #     return isinstance(obj, Tag)
    #
    # def getelementlistwithlabel(tagObj, label, options=None):
    #     if options is None:
    #         options = {}
    #
    #     if isinstance(tagObj, Tag):
    #         elementlist = []
    #         templist = tagObj.find_all(label, attrs=options)
    #         elementlist.extend(templist)
    #         return elementlist
    #     else:
    #         print('传入的值有误,不是Tag类型 不作处理:' + tagObj)
    #         return None
    #
    # def gettextlistwithlabel(tagObj):
    #     if isinstance(tagObj, Tag):
    #
    #         strlist = tagObj.get_text()
    #
    #         return strlist.encode('utf-8')
    #     else:
    #         print('传入的值有误,不是Tag类型 不作处理:' + tagObj)
    #         return None

def isTagClass(obj):
    return isinstance(obj, Tag)

def getelementlistwithlabel(tagObj, label, options = None):
    if options is None:
        options = {}

    if isinstance(tagObj, Tag):
        elementlist = []
        templist = tagObj.find_all(label, attrs=options)
        elementlist.extend(templist)
        return elementlist
    else:
        print('传入的值有误,不是Tag类型 不作处理:' + tagObj)
        return None

def gettextlistwithlabel(tagObj):
    if isinstance(tagObj, Tag):

        strlist = tagObj.get_text()

        return strlist.encode('utf-8')
    else:
        print('传入的值有误,不是Tag类型 不作处理:' + tagObj)
        return None

if __name__ == "__main__":
    soupObj = SoupHelper('http://www.taotuxp.com/252555.html')
    # print soupObj.html_content
    imgContainer = soupObj.getOneTagObjWithId("post_content")
    ele = imgContainer.find_all('img')
    for img in ele:
        print(img.get('src'))
    # ele = soupObj.gethtmllistwithlabel('img')
    # for img in ele:
    #     print img.get('src')
