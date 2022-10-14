import time, re, json
from lxml import etree
from sqlalchemy import Column, String, create_engine, Integer, and_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import requests
import execjs

# 创建对象的基类:
Base = declarative_base()


class Medicine(Base):
    # 表的名字:
    __tablename__ = 'company_pay_tax'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    company_name = Column(String(256))
    company_id = Column(String(256))
    tax_type = Column(Integer())
    tax_date = Column(String(256))
    pay_base = Column(String(256))
    pay_person_num = Column(String(256))
    pay_current_tax = Column(String(256))

    gmt_created = Column(String(256))
    gmt_updated = Column(String(256))


class Account(Base):
    # 表的名字:
    __tablename__ = 'account_setting'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    accout_name = Column(String(256))
    company_id = Column(String(256))


# 初始化数据库连接:
engine = create_engine('mysql+pymysql://root:BOOT-xwork1024@192.168.2.96:3306/zl_saas')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
# 创建session对象:
session = DBSession()

# 创建session对象:
session_company_info = DBSession()
proxys = []

import re, json


def main():
    with open('1.txt', encoding='utf-8')as d:
        c = d.readlines()
        print(c)
        for cc in c:
            ss = re.findall(
                r"'company_name': '(.*?)', 'pay_base': '(.*?)', 'pay_person_num': '(.*?)', 'pay_current_tax': '(.*?)'",
                cc)
            company_name = ss[0][0]
            tax_date = ""
            company_id = 0
            tax_type = 0
            pay_base = ss[0][1]
            pay_person_num = ss[0][2]
            pay_current_tax = ss[0][3]
            acount = session.query(Account).filter(Account.accout_name == company_name).first()
            if acount:
                company_id = acount.company_id
            print(company_id, company_name, tax_date, pay_base, pay_person_num, pay_current_tax)
            me = Medicine(company_name=company_name, company_id=company_id, tax_date=tax_date, pay_base=pay_base,
                          tax_type=tax_type,
                          pay_person_num=pay_person_num, pay_current_tax=pay_current_tax,
                          gmt_created="2022-09-22 13:30:12",
                          gmt_updated="2022-09-22 13:30:12")

            session.add(me)
            continue
    session.commit()
    session.close()


if __name__ == '__main__':
    main()
