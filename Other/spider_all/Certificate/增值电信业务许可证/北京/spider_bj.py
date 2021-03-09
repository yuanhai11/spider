#coding:utf-8
'''
 # 北京资质类数据
'''
#coding:utf-8
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
    __tablename__ = 'spider_qualification'

    # 表的结构:
    id = Column(Integer(), primary_key=True, autoincrement=True)
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

# ICP
def main_ICP():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
    }
    sum = []
    url = "https://bjca.miit.gov.cn/bsfw/gsgg/xzxk/art/2020/art_a9216d22483845678d61a355ec055240.html"
    response = requests.request(method='get', url=url, headers=headers,timeout=10).text
    tree = etree.HTML(response)

    down_load1 = 'https://bjca.miit.gov.cn' + tree.xpath('//div[@class="pages_content"]/p[last()-1]/a/@href')[0]
    file_name1 = tree.xpath('//div[@class="pages_content"]/p[last()-1]/a/text()')[0]

    down_load2 = 'https://bjca.miit.gov.cn' + tree.xpath('//div[@class="pages_content"]/p[last()-2]/a/@href')[0]
    file_name2 = tree.xpath('//div[@class="pages_content"]/p[last()-2]/a/text()')[0]
    sum.append((file_name1,down_load1))
    sum.append((file_name2,down_load2))

    for i in sum:
        file_name = i[0]
        down_load = i[1]
        file_name = r'D:\projects\Spider\local_spider\Other\spider_all\Certificate\files\{}'.format(file_name)
        print(file_name)
        time.sleep(1)
        response1 = requests.request(method='get', url=down_load, headers=headers, timeout=10).content
        with open(file_name, 'wb')as fP:
            fP.write(response1)
        continue
def parse_ICP_file1(file_name):
    # bloom = get_updated()

    workbook = open_workbook(file_name)  # 打开excel文件
    sheet2 = workbook.sheet_by_index(0)
    all_rows = sheet2.nrows
    all_col = sheet2.row_values(5)
    print(len(all_col))
    print((all_col))
    print(all_rows)
    gmt_created = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    gmt_updated = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    for i in range(6, all_rows):
        license_num = sheet2.cell(i, 0).value.strip()
        company_name = sheet2.cell(i,1).value.strip()
        import datetime,xlrd

        valid_date = sheet2.cell(i, 5).value
        invalid_date = sheet2.cell(i,6).value

        try:
            valid_date = datetime.datetime(*xlrd.xldate_as_tuple(valid_date,datemode=0))
            invalid_date = datetime.datetime(*xlrd.xldate_as_tuple(invalid_date,datemode=0))
        except:
            print(company_name,'不要脸')
            continue
        project_name = '信息服务业务（仅限互联网信息服务)'
        area = 1
        print(license_num,company_name,project_name,valid_date,invalid_date,gmt_created,gmt_updated,area)
        medicine = Medicine(license_num=license_num,company_name=company_name,project_name=project_name,valid_date=valid_date,invalid_date=invalid_date,
                            area=area,gmt_created=gmt_created,gmt_updated=gmt_updated)
        session.add(medicine)

    session.commit()
def parse_ICP_file2(file_name):
    # bloom = get_updated()

    workbook = open_workbook(file_name)  # 打开excel文件
    sheet2 = workbook.sheet_by_index(0)
    all_rows = sheet2.nrows
    all_col = sheet2.row_values(5)
    print(len(all_col))
    print((all_col))
    print(all_rows)
    gmt_created = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    gmt_updated = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    for i in range(6, all_rows):
        license_num = sheet2.cell(i, 0).value.strip()
        company_name = sheet2.cell(i,1).value.strip()
        project_name = '信息服务业务（仅限互联网信息服务)'
        area = 1
        print(license_num, company_name, project_name,gmt_created, gmt_updated, area)
        medicine = Medicine(license_num=license_num, company_name=company_name, project_name=project_name,
                            area=area, gmt_created=gmt_created, gmt_updated=gmt_updated)
        session.add(medicine)

    session.commit()


