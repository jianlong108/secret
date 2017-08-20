#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import os
import BeautifulSoupHelper
from SoccerModels import BetCompany


class SoccerGame:

    def __init__(self, url):
        self.url = url
        self.trlist = []
        self.tdList = []
        self.companyList = []
        self.leauge = ''
        self.soccer = ''
        self.oddurl = ''
        self.handiurl = ''

    def download(self,url):
        # try:
        #     html = requests.urlopen(url).read()
        # except requests.URLError as e:
        #     print("download error")
        #     html = None
        html = requests.get(url)
        return html.content


    def gethandidata(self):
        instance =  BeautifulSoupHelper.SoupHelper(self.handiurl)
        companycontainer=  instance.gethtmllistwithlabel('table', {'class' : 'socai','width' : "100%"})
        companylist = companycontainer[0]
        handicompanylist = []
        if BeautifulSoupHelper.isTagClass(companylist):
            for ele in companylist.children:
                if BeautifulSoupHelper.isTagClass(ele):
                    company = BetCompany()
                    if ele.get('class')[0]  in  [u'ni', u'ni2']:
                        targetelelist = BeautifulSoupHelper.getelementlistwithlabel(ele, 'td')
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
                                sublist = BeautifulSoupHelper.getelementlistwithlabel(subele, 'a')
                                for aElement in sublist:
                                    if aElement.get_text().encode('utf-8') == '同':
                                        company.similerMatchURL = self.url + aElement.get('href').encode('utf-8')
                            except ValueError , e:
                                print e
                                pass


                        if company.orignal_top != 0.0:
                            # 过滤没有开盘的数据
                            handicompanylist.append(company)


        print len(handicompanylist)

    def getodddata(self):
        instance = BeautifulSoupHelper.SoupHelper(self.oddurl)
        oddsList_tab = instance.gethtmllistwithlabel('table', {'id':'oddsList_tab'})
        if BeautifulSoupHelper.isTagClass(oddsList_tab):
            pass
    def writeLocal(self):
        print('写文件')
        path = os.path.join('/Users/mi/Desktop', 'soccer.txt')
        if os.path.exists(path):

            file = open(path, "a")
        else:
            file = open(path, "w")
        file.write(self.url)
        file.write('\n')
        # file.close()

    def canSaveLocal(self):
        i = 0
        for company in self.companyList:
            if company.companyTitle=='澳彩':
                if company.falldown or company.rise:
                    # i += 1
                    self.writeLocal()
                    break;

                else:
                    pass
            else:
                pass


def switchHandicap(Handicap):
    try:
        if Handicap == u'受平手/半球':
            return -0.25
        elif Handicap == u'受半球':
            return -0.5
        elif Handicap == u'受半球/一球':
            return -0.75
        elif Handicap == u'受一球':
            return -1.0
        elif Handicap == u'受一球/一球半':
            return -1.25
        elif Handicap == u'受一球半':
            return -1.5
        elif Handicap == u'受一球半/两球':
            return -1.75
        elif Handicap == u'受两球':
            return -2.0
        elif Handicap == u'受两球/两球半':
            return -2.25
        elif Handicap == u'受两球半':
            return -2.5
        elif Handicap == u'受两球半/三球':
            return -2.75
        elif Handicap == u'受三球':
            return -3.0
        elif Handicap == u'受三球/三球半':
            return -3.25
        elif Handicap == u'受三球半':
            return -3.5
        elif Handicap == u'受三球半/四球':
            return -3.75
        elif Handicap == u'平手':
            return 0
        elif Handicap == u'平手/半球':
            return 0.25
        elif Handicap == u'平手/半球':
            return 0.25
        elif Handicap == u'半球':
            return 0.5
        elif Handicap == u'半球/一球':
            return 0.75
        elif Handicap == u'一球':
            return 1.0
        elif Handicap == u'一球/球半':
            return 1.25
        elif Handicap == u'球半':
            return 1.5
        elif Handicap == u'球半/两球':
            return 1.75
        elif Handicap == u'两球':
            return 2.0
        elif Handicap == u'两球/两球半':
            return 2.25
        elif Handicap == u'两球半':
            return 2.5
        elif Handicap == u'两球半/三球':
            return 2.75
        elif Handicap == u'三球':
            return 3.0
        elif Handicap == u'三球/三球半':
            return 3.25
        elif Handicap == u'三球半':
            return 3.5
        elif Handicap == u'三球半/四球':
            return 3.75
        else:
            return 108
    except:
        pass
    finally:
        pass






