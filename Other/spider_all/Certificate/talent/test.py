import re
import time
import requests
import pymysql
from lxml import etree
from getCompanyId.get_company_id import get_company_id
from sqlalchemy import Column, String, create_engine,Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# 创建对象的基类:
Base = declarative_base()
# 定义User对象:
class Medicine(Base):
    '''
    1、更新机制：获取前30页数据
    2、频率：1周
    '''
    # 表的名字:
    __tablename__ = 'spider_high_talent'

    # 表的结构:
    id = Column(Integer(), primary_key=True,autoincrement=True)
    title_url = Column(String(256))
    name = Column(String(256))
    department = Column(String(256))
    company_name = Column(String(256))
    birth = Column(String(256))
    talent_type = Column(String(256))
    reason = Column(String(256))
    content = Column(String(256))
    release_date = Column(String(256))
    gmt_created = Column(String(256))
    gmt_updated = Column(String(256))
    company_id = Column(String(256))
# 初始化数据库连接:
engine = create_engine('mysql+pymysql://root:BOOT-xwork1024@192.168.2.97:3306/spider')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
# 创建session对象:
session = DBSession()
def main():
    data = session.query(Medicine).all()
    for d in data:
        title_url = d.title_url.replace('zjhz.hrss','hzrs.hangzhou')
        print(title_url)
        name = d.name
        department = d.department
        company_name = d.company_name
        birth = d.birth
        talent_type = d.talent_type
        reason = d.reason
        content = d.content
        release_date = d.release_date
        gmt_created = d.gmt_created
        gmt_updated = d.gmt_updated

        zhilian = Medicine(title_url=title_url, name=name, company_name=company_name, talent_type=talent_type,
                           reason=reason,
                           department=department, birth=birth, content=content, release_date=release_date,
                           gmt_created=gmt_created, gmt_updated=gmt_updated)
        session.add(zhilian)
    session.commit()

if __name__ == '__main__':
    main()