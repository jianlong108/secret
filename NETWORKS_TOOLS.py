#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import urllib2
# from selenium import webdriver
# import time
# import pycurl
# import StringIO
# browser = webdriver.Chrome()
# browser.get("http://zq.win007.com/cn/League/2018-2019/36.html")
# print browser.page_source

def get_resultstr_with_url(urlStr):
    # c = pycurl.Curl()
    #
    # c.setopt(pycurl.URL, handiURL)
    #
    # b = StringIO.StringIO()
    # c.setopt(pycurl.WRITEFUNCTION, b.write)
    # c.setopt(pycurl.FOLLOWLOCATION, 1)
    # c.setopt(pycurl.MAXREDIRS, 5)
    # c.perform()
    # resultStr = b.getvalue().encode('utf-8')
    resultStr = ''
    headers = {'User-Agent': 'Baiduspider'}
    response = requests.get(urlStr,headers=headers)
    if response.ok:
        resultStr = response.content
    return resultStr

def get_htmlcontent_with_url(url, htmldecode = 'utf-8'):
    header = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:48.0) Gecko/20100101 Firefox/48.0"}
    request = urllib2.Request(url=url, headers=header)  # 模拟浏览器进行访问
    response = urllib2.urlopen(request)
    text = response.read()
    text = text.decode(htmldecode)
    return text