#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import urllib2

def get_resultstr_with_url(urlStr):
    resultStr = ''
    headers = {'User-Agent': 'Baiduspider'}
    response = requests.get(urlStr,headers=headers)
    if response.ok:
        resultStr = response.content
    return resultStr

def get_htmlcontent_with_url(url, htmldecode = 'utf-8'):
    header = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"}
    request = urllib2.Request(url=url, headers=header)  # 模拟浏览器进行访问
    response = urllib2.urlopen(request)
    text = response.read()
    text = text.decode(htmldecode)
    return text