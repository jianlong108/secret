#!/usr/bin/env python
# -*- coding: utf-8 -*-

from GetData.DBHelper import *

class MainSoccer:
    def __init__(self):
        self.contientList = []
        self.index = 0
        self.countryList = []
    def getContientModel(self, contientID):
        targetModel = None
        for model in self.contientList:
            if model.continentID == contientID:
                targetModel = model
                break
        return targetModel

    def getCountryModel(self, countryID):
        targetModel = None
        for model in self.countryList:
            if model.countryID == countryID:
                targetModel = model
                break
        return targetModel


    def switchModel(self, complexStr):
        if self.index == 0:
            array = complexStr.split('$$')

            contientStr = array[0]
            self.creatContientModel(contientStr)

            countryStr = array[1]
            self.creatCountryModel(countryStr)
        elif self.index == 1:
            array = complexStr.split('$$')

            countryStr = array[0]
            self.creatCountryModel(countryStr)

            leagueStr = array[1]
            self.creatLeagueModel(leagueStr)
        else:
            array = complexStr.split('$$')

            leagueStr = array[0]
            self.creatLeagueModel(leagueStr)

        self.index += 1

    def creatContientModel(self, complexStr):
        model = ContinentSoccer()
        array = complexStr.split('^')
        model.continentID = array[0]
        model.continentName = array[1]
        self.contientList.append(model)


    def creatCountryModel(self, complexStr):
        model = CountrySoccer()
        array = complexStr.split('^')
        model.countryID = array[0]
        model.belongtoContinentID = array[1]
        model.countryName = array[2]

        contientModel = self.getContientModel(model.belongtoContinentID)
        contientModel.countryList.append(model)
        self.countryList.append(model)

    def creatLeagueModel(self, complexStr):
        model = League()
        array = complexStr.split('^')
        model.leagueID = int(array[0])
        model.belongtoCountryID = int(array[1])
        model.leagueName = array[2]
        model.breifLeagueName = array[3]
        model.aviableSeasonStr = array[5]
        model.creatSeasonList()
        countryModel = self.getCountryModel(model.belongtoCountryID)
        if countryModel != None:
            countryModel.leagueList.append(model)

        insert_League(model)

        # if model.leagueID == 26:
        #     print model.leagueName + '========='
        #     league = GetLeague(model)
        #     # 杯赛去请求杯赛接口,逻辑
        #     if '杯' in model.breifLeagueName:
        #         league.getCupDetails()
        #     #     否则全部视为联赛
        #     else:
        #         league.getOfficialLeague()






    def getData(self):
        try:
            url = "http://121.10.245.46:8072/phone/InfoIndex.aspx?an=iosQiuTan&av=5.9" \
                  "&from=2&lang=0&r=1491480939"
            print url
        except:
            pass
        resultStr = ''
        response = requests.get(url)
        if response.ok:
            resultStr = response.content;
        else:
            pass

        if resultStr != '':
            allArray = resultStr.split('!')
            for complexStr in allArray:
                # print complexStr.decode('utf-8')
                # print '===='
                if '$$' in complexStr:
                    # 切换模型 生成
                    self.switchModel(complexStr)
                else:
                    unitArray = complexStr.split('^')

                    if len(unitArray) == 2:
                        self.creatContientModel(complexStr)
                    elif len(unitArray) == 3:
                        self.creatCountryModel(complexStr)
                    else:
                        self.creatLeagueModel(complexStr)



if __name__ == '__main__':
    create_database()
    main = MainSoccer()
    main.getData()
