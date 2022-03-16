# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import time

import pymysql
from sqlalchemy import Column, String, create_engine,Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from itemadapter import ItemAdapter
from .fetch_free_proxyes import logger

class InvoicedataPipeline:
    def process_item(self, item, spider):
        return item

# 创建对象的基类:
Base = declarative_base()
# 定义User对象:
class Medicine(Base):
    # 表的名字:
    __tablename__ = 'company_title'

    # 表的结构:
    id = Column(Integer(), primary_key=True,autoincrement=True)
    company_name = Column(String(256))
    company_num = Column(String(256))
    tax_num = Column(String(256))
    reg_addr = Column(String(256))
    phone = Column(String(256))
    bank = Column(String(256))
    bank_card = Column(String(256))

    gmt_created = Column(String(256))
    gmt_updated = Column(String(256))


class InvoicedataPipelineMysql(object):

    def open_spider(self, spider):

        # 初始化数据库连接:
        engine = create_engine('mysql+pymysql://root:BOOT-xwork1024@192.168.2.97:3306/spider')
        # 创建DBSession类型:
        DBSession = sessionmaker(bind=engine)
        # 创建session对象:
        self.session = DBSession()
        logger.info("连接数据库成功")

    # 爬虫开始执行1次,用于数据库连接
    def process_item(self, item, spider):

        name = item['name']
        gid = item['gid']
        taxnum = item['taxnum']
        address = item['address']
        phone = item['phone']
        bank = item['bank']
        bankAccount = item['bankAccount']
        times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        medi = Medicine(company_name=name, company_num=gid, tax_num=taxnum, reg_addr=address, phone=phone, bank=bank,
                        bank_card=bankAccount, gmt_created=times, gmt_updated=times)
        logger.info('{}-{}-{}-{}-{}-{}-{}'.format(gid,name,taxnum,address, phone, bank, bankAccount))

        self.session.add(medi)
        self.session.commit()


    # 用于存储抓取的item数据
    def close_spider(self, spider):
        self.session.close()
