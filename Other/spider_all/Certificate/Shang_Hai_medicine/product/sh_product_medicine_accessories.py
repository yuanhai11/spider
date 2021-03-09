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
    __tablename__ = 'spider_sh_product_medicine_accessories'

    # 表的结构:
    id = Column(Integer(), primary_key=True,autoincrement=True)
    record_id = Column(String(256))
    accept_number = Column(String(256))
    approval_document_number = Column(String(256))
    old_approval_number = Column(String(256))
    approval_number = Column(String(256))
    product_name = Column(String(256))
    produce_company = Column(String(256))
    produce_addr = Column(String(256))
    standard = Column(String(256))
    gmt_created = Column(String(256))
    gmt_updated = Column(String(256))
# 初始化数据库连接:
engine = create_engine('mysql+mysqlconnector://root:BOOT-xwork1024@192.168.2.99:3306/spider')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
# 创建session对象:
session = DBSession()

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
}
proxys = []
def dl():
    dlurl = 'http://dps.kdlapi.com/api/getdps/?orderid=969607686104916&num=1&pt=2&sep=1'
    resp = requests.get(dlurl).text
    time.sleep(2)
    resp = re.sub(r'\n', '', resp)
    proxy = {
        'https': resp
    }
    proxys.append(proxy)
    print(proxys[-1])
dl()

def get_time(t):
    import time
    t = int(str(t)[:-3])
    time_local = time.localtime(t)
    dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
    return dt
def reload(page):
    time.sleep(10)
    data = {
        'currentPage': page,
        'pageSize': '10',
        'groupSize': '8',
        'pageName': 'apparatusWTProdList',
    }
    url = "http://xuke.yjj.sh.gov.cn/AppRoveManage/selectLicense/selectData"
    response_web = ""
    for IP in range(10):
        try:
            response_web = requests.request(method='post', url=url, data=data, headers=headers, proxies=proxys[-1],
                                            timeout=10)
            # print(response)
            if response_web.status_code == 200:
                response_web = response_web.content.decode('utf8')
                break
        except Exception:
            dl()
    response = json.loads(response_web)
    results = response.get('rowData')
    return results


def main():
    bloom = get_updated()
    sum = []

    url = "http://hdcx.smda.sh.cn:8088/sfda/table.do?page=1&check=1&method=search&Id=71"
    response_web = ""
    for IP in range(10):
        try:
            response_web = requests.request(method='get', url=url,headers=headers, proxies=proxys[-1],
                                            timeout=10)
            # print(response)
            if response_web.status_code == 200:
                response_web = response_web.content.decode('utf8')
                break
        except Exception:
            dl()

    pages = int(re.findall('共(.*?)页',response_web,re.S)[0])
    print('数据总数：{}页！！！'.format(pages))
    for page in range(1,pages+1):
        url = "http://hdcx.smda.sh.cn:8088/sfda/table.do?page={}&check=1&method=search&Id=71".format(page)
        response_web = ""
        for IP in range(10):
            try:
                response_web = requests.request(method='get', url=url,headers=headers,proxies=proxys[-1],
                                                timeout=10)
                # print(response)
                if response_web.status_code == 200:
                    response_web = response_web.content.decode('utf8')
                    break
            except Exception:
                dl()
        tree = etree.HTML(response_web)
        element_list = tree.xpath('//table[@bgcolor="#CCCCCC"]/tbody/tr')[1:-1]
        for ele in element_list:
            detail_url = 'http://hdcx.smda.sh.cn:8088/sfda/' + ele.xpath('./td[last()]/a/@href')[0].replace(' ','')
            hea = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
                'cookie':'JSESSIONID=D53AFF54CF8F74459A8ABC4C42350F17; zh_choose=s; _pk_ref.2.8c15=%5B%22%22%2C%22%22%2C1600251367%2C%22http%3A%2F%2Fxuke.yjj.sh.gov.cn%2FAppRoveManage%2FselectLicense%2Fzww%3FpageName%3DapparatusProdBackList%22%5D; _pk_id.2.8c15=1c50b8bddf2e2c19.1599717248.2.1600251380.1600251367.; AlteonP=AKZTPaHgEqzFFxMQllubNw$$'
            }
            response_web = ""
            for IP in range(10):
                try:
                    response_web = requests.request(method='get', url=detail_url, headers=hea, proxies=proxys[-1],
                                                    timeout=10)
                    # print(response)
                    if response_web.status_code == 200:
                        response_web = response_web.content.decode('utf8')
                        break
                except Exception:
                    dl()
            tree = etree.HTML(response_web)
            element_list = tree.xpath('//table[@bgcolor="#CCCCCC"]/tbody')
            for e in element_list:
                accept_number = e.xpath('./tr[1]/td[2]/text()')
                if len(accept_number) != 0:
                    accept_number = accept_number[0]
                else:
                    accept_number = ""
                approval_document_number = e.xpath('./tr[2]/td[2]/text()')
                if len(approval_document_number) != 0:
                    approval_document_number = approval_document_number[0]
                else:
                    approval_document_number = ""
                old_approval_number = e.xpath('./tr[3]/td[2]/text()')
                if len(old_approval_number) != 0:
                    old_approval_number = old_approval_number[0]
                else:
                    old_approval_number = ""
                approval_number = e.xpath('./tr[4]/td[2]/text()')
                if len(approval_number) != 0:
                    approval_number = approval_number[0]
                else:
                    approval_number = ""
                product_name = e.xpath('./tr[5]/td[2]/text()')
                if len(product_name) != 0:
                    product_name = product_name[0]
                else:
                    product_name = ""
                produce_company = e.xpath('./tr[6]/td[2]/text()')
                if len(produce_company) != 0:
                    produce_company = produce_company[0]
                else:
                    produce_company = ""
                produce_addr = e.xpath('./tr[7]/td[2]/text()')
                if len(produce_addr) != 0:
                    produce_addr = produce_addr[0]
                else:
                    produce_addr = ""
                standard = e.xpath('./tr[8]/td[2]/text()')
                if len(standard) != 0:
                    standard = standard[0]
                else:
                    standard = ""
                print(accept_number,approval_document_number,old_approval_number,approval_number,product_name,produce_company,produce_addr,standard)
                times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

                if id not in bloom:
                    zhilian = Medicine(record_id=detail_url,accept_number=accept_number,approval_document_number=approval_document_number,old_approval_number=old_approval_number,
                                       product_name=product_name,approval_number=approval_number,produce_company=produce_company,produce_addr=produce_addr,standard=standard,
                                       gmt_created=times, gmt_updated=times)
                    sum.append(zhilian)
            time.sleep(1.5)

        time.sleep(2)

    if len(sum) == 0:
        print('本次无更新数据！！！')
    else:
        print('本地数据更新了{}条！！！'.format(len(sum)))
        write_db(sum)

def get_updated():
    db = pymysql.connect(host="192.168.2.99", user="root", password='BOOT-xwork1024', database="spider", port=3306)
    cursor = db.cursor()
    sql = "select record_id from spider_sh_product_medicine_accessories"
    cursor.execute(sql)
    db_data = cursor.fetchall()
    # print(db_data)
    # exit()
    data = [i[0] for i in db_data]
    from pybloom_live import ScalableBloomFilter
    bloom = ScalableBloomFilter(initial_capacity=10000, error_rate=0.001)
    for bl in data:
        bloom.add(bl)
    return bloom

def write_db(sum):
    for i in sum:
        session.add(i)
    session.commit()
    session.close()


if __name__ == '__main__':
    main()
