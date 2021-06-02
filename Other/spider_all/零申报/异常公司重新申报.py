# coding:utf-8
import pymysql
import requests
import json
data = json.loads(input('请输:'))
data = data['data']['pageList']
data = [i['id'] for i in data]
print(data)
print(len(data))
db = pymysql.connect(host="192.168.2.99", user="root", password='BOOT-xwork1024', database="prod_spider", port=3306)
cursor = db.cursor()

for i in data:
    sql = "update tax_visit set tax_status=5 where declare_id = {}".format(i)
    cursor.execute(sql)

db.commit()
db.close()