#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymysql
from GetData import SOCCER_MODELS

import traceback
# 替换以下变量为你的数据库信息
host = 'localhost'
user = 'root'
password = 'longge108'
database_name = 'JL'
try:
# 连接 MySQL 服务器
    conn = pymysql.connect(
        host=host,
        user=user,
        password=password
    )
    cursor = conn.cursor()
except BaseException as e:
    print(e)

def creatDataBase():
    global conn
    global cursor
    # 查询数据库是否已经存在
    cursor.execute(f"SHOW DATABASES LIKE '{database_name}'")

    # 检查查询结果
    result = cursor.fetchone()

    # 如果数据库不存在，创建数据库
    if not result:
        cursor.execute(f'CREATE DATABASE {database_name}')
        print(f"Database '{database_name}' created successfully.")
    else:
        print(f"Database '{database_name}' already exists.")

    # 关闭连接
    cursor.close()
    conn.close()

def creatTable():
    global conn
    global cursor

    conn = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database_name
    )
    cursor = conn.cursor()
    # 创建新表
    create_table_query = """
        CREATE TABLE IF NOT EXISTS DisorderPanGames (
            soccerid       INT  PRIMARY KEY,
            leagueid       INT              NOT NULL,
            league         VARCHAR(15)          NOT NULL,
            begintime      VARCHAR(15)          NOT NULL,
            hometeam       VARCHAR(15)          NOT NULL,
            awayteam       VARCHAR(15)          NOT NULL,
            homescore      INT,
            awayscore      INT,
            homehalfscore  INT,
            awayhalfscore  INT,
            aomenoripan    FLOAT                NOT NULL,
            aomennowpan    FLOAT                NOT NULL,
            oripans        VARCHAR(15),
            nowpans        VARCHAR(15),
            result         VARCHAR(15),
            oriResult      VARCHAR(15),
            ori365         FLOAT,
            now365         FLOAT)
    """
    cursor.execute(create_table_query)

    # 创建新表
    create_ODD_table_query = '''
        create table if not exists CompanyOdd (
            soccerID INT NOT NULL,
            companyid INT NOT NULL,
            company VARCHAR(15),
            oriwin FLOAT ,
            oridraw FLOAT ,
            orilose FLOAT,
            win FLOAT ,
            draw FLOAT,
            lose FLOAT,
            hometeamid INT,
            awayteamid INT,
            PRIMARY KEY (soccerID, companyid))
        '''
    cursor.execute(create_ODD_table_query)
    create_table_query = """
        CREATE TABLE IF NOT EXISTS CompanyHandi (
            soccerID INT NOT NULL,
            companyid INT NOT NULL,
            company VARCHAR(15),
            oripantime VARCHAR(20),
            oripantimest INT ,
            ishighest INT,
            islowest INT,
            isearlyest INT,
            homeoriwater FLOAT ,
            oripan FLOAT ,
            awayoriwater FLOAT,
            homenowwater FLOAT ,
            nowpan FLOAT,
            awaynowwater FLOAT,
            hometeamid INT,
            awayteamid INT,
            PRIMARY KEY (soccerID, companyid))
    """
    cursor.execute(create_table_query)

    creatGamesTabelSQL = """
        CREATE TABLE IF NOT EXISTS Games (
            soccerid       INT              NOT NULL,
            leagueid       INT              NOT NULL,
            league         VARCHAR(15)          NOT NULL,
            starttime      VARCHAR(30)          NOT NULL,
            season         VARCHAR(15)          ,
            round          INT,
            hometeamrank   INT,
            hometeam       VARCHAR(15)          NOT NULL,
            awayteamrank   INT,
            awayteam       VARCHAR(15)          NOT NULL,
            homescore      INT,
            awayscore      INT,
            homehalfscore  INT,
            awayhalfscore  INT,
            aomenoripan    FLOAT                NOT NULL,
            aomennowpan    FLOAT                NOT NULL,
            oriwinodds  FLOAT,
            oritieodds  FLOAT,
            oriloseodds FLOAT,
            nowwinodds  FLOAT,
            nowtieodds  FLOAT,
            nowloseodds FLOAT,
            PRIMARY KEY soccerid)
        """
    cursor.execute(creatGamesTabelSQL)
    creatPanLuDetailTabelSQL = """
            CREATE TABLE IF NOT EXISTS SeasonPanluDetail (
                teamid         INT                  NOT NULL,
                teamname       VARCHAR(15)          NOT NULL,
                leagueid       INT                  NOT NULL,
                league         VARCHAR(15)          NOT NULL,
                season         VARCHAR(15),
                type           INT,
                games          INT,
                upgames        INT,
                drawgames      INT,
                downgames      INT,
                winpans        INT,
                zoupans        INT,
                losepans       INT,
                netwins        INT,
                winrate        FLOAT,
                zourate        FLOAT,
                loserate       FLOAT,
                PRIMARY KEY (teamid, leagueid, season, type))
            """
    cursor.execute(creatPanLuDetailTabelSQL)
    creatPanLuTabelSQL = """
        CREATE TABLE IF NOT EXISTS SeasonPanlu (
            teamid              INT                  NOT NULL,
            teamname            VARCHAR(15)          NOT NULL,
            leagueid            INT                  NOT NULL,
            league              VARCHAR(15)          NOT NULL,
            season              VARCHAR(15),
            rounds              INT,
            allnetwins          INT,
            homenetwins         INT,
            awaynetwins         INT,
            halfnetwins         INT,
            halfhomenetwins     INT,
            halfawaynetwins     INT,
            winrate             FLOAT,
            loserate            FLOAT,
            homewinrate         FLOAT,
            homeloserate        FLOAT,
            awaywinrate         FLOAT,
            awayloserate        FLOAT,
            halfwinrate         FLOAT,
            halfloserate        FLOAT,
            halfhomewinrate     FLOAT,
            halfhomeloserate    FLOAT,
            halfawaywinrate     FLOAT,
            halfawayloserate    FLOAT,
            PRIMARY KEY (teamid, leagueid, season))
        """
    cursor.execute(creatPanLuTabelSQL)

    creatJifenDetailTabelSQL = """
            CREATE TABLE IF NOT EXISTS SeasonJifenDetail (
                teamid         INT                  NOT NULL,
                teamname       VARCHAR(15)          NOT NULL,
                leagueid       INT                  NOT NULL,
                league         VARCHAR(15)          NOT NULL,
                season         VARCHAR(15),
                ranking        INT,
                type           INT,
                games          INT,
                wincount        INT,
                drawcount      INT,
                losecount      INT,
                goalcount        INT,
                losegoalcount        INT,
                goaloffset       INT,
                winrate        FLOAT,
                drawrate        FLOAT,
                loserate       FLOAT,
                avggoal        FLOAT,
                avglosegoal        FLOAT,
                points       INT,
                PRIMARY KEY (teamid, leagueid, season, type))
            """
    cursor.execute(creatJifenDetailTabelSQL)
    creatJifenTabelSQL = """
        CREATE TABLE IF NOT EXISTS SeasonJifen (
                teamid         INT                  NOT NULL,
                teamname       VARCHAR(15)          NOT NULL,
                leagueid       INT                  NOT NULL,
                league         VARCHAR(15)          NOT NULL,
                season         VARCHAR(15),
                ranking        INT,
                games          INT,
                wincount        INT,
                drawcount      INT,
                losecount      INT,
                goalcount        INT,
                losegoalcount        INT,
                goaloffset       INT,
                winrate        FLOAT,
                drawrate        FLOAT,
                loserate       FLOAT,
                avggoal        FLOAT,
                avglosegoal        FLOAT,
                points       INT,
            PRIMARY KEY (teamid, leagueid, season))
        """
    cursor.execute(creatJifenTabelSQL)
    # 关闭连接
    cursor.close()
    conn.close()


