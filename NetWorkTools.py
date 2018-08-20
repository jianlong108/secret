#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
# import time
# import pycurl
# import StringIO

def GetResultStrWithURLStr(urlStr):
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
