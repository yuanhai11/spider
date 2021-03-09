#coding:utf-8
import re
import time,pymysql
import requests,json
from lxml import etree
from sqlalchemy import Column, String, create_engine,Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# 创建对象的基类:
Base = declarative_base()
# 定义User对象:
class Medicine(Base):
    # 表的名字:
    __tablename__ = 'spider_abnormal'

    # 表的结构:
    id = Column(Integer(), primary_key=True,autoincrement=True)
    company_name = Column(String(256))
    abnormal_date = Column(String(256))
    tax_status = Column(String(256))

# 初始化数据库连接:
engine = create_engine('mysql+pymysql://root:BOOT-xwork1024@192.168.2.97:3306/spider')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
# 创建session对象:
session = DBSession()

def main():
    sum = []
    for i in range(1,33):
        with open(r'D:\projects\Spider\local_spider\Other\spider_all\Certificate\cata_4928_json/cata_4928_{}.json'.format(i),encoding='utf-8')as fp:
            content = json.loads(fp.read())[1:]
            sum+=content
    print(len(sum))
    for d in sum:
        print(d)
        medicine = Medicine(company_name=d[5],abnormal_date=d[3])
        session.add(medicine)
    session.commit()

if __name__ == '__main__':
    main()
