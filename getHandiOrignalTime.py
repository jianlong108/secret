#!/usr/bin/env python
# -*- coding: utf-8 -*-

from BeautifulSoupHelper import *
from SoccerModels import *
from soccerTool import *
import sys

reload(sys)
sys.setdefaultencoding('utf8')

def gethandiTime(soccerid=0):

    # url = 'http://www.310win.com/info/1x2exchange.aspx?id=' + str(soccerid) + '&cids=,' + str(companyid) + ',&type=3'
    url = 'http://www.310win.com/handicap/' + str(soccerid) + '.html'
    # print url
    soupInstance = SoupHelper(url)
    tablelist = soupInstance.gethtmllistwithlabel('table', {'width': '860', 'class':'socai'})
    trlist = getelementlistwithlabel(tablelist[0], 'tr')
    count = len(trlist)
    tr = trlist[count - 1]
    if isTagClass(tr):
        tdlist = tr.contents
        if len(tdlist) > 0:
            flag = tdlist[0].get_text()
            if flag.strip() != u'':
               return True
            else:
                return False
        else:
            return False
    else:
        return False



# if sys.argv.__len__()==1:
#     sys.exit('\033[0;36;40m使用说明:\n1个参数:\n事例: python TodaySoccer.pyc 12344\033[0m')

# if __name__ == '__main__':
#     getexchange(sys.argv[1])

# getexchange(1401828)