# EDI
def main_EDI():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
    }
    sum = []
    url = "https://bjca.miit.gov.cn/bsfw/gsgg/xzxk/art/2020/art_007ea130df694e2d8b377efa63884112.html"
    response = requests.request(method='get', url=url, headers=headers,timeout=10).text
    tree = etree.HTML(response)

    down_load1 = 'https://bjca.miit.gov.cn' + tree.xpath('//div[@class="pages_content"]/div[last()]/p[1]/a/@href')[0]
    file_name1 = tree.xpath('//div[@class="pages_content"]/div[last()]/p[1]/a/text()')[0]

    down_load2 = 'https://bjca.miit.gov.cn' + tree.xpath('//div[@class="pages_content"]/div[last()]/p[2]/a/@href')[0]
    file_name2 = tree.xpath('//div[@class="pages_content"]/div[last()]/p[2]/a/text()')[0]
    sum.append((file_name1,down_load1))
    sum.append((file_name2,down_load2))

    for i in sum:
        file_name = i[0]
        down_load = i[1]
        file_name = r'D:\projects\Spider\local_spider\Other\spider_all\Certificate\files\{}'.format(file_name)
        print(file_name)
        time.sleep(1)
        response1 = requests.request(method='get', url=down_load, headers=headers, timeout=10).content
        with open(file_name, 'wb')as fP:
            fP.write(response1)
        continue
def parse_EDI_file1(file_name):
    # bloom = get_updated()

    workbook = open_workbook(file_name)  # 打开excel文件
    sheet2 = workbook.sheet_by_index(0)
    all_rows = sheet2.nrows
    all_col = sheet2.row_values(5)
    print(len(all_col))
    print((all_col))
    print(all_rows)
    gmt_created = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    gmt_updated = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    for i in range(6, all_rows):
        license_num = sheet2.cell(i, 0).value.strip()
        company_name = sheet2.cell(i,1).value.strip()
        import datetime,xlrd

        valid_date = sheet2.cell(i, 4).value
        invalid_date = sheet2.cell(i,5).value

        try:
            valid_date = datetime.datetime(*xlrd.xldate_as_tuple(valid_date,datemode=0))
            invalid_date = datetime.datetime(*xlrd.xldate_as_tuple(invalid_date,datemode=0))
        except:
            print(company_name,'不要脸')
            continue
        project_name = '在线数据处理与交易处理业务'
        area = 1
        print(license_num,company_name,project_name,valid_date,invalid_date,gmt_created,gmt_updated,area)
        medicine = Medicine(license_num=license_num,company_name=company_name,project_name=project_name,valid_date=valid_date,invalid_date=invalid_date,
                            area=area,gmt_created=gmt_created,gmt_updated=gmt_updated)
        session.add(medicine)

    session.commit()
def parse_EDI_file2(file_name):
    # bloom = get_updated()

    workbook = open_workbook(file_name)  # 打开excel文件
    sheet2 = workbook.sheet_by_index(0)
    all_rows = sheet2.nrows
    all_col = sheet2.row_values(5)
    print(len(all_col))
    print((all_col))
    print(all_rows)
    gmt_created = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    gmt_updated = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    for i in range(5, all_rows):
        license_num = sheet2.cell(i, 0).value.strip()
        company_name = sheet2.cell(i,1).value.strip()
        project_name = '在线数据处理与交易处理业务'
        area = 1
        print(license_num, company_name, project_name,gmt_created, gmt_updated, area)
        medicine = Medicine(license_num=license_num, company_name=company_name, project_name=project_name,
                            area=area, gmt_created=gmt_created, gmt_updated=gmt_updated)
        session.add(medicine)
    session.commit()

def main_3():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
    }
    sum = []
    url = "https://bjca.miit.gov.cn/bsfw/gsgg/xzxk/art/2020/art_7332e5467a2a4a8abc35db865a6a901b.html"
    response = requests.request(method='get', url=url, headers=headers,timeout=10).text
    tree = etree.HTML(response)

    down_load1 = 'https://bjca.miit.gov.cn' + tree.xpath('//div[@class="pages_content"]/p[last()-1]/a/@href')[0]
    file_name1 = tree.xpath('//div[@class="pages_content"]/p[last()-1]/a/text()')[0]

    down_load2 = 'https://bjca.miit.gov.cn' + tree.xpath('//div[@class="pages_content"]/p[last()]/a/@href')[0]
    file_name2 = tree.xpath('//div[@class="pages_content"]/p[last()]/a/text()')[0]
    sum.append((file_name1,down_load1))
    sum.append((file_name2,down_load2))

    for i in sum:
        file_name = i[0]
        down_load = i[1]
        file_name = r'D:\projects\Spider\local_spider\Other\spider_all\Certificate\files\{}'.format(file_name)
        print(file_name)
        time.sleep(1)
        response1 = requests.request(method='get', url=down_load, headers=headers, timeout=10).content
        with open(file_name, 'wb')as fP:
            fP.write(response1)
        continue
