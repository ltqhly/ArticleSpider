# -*- coding: utf-8 -*-

import psycopg2
# 数据库连接参数
conn = psycopg2.connect(database="Article", user="liutanqi", password="", host="127.0.0.1", port="5432")
cur = conn.cursor()

cur.execute("SELECT title FROM articale;")
rows = cur.fetchall()# all rows in table

for a in rows:
    print a[0]
conn.commit()
cur.close()
conn.close()