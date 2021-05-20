#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import os
import pymysql.cursors

# db = pymysql.connect(host='localhost',user='dalong',password='long',port=3306)
db = pymysql.connect("localhost", "dalong", "long", charset='utf8' )


cur = db.cursor()
cur.execute("SELECT VERSION()")

# cur.execute("SELECT * FROM pages WHERE id=1")
print cur.fetchone()

cur.close()
db.close()