def parse_3_file1(file_name = r'D:\projects\Spider\local_spider\Other\spider_all\Certificate\files\信息服务业务（不含固定网电话信息服务和互联网信息服务）许可证名录-自2016年11月1日起.xlsx'):
    # bloom = get_updated()

    workbook = open_workbook(file_name)  # 打开excel文件
    sheet2 = workbook.sheet_by_index(0)
    all_rows = sheet2.nrows
    all_col = sheet2.row_values(5)
    print(len(all_col))
    print((all_col))
    print(all_rows)
    gmt_created = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    gmt_updated = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    for i in range(6, all_rows):
        license_num = sheet2.cell(i, 0).value.strip()
        company_name = sheet2.cell(i, 1).value.strip()
        import datetime, xlrd

        valid_date = sheet2.cell(i, 4).value
        invalid_date = sheet2.cell(i, 5).value

        try:
            valid_date = datetime.datetime(*xlrd.xldate_as_tuple(valid_date, datemode=0))
            invalid_date = datetime.datetime(*xlrd.xldate_as_tuple(invalid_date, datemode=0))
        except:
            print(company_name, '不要脸')
            continue
        project_name = '信息服务业务（不含固定网电话信息服务和互联网信息服务）'
        area = 1
        print(license_num, company_name, project_name, valid_date, invalid_date, gmt_created, gmt_updated, area)
        medicine = Medicine(license_num=license_num, company_name=company_name, project_name=project_name,
                            valid_date=valid_date, invalid_date=invalid_date,
                            area=area, gmt_created=gmt_created, gmt_updated=gmt_updated)
        session.add(medicine)

    session.commit()
def parse_3_file2(file_name=r'D:\projects\Spider\local_spider\Other\spider_all\Certificate\files\信息服务业务（不含固定网电话信息服务和互联网信息服务）许可证名录-2016年10月30日前.xlsx'):
        # bloom = get_updated()

        workbook = open_workbook(file_name)  # 打开excel文件
        sheet2 = workbook.sheet_by_index(0)
        all_rows = sheet2.nrows
        all_col = sheet2.row_values(5)
        print(len(all_col))
        print((all_col))
        print(all_rows)
        gmt_created = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        gmt_updated = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        for i in range(6, all_rows):
            license_num = sheet2.cell(i, 0).value.strip()
            company_name = sheet2.cell(i, 1).value.strip()
            project_name = '信息服务业务（不含固定网电话信息服务和互联网信息服务）'
            area = 1
            print(license_num, company_name, project_name, gmt_created, gmt_updated, area)
            medicine = Medicine(license_num=license_num, company_name=company_name, project_name=project_name,
                                area=area, gmt_created=gmt_created, gmt_updated=gmt_updated)
            session.add(medicine)

        session.commit()


def main_4():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
    }
    sum = []
    url = "https://bjca.miit.gov.cn/bsfw/gsgg/xzxk/art/2020/art_4f4730dbb3ad4125b5bd6ae4077e327a.html"
    response = requests.request(method='get', url=url, headers=headers, timeout=10).text
    tree = etree.HTML(response)

    down_load1 = 'https://bjca.miit.gov.cn' + tree.xpath('//div[@class="pages_content"]/p[6]/a[2]/@href')[0]
    file_name1 = tree.xpath('//div[@class="pages_content"]/p[6]/a[2]/text()')[0]

    down_load2 = 'https://bjca.miit.gov.cn' + tree.xpath('//div[@class="pages_content"]/p[8]/a[2]/@href')[0]
    file_name2 = tree.xpath('//div[@class="pages_content"]/p[8]/a[2]/text()')[0]
    sum.append((file_name1, down_load1))
    sum.append((file_name2, down_load2))

    for i in sum:
        file_name = i[0]
        down_load = i[1]
        file_name = r'D:\projects\Spider\local_spider\Other\spider_all\Certificate\files\{}'.format(file_name)
        print(file_name)
        time.sleep(1)
        response1 = requests.request(method='get', url=down_load, headers=headers, timeout=10).content
        with open(file_name, 'wb')as fP:
            fP.write(response1)
        continue
