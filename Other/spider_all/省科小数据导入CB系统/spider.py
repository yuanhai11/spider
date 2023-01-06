import re
import time
import requests
import pymysql
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
    __tablename__ = 'culture'

    # 表的结构:
    id = Column(Integer(), primary_key=True,autoincrement=True)
    declare_detail_id = Column(String(256))

    # gmt_created = Column(String(256))
    # gmt_updated = Column(String(256))

# 初始化数据库连接:
engine = create_engine('mysql+mysqlconnector://root:BOOT-xwork1024@rm-bp1x7590o7df9vv70o.mysql.rds.aliyuncs.com:3306/zl_saas')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
# 创建session对象:
session = DBSession()
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
}

def parse_3_file1(file_name = r'D:\projects\S_Git_proj\spider\Other\spider_all\省科小数据导入CB系统\model.xlsx'):

    workbook = open_workbook(file_name)  # 打开excel文件
    sheet2 = workbook.sheet_by_index(0)
    all_rows = sheet2.nrows
    all_col = sheet2.row_values(5)
    print(len(all_col))
    print((all_col))
    print(all_rows)

    gmt_created = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    gmt_updated = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    a = []
    for i in range(6, all_rows):
        company_name = sheet2.cell(i, 0).value.strip()
        busi_status = sheet2.cell(i, 1).value.strip()
        date = sheet2.cell(i, 2).value.strip()
        provice = sheet2.cell(i, 3).value.strip()
        city = sheet2.cell(i, 4).value.strip()
        area = sheet2.cell(i, 5).value.strip()
        insure = sheet2.cell(i, 6).value.strip()
        type = sheet2.cell(i, 7).value.strip()
        industry = sheet2.cell(i, 8).value.strip()
        phone = sheet2.cell(i, 9).value.strip()
        busi_range = sheet2.cell(i, 10).value.strip()
        if type not in ['有限责任公司(自然人投资或控股)','有限责任公司(自然人独资)','有限责任公司（自然人投资或控股的法人独资）']:
            continue
        print(company_name,busi_status,date,provice,city,area,insure,type,industry,phone,busi_range)
        a.append(company_name)
    print(len(a))

def main():
    con = session.query(Medicine).all()
    print(len(con))
    session.close()

    parse_3_file1()

if __name__ == '__main__':
    main()
