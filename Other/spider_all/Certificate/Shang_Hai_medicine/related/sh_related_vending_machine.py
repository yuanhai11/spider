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
    __tablename__ = 'spider_sh_related_vending_machine'

    # 表的结构:
    id = Column(Integer(), primary_key=True,autoincrement=True)
    record_id = Column(String(256))
    company_name = Column(String(256))
    mechine_num = Column(String(256))
    mechine_name = Column(String(256))
    area = Column(String(256))
    street = Column(String(256))
    addr = Column(String(256))
    business_time = Column(String(256))
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
    time.sleep(4)
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
def main():
    bloom = get_updated()
    sum = []

    url = "http://ssjk.smda.sh.cn:8867/openApi/zdsyjItemJqgrid?enpName=&regionCode=&syjAddr=&auditStatus=0&type=public&search=false&nd=1600420570184&rows=20&page=2&sidx=&sord=desc&totalrows=2000"
    response_web = ""
    for IP in range(10):
        try:
            response_web = requests.request(method='get', url=url, headers=headers, proxies=proxys[-1],
                                            timeout=10)
            # print(response)
            if response_web.status_code == 200:
                response_web = response_web.content.decode('utf8')
                break
        except Exception:
            dl()
    response = json.loads(response_web)
    pages = int(response.get('total'))
    print('数据总数：{}页！！！'.format(pages))
    time.sleep(3)

    for page in range(1,pages+1):
        url = "http://ssjk.smda.sh.cn:8867/openApi/zdsyjItemJqgrid?enpName=&regionCode=&syjAddr=&auditStatus=0&type=public&search=false&nd=1600420570184&rows=20&page={}&sidx=&sord=desc&totalrows=2000".format(page)
        response_web = ""
        for IP in range(10):
            try:
                response_web = requests.request(method='get', url=url, headers=headers,proxies=proxys[-1],
                                                timeout=10)
                # print(response)
                if response_web.status_code == 200:
                    response_web = response_web.content.decode('utf8')
                    break
            except Exception:
                dl()
        response = json.loads(response_web)
        results = response.get('rows')
        for i in results:
            id = i.get('syjNo')
            company_name = i.get('enpName')
            mechine_num = i.get('syjNo')
            mechine_name = i.get('syjName')
            area = i.get('regionName')
            street = i.get('streetName')
            addr = i.get('syjAddr')
            busBeginHour = i.get('busBeginHour')
            busEndHour = i.get('busEndHour')
            business_time = busBeginHour + '至' +busEndHour
            times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            print((id,company_name,mechine_num,mechine_name,area,street,addr,business_time))

            if id not in bloom:
                zhilian = Medicine(record_id=id,company_name=company_name,mechine_num=mechine_num,mechine_name=mechine_name,
                               area=area,street=street,addr=addr,business_time=business_time,gmt_created=times, gmt_updated=times)
                sum.append(zhilian)
        time.sleep(5)
    if len(sum) == 0:
        print('本次无更新数据！！！')
    else:
        print('本地数据更新了{}条！！！'.format(len(sum)))
        write_db(sum)

def get_updated():
    db = pymysql.connect(host="192.168.2.99", user="root", password='BOOT-xwork1024', database="spider", port=3306)
    cursor = db.cursor()
    sql = "select record_id from spider_sh_related_vending_machine"
    cursor.execute(sql)
    db_data = cursor.fetchall()
    # print(db_data)
    # exit()
    data = [i[0] for i in db_data]
    from pybloom_live import ScalableBloomFilter
    bloom = ScalableBloomFilter(initial_capacity=10000,error_rate=0.001)
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