def parse_4_file1(file_name=r'D:\projects\Spider\local_spider\Other\spider_all\Certificate\files\互联网接入服务业务许可证名录-自2016年11月1日起.xlsx'):
    # bloom = get_updated()

    workbook = open_workbook(file_name)  # 打开excel文件
    sheet2 = workbook.sheet_by_index(0)
    all_rows = sheet2.nrows
    all_col = sheet2.row_values(5)
    print(len(all_col))
    print((all_col))
    print(all_rows)
    gmt_created = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    gmt_updated = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    for i in range(6, all_rows):
        license_num = sheet2.cell(i, 0).value.strip()
        company_name = sheet2.cell(i, 1).value.strip()
        import datetime, xlrd

        valid_date = sheet2.cell(i, 4).value
        invalid_date = sheet2.cell(i, 5).value

        try:
            valid_date = datetime.datetime(*xlrd.xldate_as_tuple(valid_date, datemode=0))
            invalid_date = datetime.datetime(*xlrd.xldate_as_tuple(invalid_date, datemode=0))
        except:
            print(company_name, '不要脸')
            continue
        project_name = '互联网接入服务业务'
        area = 1
        print(license_num, company_name, project_name, valid_date, invalid_date, gmt_created, gmt_updated, area)
        medicine = Medicine(license_num=license_num, company_name=company_name, project_name=project_name,
                            valid_date=valid_date, invalid_date=invalid_date,
                            area=area, gmt_created=gmt_created, gmt_updated=gmt_updated)
        session.add(medicine)

    session.commit()
def parse_4_file2(file_name=r'D:\projects\Spider\local_spider\Other\spider_all\Certificate\files\互联网接入服务业务许可证名录-2016年10月30日前.xlsx'):
    # bloom = get_updated()

    workbook = open_workbook(file_name)  # 打开excel文件
    sheet2 = workbook.sheet_by_index(0)
    all_rows = sheet2.nrows
    all_col = sheet2.row_values(5)
    print(len(all_col))
    print((all_col))
    print(all_rows)
    gmt_created = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    gmt_updated = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    for i in range(6, all_rows):
        license_num = sheet2.cell(i, 0).value.strip()
        company_name = sheet2.cell(i, 1).value.strip()
        project_name = '互联网数据中心业务'
        area = 1
        print(license_num, company_name, project_name, gmt_created, gmt_updated, area)
        medicine = Medicine(license_num=license_num, company_name=company_name, project_name=project_name,
                            area=area, gmt_created=gmt_created, gmt_updated=gmt_updated)
        session.add(medicine)

    session.commit()

def main_5():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
    }
    sum = []
    url = "https://bjca.miit.gov.cn/bsfw/gsgg/xzxk/art/2020/art_0e8dc3eab13e4e0aaa3f14fbe8c95b05.html"
    response = requests.request(method='get', url=url, headers=headers,timeout=10).text
    tree = etree.HTML(response)

    down_load1 = 'https://bjca.miit.gov.cn' + tree.xpath('//div[@class="pages_content"]/p[last()]/a/@href')[0]
    file_name1 = tree.xpath('//div[@class="pages_content"]/p[last()]/a/text()')[0]

    sum.append((file_name1,down_load1))

    for i in sum:
        file_name = i[0]
        down_load = i[1]
        file_name = r'D:\projects\Spider\local_spider\Other\spider_all\Certificate\files\{}'.format(file_name)
        print(file_name)
        time.sleep(1)
        response1 = requests.request(method='get', url=down_load, headers=headers, timeout=10).content
        with open(file_name, 'wb')as fP:
            fP.write(response1)
        continue
def parse_5_file1(file_name = r'D:\projects\Spider\local_spider\Other\spider_all\Certificate\files\互联网域名解析服务业务许可证名录.xlsx'):
    # bloom = get_updated()

    workbook = open_workbook(file_name)  # 打开excel文件
    sheet2 = workbook.sheet_by_index(0)
    all_rows = sheet2.nrows
    all_col = sheet2.row_values(6)
    print(len(all_col))
    print((all_col))
    print(all_rows)
    gmt_created = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    gmt_updated = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    for i in range(7, all_rows):
        license_num = sheet2.cell(i, 0).value.strip()
        company_name = sheet2.cell(i, 1).value.strip()
        import datetime, xlrd

        valid_date = sheet2.cell(i, 4).value
        invalid_date = sheet2.cell(i, 5).value
        # print(valid_date)
        if str(valid_date).endswith('.0'):
            try:
                valid_date = datetime.datetime(*xlrd.xldate_as_tuple(valid_date, datemode=0))
                invalid_date = datetime.datetime(*xlrd.xldate_as_tuple(invalid_date, datemode=0))
            except:
                print(company_name, '不要脸')
                continue

        project_name = '互联网域名解析服务业务'
        area = 1
        print(license_num, company_name, project_name, valid_date, invalid_date, gmt_created, gmt_updated, area)
        medicine = Medicine(license_num=license_num, company_name=company_name, project_name=project_name,
                            valid_date=valid_date, invalid_date=invalid_date,
                            area=area, gmt_created=gmt_created, gmt_updated=gmt_updated)
        session.add(medicine)

    session.commit()

