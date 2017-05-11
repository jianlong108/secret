#!/usr/bin/env python
# -*- coding: utf-8 -*-

from SendMail import *

import urllib2
from bs4 import BeautifulSoup
import sys

reload(sys)
sys.setdefaultencoding('utf8')

def getexchange(soccerid=0):
    html = None
    # url = 'http://www.310win.com/info/1x2exchange.aspx?id=' + str(soccerid) + '&cids=,' + str(companyid) + ',&type=3'
    url = 'http://www.310win.com/info/1x2exchange.aspx?id=' + str(soccerid) + '&cids=,81,80,545,281,16,&type=3'
    print("downloading", url)
    try:
        html = urllib2.urlopen(url).read()
        # html = Request.urlopen(url).read()
        # print html
    except:
        print("download error")
        html = None

    soup = BeautifulSoup(html, "html.parser")
    trList = []
    tr_ni = soup.find_all('td')
    trList.extend(tr_ni)
    tempList = []
    for tr in trList[18:]:
        tempList.append(str(tr.string).encode('utf-8'))
        print str(tr.string).encode('utf-8')
    # print tempList
    # send_mail(str(soccerid), ''.join(tempList))


if sys.argv.__len__()==1:
    sys.exit('\033[0;36;40m使用说明:\n1个参数:\n事例: python TodaySoccer.pyc 12344\033[0m')

if __name__ == '__main__':
    getexchange(sys.argv[1])

# getexchange(1379126)