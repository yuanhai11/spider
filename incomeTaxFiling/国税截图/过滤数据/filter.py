'''
新增数据获取
'''
import time,re,json,uuid
import requests,pymysql
from lxml import etree
from sqlalchemy import Column, String, create_engine, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy import or_
from sqlalchemy.ext.declarative import declarative_base
# 创建对象的基类:
Base = declarative_base()
# 定义User对象:
class TaxCertAllData(Base):
    # 表的名字:
    __tablename__ = 'tax_cert_all_data'

    # 表的结构:
    id = Column(Integer(), primary_key=True, autoincrement=True)

    company_name = Column(String(256))
    company_id = Column(String(256))
    tax_declaration_id = Column(String(256))
    tax_date = Column(String(256))
    tax_type = Column(String(256))
    images = Column(String(256))
    gmt_created = Column(String(256))
    gmt_updated = Column(String(256))

class TaxCert(Base):
    # 表的名字:
    __tablename__ = 'tax_cert'

    # 表的结构:
    id = Column(Integer(), primary_key=True, autoincrement=True)

    company_name = Column(String(256))
    company_id = Column(String(256))
    tax_declaration_id = Column(String(256))
    tax_date = Column(String(256))
    tax_type = Column(String(256))
    images = Column(String(256))
    gmt_created = Column(String(256))
    gmt_updated = Column(String(256))

class TaxCertProd(Base):
    # 表的名字:
    __tablename__ = 'tax_cert_prod'

    # 表的结构:
    id = Column(Integer(), primary_key=True, autoincrement=True)

    company_name = Column(String(256))
    company_id = Column(String(256))
    tax_declaration_id = Column(String(256))
    images = Column(String(256000))
    result = Column(String(256))


# 初始化数据库连接:
engine = create_engine('mysql+pymysql://root:BOOT-xwork1024@192.168.2.96:3306/zl_saas')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
# 创建session对象:
session = DBSession()


all_data = session.query(TaxCertAllData).filter(TaxCertAllData.tax_date == "2022-05").all()
print(len(all_data))

for index,data in enumerate(all_data):
    # if index < 1000:
    #     continue
    # 1.取出每一条数据和task_cert表进行比对
    images = data.images
    if images == '{}' or 'apply_date' in images:
        continue

    company_name = data.company_name
    company_id = data.company_id
    tax_declaration_id = data.tax_declaration_id
    tax_date = data.tax_date
    tax_type = data.tax_type
    images = data.images

    dic = {}
    dd = json.loads(images)['常规申报列表']
    dic['常规申报列表'] = dd
    print(company_name)
    print(dic)

    times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    tax = TaxCert(company_id = company_id,company_name=company_name,
                      tax_declaration_id = tax_declaration_id,tax_date=tax_date,tax_type=tax_type,
                      images = json.dumps(dic,ensure_ascii=False),gmt_created = times,gmt_updated = times
                      )

    session.add(tax)
session.commit()
    # exit()
