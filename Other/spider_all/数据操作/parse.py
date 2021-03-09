import json
import pymysql


'''
从97数据库下的company_info中过滤部分 杭州的数据
条件：reg_authority字段含有：（基础电信业务/第一类增值电信业务/第二类增值电信业务/互联网新闻信息服务）等
关键字段：reg_authority
'''

def get_filter_hz():
    sum = []
    db = pymysql.connect(host='192.168.2.97', password='BOOT-xwork1024', database='spider', user='root')
    cursor = db.cursor()
    sql = "SELECT company_name,business_project FROM `company_info` WHERE " \
          "(`reg_authority` LIKE '绍兴%' OR `reg_authority` LIKE '新昌%' OR `reg_authority`LIKE '诸暨%' OR `reg_authority` LIKE '嵊州%') OR" \
          "`reg_authority` LIKE '金华%' OR `reg_authority` LIKE '武义%' OR `reg_authority` LIKE '浦江%' OR `reg_authority` LIKE '兰溪%' OR `reg_authority` LIKE '义乌%' OR `reg_authority` LIKE '东阳%' OR `reg_authority` LIKE '永康%'" \
          "OR `reg_authority` LIKE '宁波%' OR `reg_authority` LIKE '象山%' OR `reg_authority` LIKE '宁海%' OR `reg_authority` LIKE '余姚%' OR `reg_authority` LIKE '慈溪%'" \
          "OR `reg_authority` LIKE '衢州%' OR `reg_authority` LIKE '常山%' OR `reg_authority` LIKE '开化%' OR `reg_authority` LIKE '龙游%' OR `reg_authority` LIKE '江山%'" \
          "OR `reg_authority` LIKE '温州%' OR `reg_authority` LIKE '永嘉%' OR `reg_authority` LIKE '平阳%' OR `reg_authority` LIKE '苍南%' OR `reg_authority` LIKE '文成%' OR `reg_authority` LIKE '泰顺%' OR `reg_authority` LIKE '瑞安%' OR `reg_authority` LIKE '乐清%'" \
          "OR `reg_authority` LIKE '嘉兴%' OR `reg_authority` LIKE '嘉善%' OR `reg_authority`LIKE '海盐%' OR `reg_authority` LIKE '海宁%' OR `reg_authority` LIKE '平湖%' OR `reg_authority` LIKE '桐乡%'" \
          "OR `reg_authority` LIKE '台州%' OR `reg_authority` LIKE '三门%' OR `reg_authority`LIKE '天台%' OR `reg_authority` LIKE '仙居%' OR `reg_authority` LIKE '温岭%' OR `reg_authority` LIKE '临海%' OR `reg_authority` LIKE '玉环%'" \
          "OR `reg_authority` LIKE '湖州%' OR `reg_authority` LIKE '德清%' OR `reg_authority`LIKE '长兴%' OR `reg_authority` LIKE '安吉%'" \
          "OR `reg_authority` LIKE '舟山%' OR `reg_authority` LIKE '普陀%' OR `reg_authority`LIKE '岱山%' OR `reg_authority` LIKE '嵊泗%'" \
          "OR `reg_authority` LIKE '丽水%' OR `reg_authority` LIKE '青田%' OR `reg_authority`LIKE '缙云%' OR `reg_authority` LIKE '遂昌%' OR `reg_authority` LIKE '松阳%' OR `reg_authority` LIKE '云和%' OR `reg_authority` LIKE '庆元%' OR `reg_authority` LIKE '景宁畲族自治%' OR `reg_authority` LIKE '龙泉%'"
    cursor.execute(sql)
    data = cursor.fetchall()
    data = [[i[0], i[1]] for i in data]
    print(len(data))
    for i in data:
        if i[1] == None:
            continue
        if '基础电信业务' in i[1]:
            sum.append(i)
        elif '第一类增值电信业务' in i[1]:
            sum.append(i)
        elif '第二类增值电信业务' in i[1]:
            sum.append(i)
        elif '互联网新闻信息服务' in i[1]:
            sum.append(i)
        elif '药品互联网信息服务' in i[1]:
            sum.append(i)
        elif '互联网信息服务' in i[1]:
            sum.append(i)
        elif '医疗器械互联网信息服务' in i[1]:
            sum.append(i)
        elif '呼叫中心' in i[1]:
            sum.append(i)
        elif '经营电信业务' in i[1]:
            sum.append(i)
    print(len(sum))
    with open('../ICP/data/business_project除了杭州的浙江数据.json', 'a', encoding='utf-8')as fp:
        fp.write(json.dumps(sum, ensure_ascii=False))

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
    get_filter_hz()