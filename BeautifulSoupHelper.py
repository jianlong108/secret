#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from bs4 import Tag
from NetWorkTools import *

class SoupHelper(object):
    def __init__(self, url):
        self.htmlUrl = url
        self.html    = None
        self.download(url)

    def download(self,url):

        try:
            self.html = GetResultStrWithURLStr(url)
            return self.html
        except EnvironmentError:
            pass
        else:
            print '解析URL出错:' + str(url)
        finally:
            pass

    def gethtmllistwithlabel(self, label, options={}, fromencoding = 'gb18030'):
        if self.html is None:
            return None
        soup = BeautifulSoup(self.html,"html.parser",from_encoding= fromencoding)
        elementlist = []
        templist = soup.find_all(label,attrs=options)
        elementlist.extend(templist)
        return elementlist

    


def isTagClass(obj):
    return isinstance(obj, Tag)


def getelementlistwithlabel(tagObj, label, options={}):

    if isinstance(tagObj, Tag):
        elementlist = []
        templist = tagObj.find_all(label, attrs=options)
        elementlist.extend(templist)
        return elementlist
    else:
        print '传入的值有误,不是Tag类型 不作处理:' + tagObj
        return None

def gettextlistwithlabel(tagObj):

    if isinstance(tagObj, Tag):

        strlist = tagObj.get_text()

        return strlist.encode('utf-8')
    else:
        print '传入的值有误,不是Tag类型 不作处理:' + tagObj
        return None