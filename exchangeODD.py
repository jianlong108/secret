#!/usr/bin/env python
# -*- coding: utf-8 -*-

from BeautifulSoupHelper import *
from SoccerModels import *
from soccerTool import *
import sys

reload(sys)
sys.setdefaultencoding('utf8')

'''
16 10bet
18 12bet
80 澳门
81 伟德
90 易胜博
281 bet365
517 明盛
545 sb

'''

def getexchange(soccerid=0):

    # url = 'http://www.310win.com/info/1x2exchange.aspx?id=' + str(soccerid) + '&cids=,' + str(companyid) + ',&type=3'
    url = 'http://www.310win.com/info/1x2exchange.aspx?id=' + str(soccerid) + '&cids=,16,18,80,81,90,281,517,545,&type=3'
    print url
    soupInstance = SoupHelper(url)
    trlist = soupInstance.gethtmllistwithlabel('tr', {'bgcolor': '#FFFFFF'})

    companieslist = []
    colorResultStr = ''
    for tr in trlist:
        if isTagClass(tr):
            oneCompany = BetCompany()
            resultStr = tr.get_text('^').encode('utf-8')
            unitStrList = resultStr.split('^')
            # print resultStr

            oneCompany.companyTitle = unitStrList[0]
            colorResultStr += unitStrList[0]
            colorResultStr += ' 转换后: '
            colorResultStr += unitStrList[5]
            colorResultStr += ' '
            colorResultStr += unitStrList[6]
            colorResultStr += ' '
            colorResultStr += unitStrList[7]
            colorResultStr += ' 实际: '
            colorResultStr += unitStrList[8]
            colorResultStr += ' '
            colorResultStr += unitStrList[9]
            colorResultStr += ' '
            colorResultStr += unitStrList[10]
            colorResultStr += ' '
            colorResultStr += '\n'
            try:
                # 胜平负
                oneCompany.winOdd = float(unitStrList[1])
                oneCompany.drawOdd = float(unitStrList[2])
                oneCompany.loseOdd = float(unitStrList[3])
                # 转换后的亚盘
                oneCompany.exchange_top = float(unitStrList[5])
                # oneCompany.exchange_Handicap = switchHandicap(unitStrList[6])
                oneCompany.exchange_bottom = float(unitStrList[7])
                # 当前的亚盘
                oneCompany.now_top = float(unitStrList[8])
                # oneCompany.now_Handicap = switchHandicap(unitStrList[9])
                oneCompany.now_top = float(unitStrList[10])

            except BaseException as e:
                print e
            else:
                companieslist.append(oneCompany)

    print "\033[1;31;40m%s\033[0m" % colorResultStr
    return colorResultStr



# if sys.argv.__len__()==1:
#     sys.exit('\033[0;36;40m使用说明:\n1个参数:\n事例: python TodaySoccer.pyc 12344\033[0m')

# if __name__ == '__main__':
#     getexchange(sys.argv[1])

getexchange(1401828)