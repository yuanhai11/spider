#-*- conding: utf-8 -*-
import requests
from lxml import etree
'''
解析pdf里的table
'''
def parse_pdf_table():
    import tabula

    df = tabula.read_pdf(r'C:\Users\20945\Desktop\Spider\local_spider\Other\1.pdf', encoding='gbk', pages='all')
    print(df)

    for j in df:
        for indexs in j.index:
            print(j.loc[indexs].values[1].strip())
'''
解析docx的数据
'''
def parse_docx():
    import docx
    data = docx.Document(r'C:\Users\20945\Desktop\Spider\now_spider\goverment_infomation_source_data\files\杭州市2016年第一批浙江省科技型企业公示名单.docx')
    print(data)
    all_tables = data.tables
    sum = []
    for ta in all_tables:
        rows = ta.rows
        for j in range(1, len(rows)):
            name = ta.cell(j, 1).text
            area = ta.cell(j, 2).text
            year = '2016'
            type = '省科技型'
            batch = '第一批'
            print((name,area))
            sum.append((name,area,year,type,batch))
'''
解析excle里的数据
'''
import xlrd
def parse_excle():
    from xlrd import open_workbook
    workbook = open_workbook(
        r'D:\projects\Spider\local_spider\Other\spider_company_icp.xlsx')  # 打开excel文件
    sheet2 = workbook.sheet_by_index(0)
    print(sheet2.nrows)
    sum = []
    for i in range(1, sheet2.nrows):
        company_name = sheet2.cell(i, 1).value
        web_name = sheet2.cell(i, 2).value
        permit_number = sheet2.cell(i, 3).value
        web_domain = sheet2.cell(i, 4).value
        web_index = sheet2.cell(i, 5).value
        web_type = sheet2.cell(i, 6).value
        verify_time = xlrd.xldate.xldate_as_datetime(sheet2.cell(i, 7).value, 0).strftime("%Y-%m-%d %H:%M:%S")
        gmt_created = xlrd.xldate.xldate_as_datetime(sheet2.cell(i, 8).value, 0).strftime("%Y-%m-%d %H:%M:%S")
        gmt_updated = xlrd.xldate.xldate_as_datetime(sheet2.cell(i, 9).value, 0).strftime("%Y-%m-%d %H:%M:%S")

        single = (company_name,web_name,permit_number,web_domain,web_index,web_type,verify_time,
               gmt_created,gmt_updated)
        print(single)
        sum.append(single)
def insert_db():
    pass

'''
解析客户端里的数据
'''
# 众创
'''
import requests
from lxml import etree
from getCompanyId.get_company_id import get_company_id
from sqlalchemy import Column, String, create_engine,Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# 创建对象的基类:
Base = declarative_base()
# 定义User对象:
class Medicine(Base):
    # 表的名字:
    __tablename__ = 'spider_company_province_level_makerspace'

    # 表的结构:
    id = Column(Integer(), primary_key=True,autoincrement=True)
    space_name = Column(String(256))
    company_name = Column(String(256))
    city = Column(String(256))
    area = Column(String(256))
    year = Column(String(256))
    gmt_created = Column(String(256))
    gmt_updated = Column(String(256))
    company_id = Column(String(256))
# 初始化数据库连接:
engine = create_engine('mysql+pymysql://root:BOOT-xwork1024@192.168.2.99:3306/spider')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
# 创建session对象:
session = DBSession()

def parse_web():
    import pymysql,time
    sum = []
    url = "http://kjt.zj.gov.cn/art/2020/10/12/art_1228971387_58940078.html"
    headers = {
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
    }
    response = requests.request(method='get',url=url,headers = headers).content.decode('utf-8')
    tree = etree.HTML(response)
    ele_lists = tree.xpath('//div[@class="article-conter"]/div//tbody/tr')
    for ele in ele_lists:
        space_name = ele.xpath('./td[2]/p/text()')[0]
        company_name = ele.xpath('./td[3]/p/text()')[0]
        city = ele.xpath('./td[4]/p/text()')[0]
        area = ele.xpath('./td[5]/p/text()')[0]
        year = '2020'
        gmt_created = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
        gmt_updated = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())

        from getCompanyId.get_company_id import get_company_id
        company_id = get_company_id(company_name)
        if company_id:
            zhilian = Medicine(space_name=space_name,company_name=company_name,year=year,city=city,area=area,
                               gmt_created=gmt_created,gmt_updated=gmt_updated,company_id=company_id)
            sum.append(zhilian)
        else:
            zhilian = Medicine(space_name=space_name, company_name=company_name, year=year, city=city, area=area,
                               gmt_created=gmt_created, gmt_updated=gmt_updated)
            sum.append(zhilian)

    for i in sum:
        session.add(i)
    session.commit()
    session.close()
'''

# 孵化器
'''
# import requests
# from lxml import etree
# from getCompanyId.get_company_id import get_company_id
# from sqlalchemy import Column, String, create_engine,Integer
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
# # 创建对象的基类:
# Base = declarative_base()
# # 定义User对象:
# class Medicine(Base):
#     # 表的名字:
#     __tablename__ = 'spider_company_province_tech_incubator'
# 
#     # 表的结构:
#     id = Column(Integer(), primary_key=True,autoincrement=True)
#     incubator_name = Column(String(256))
#     company_name = Column(String(256))
#     type = Column(String(256))
#     city = Column(String(256))
#     area = Column(String(256))
#     year = Column(String(256))
#     gmt_created = Column(String(256))
#     gmt_updated = Column(String(256))
#     company_id = Column(String(256))
# # 初始化数据库连接:
# engine = create_engine('mysql+pymysql://root:BOOT-xwork1024@192.168.2.99:3306/spider')
# # 创建DBSession类型:
# DBSession = sessionmaker(bind=engine)
# # 创建session对象:
# session = DBSession()
# 
# def parse_web():
#     import pymysql,time
#     sum = []
#     url = "http://kjt.zj.gov.cn/art/2020/10/12/art_1228971387_58940079.html"
#     headers = {
#         'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
#     }
#     response = requests.request(method='get',url=url,headers = headers).content.decode('utf-8')
#     tree = etree.HTML(response)
#     ele_lists = tree.xpath('//div[@class="article-conter"]/div//tbody/tr')
#     for ele in ele_lists:
#         incubator_name = ele.xpath('./td[2]/p/text()')[0]
#         company_name = ele.xpath('./td[3]/p/text()')[0]
#         type = ele.xpath('./td[4]/p/text()')[0]
#         city = ele.xpath('./td[5]/p/text()')[0]
#         area = ele.xpath('./td[6]/p/text()')[0]
#         year = '2020'
#         gmt_created = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
#         gmt_updated = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
# 
#         from getCompanyId.get_company_id import get_company_id
#         company_id = get_company_id(company_name)
#         if company_id:
#             zhilian = Medicine(incubator_name=incubator_name,company_name=company_name,year=year,city=city,area=area,type=type,
#                                gmt_created=gmt_created,gmt_updated=gmt_updated,company_id=company_id)
#             sum.append(zhilian)
#         else:
#             zhilian = Medicine(incubator_name=incubator_name, company_name=company_name, year=year, city=city, area=area,type=type,
#                                gmt_created=gmt_created, gmt_updated=gmt_updated)
#             sum.append(zhilian)
# 
#     for i in sum:
#         session.add(i)
#     session.commit()
#     session.close()
'''
if __name__ == '__main__':
    parse_excle()
