#!/usr/bin/env python
# -*- coding: utf-8 -*-

from BEAUTIFUL_SOUP_HELPER import SoupHelper,isTagClass

instance = SoupHelper('http://www.310win.com/info/match/AllScore.aspx')
list = instance.gethtmllistwithlabel('table',options = {'id':'live'})
print(instance)