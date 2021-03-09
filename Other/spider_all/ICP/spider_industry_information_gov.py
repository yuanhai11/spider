
#coding:utf-8
'''
反爬：304：加参数解决：
    'If-None-Natch':'',
    'If-Modified-Since':''
}
'''
#coding:utf-8
import json
import shutil
import re
import os
import time
import requests
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
    __tablename__ = 'spider_industry_information_gov'

    # 表的结构:
    id = Column(Integer(), primary_key=True,autoincrement=True)
    permit_number = Column(String(256))
    company_name = Column(String(256))
    busi_type = Column(String(256))
    busi_range = Column(String(256))
    invalid_date = Column(String(256))
    gmt_created = Column(String(256))
    gmt_updated = Column(String(256))
    company_id = Column(String(256))
# 初始化数据库连接:
engine = create_engine('mysql+pymysql://root:BOOT-xwork1024@192.168.2.99:3306/spider')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
# 创建session对象:
session = DBSession()

file_path = os.path.abspath('.')

proxys = []
def dl():
    dlurl = 'http://api.goubanjia.com/dynamic/get/d490a5d4debefc8980ae6ee4c4148552.html?sep=3'
    resp = requests.get(dlurl).text
    time.sleep(3)
    resp = re.sub(r'\n', '', resp)
    proxy = {
        'https': resp
    }
    proxys.append(proxy)
    print(proxys[-1])
dl()

def main():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
    }
    sum = []
    for page in range(1500,2098):
        url = 'https://zwfw.miit.gov.cn/miit/resultSearch?wd=&categoryTreeId=302&categoryTreePid=&pagenow={}'.format(page)
        response = ""
        for IP in range(20):
            try:
                response = requests.request(method='get', url=url, headers=headers,proxies=proxys[-1],timeout=10)
                if response.status_code == 200:
                    response = response.content.decode('utf8')
                    print('获取信息成功！！！')
                    print('break！！！')
                    break
            except Exception:
                dl()
        tree = etree.HTML(response)
        element_list = tree.xpath('//table[@class="table table-bordered table-responsive"]/tbody/tr')
        for ele in element_list:
            permit_number = ele.xpath('./td[2]/@title')[0]
            company_name = ele.xpath('./td[3]/@title')[0]
            busi_type = ele.xpath('./td[4]/@title')[0]
            busi_range = ele.xpath('./td[5]/@title')[0]
            invalid_date = ele.xpath('./td[6]/@title')[0]

            times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            company_id = get_company_id(company_name)
            print(permit_number, company_name, busi_type, busi_range, invalid_date)

            if company_id:
                zhilian = Medicine(permit_number=permit_number,company_name=company_name,busi_type=busi_type,busi_range=busi_range,invalid_date=invalid_date,
                                   gmt_created=times,gmt_updated=times,company_id=company_id)
                sum.append(zhilian)
            else:
                zhilian = Medicine(permit_number=permit_number,company_name=company_name,busi_type=busi_type,busi_range=busi_range,invalid_date=invalid_date,
                                   gmt_created=times,gmt_updated=times)
                sum.append(zhilian)
        time.sleep(2)

    write_db(sum)

def write_db(sum):
    for i in sum:
        session.add(i)
    session.commit()
    session.close()

if __name__ == '__main__':
    main()

