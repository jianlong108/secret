#!/usr/bin/env python
# -*- coding: utf-8 -*-

def switchHandicap(Handicap):
    try:
        if Handicap == '受平/半':
            return -0.25
        elif Handicap == '受半球':
            return -0.5
        elif Handicap == '受半/一':
            return -0.75
        elif Handicap == '受一球':
            return -1.0
        elif Handicap == '受一/球半':
            return -1.25
        elif Handicap == '受球半':
            return -1.5
        elif Handicap == '受球半/两':
            return -1.75
        elif Handicap == '受两球':
            return -2.0
        elif Handicap == '受两/两半':
            return -2.25
        elif Handicap == '受两球半':
            return -2.5
        elif Handicap == '受两半/三':
            return -2.75
        elif Handicap == '受三球':
            return -3.0
        elif Handicap == '受三/三半':
            return -3.25
        elif Handicap == '受三球半':
            return -3.5
        elif Handicap == '受三半/四':
            return -3.75
        elif Handicap == '平手':
            return 0
        elif Handicap == '平/半':
            return 0.25
        elif Handicap == '半球':
            return 0.5
        elif Handicap == '半/一':
            return 0.75
        elif Handicap == '一球':
            return 1.0
        elif Handicap == '一/球半':
            return 1.25
        elif Handicap == '球半':
            return 1.5
        elif Handicap == '球半/两':
            return 1.75
        elif Handicap == '两球':
            return 2.0
        elif Handicap == '两/两半':
            return 2.25
        elif Handicap == '两球半':
            return 2.5
        elif Handicap == '两半/三':
            return 2.75
        elif Handicap == '三球':
            return 3.0
        elif Handicap == '三球/三半':
            return 3.25
        elif Handicap == '三球半':
            return 3.5
        elif Handicap == '三球半/四':
            return 3.75
        else:
            return 108
    except TypeError as e:
        print e
        pass
    finally:
        pass

def isdigitalAndPoint(unitstr):
    return str.isdigit or ('.' is unitstr)