def main_6():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
    }
    sum = []
    url = 'https://bjca.miit.gov.cn/bsfw/gsgg/xzxk/art/2020/art_1f1d00242e3c4b0e83a2f06c85632f9f.html'
    response = requests.request(method='get', url=url, headers=headers,timeout=10).text
    tree = etree.HTML(response)

    down_load1 = 'https://bjca.miit.gov.cn' + tree.xpath('//div[@class="pages_content"]/p[last()-1]/a/@href')[0]
    file_name1 = tree.xpath('//div[@class="pages_content"]/p[last()-1]/a/text()')[0]

    down_load2 = 'https://bjca.miit.gov.cn' + tree.xpath('//div[@class="pages_content"]/p[last()]/a/@href')[0]
    file_name2 = tree.xpath('//div[@class="pages_content"]/p[last()]/a/text()')[0]
    sum.append((file_name1,down_load1))
    sum.append((file_name2,down_load2))

    for i in sum:
        file_name = i[0]
        down_load = i[1]
        file_name = r'D:\projects\Spider\local_spider\Other\spider_all\Certificate\files\{}'.format(file_name)
        print(file_name)
        time.sleep(1)
        response1 = requests.request(method='get', url=down_load, headers=headers, timeout=10).content
        with open(file_name, 'wb')as fP:
            fP.write(response1)
        continue
def parse_6_file1(file_name = r'D:\projects\Spider\local_spider\Other\spider_all\Certificate\files\互联网数据中心业务许可证名录-自2016年11月1日起.xlsx'):
    # bloom = get_updated()

    workbook = open_workbook(file_name)  # 打开excel文件
    sheet2 = workbook.sheet_by_index(0)
    all_rows = sheet2.nrows
    all_col = sheet2.row_values(5)
    print(len(all_col))
    print((all_col))
    print(all_rows)
    gmt_created = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    gmt_updated = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    for i in range(6, all_rows):
        license_num = sheet2.cell(i, 0).value.strip()
        company_name = sheet2.cell(i, 1).value.strip()
        import datetime, xlrd

        valid_date = sheet2.cell(i, 4).value
        invalid_date = sheet2.cell(i, 5).value

        try:
            valid_date = datetime.datetime(*xlrd.xldate_as_tuple(valid_date, datemode=0))
            invalid_date = datetime.datetime(*xlrd.xldate_as_tuple(invalid_date, datemode=0))
        except:
            print(company_name, '不要脸')
            continue
        project_name = '互联网数据中心业务'
        area = 1
        print(license_num, company_name, project_name, valid_date, invalid_date, gmt_created, gmt_updated, area)
        medicine = Medicine(license_num=license_num, company_name=company_name, project_name=project_name,
                            valid_date=valid_date, invalid_date=invalid_date,
                            area=area, gmt_created=gmt_created, gmt_updated=gmt_updated)
        session.add(medicine)

    session.commit()
def parse_6_file2(file_name=r'D:\projects\Spider\local_spider\Other\spider_all\Certificate\files\互联网数据中心业务许可证名录-2016年10月30日前.xlsx'):
        # bloom = get_updated()

        workbook = open_workbook(file_name)  # 打开excel文件
        sheet2 = workbook.sheet_by_index(0)
        all_rows = sheet2.nrows
        all_col = sheet2.row_values(5)
        print(len(all_col))
        print((all_col))
        print(all_rows)
        gmt_created = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        gmt_updated = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        for i in range(6, all_rows):
            license_num = sheet2.cell(i, 0).value.strip()
            company_name = sheet2.cell(i, 1).value.strip()
            project_name = '互联网数据中心业务'
            area = 1
            print(license_num, company_name, project_name, gmt_created, gmt_updated, area)
            medicine = Medicine(license_num=license_num, company_name=company_name, project_name=project_name,
                                area=area, gmt_created=gmt_created, gmt_updated=gmt_updated)
            session.add(medicine)

        session.commit()

