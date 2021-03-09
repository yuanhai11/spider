import re
import time
import requests
import pymysql
from lxml import etree
from sqlalchemy import Column, String, create_engine,Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# 创建对象的基类:
Base = declarative_base()
# 定义User对象:
class Medicine(Base):
    # 表的名字:
    __tablename__ = 'spider_talent_room'

    # 表的结构:
    id = Column(Integer(), primary_key=True,autoincrement=True)
    business_type = Column(String(256))
    apply_person_name = Column(String(256))
    apply_person_id_card = Column(String(256))
    company_name = Column(String(256))
    talent_type = Column(String(256))
    loved_name = Column(String(256))
    loved_id_card = Column(String(256))
    loved_company = Column(String(256))
    show_start_end_date = Column(String(256))
    gmt_created = Column(String(256))
    gmt_updated = Column(String(256))
    year = Column(String(256))
# 初始化数据库连接:
engine = create_engine('mysql+pymysql://root:BOOT-xwork1024@192.168.2.99:3306/spider')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
# 创建session对象:
session = DBSession()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
}
proxys = []
def dl():
    dlurl = 'http://dps.kdlapi.com/api/getdps/?orderid=969607686104916&num=1&pt=2&sep=1'
    resp = requests.get(dlurl).text
    time.sleep(4)
    resp = re.sub(r'\n', '', resp)
    proxy = {
        'https': resp
    }
    proxys.append(proxy)
    print(proxys[-1])
dl()

'''
代码目前不考虑更新
'''
def main_2020():
    sum = []
    urls = ['http://rc.zjhz.hrss.gov.cn/articles/detail/11007.html']
    for url in urls:
        response_web = ""
        for IP in range(10):
            try:
                response_web = requests.request(method='get', url=url, headers=headers, proxies=proxys[-1],
                                                timeout=15)
                if response_web.status_code == 200:
                    response_web = response_web.content.decode('utf8')
                    break
            except Exception:
                dl()
                time.sleep(1.5)
        tree = etree.HTML(response_web)
        ele_list = tree.xpath('//div[@class="articel-detail-con mgtop20"]/table//tr')[1::]
        print(len(ele_list))
        for ele in ele_list:
            business_type = ele.xpath('./td[2]/text()')[0].strip()
            apply_person_name = ele.xpath('./td[3]/text()')[0].strip()
            apply_person_id_card = ele.xpath('./td[4]/text()')[0].strip()
            company_name = ele.xpath('./td[5]/text()')[0].strip()
            talent_type = ele.xpath('./td[6]/text()')[0].strip()
            loved_name = ele.xpath('./td[7]/text()')[0].strip()
            loved_id_card = ele.xpath('./td[8]/text()')[0].strip()
            loved_company = ele.xpath('./td[9]/text()')[0].strip()
            show_start_end_date = ele.xpath('./td[10]/text()')[0].strip()
            times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            year = '2020'
            print(business_type, apply_person_name, apply_person_id_card, company_name, talent_type, loved_name,
                  loved_id_card, loved_company, show_start_end_date)
            zhilian = Medicine(business_type=business_type,apply_person_name=apply_person_name,apply_person_id_card=apply_person_id_card,company_name=company_name,
                               talent_type=talent_type,loved_name=loved_name,loved_id_card=loved_id_card,loved_company=loved_company,show_start_end_date=show_start_end_date,
                               gmt_created=times, gmt_updated=times,year=year)
            sum.append(zhilian)

    if len(sum) == 0:
        print('本次无更新数据！！！')
    else:
        print('本地数据更新了{}条！！！'.format(len(sum)))
        write_db(sum)

def main_2019():
    sum = []
    urls = ['http://rc.zjhz.hrss.gov.cn/articles/detail/5518.html']
    for url in urls:
        response_web = ""
        for IP in range(10):
            try:
                response_web = requests.request(method='get', url=url, headers=headers, proxies=proxys[-1],
                                                timeout=15)
                if response_web.status_code == 200:
                    response_web = response_web.content.decode('utf8')
                    break
            except Exception:
                dl()
                time.sleep(1.5)
        tree = etree.HTML(response_web)
        ele_list = tree.xpath('//div[@class="articel-detail-con mgtop20"]/table//tr')[1::]
        print(len(ele_list))
        for ele in ele_list:
            business_type = ele.xpath('./td[2]/text()')[0].strip()
            apply_person_name = ele.xpath('./td[3]/text()')[0].strip()
            apply_person_id_card = ele.xpath('./td[4]/text()')[0].strip()
            company_name = ele.xpath('./td[5]/text()')[0].strip()
            talent_type = ele.xpath('./td[6]/text()')[0].strip()
            loved_name = ele.xpath('./td[7]/text()')[0].strip()
            loved_id_card = ele.xpath('./td[8]/text()')[0].strip()
            loved_company = ele.xpath('./td[9]/text()')[0].strip()
            show_start_end_date = "".join(ele.xpath('./td[10]//text()')).strip()
            times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            year = '2019'
            print(business_type, apply_person_name, apply_person_id_card, company_name, talent_type, loved_name,
                  loved_id_card, loved_company, show_start_end_date)
            zhilian = Medicine(business_type=business_type,apply_person_name=apply_person_name,apply_person_id_card=apply_person_id_card,company_name=company_name,
                               talent_type=talent_type,loved_name=loved_name,loved_id_card=loved_id_card,loved_company=loved_company,show_start_end_date=show_start_end_date,
                               gmt_created=times, gmt_updated=times,year=year)
            sum.append(zhilian)
        write_db(sum)

def write_db(sum):
    for i in sum:
        session.add(i)
    session.commit()
    session.close()


if __name__ == '__main__':
    main_2019()