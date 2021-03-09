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
    __tablename__ = 'spider_qualification_revoke'

    # 表的结构:
    id = Column(Integer(), primary_key=True, autoincrement=True)
    company_name = Column(String(256))
    revoke_information = Column(Integer())

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
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
    }
    url = 'https://bjca.miit.gov.cn/api-gateway/jpaas-publish-server/front/page/build/unit?webId=25b2fd3da2f44402bedeb4364e630274&pageId=5ea7e69e52d34260a34b9a473ffee325&parseType=bulidstatic&pageType=column&tagId=%E5%BD%93%E5%89%8D%E6%A0%8F%E7%9B%AE_list&tplSetId=642c6445dd804d0ca01ea12549b79493&paramJson={"pageNo":6,"pageSize":20}'
    response = requests.request(method='get', url=url,headers=headers,timeout=10).json()['data']['html']
    print(response)
    data = re.findall(r'<a href="(.*?)" title="(.*?)" target="_blank"',response,re.S)
    print(data)
    gmt_created = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    gmt_updated = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    for l in data:
        title = l[1]
        if '增值电信业务经营许可证' in title and '拟注销' not in title:
            url = 'https://bjca.miit.gov.cn' + l[0]
            print(url)
            response = requests.request(method='get', url=url, data=data, headers=headers, timeout=10).text
            excle_url = 'https://bjca.miit.gov.cn' + re.findall(r'<a .*? target="_blank" href="(.*?)">',response,re.S)[0]
            print(excle_url)
            file_name = excle_url.split('/')[-1].split('&')[0]
            print(file_name)
            response = requests.request(method='get', url=excle_url, data=data, headers=headers, timeout=10).content
            with open(r'D:\projects\Spider\local_spider\Other\spider_all\Certificate\北京\revoke_file\{}'.format(file_name),'wb')as fp:
                fp.write(response)
            time.sleep(0.5)

def parse():
    # bloom = get_updated()
    file = r'/Certificate/增值电信业务许可证/北京/revoke_file'
    file_names = os.listdir(file)
    for i in file_names:
        print(i)
        workbook = open_workbook(file + '\\' + i)  # 打开excel文件
        sheet2 = workbook.sheet_by_index(0)
        all_rows = sheet2.nrows
        all_col = sheet2.row_values(4)
        print(len(all_col))
        print((all_col))
        print(all_rows)

        for i in range(5, all_rows):
            company_name = sheet2.cell(i, 0).value.strip()
            if company_name == '':
                continue
            print(company_name)
            medicine = Medicine(company_name=company_name)
            session.add(medicine)
    session.commit()

if __name__ == '__main__':
    parse()
    # main_11()