def mysql_insert_game_to_season_games(gameobj):
    # if not isinstance(gameobj, FootballGame):
    #     return
    try:
        global conn
        global cursor

        conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database_name
        )
        cursor = conn.cursor()
        # 数据
        data = (
            gameobj.soccerID, gameobj.leaugeid, gameobj.leauge, gameobj.beginTime,
            gameobj.season, 0, gameobj.homeTeamLevel, gameobj.homeTeam, gameobj.friendTeamLevel,
            gameobj.friendTeam, gameobj.allHome, gameobj.allFriend, gameobj.halfHome,
            gameobj.halfFriend, gameobj.orignal_aomenHandi, gameobj.now_aomenHandi,
            0 if gameobj.aomenOddCompany is None else gameobj.aomenOddCompany.orignal_winOdd,
            0 if gameobj.aomenOddCompany is None else gameobj.aomenOddCompany.orignal_drawOdd,
            0 if gameobj.aomenOddCompany is None else gameobj.aomenOddCompany.orignal_loseOdd,
            0 if gameobj.aomenOddCompany is None else gameobj.aomenOddCompany.winOdd,
            0 if gameobj.aomenOddCompany is None else gameobj.aomenOddCompany.drawOdd,
            0 if gameobj.aomenOddCompany is None else gameobj.aomenOddCompany.loseOdd,
            gameobj.orignal_aomenHandi, gameobj.now_aomenHandi,
            0 if gameobj.aomenOddCompany is None else gameobj.aomenOddCompany.orignal_winOdd,
            0 if gameobj.aomenOddCompany is None else gameobj.aomenOddCompany.orignal_drawOdd,
            0 if gameobj.aomenOddCompany is None else gameobj.aomenOddCompany.orignal_loseOdd,
            0 if gameobj.aomenOddCompany is None else gameobj.aomenOddCompany.winOdd,
            0 if gameobj.aomenOddCompany is None else gameobj.aomenOddCompany.drawOdd,
            0 if gameobj.aomenOddCompany is None else gameobj.aomenOddCompany.loseOdd,
            gameobj.season,gameobj.beginTime
        )

        # 插入或更新数据
        insert_query = """
        INSERT INTO Games (soccerid, leagueid, league, starttime, 
                           season, round, hometeamrank, hometeam,
                           awayteamrank, awayteam, homescore, awayscore,
                           homehalfscore, awayhalfscore, aomenoripan, aomennowpan, 
                           oriwinodds, oritieodds, oriloseodds, nowwinodds,
                           nowtieodds, nowloseodds)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE 
            aomenoripan = %s, aomennowpan = %s, oriwinodds = %s, oritieodds = %s, 
            oriloseodds = %s, nowwinodds = %s, nowtieodds = %s, nowloseodds = %s, season = %s, starttime = %s;
        """

        cursor.execute(insert_query, data)

        companies = gameobj.yapanCompanies
        if companies is not None and len(companies) > 0:
            for company in companies:
                if gameobj.soccerID != company.soccerGameId:
                    continue
                # 数据
                data_company = (
                    company.soccerGameId,company.companyID,company.companyTitle,company.oriTimeStr,
                    company.oriTimeStamp,company.highest,company.lowest,company.earlyest,
                    company.orignal_top,company.orignal_Handicap, company.orignal_bottom,company.now_top,
                    company.now_Handicap, company.now_bottom,gameobj.homeTeamId,gameobj.friendTeamId,company.oriTimeStr,
                    company.oriTimeStamp,company.highest,company.lowest,company.earlyest,
                    company.orignal_top,company.orignal_Handicap, company.orignal_bottom,company.now_top,
                    company.now_Handicap, company.now_bottom,gameobj.homeTeamId,gameobj.friendTeamId
                )

                # 插入数据
                insert_company_query = """
                INSERT INTO CompanyHandi (soccerID, companyid, company, oripantime, 
                                          oripantimest, ishighest, islowest, isearlyest,
                                          homeoriwater, oripan, awayoriwater, homenowwater, 
                                          nowpan, awaynowwater, hometeamid, awayteamid)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE 
                    oripantime = %s, oripantimest = %s, ishighest = %s, islowest = %s, 
                    isearlyest = %s, homeoriwater = %s, oripan = %s, awayoriwater = %s,
                    homenowwater = %s, nowpan = %s, awaynowwater = %s, hometeamid = %s, awayteamid= %s;
                """

                cursor.execute(insert_company_query, data_company)


        oddcompanies = gameobj.oddCompanies
        if oddcompanies is not None and len(oddcompanies) > 0:
            for company in oddcompanies:
                if gameobj.soccerID != company.soccerGameId:
                    continue
                # 数据
                data_odd_company = (
                    company.soccerGameId, company.companyID, company.companyTitle, company.orignal_winOdd,
                    company.orignal_drawOdd, company.orignal_loseOdd, company.winOdd, company.drawOdd,
                    company.loseOdd, gameobj.homeTeamId, gameobj.friendTeamId, company.orignal_winOdd,
                    company.orignal_drawOdd, company.orignal_loseOdd, company.winOdd, company.drawOdd,
                    company.loseOdd
                )
                insert_odd_company_query = """
                                INSERT INTO CompanyOdd (soccerID, companyid, company, oriwin, 
                                                          oridraw, orilose, win, draw,
                                                          lose, hometeamid, awayteamid)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                ON DUPLICATE KEY UPDATE 
                                     oriwin = %s, oridraw = %s, orilose = %s, win = %s, draw = %s, lose = %s;
                                """
                # 插入数据
                cursor.execute(insert_odd_company_query, data_odd_company)

        conn.commit()

        print("插入成功")
    except Exception as e:
        print(e)
        conn.rollback()
        traceback.print_exc()
    finally:
        # 关闭连接
        cursor.close()
        conn.close()


