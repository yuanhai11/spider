# coding:utf-8
import time
import re
import json
import requests, pymysql
from sqlalchemy import Column, String, create_engine, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# 创建对象的基类:
Base = declarative_base()
# 定义User对象:
class Medicine(Base):
    # 表的名字:
    __tablename__ = 'spider_58_company'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    company = Column(String(256))
    city = Column(String(256))

# 初始化数据库连接:
engine = create_engine('mysql+pymysql://root:BOOT-xwork1024@192.168.2.97:3306/spider')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
# 创建session对象:
session = DBSession()

def insert():
    import os,json
    lists = os.listdir('company_hz')
    print(lists)
    number = []
    for i in lists:
        with open('company_hz/{}'.format(i),encoding='utf-8')as fp:
            content = json.loads(fp.read())
            number+=content
    print(len(number))
    number = list(set(number))
    print(len(number))
    # exit()
    for n in number:
        me = Medicine(company=n,city='hz')
        session.add(me)
    session.commit()

if __name__ == '__main__':
    insert()
