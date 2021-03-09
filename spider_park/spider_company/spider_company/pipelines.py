# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import time
import pymysql
import re
import os
import json
import math
import time
import requests
import pymysql
import json
from lxml import etree

from sqlalchemy import Column, String, create_engine,Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# 创建对象的基类:
Base = declarative_base()
# 定义User对象:
class Medicine(Base):
    # 表的名字:
    __tablename__ = 'spider_park'

    # 表的结构:
    id = Column(Integer(), primary_key=True,autoincrement=True)
    park_url = Column(String(256))
    park_name = Column(String(256))
    province = Column(String(256))
    city = Column(String(256))
    area = Column(String(256))
    gmt_created = Column(String(256))
    gmt_updated = Column(String(256))

class SpiderCompanyPipeline:

    def open_spider(self,spider):
        # 初始化数据库连接:
        self.engine = create_engine('mysql+pymysql://root:123456@192.168.2.222:3306/spider')
        # 创建DBSession类型:
        self.DBSession = sessionmaker(bind=self.engine)
        # 创建session对象:
        self.session = self.DBSession()

    def process_item(self, item, spider):
        park_url= item['park_url']
        park_name=item['park_name']
        province=item['province']
        city=item['city']
        area=item['area']
        gmt_created =item['gmt_created']
        gmt_updated =item['gmt_updated']

        medicine = Medicine(park_url=park_url,park_name=park_name,province=province,city=city,area=area,gmt_created=gmt_created,gmt_updated=gmt_updated)
        self.session.add(medicine)
        return item

    def close_spider(self,spider):
        self.session.commit()
        self.session.close()