def mysql_insert_game_to_disorder(gameobj):
    # if not isinstance(gameobj, FootballGame):
    #     return
    try:
        global conn
        global cursor

        conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database_name
        )
        cursor = conn.cursor()
        # 数据
        data = (
            gameobj.soccerID, gameobj.leaugeid, gameobj.leauge, gameobj.beginTime,
            gameobj.homeTeam, gameobj.friendTeam, gameobj.allHome,gameobj.allFriend,
            gameobj.halfHome, gameobj.halfFriend, gameobj.orignal_aomenHandi, gameobj.now_aomenHandi,
            gameobj.db_ori_pans, gameobj.db_now_pans, gameobj.winhandi,gameobj.oriWinhandi,
            gameobj.orignal_365Handi,gameobj.now_365Handi
        )
        # 插入或更新数据
        insert_query = """
        INSERT IGNORE INTO DisorderPanGames (soccerid, leagueid, league, begintime, 
                                            hometeam, awayteam, homescore, awayscore,
                                            homehalfscore, awayhalfscore, aomenoripan, aomennowpan, 
                                            oripans, nowpans, result, oriResult, 
                                            ori365, now365)
        VALUES (%s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(insert_query, data)

        companies = gameobj.yapanCompanies
        if companies is not None and len(companies) > 0:
            for company in companies:
                if gameobj.soccerID != company.soccerGameId:
                    continue
                # 数据
                data_company = (
                    company.soccerGameId,company.companyID,company.companyTitle,company.oriTimeStr,
                    company.oriTimeStamp,company.highest,company.lowest,company.earlyest,
                    company.orignal_top,company.orignal_Handicap, company.orignal_bottom,company.now_top,
                    company.now_Handicap, company.now_bottom,gameobj.homeTeamId,gameobj.friendTeamId
                )

                # 插入数据
                insert_company_query = """
                INSERT IGNORE INTO CompanyHandi (soccerID, companyid, company, oripantime, 
                    oripantimest, ishighest, islowest, isearlyest,
                    homeoriwater, oripan, awayoriwater, homenowwater, 
                    nowpan, awaynowwater, hometeamid, awayteamid)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s, %s)
                """

                cursor.execute(insert_company_query, data_company)


        conn.commit()

        print("插入成功")
    except Exception as e:
        print(e)
        conn.rollback()
    finally:
        # 关闭连接
        cursor.close()
        conn.close()

def mysql_insert_game_to_seasonpanlu(teamPanlu):
    if teamPanlu is None:
        print('mysql_insert_game_to_seasonpanlu 没有合法数据')
        return
    try:
        global conn
        global cursor

        conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database_name
        )
        cursor = conn.cursor()
        # 数据
        data = (
            teamPanlu.teamID, teamPanlu.teamName, teamPanlu.belongLeagueID, teamPanlu.belongLeagueName,
            teamPanlu.season, teamPanlu.rounds, 0 if teamPanlu.allDetail is None else teamPanlu.allDetail.offset, 0 if teamPanlu.homeDetail is None else teamPanlu.homeDetail.offset,
            0 if teamPanlu.awayDetail is None else teamPanlu.awayDetail.offset, 0 if teamPanlu.halfAllDetail is None else teamPanlu.halfAllDetail.offset,
            0 if teamPanlu.halfHomeDetail is None else teamPanlu.halfHomeDetail.offset, 0 if teamPanlu.halfAllDetail is None else teamPanlu.halfAwayDetail.offset,
            0 if teamPanlu.allDetail is None else teamPanlu.allDetail.winRate, 0 if teamPanlu.allDetail is None else teamPanlu.allDetail.loseRate,
            0 if teamPanlu.homeDetail is None else teamPanlu.homeDetail.winRate, 0 if teamPanlu.homeDetail is None else teamPanlu.homeDetail.loseRate,
            0 if teamPanlu.awayDetail is None else teamPanlu.awayDetail.winRate, 0 if teamPanlu.awayDetail is None else teamPanlu.awayDetail.loseRate,
            0 if teamPanlu.halfAllDetail is None else teamPanlu.halfAllDetail.winRate, 0 if teamPanlu.halfAllDetail is None else teamPanlu.halfAllDetail.loseRate,
            0 if teamPanlu.halfHomeDetail is None else teamPanlu.halfHomeDetail.winRate, 0 if teamPanlu.halfHomeDetail is None else teamPanlu.halfHomeDetail.loseRate,
            0 if teamPanlu.halfAwayDetail is None else teamPanlu.halfAwayDetail.winRate, 0 if teamPanlu.halfAwayDetail is None else teamPanlu.halfAwayDetail.loseRate,
            teamPanlu.rounds, 0 if teamPanlu.allDetail is None else teamPanlu.allDetail.offset,
            0 if teamPanlu.homeDetail is None else teamPanlu.homeDetail.offset,
            0 if teamPanlu.awayDetail is None else teamPanlu.awayDetail.offset,
            0 if teamPanlu.halfAllDetail is None else teamPanlu.halfAllDetail.offset,
            0 if teamPanlu.halfHomeDetail is None else teamPanlu.halfHomeDetail.offset,
            0 if teamPanlu.halfAllDetail is None else teamPanlu.halfAwayDetail.offset,
            0 if teamPanlu.allDetail is None else teamPanlu.allDetail.winRate,
            0 if teamPanlu.allDetail is None else teamPanlu.allDetail.loseRate,
            0 if teamPanlu.homeDetail is None else teamPanlu.homeDetail.winRate,
            0 if teamPanlu.homeDetail is None else teamPanlu.homeDetail.loseRate,
            0 if teamPanlu.awayDetail is None else teamPanlu.awayDetail.winRate,
            0 if teamPanlu.awayDetail is None else teamPanlu.awayDetail.loseRate,
            0 if teamPanlu.halfAllDetail is None else teamPanlu.halfAllDetail.winRate,
            0 if teamPanlu.halfAllDetail is None else teamPanlu.halfAllDetail.loseRate,
            0 if teamPanlu.halfHomeDetail is None else teamPanlu.halfHomeDetail.winRate,
            0 if teamPanlu.halfHomeDetail is None else teamPanlu.halfHomeDetail.loseRate,
            0 if teamPanlu.halfAwayDetail is None else teamPanlu.halfAwayDetail.winRate,
            0 if teamPanlu.halfAwayDetail is None else teamPanlu.halfAwayDetail.loseRate
        )
        # 插入或更新数据
        insert_query = """
        INSERT INTO SeasonPanlu (teamid, teamname, leagueid, league, 
                                        season, rounds, allnetwins, homenetwins,
                                        awaynetwins, halfnetwins, halfhomenetwins, halfawaynetwins, 
                                        winrate, loserate, homewinrate, homeloserate, 
                                        awaywinrate, awayloserate, halfwinrate, halfloserate,
                                        halfhomewinrate, halfhomeloserate, halfawaywinrate,halfawayloserate)
        VALUES (%s, %s, %s, %s, %s, %s, %s,%s, 
                %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE 
            rounds = %s, allnetwins = %s, homenetwins = %s, awaynetwins = %s, 
            halfnetwins = %s, halfhomenetwins = %s, halfawaynetwins = %s, winrate = %s, 
            loserate = %s, homewinrate = %s, homeloserate = %s, awaywinrate = %s, 
            awayloserate = %s, halfwinrate = %s, halfloserate = %s, halfhomewinrate = %s, 
            halfhomeloserate = %s, halfawaywinrate = %s, halfawayloserate = %s;
        """

        cursor.execute(insert_query, data)

        detail = teamPanlu.allDetail
        if detail is not None:
            # 数据
            data_detail = (
                detail.teamID, detail.teamName, detail.belongLeagueID, detail.belongLeagueName,
                detail.season, detail.type, detail.numberOfGame, detail.upNumberOfGame, detail.drawNumberOfGame,
                detail.downNumberOfGame, detail.winNumberOfGame, detail.zouNumberOfGame, detail.loseNumberOfGame,
                detail.offset, detail.winRate, detail.drawRate, detail.loseRate,detail.numberOfGame, detail.upNumberOfGame, detail.drawNumberOfGame,
                detail.downNumberOfGame, detail.winNumberOfGame, detail.zouNumberOfGame, detail.loseNumberOfGame,
                detail.offset, detail.winRate, detail.drawRate, detail.loseRate
            )
            # 插入数据
            insert_detail_query = """
                INSERT INTO SeasonPanluDetail (teamid, teamname, leagueid, league, 
                                                      season, type, games, upgames, drawgames,
                                                      downgames, winpans, zoupans, losepans,
                                                      netwins, winrate, zourate, loserate)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE 
                games = %s, upgames = %s, drawgames = %s, downgames = %s, 
                winpans = %s, zoupans = %s, losepans = %s, netwins = %s, 
                winrate = %s, zourate = %s, loserate = %s
                """
            cursor.execute(insert_detail_query, data_detail)

        detail = teamPanlu.homeDetail
        if detail is not None:
            # 数据
            data_detail = (
                detail.teamID, detail.teamName, detail.belongLeagueID, detail.belongLeagueName,
                detail.season, detail.type, detail.numberOfGame, detail.upNumberOfGame, detail.drawNumberOfGame,
                detail.downNumberOfGame, detail.winNumberOfGame, detail.zouNumberOfGame, detail.loseNumberOfGame,
                detail.offset, detail.winRate, detail.drawRate, detail.loseRate,detail.numberOfGame, detail.upNumberOfGame, detail.drawNumberOfGame,
                detail.downNumberOfGame, detail.winNumberOfGame, detail.zouNumberOfGame, detail.loseNumberOfGame,
                detail.offset, detail.winRate, detail.drawRate, detail.loseRate
            )
            # 插入数据
            insert_detail_query = """
                INSERT INTO SeasonPanluDetail (teamid, teamname, leagueid, league, 
                                                      season, type, games, upgames, drawgames,
                                                      downgames, winpans, zoupans, losepans,
                                                      netwins, winrate, zourate, loserate)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE 
                games = %s, upgames = %s, drawgames = %s, downgames = %s, 
                winpans = %s, zoupans = %s, losepans = %s, netwins = %s, 
                winrate = %s, zourate = %s, loserate = %s
                """
            cursor.execute(insert_detail_query, data_detail)

        detail = teamPanlu.awayDetail
        if detail is not None:
            # 数据
            data_detail = (
                detail.teamID, detail.teamName, detail.belongLeagueID, detail.belongLeagueName,
                detail.season, detail.type, detail.numberOfGame, detail.upNumberOfGame, detail.drawNumberOfGame,
                detail.downNumberOfGame, detail.winNumberOfGame, detail.zouNumberOfGame, detail.loseNumberOfGame,
                detail.offset, detail.winRate, detail.drawRate, detail.loseRate,detail.numberOfGame, detail.upNumberOfGame, detail.drawNumberOfGame,
                detail.downNumberOfGame, detail.winNumberOfGame, detail.zouNumberOfGame, detail.loseNumberOfGame,
                detail.offset, detail.winRate, detail.drawRate, detail.loseRate
            )
            # 插入数据
            insert_detail_query = """
                INSERT INTO SeasonPanluDetail (teamid, teamname, leagueid, league, 
                                                      season, type, games, upgames, drawgames,
                                                      downgames, winpans, zoupans, losepans,
                                                      netwins, winrate, zourate, loserate)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE 
                games = %s, upgames = %s, drawgames = %s, downgames = %s, 
                winpans = %s, zoupans = %s, losepans = %s, netwins = %s, 
                winrate = %s, zourate = %s, loserate = %s
                """
            cursor.execute(insert_detail_query, data_detail)

        detail = teamPanlu.halfAllDetail
        if detail is not None:
            # 数据
            data_detail = (
                detail.teamID, detail.teamName, detail.belongLeagueID, detail.belongLeagueName,
                detail.season, detail.type, detail.numberOfGame, detail.upNumberOfGame, detail.drawNumberOfGame,
                detail.downNumberOfGame, detail.winNumberOfGame, detail.zouNumberOfGame, detail.loseNumberOfGame,
                detail.offset, detail.winRate, detail.drawRate, detail.loseRate,detail.numberOfGame, detail.upNumberOfGame, detail.drawNumberOfGame,
                detail.downNumberOfGame, detail.winNumberOfGame, detail.zouNumberOfGame, detail.loseNumberOfGame,
                detail.offset, detail.winRate, detail.drawRate, detail.loseRate
            )
            # 插入数据
            insert_detail_query = """
                INSERT INTO SeasonPanluDetail (teamid, teamname, leagueid, league, 
                                                      season, type, games, upgames, drawgames,
                                                      downgames, winpans, zoupans, losepans,
                                                      netwins, winrate, zourate, loserate)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE 
                games = %s, upgames = %s, drawgames = %s, downgames = %s, 
                winpans = %s, zoupans = %s, losepans = %s, netwins = %s, 
                winrate = %s, zourate = %s, loserate = %s
                """
            cursor.execute(insert_detail_query, data_detail)

        detail = teamPanlu.halfHomeDetail
        if detail is not None:
            # 数据
            data_detail = (
                detail.teamID, detail.teamName, detail.belongLeagueID, detail.belongLeagueName,
                detail.season, detail.type, detail.numberOfGame, detail.upNumberOfGame, detail.drawNumberOfGame,
                detail.downNumberOfGame, detail.winNumberOfGame, detail.zouNumberOfGame, detail.loseNumberOfGame,
                detail.offset, detail.winRate, detail.drawRate, detail.loseRate,detail.numberOfGame, detail.upNumberOfGame, detail.drawNumberOfGame,
                detail.downNumberOfGame, detail.winNumberOfGame, detail.zouNumberOfGame, detail.loseNumberOfGame,
                detail.offset, detail.winRate, detail.drawRate, detail.loseRate
            )
            # 插入数据
            insert_detail_query = """
                INSERT INTO SeasonPanluDetail (teamid, teamname, leagueid, league, 
                                                      season, type, games, upgames, drawgames,
                                                      downgames, winpans, zoupans, losepans,
                                                      netwins, winrate, zourate, loserate)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE 
                games = %s, upgames = %s, drawgames = %s, downgames = %s, 
                winpans = %s, zoupans = %s, losepans = %s, netwins = %s, 
                winrate = %s, zourate = %s, loserate = %s
                """
            cursor.execute(insert_detail_query, data_detail)
        detail = teamPanlu.halfAwayDetail
        if detail is not None:
            # 数据
            data_detail = (
                detail.teamID, detail.teamName, detail.belongLeagueID, detail.belongLeagueName,
                detail.season, detail.type, detail.numberOfGame, detail.upNumberOfGame, detail.drawNumberOfGame,
                detail.downNumberOfGame, detail.winNumberOfGame, detail.zouNumberOfGame, detail.loseNumberOfGame,
                detail.offset, detail.winRate, detail.drawRate, detail.loseRate,detail.numberOfGame, detail.upNumberOfGame, detail.drawNumberOfGame,
                detail.downNumberOfGame, detail.winNumberOfGame, detail.zouNumberOfGame, detail.loseNumberOfGame,
                detail.offset, detail.winRate, detail.drawRate, detail.loseRate
            )
            # 插入数据
            insert_detail_query = """
                INSERT INTO SeasonPanluDetail (teamid, teamname, leagueid, league, 
                                                      season, type, games, upgames, drawgames,
                                                      downgames, winpans, zoupans, losepans,
                                                      netwins, winrate, zourate, loserate)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE 
                games = %s, upgames = %s, drawgames = %s, downgames = %s, 
                winpans = %s, zoupans = %s, losepans = %s, netwins = %s, 
                winrate = %s, zourate = %s, loserate = %s
                """
            cursor.execute(insert_detail_query, data_detail)

        conn.commit()

    except Exception as e:
        print(e)
        conn.rollback()
    finally:
        # 关闭连接
        cursor.close()
        conn.close()

def mysql_insert_game_to_seasonjifen(teamPoints):
    if teamPoints is None:
        print('mysql_insert_game_to_seasonjifen 没有合法数据')
        return
    try:
        global conn
        global cursor

        conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database_name
        )
        cursor = conn.cursor()
        # 数据
        data = (
            teamPoints.teamID,    teamPoints.teamName,     teamPoints.leagueid,  teamPoints.league,
            teamPoints.season,    teamPoints.ranking,      teamPoints.gamecount, teamPoints.winCount,
            teamPoints.drawCount, teamPoints.loseCount,    teamPoints.goalcount, teamPoints.losegoalcount,
            teamPoints.goaloffset,teamPoints.winRate,      teamPoints.drawRate,  teamPoints.loseRate,
            teamPoints.avgGoal,   teamPoints.avgLostGoal,  teamPoints.points,    teamPoints.ranking,
            teamPoints.gamecount, teamPoints.winCount,     teamPoints.drawCount, teamPoints.loseCount,
            teamPoints.goalcount, teamPoints.losegoalcount,teamPoints.goaloffset,teamPoints.winRate,
            teamPoints.drawRate,  teamPoints.loseRate,     teamPoints.avgGoal,   teamPoints.avgLostGoal,
            teamPoints.points
        )
        # 插入或更新数据


        insert_query = """
        INSERT INTO SeasonJifen (teamid, teamname, leagueid, league,
                                season, ranking, games, wincount,
                                drawcount, losecount, goalcount, losegoalcount,
                                goaloffset, winrate, drawrate, loserate,
                                avggoal, avglosegoal, points)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 
                %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s)
        ON DUPLICATE KEY UPDATE 
            ranking = %s, games = %s, wincount = %s, drawcount = %s, 
            losecount = %s, goalcount = %s, losegoalcount = %s, goaloffset = %s,
            winrate = %s, drawrate = %s, loserate = %s, avggoal = %s,
            avglosegoal = %s, points = %s
        """

        cursor.execute(insert_query, data)

        detail = teamPoints.homePoints
        if detail is not None:
            # 数据
            data_detail = (
                detail.teamID, detail.teamName, detail.leagueid, detail.league,
                detail.season, detail.ranking, detail.gamecount, detail.type,
                detail.winCount, detail.drawCount, detail.loseCount, detail.goalcount,
                detail.losegoalcount, detail.goaloffset, detail.winRate, detail.drawRate,
                detail.loseRate, detail.avgGoal, detail.avgLostGoal, detail.points,
                detail.ranking, detail.gamecount, detail.winCount, detail.drawCount,
                detail.loseCount, detail.goalcount, detail.losegoalcount, detail.goaloffset,
                detail.winRate, detail.drawRate, detail.loseRate, detail.avgGoal,
                detail.avgLostGoal, detail.points
            )
            # 插入数据
            insert_detail_query = """
                INSERT INTO SeasonJifenDetail (teamid, teamname, leagueid, league,
                                                season, ranking, games, type,
                                                wincount, drawcount, losecount, goalcount, 
                                                losegoalcount, goaloffset, winrate, drawrate, 
                                                loserate, avggoal, avglosegoal, points)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    ranking = %s, games = %s, wincount = %s, drawcount = %s,
                    losecount = %s, goalcount = %s, losegoalcount = %s, goaloffset = %s, 
                    winrate = %s, drawrate = %s, loserate = %s, avggoal = %s, 
                    avglosegoal = %s, points = %s
                """
            cursor.execute(insert_detail_query, data_detail)

        detail = teamPoints.awayPoints
        if detail is not None:
            # 数据
            data_detail = (
                detail.teamID, detail.teamName, detail.leagueid, detail.league,
                detail.season, detail.ranking, detail.gamecount, detail.type,
                detail.winCount, detail.drawCount, detail.loseCount, detail.goalcount,
                detail.losegoalcount, detail.goaloffset, detail.winRate, detail.drawRate,
                detail.loseRate, detail.avgGoal, detail.avgLostGoal, detail.points,
                detail.ranking, detail.gamecount, detail.winCount, detail.drawCount,
                detail.loseCount, detail.goalcount, detail.losegoalcount, detail.goaloffset,
                detail.winRate, detail.drawRate, detail.loseRate, detail.avgGoal,
                detail.avgLostGoal, detail.points
            )
            # 插入数据
            insert_detail_query = """
                INSERT INTO SeasonJifenDetail (teamid, teamname, leagueid, league,
                                                season, ranking, games, type,
                                                wincount, drawcount, losecount, goalcount, 
                                                losegoalcount, goaloffset, winrate, drawrate, 
                                                loserate, avggoal, avglosegoal, points)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    ranking = %s, games = %s, wincount = %s, drawcount = %s,
                    losecount = %s, goalcount = %s, losegoalcount = %s, goaloffset = %s, 
                    winrate = %s, drawrate = %s, loserate = %s, avggoal = %s, 
                    avglosegoal = %s, points = %s
                """
            cursor.execute(insert_detail_query, data_detail)

        detail = teamPoints.halfPoints
        if detail is not None:
            # 数据
            data_detail = (
                detail.teamID, detail.teamName, detail.leagueid, detail.league,
                detail.season, detail.ranking, detail.gamecount, detail.type,
                detail.winCount, detail.drawCount, detail.loseCount, detail.goalcount,
                detail.losegoalcount, detail.goaloffset, detail.winRate, detail.drawRate,
                detail.loseRate, detail.avgGoal, detail.avgLostGoal, detail.points,
                detail.ranking, detail.gamecount, detail.winCount, detail.drawCount,
                detail.loseCount, detail.goalcount, detail.losegoalcount, detail.goaloffset,
                detail.winRate, detail.drawRate, detail.loseRate, detail.avgGoal,
                detail.avgLostGoal, detail.points
            )
            # 插入数据
            insert_detail_query = """
                INSERT INTO SeasonJifenDetail (teamid, teamname, leagueid, league,
                                                season, ranking, games, type,
                                                wincount, drawcount, losecount, goalcount, 
                                                losegoalcount, goaloffset, winrate, drawrate, 
                                                loserate, avggoal, avglosegoal, points)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    ranking = %s, games = %s, wincount = %s, drawcount = %s,
                    losecount = %s, goalcount = %s, losegoalcount = %s, goaloffset = %s, 
                    winrate = %s, drawrate = %s, loserate = %s, avggoal = %s, 
                    avglosegoal = %s, points = %s
                """
            cursor.execute(insert_detail_query, data_detail)

        detail = teamPoints.halfHomePoints
        if detail is not None:
            # 数据
            data_detail = (
                detail.teamID, detail.teamName, detail.leagueid, detail.league,
                detail.season, detail.ranking, detail.gamecount, detail.type,
                detail.winCount, detail.drawCount, detail.loseCount, detail.goalcount,
                detail.losegoalcount, detail.goaloffset, detail.winRate, detail.drawRate,
                detail.loseRate, detail.avgGoal, detail.avgLostGoal, detail.points,
                detail.ranking, detail.gamecount, detail.winCount, detail.drawCount,
                detail.loseCount, detail.goalcount, detail.losegoalcount, detail.goaloffset,
                detail.winRate, detail.drawRate, detail.loseRate, detail.avgGoal,
                detail.avgLostGoal, detail.points
            )
            # 插入数据
            insert_detail_query = """
                INSERT INTO SeasonJifenDetail (teamid, teamname, leagueid, league,
                                                season, ranking, games, type,
                                                wincount, drawcount, losecount, goalcount, 
                                                losegoalcount, goaloffset, winrate, drawrate, 
                                                loserate, avggoal, avglosegoal, points)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    ranking = %s, games = %s, wincount = %s, drawcount = %s,
                    losecount = %s, goalcount = %s, losegoalcount = %s, goaloffset = %s, 
                    winrate = %s, drawrate = %s, loserate = %s, avggoal = %s, 
                    avglosegoal = %s, points = %s
                """
            cursor.execute(insert_detail_query, data_detail)

        detail = teamPoints.halfAwayPoints
        if detail is not None:
            # 数据
            data_detail = (
                detail.teamID, detail.teamName, detail.leagueid, detail.league,
                detail.season, detail.ranking, detail.gamecount, detail.type,
                detail.winCount, detail.drawCount, detail.loseCount, detail.goalcount,
                detail.losegoalcount, detail.goaloffset, detail.winRate, detail.drawRate,
                detail.loseRate, detail.avgGoal, detail.avgLostGoal, detail.points,
                detail.ranking, detail.gamecount, detail.winCount, detail.drawCount,
                detail.loseCount, detail.goalcount, detail.losegoalcount, detail.goaloffset,
                detail.winRate, detail.drawRate, detail.loseRate, detail.avgGoal,
                detail.avgLostGoal, detail.points
            )
            # 插入数据
            insert_detail_query = """
                INSERT INTO SeasonJifenDetail (teamid, teamname, leagueid, league,
                                                season, ranking, games, type,
                                                wincount, drawcount, losecount, goalcount, 
                                                losegoalcount, goaloffset, winrate, drawrate, 
                                                loserate, avggoal, avglosegoal, points)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    ranking = %s, games = %s, wincount = %s, drawcount = %s,
                    losecount = %s, goalcount = %s, losegoalcount = %s, goaloffset = %s, 
                    winrate = %s, drawrate = %s, loserate = %s, avggoal = %s, 
                    avglosegoal = %s, points = %s
                """
            cursor.execute(insert_detail_query, data_detail)

        conn.commit()

        print("插入成功")
    except Exception as e:
        print(e)
        conn.rollback()
        traceback.print_exc()
    finally:
        # 关闭连接
        cursor.close()
        conn.close()

if __name__ == '__main__':
    # creatDataBase()
    creatTable()