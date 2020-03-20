#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import pymysql

conn = pymysql.connect(host="127.0.0.1", user="speed", password="itazhe123", database="speed", charset="utf8")

uname = 'azhe'
upass = '1234567890'
phone = '17740506387'
email = 'miraclebo@fixmail.com'

cur = conn.cursor()
cur.execute("INSERT INTO user VALUES (default, %s, md5(%s), %s, %s, sysdate(), sysdate(), '2', '1')", (uname, uname + upass, phone, email))
cur.close()
conn.commit()
