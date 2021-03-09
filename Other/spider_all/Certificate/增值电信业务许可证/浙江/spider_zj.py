import json
import shutil
import re
import os
import time
import requests
import pymysql
from lxml import etree
from xlrd import open_workbook
from getCompanyId.get_company_id import get_company_id
from sqlalchemy import Column, String, create_engine,Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# 创建对象的基类:
Base = declarative_base()
# 定义User对象:

class Medicine(Base):
    # 表的名字:
    __tablename__ = 'spider_add_value_telecom_zj'
    id = Column(Integer(), primary_key=True,autoincrement=True)
    permit_number = Column(String(256))
    company_name = Column(String(256))
    busi_type = Column(String(256))
    certificate_valid_date = Column(String(256))
    certificate_invalid_date = Column(String(256))

    gmt_created = Column(String(256))
    gmt_updated = Column(String(256))
    company_id = Column(String(256))


class Medicine1(Base):
    # 表的名字:
    __tablename__ = 'spider_qualification'
    id = Column(Integer(), primary_key=True,autoincrement=True)
    url = Column(String(256))
    license_num = Column(String(256))
    company_name = Column(String(256))
    project_name = Column(String(256))
    valid_date = Column(String(256))
    invalid_date = Column(String(256))
    area = Column(Integer())

    gmt_created = Column(String(256))
    gmt_updated = Column(String(256))
    company_id = Column(String(256))

# 初始化数据库连接:
engine = create_engine('mysql+pymysql://root:BOOT-xwork1024@192.168.2.97:3306/spider')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
# 创建session对象:
session = DBSession()

def main_11():
    data = session.query(Medicine).all()
    for d in data:
        permit_number = d.permit_number
        if not permit_number:
            continue
        company_name = d.company_name
        busi_type = d.busi_type
        certificate_valid_date = d.certificate_valid_date
        certificate_invalid_date = d.certificate_invalid_date
        gmt_created = d.gmt_created
        gmt_updated = d.gmt_updated

        medicine = Medicine1(license_num=permit_number,company_name=company_name,project_name=busi_type,valid_date=certificate_valid_date,invalid_date=certificate_invalid_date,
                  gmt_created=gmt_created,gmt_updated=gmt_updated,area = 9
                  )
        print(company_name,permit_number,busi_type,certificate_valid_date,certificate_invalid_date)
        session.add(medicine)
    session.commit()

if __name__ == '__main__':
    main_11()