def main_7():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
    }
    sum = []
    url = 'https://bjca.miit.gov.cn/bsfw/gsgg/xzxk/art/2020/art_26b57023fb0343e39d6818fee59ebb11.html'
    response = requests.request(method='get', url=url, headers=headers,timeout=10).text
    tree = etree.HTML(response)

    down_load1 = 'https://bjca.miit.gov.cn' + tree.xpath('//div[@class="pages_content"]/p[last()-2]/span/a/@href')[0]
    file_name1 = tree.xpath('//div[@class="pages_content"]/p[last()-2]/span/a/text()')[0]

    down_load2 = 'https://bjca.miit.gov.cn' + tree.xpath('//div[@class="pages_content"]/p[last()-1]/span/a/@href')[0]
    file_name2 = tree.xpath('//div[@class="pages_content"]/p[last()-1]/span/a/text()')[0]
    sum.append((file_name1,down_load1))
    sum.append((file_name2,down_load2))

    for i in sum:
        file_name = i[0]
        down_load = i[1]
        file_name = r'D:\projects\Spider\local_spider\Other\spider_all\Certificate\files\{}'.format(file_name)
        print(file_name)
        time.sleep(1)
        response1 = requests.request(method='get', url=down_load, headers=headers, timeout=10).content
        with open(file_name, 'wb')as fP:
            fP.write(response1)
        continue
def parse_7_file1(file_name = r'D:\projects\Spider\local_spider\Other\spider_all\Certificate\files\呼叫中心业务许可证名录-自2016年11月1日起.xlsx'):
    # bloom = get_updated()

    workbook = open_workbook(file_name)  # 打开excel文件
    sheet2 = workbook.sheet_by_index(0)
    all_rows = sheet2.nrows
    all_col = sheet2.row_values(5)
    print(len(all_col))
    print((all_col))
    print(all_rows)
    gmt_created = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    gmt_updated = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    for i in range(6, all_rows):
        license_num = sheet2.cell(i, 0).value.strip()
        company_name = sheet2.cell(i, 1).value.strip()
        import datetime, xlrd

        valid_date = sheet2.cell(i, 4).value
        invalid_date = sheet2.cell(i, 5).value

        try:
            valid_date = datetime.datetime(*xlrd.xldate_as_tuple(valid_date, datemode=0))
            invalid_date = datetime.datetime(*xlrd.xldate_as_tuple(invalid_date, datemode=0))
        except:
            print(company_name, '不要脸')
            continue
        project_name = '呼叫中心业务'
        area = 1
        print(license_num, company_name, project_name, valid_date, invalid_date, gmt_created, gmt_updated, area)
        medicine = Medicine(license_num=license_num, company_name=company_name, project_name=project_name,
                            valid_date=valid_date, invalid_date=invalid_date,
                            area=area, gmt_created=gmt_created, gmt_updated=gmt_updated)
        session.add(medicine)

    session.commit()
def parse_7_file2(file_name=r'D:\projects\Spider\local_spider\Other\spider_all\Certificate\files\呼叫中心业务许可证名录-2016年10月30日前.xlsx'):
        # bloom = get_updated()

        workbook = open_workbook(file_name)  # 打开excel文件
        sheet2 = workbook.sheet_by_index(0)
        all_rows = sheet2.nrows
        all_col = sheet2.row_values(4)
        print(len(all_col))
        print((all_col))
        print(all_rows)
        gmt_created = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        gmt_updated = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        for i in range(5, all_rows):
            license_num = sheet2.cell(i, 0).value.strip()
            company_name = sheet2.cell(i, 1).value.strip()
            project_name = '呼叫中心业务'
            area = 1
            print(license_num, company_name, project_name, gmt_created, gmt_updated, area)
            medicine = Medicine(license_num=license_num, company_name=company_name, project_name=project_name,
                                area=area, gmt_created=gmt_created, gmt_updated=gmt_updated)
            session.add(medicine)

        session.commit()

