import time,re,json
import requests
from sqlalchemy import Column, String, create_engine, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# 创建对象的基类:
Base = declarative_base()
# 定义User对象:
class Medicine(Base):
    # 表的名字:
    __tablename__ = 'revoke_model'

    # 表的结构:
    id = Column(Integer(), primary_key=True, autoincrement=True)
    company_name = Column(String(256))

# 初始化数据库连接:
engine = create_engine('mysql+pymysql://root:BOOT-xwork1024@192.168.2.97:3306/spider')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
# 创建session对象:
session = DBSession()

data = session.query(Medicine).all()
data = [i.company_name for i in data][:50000]
print(len(data))
print(data)
exit()

import pymysql

db = pymysql.connect(host='192.168.2.97', password='BOOT-xwork1024', database='spider', user='root')
cursor = db.cursor()
sql = 'select * from revoke_model limit 50000'
cursor.execute(sql)
data = cursor.fetchall()
data = [i[1] for i in data]
print(data)

with open('spider_tyc/hz_data_50000.json', 'w', encoding='utf-8')as fp:
    fp.write(json.dumps(data,ensure_ascii=False))