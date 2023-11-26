#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time

from GetData.SOCCER_MODELS import *
from GetData.SOCCER_TOOL import *

reload(sys)
sys.setdefaultencoding('utf-8')


'''
获取单场比赛 各个公司的开盘历史胜率
'''

def getMatchSingle(matchid):
    mainurl = 'http://www.310win.com'
    URL = '%s/handicap/%s.html' % (mainurl, str(matchid))
    print(URL)

    instance = SoupHelper(URL)
    companycontainer = instance.gethtmllistwithlabel('table', {'class': 'socai', 'width': "100%"})
    if len(companycontainer) == 0:
        return
    companylist = companycontainer[0]
    handicompanylist = []
    if isTagClass(companylist):
        for ele in companylist.children:
            if isTagClass(ele):
                company = BetCompany()
                if ele.get('class')[0] in [u'ni', u'ni2']:
                    targetelelist = getelementlistwithlabel(ele, 'td')
                    if len(targetelelist) > 0:
                        try:
                            company.companyTitle = targetelelist[0].get_text().encode('utf-8')
                            # print targetelelist[1].get_text().encode('utf-8')
                            if targetelelist[1].get_text().encode('utf-8') == '':
                                continue
                            company.orignal_top = float(targetelelist[1].get_text())
                            company.orignal_Handicap = switchHandicap(targetelelist[2].get_text())
                            company.orignal_bottom = float(targetelelist[3].get_text())
                            company.now_top = float(targetelelist[4].get_text().encode('utf-8'))
                            company.now_Handicap = switchHandicap(targetelelist[5].get_text())
                            company.now_bottom = float(targetelelist[6].get_text())
                            # 球队盘口走势 暂时忽略
                            # company.companyTitle = targetelelist[7].get_text().encode('utf-8')
                            subele = targetelelist[8]
                            sublist = getelementlistwithlabel(subele, 'a')
                            for aElement in sublist:
                                if aElement.get_text().encode('utf-8') == '同':
                                    if company.orignal_top != 0.0:
                                        company.similerMatchURL = mainurl + aElement.get('href').encode('utf-8')
                                        company.getwiningpercentage()
                                        time.sleep(0.5)

                        except ValueError as e:
                            print(e)

                    if company.orignal_top != 0.0:
                        # 过滤没有开盘的数据
                        handicompanylist.append(company)


if __name__ == '__main__':
    getMatchSingle(1197755)