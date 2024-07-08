#!/usr/bin/env python
# -*- coding: utf-8 -*-

def switchHandicap(Handicap):
    try:
        if Handicap == '受让平手/半球':
            return -0.25
        elif Handicap == '受让半球':
            return -0.5
        elif Handicap == '受让半球/一球':
            return -0.75
        elif Handicap == '受让一球':
            return -1.0
        elif Handicap == '受让一球/一球半':
            return -1.25
        elif Handicap == '受让球半':
            return -1.5
        elif Handicap == '受让一球半/两球':
            return -1.75
        elif Handicap == '受让两球':
            return -2.0
        elif Handicap == '受让两球/两球半':
            return -2.25
        elif Handicap == '受让两球半':
            return -2.5
        elif Handicap == '受让两球半/三球':
            return -2.75
        elif Handicap == '受让三球':
            return -3.0
        elif Handicap == '受让三球/三球半':
            return -3.25
        elif Handicap == '受让三球半':
            return -3.5
        elif Handicap == '受让三球半/四球':
            return -3.75
        elif Handicap == '平手':
            return 0
        elif Handicap == '平手/半球':
            return 0.25
        elif Handicap == '半球':
            return 0.5
        elif Handicap == '半球/一球':
            return 0.75
        elif Handicap == '一球':
            return 1.0
        elif Handicap == '一球/球半':
            return 1.25
        elif Handicap == '一球/球半':
            return 1.25
        elif Handicap == '球半':
            return 1.5
        elif Handicap == '一球半':
            return 1.5
        elif Handicap == '球半/两球':
            return 1.75
        elif Handicap == '球半/两球':
            return 1.75
        elif Handicap == '两球':
            return 2.0
        elif Handicap == '两/两半':
            return 2.25
        elif Handicap == '两球/两半':
            return 2.25
        elif Handicap == '两球半':
            return 2.5
        elif Handicap == '两半/三':
            return 2.75
        elif Handicap == '两半/三球':
            return 2.75
        elif Handicap == '三球':
            return 3.0
        elif Handicap == '三球/三半':
            return 3.25
        elif Handicap == '三球/三球半':
            return 3.25
        elif Handicap == '三球半':
            return 3.5
        elif Handicap == '三球半/四':
            return 3.75
        elif Handicap == '三球半/四球':
            return 3.75
        else:
            raise Exception(f'不支持的盘口:{Handicap}')
    except TypeError as e:
        print(e)
        pass
    finally:
        pass

# def isdigitalAndPoint(unitstr):
#     return str.isdigit or ('.' is unitstr)
