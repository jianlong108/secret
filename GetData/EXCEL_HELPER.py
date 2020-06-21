#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import xlwt
import xlrd
from  xlutils.copy import copy

header = [u'球队', u'联赛', '2018-2019', '2017-2018', '2016-2017', '2015-2016',
              '2014-2015', '2013-2014', '2012-2013', '2011-2012', '2010-2011'
        , '2009-2010', '2008-2009', '2007-2008', '2006-2007', '2005-2006', '2004-2005','2003-2004']

def set_style(name, height, bold=False):
    style = xlwt.XFStyle()  # 初始化样式

    font = xlwt.Font()  # 为样式创建字体
    font.name = name
    font.bold = bold
    font.color_index = 4
    font.height = height

    style.font = font
    return style

def creat_excel():
    location = os.path.expanduser('~/Desktop/winPan.xls')
    workbook = xlwt.Workbook(encoding='utf-8')
    winPanSheet = workbook.add_sheet('winPan')
    for i in range(len(header)):
        winPanSheet.write(0, i, header[i], set_style('Times New Roman', 220, True))
    workbook.save(location)

def write_excel(teamList):
    # 创建工作簿
    location = os.path.expanduser('~/Desktop/winPan.xls')

    workbook = xlrd.open_workbook(location)
    index = workbook.sheets()[0].nrows

    wb = copy(workbook)
    winPanSheet = wb.get_sheet('winPan')

    for teamTuple in teamList:
        for i in range(len(header)):
            # winPanSheet.write(index, i, teamTuple[i], set_style('Times New Roman', 220, True))
            winPanSheet.write(index, i, teamTuple[i])
        index += 1
    wb.save(location)

creat_excel()