#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
    except TypeError as e:
        print e
        pass
    finally:
        pass

def isdigitalAndPoint(unitstr):
    return str.isdigit or ('.' is unitstr)
