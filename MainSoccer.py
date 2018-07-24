#!/usr/bin/env python
# -*- coding: utf-8 -*-

from GetData.DBHelper import *

class MainSoccer:
    def __init__(self):
        self.contientList = []
        self.index = 0
        self.countryList = []
        self.leagueList = []

    def creatContientModel(self, complexStr):
        tmp_continentList = complexStr.split('!')
        for continentStr in tmp_continentList:
            continentModel = ContinentSoccer()
            oneContinentList = continentStr.split('^')
            continentModel.continentID = int(oneContinentList[0])
            continentModel.continentName = oneContinentList[1]
            self.contientList.append(continentModel)

    def creatCountryModel(self, complexStr):
        tmp_countryList = complexStr.split('!')
        for countryStr in tmp_countryList:
            countryModel = CountrySoccer()
            oneCountryList = countryStr.split('^')
            countryModel.countryID = int(oneCountryList[0])
            countryModel.belongtoContinentID = int(oneCountryList[1])
            countryModel.countryName = oneCountryList[2]

            for tmpModel in self.contientList:
                if isinstance(tmpModel,ContinentSoccer):
                    if tmpModel.continentID == countryModel.belongtoContinentID:
                        countryModel.belongtoContinentName = tmpModel.continentName
            self.countryList.append(countryModel)


    def creatLeagueModel(self, complexStr):
        tmp_leagueList = complexStr.split('!')
        for leagueStr in tmp_leagueList:
            leagueModel = League()
            oneLeagueList = leagueStr.split('^')
            leagueModel.leagueID = int(oneLeagueList[0])
            leagueModel.belongtoCountryID = int(oneLeagueList[1])
            leagueModel.leagueName = oneLeagueList[2]
            leagueModel.breifLeagueName = oneLeagueList[3]
            leagueModel.subLeagueID = int(oneLeagueList[4])
            leagueModel.aviableSeasonStr = oneLeagueList[5]
            for tmpModel in self.countryList:
                if isinstance(tmpModel, CountrySoccer):
                    if tmpModel.countryID == leagueModel.belongtoCountryID:
                        leagueModel.belongtoCountryName = tmpModel.countryName
                        leagueModel.belongtoContinentName = tmpModel.belongtoContinentName
            self.leagueList.append(leagueModel)

    def getData(self):
        try:
            url = "http://121.10.245.46:8072/phone/InfoIndex.aspx?an=iosQiuTan&av=5.9" \
                  "&from=2&lang=0&r=1491480939"
            print url
        except BaseException as e:
            print e

        resultStr = ''
        response = requests.get(url)
        if response.ok:
            resultStr = response.content;
        else:
            print '获取所有联赛接口失败'

        if resultStr != '':
            allArray = resultStr.split('$$')
            contientComplexStr = allArray[0]
            countryComplexStr = allArray[1]
            leagueComplexStr = allArray[2]

            self.creatContientModel(contientComplexStr)
            self.creatCountryModel(countryComplexStr)
            self.creatLeagueModel(leagueComplexStr)




if __name__ == '__main__':
    create_database()
    main = MainSoccer()
    main.getData()
    InsertLeagueList(main.leagueList)
