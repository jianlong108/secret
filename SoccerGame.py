#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import os
import re
import BeautifulSoupHelper


class ElementModel:
    def __init__(self,title,src):
        self.title = title
        self.src = src

class BetCompany:
    companyTitle = ''
    orignal_top = ''
    orignal_bottom = ''
    orignal_Handicap = 0.0
    now_top = ''
    now_bottom = ''
    now_Handicap = 0.0
    orignal = ''
    now = ''

    falldown = False
    rise = False
    lowest = False
    highest = False



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
                    targetelelist = BeautifulSoupHelper.getelementlistwithlabel(ele, 'tr', {'class' : 'ni'})
                    if len(targetelelist) > 0:
                        handicompanylist.extend(targetelelist)
                    targetelelist = []
                    targetelelist = BeautifulSoupHelper.getelementlistwithlabel(ele, 'tr', {'class': 'ni2'})
                    if len(targetelelist) > 0:
                        handicompanylist.extend(targetelelist)

        print handicompanylist


    def parserHtml(self):

        html = self.download(self.url)
        soup = ''
        try:
            table = soup.find('table', attrs={'class': 'socai'})
            list_ni = table.find_all('tr', attrs={'class': 'ni'})
            list_ni2 = table.find_all('tr', attrs={'class': 'ni2'})
            self.trlist.extend(list_ni)
            self.trlist.extend(list_ni2)
            for tr in self.trlist:
                self.tdList.append(tr.find_all('td')[:7])

            for td in self.tdList:
                company = BetCompany()

                for (i, value) in enumerate(td):
                    if i == 0:
                        match = re.findall('((\S)*(\S))', value.get_text())
                        # print(match[0][0])
                        company.companyTitle = match[0][0]
                    elif i == 1:
                        company.orignal_top = value.get_text()
                    elif i == 2:
                        company.orignal_Handicap = switchHandicap(value.get_text())
                        company.orignal = value.get_text()
                    elif i == 3:
                        company.orignal_bottom = value.get_text()
                    elif i == 4:
                        company.now_top = value.get_text()
                    elif i == 5:
                        company.now_Handicap = switchHandicap(value.get_text())
                        company.now = value.get_text()
                    elif i == 6:
                        company.now_bottom = value.get_text()
                    else:
                        pass
                # if company.companyTitle == '澳彩':
                #     print('初盘',company.orignal_Handicap,'当前盘',company.now_Handicap,self.url)
                self.companyList.append(company)
        except Exception, e:
            print Exception, ":", e



    def beginCaculte(self):

        # print('公司 ge个数',len(self.companyList),self.url)
        for company in self.companyList:
            # print(company.companyTitle, company.now_Handicap, company.orignal_Handicap)

            try:
                if company.orignal_Handicap - company.now_Handicap > 0:
                    if company.companyTitle== u'澳彩':
                     # print(company.orignal_top,company.orignal_Handicap,company.orignal_bottom,company.now_Top,company.now_Handicap,company.now_Bottom,self.url,self.leauge,self.soccer)
                     print(company.orignal_top,company.orignal,company.orignal_bottom,company.now_top, company.now,company.now_bottom, self.url, self.leauge, self.soccer)
                     if self.soccer != None:
                         par = (self.leauge, self.soccer, self.url, company.orignal_top, company.orignal,
                                company.orignal_bottom, company.now_top, company.now, company.now_bottom)
                         HtmlParser.insert_record(par)

                     company.falldown = True
                    else:
                        pass
                elif company.orignal_Handicap - company.now_Handicap < 0:
                    if company.companyTitle== u'澳彩':
                        print(company.orignal_top, company.orignal, company.orignal_bottom, company.now_top,
                              company.now, company.now_bottom, self.url, self.leauge, self.soccer)
                        if self.soccer != None:
                            par = (self.leauge, self.soccer, self.url, company.orignal_top, company.orignal,
                                   company.orignal_bottom, company.now_top, company.now, company.now_bottom)
                            HtmlParser.insert_record(par)
                        company.rise = True
                    else:
                        pass
                elif float(company.now_top) < 0.85:
                    company.lowest = True
                elif float(company.now_top) > 1.1:
                    company.highest = True
                elif float(company.now_bottom) < 0.85:
                    company.lowest = True
                elif float(company.now_bottom) > 1.1:
                    company.highest = True
                else:
                    pass
            except:
                pass
            finally:
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






