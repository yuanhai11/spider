# encoding:utf-8
import re
import time
import requests
import json
import pymysql
from sqlalchemy import Column, String, create_engine, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# from getCompanyId.get_company_id import get_company_id

# 创建对象的基类:
Base = declarative_base()
# 定义User对象:
class Medicine(Base):
    # 表的名字:
    __tablename__ = 'spider_company_icp'

    # 表的结构:
    id = Column(Integer(), primary_key=True, autoincrement=True)
    company_name = Column(String(256))
    web_name = Column(String(256))
    permit_number = Column(String(256))
    web_domain = Column(String(256))
    web_index = Column(String(256))
    web_type = Column(String(256))
    verify_time = Column(String(256))
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

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'
}
proxys = []
def dl():
    while 1:
        try:
            dlurl = 'http://api.goubanjia.com/dynamic/get/d490a5d4debefc8980ae6ee4c4148552.html?sep=3'
            resp = requests.get(dlurl).text
            break
        except Exception:
            pass
    time.sleep(3)
    resp = re.sub(r'\n', '', resp)
    proxy = {
        'https': resp
    }
    proxys.append(proxy)
    print(proxys[-1])
dl()

def get_icp():
    with open('../data/business_project除了杭州的浙江数据.json', encoding='utf-8')as fp:
        content = fp.read()
    company_list = json.loads(content)
    print(len(company_list))
    for index,company in enumerate(company_list):
        company = company[0]
        data = {
            'pageNo': 1,
            'pageSize': 100,
            'Kw':company
        }
        try:
            response = ""
            while 1:
                time.sleep(1)
                try:
                    response = requests.request(method='post',url='https://icp.chinaz.com/Home/PageData',headers=headers,data=data,proxies=proxys[-1],timeout=8)
                    if response.status_code == 200:
                        response = json.loads(response.text).get('data')
                        break
                except Exception:
                    dl()
            if len(response) == 0:
                print('{} not exits data！'.format(company))
                continue
            permit_number_lists = []
            for detail in response:
                company_name = company
                web_name = detail.get('webName')
                permit_number = detail.get('permit')
                if permit_number in permit_number_lists:
                    continue
                web_domain = detail.get('host')
                web_index = 'www.' + web_domain
                web_type = detail.get('typ')
                verify_time = detail.get('verifyTime')
                times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

                print(company_name,web_name,permit_number,web_domain,web_index,web_type,verify_time)

                zhilian = Medicine(company_name=company_name,web_name=web_name,permit_number=permit_number,
                                   web_domain=web_domain,web_index=web_index,web_type=web_type,verify_time=verify_time,
                                   gmt_created=times,gmt_updated=times,
                                   area = 9,
                                   )
                session.add(zhilian)
                permit_number_lists.append(permit_number)
        except Exception as e:
            print(e)
            continue

    session.commit()

if __name__ == '__main__':
    get_icp()
