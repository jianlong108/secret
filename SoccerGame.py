#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import requests

import BEAUTIFUL_SOUP_HELPER
from GetData.SOCCER_MODELS import BetCompany
from GetData.SOCCER_TOOL import *


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

        self.hometeam = ''
        self.guestteam = ''
        self.matchid = ''

    def download(self,url):
        # try:
        #     html = requests.urlopen(url).read()
        # except requests.URLError as e:
        #     print("download error")
        #     html = None
        html = requests.get(url)
        return html.content


    def gethandidata(self):
        instance =  BEAUTIFUL_SOUP_HELPER.SoupHelper(self.handiurl)
        companycontainer=  instance.gethtmllistwithlabel('table', {'class' : 'socai','width' : "100%"})
        if len(companycontainer) == 0:
            return
        companylist = companycontainer[0]
        handicompanylist = []
        if BEAUTIFUL_SOUP_HELPER.isTagClass(companylist):
            for ele in companylist.children:
                if BEAUTIFUL_SOUP_HELPER.isTagClass(ele):
                    company = BetCompany()
                    if ele.get('class')[0]  in  [u'ni', u'ni2']:
                        targetelelist = BEAUTIFUL_SOUP_HELPER.getelementlistwithlabel(ele, 'td')
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
                                sublist = BEAUTIFUL_SOUP_HELPER.getelementlistwithlabel(subele, 'a')
                                for aElement in sublist:
                                    if aElement.get_text().encode('utf-8') == '同':
                                        company.similerMatchURL = self.url + aElement.get('href').encode('utf-8')
                                        company.getwiningpercentage()
                                        time.sleep(1.5)
                            except ValueError as e:
                                print(e)


                        if company.orignal_top != 0.0:
                            # 过滤没有开盘的数据
                            handicompanylist.append(company)


        print(len(handicompanylist))

    def getodddata(self):
        instance = BEAUTIFUL_SOUP_HELPER.SoupHelper(self.oddurl)
        oddsList_tab = instance.gethtmllistwithlabel('table', {'id':'oddsList_tab'})
        if BEAUTIFUL_SOUP_HELPER.isTagClass(oddsList_tab):
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









