#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from bs4 import Tag
from NETWORKS_TOOLS import get_htmlcontent_with_url

class SoupHelper(object):
    def __init__(self, url, htmldecode = 'utf-8'):
        self.html_url = url
        self.html_content    = None
        self.html_contetn_decode = htmldecode
        self.download(url)

    def download(self,url):

        try:
            self.html_content =  get_htmlcontent_with_url(url, self.html_contetn_decode)
            return self.html_content
        except EnvironmentError as e:
            print e
        except BaseException as e:
            print e

    def gethtmllistwithlabel(self, label, options = None, fromencoding = 'gb18030'):
        if options is None:
            options = {}
        if self.html_content is None:
            return None
        soup = BeautifulSoup(self.html_content,"html.parser",from_encoding= self.html_contetn_decode)
        elementlist = []
        templist = soup.find_all(label,attrs=options)
        elementlist.extend(templist)
        return elementlist

    


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
        print '传入的值有误,不是Tag类型 不作处理:' + tagObj
        return None

def gettextlistwithlabel(tagObj):

    if isinstance(tagObj, Tag):

        strlist = tagObj.get_text()

        return strlist.encode('utf-8')
    else:
        print '传入的值有误,不是Tag类型 不作处理:' + tagObj
        return None