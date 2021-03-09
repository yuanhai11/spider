#coding:utf-8
'''
数仓里的浙江数据，去http://202.106.121.52:8580/searchweb/query.jsp拿数据
'''
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
    __tablename__ = 'spider_add_value_telecom_zj'

    # 表的结构:
    id = Column(Integer(), primary_key=True,autoincrement=True)
    permit_number = Column(String(256))
    company_name = Column(String(256))
    busi_web = Column(String(256))
    busi_type = Column(String(256))
    customer_service_tel = Column(String(256))
    certificate_valid_date = Column(String(256))
    certificate_invalid_date = Column(String(256))
    gmt_created = Column(String(256))
    gmt_updated = Column(String(256))
    company_id = Column(String(256))
# 初始化数据库连接:
engine = create_engine('mysql+pymysql://root:BOOT-xwork1024@192.168.2.97:3306/spider')
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

def post_data():
    with open('data/business_project除了杭州的浙江数据.json', encoding='utf-8')as fp:
        content = json.loads(fp.read())
    print(len(content))
    sum = []
    for company_name,ranges in content:

        time.sleep(3)
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Length': '332',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'asopSearchUserName=C0E6C927-A7FA-F8E8-197C-339630838038; lastAccessTime=1599630838038; JSESSIONID=5E36F6AD6962754A4EF96AE3E5BBE0BE; lastLoginTime=1599634000115',
            'Host': '202.106.121.52:8580',
            'Origin': 'http://202.106.121.52:8580',
            'Referer': 'http://202.106.121.52:8580/searchweb/query.jsp',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }
        post_url = "http://202.106.121.52:8580/searchweb/search"
        data = {
            'fullText':company_name,
            'pageSize': '10',
            'pageNow': '1',
            'sortType': '0',
            'searchType': '0',
            'titleFoldBegin': '-1',
            'titleFoldPage': '-1',
            'urls': 'zjca.miit.gov.cn/n477169/n477283/'  # 关键字段
        }
        response = json.loads(requests.post(post_url, data=data, headers=headers, proxies=proxys[-1], timeout=10).text).get('array')

        times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        if not response:
            print('{} can not find ！！！'.format(company_name))
            zhilian = Medicine(company_name=company_name,gmt_created=times, gmt_updated=times)
            sum.append(zhilian)
            continue

        if len(response) > 1:
            print('{} have many msg but i only get one !'.format(company_name))

        detail_url = [i.get('url') for i in response][0]
        head = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
            'If-None-Natch': '',
            'If-Modified-Since': ''
        }
        response = ""
        for IP in range(20):
            try:
                response = requests.request(method='get', url=detail_url, headers=head, proxies=proxys[-1],
                                            timeout=10, )
                if response.status_code == 200:
                    response = response.content.decode('utf-8')
                    break
            except Exception:
                dl()
        if not response:
            print('{} get 404 page !'.format(company_name))
            zhilian = Medicine(company_name=company_name, gmt_created=times, gmt_updated=times)
            sum.append(zhilian)
            continue
        tree = etree.HTML(response)
        element_list = tree.xpath('//table[@class="table_biaoge"]/tbody')
        for ele in element_list:
            permit_number = ele.xpath('./tr[2]/td[2]/a/text()')[0].strip()
            company_name = ele.xpath('./tr[3]/td[2]/a/text()')[0].strip()
            busi_web = ele.xpath('./tr[4]/td[2]/a/text()')[0].strip()
            if '$content' in busi_web:
                busi_web = '数据显示错误'
            busi_type = ele.xpath('./tr[5]/td[2]/a/text()')[0].strip()
            customer_service_tel = ele.xpath('./tr[6]/td[2]/a/text()')[0].strip()
            if '$content' in customer_service_tel:
                customer_service_tel = '数据显示错误'
            certificate_valid_date = ele.xpath('./tr[7]/td[2]/a/text()')[0].strip()
            certificate_invalid_date = ele.xpath('./tr[8]/td[2]/a/text()')[0].strip()

            times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print((permit_number, company_name, busi_web, busi_type, customer_service_tel,
                   certificate_valid_date, certificate_invalid_date))
            zhilian = Medicine(company_name=company_name, permit_number=permit_number,
                               busi_web=busi_web, busi_type=busi_type,
                               customer_service_tel=customer_service_tel,
                               certificate_valid_date=certificate_valid_date,
                               certificate_invalid_date=certificate_invalid_date,
                               gmt_created=times, gmt_updated=times)
            sum.append(zhilian)


    if len(sum) == 0:
        print('本次无更新数据！！！')
    else:
        print('本地数据更新了{}条！！！'.format(len(sum)))
        write_db(sum)

def write_db(sum):
    for i in sum:
        session.add(i)
    session.commit()
    session.close()

if __name__ == '__main__':
    post_data()

