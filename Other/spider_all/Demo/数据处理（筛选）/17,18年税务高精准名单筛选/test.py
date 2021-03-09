from xlrd import open_workbook
import re
import time
import requests,pymysql
import base64
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pksc1_v1_5
from Crypto.PublicKey import RSA
from sqlalchemy import Column, String, create_engine,Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# 创建对象的基类:
Base = declarative_base()
# 定义User对象:

class Medicine(Base):
    # 表的名字:
    __tablename__ = 'sheet1'
    id = Column(Integer(), primary_key=True,autoincrement=True)
    a = Column(String(256))
    b = Column(String(256))
    c = Column(String(256))
    d = Column(String(256))
    e = Column(String(256))
    f = Column(String(256))

# 初始化数据库连接:
engine = create_engine('mysql+pymysql://root:BOOT-xwork1024@192.168.2.97:3306/spider')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
# 创建session对象:
session = DBSession()

workbook = open_workbook('17、18年税务高精准名单.xlsx')  # 打开excel文件
sum = []


for index in range(1,19):# 19
    sheet2 = workbook.sheet_by_index(index)
    print(sheet2.nrows)
    for i in range(1, sheet2.nrows):
        a = sheet2.cell(i, 0).value
        if a in sum:
            continue
        b = sheet2.cell(i, 1).value
        c = sheet2.cell(i, 2).value
        if '-' not in str(c):
            from datetime import datetime
            from xlrd import xldate_as_tuple
            c = datetime(*xldate_as_tuple(c, 0))
            c = c.strftime('%Y-%m-%d')

        d = sheet2.cell(i, 3).value
        e = sheet2.cell(i, 4).value
        f = str(sheet2.cell(i, 5).value).replace('.0','')
        if '富阳' in e or '桐庐' in e or '建德' in e or '淳安' in e or '-' in f:
            continue
        else:
            with open('../data.txt', 'a', encoding='utf-8')as fp:
                fp.write(str(index))
                fp.write(str(a))
            print(index,a,b,c,d,e,f)
            # medi = Medicine(a=a,b=b,c=c,d=d,e=e,f=f)
            # session.add(medi)
            # sum.append(a)
# session.commit()
    # exit()