def main_8():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
    }
    url = "https://bjca.miit.gov.cn/bsfw/gsgg/xzxk/art/2020/art_44f25aae36b04a049cfa515179574be9.html"
    response = requests.request(method='get', url=url, headers=headers,timeout=10).text
    tree = etree.HTML(response)
    lists = tree.xpath('//div[@class="pages_content"]/div/table/tbody/tr[position()>1]')

    gmt_created = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    gmt_updated = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    for l in lists:
        license_num = l.xpath('./td[1]//text()')[0]
        company_name = l.xpath('./td[2]//text()')[0]
        project_name = '国内互联网虚拟专用网业务'
        area = 1

        print(company_name,license_num,gmt_created,gmt_updated,area)
        medicine = Medicine(company_name=company_name,license_num=license_num,
                 gmt_created=gmt_created,gmt_updated=gmt_updated,area=area,project_name = project_name)
        session.add(medicine)
    session.commit()

def main_9():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
    }
    sum = []
    url = 'https://bjca.miit.gov.cn/bsfw/gsgg/xzxk/art/2020/art_5335df77f21f46c58dc64de4724067e3.html'
    response = requests.request(method='get', url=url, headers=headers,timeout=10).text
    tree = etree.HTML(response)
    lists = tree.xpath('//div[@class="pages_content"]/table/tbody/tr[position()>1]')

    gmt_created = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    gmt_updated = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    for l in lists:
        license_num = l.xpath('./td[3]//text()')[0]
        company_name = l.xpath('./td[1]//text()')[0]
        project_name = '无线寻呼业务'
        area = 1

        print(company_name, license_num, gmt_created, gmt_updated, area)
        medicine = Medicine(company_name=company_name, license_num=license_num,
                            gmt_created=gmt_created, gmt_updated=gmt_updated, area=area, project_name=project_name)
        session.add(medicine)
    session.commit()

def main_10():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
    }
    sum = []
    url = 'https://bjca.miit.gov.cn/bsfw/gsgg/xzxk/art/2020/art_00f0e1881a7f4e57a0eb08427f6c6356.html'
    response = requests.request(method='get', url=url, headers=headers,timeout=10).text
    tree = etree.HTML(response)
    lists = tree.xpath('//div[@class="pages_content"]/table/tbody/tr[position()>1]')

    gmt_created = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    gmt_updated = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    for l in lists:
        license_num = l.xpath('./td[1]//text()')[0]
        company_name = l.xpath('./td[2]//text()')[0]
        project_name = '存储转发类业务'
        area = 1

        print(company_name, license_num, gmt_created, gmt_updated, area)
        medicine = Medicine(company_name=company_name, license_num=license_num,
                            gmt_created=gmt_created, gmt_updated=gmt_updated, area=area, project_name=project_name)
        session.add(medicine)
    session.commit()

def main_11():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
    }
    sum = []
    url = 'https://bjca.miit.gov.cn/wzpz/art/2020/art_aec0bb53a8aa496388150038b3c2d4a8.html'
    response = requests.request(method='get', url=url, headers=headers,timeout=10).text
    tree = etree.HTML(response)
    lists = tree.xpath('//div[@class="pages_content"]/span/table/tbody/tr[position()>1]')

    gmt_created = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    gmt_updated = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    for l in lists:
        license_num = l.xpath('./td[1]//text()')[0]
        company_name = l.xpath('./td[2]//text()')[0]
        valid_date = l.xpath('./td[5]//text()')[0]
        invalid_date = l.xpath('./td[6]//text()')[0]
        project_name = '固定网国内数据传送业务'
        area = 1

        print(company_name, license_num, gmt_created, gmt_updated, area)
        medicine = Medicine(company_name=company_name, license_num=license_num,valid_date=valid_date,invalid_date=invalid_date,
                            gmt_created=gmt_created, gmt_updated=gmt_updated, area=area, project_name=project_name)
        session.add(medicine)
    session.commit()


def get_updated():
    db = pymysql.connect(host="192.168.2.99", user="root", password='BOOT-xwork1024', database="spider", port=3306)
    cursor = db.cursor()
    sql = "select permit_number from spider_add_value_telecom_info"
    cursor.execute(sql)
    db_data = cursor.fetchall()
    # print(db_data)
    # exit()
    data = [i[0].strip() for i in db_data]
    # print(data)
    # exit()
    from pybloom_live import ScalableBloomFilter
    bloom = ScalableBloomFilter(initial_capacity=10000,error_rate=0.001)
    for bl in data:
        bloom.add(bl)
    return bloom


if __name__ == '__main__':
    main_11()
    # parse_7_file2()