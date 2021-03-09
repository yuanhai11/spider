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
# 初始化数据库连接:
engine = create_engine('mysql+mysqlconnector://root:BOOT-xwork1024@192.168.2.99:3306/spider')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
# 创建session对象:
session = DBSession()
# 定义User对象:
class Medicine(Base):
    # 表的名字:
    __tablename__ = 'spider_sh_related_medicine_export_sale_prove'

    # 表的结构:
    id = Column(Integer(), primary_key=True,autoincrement=True)
    record_id = Column(String(256))
    license_num = Column(String(256))
    company_name = Column(String(256))
    medicine_name = Column(String(256))
    license_valid_date = Column(String(256))

    gmt_created = Column(String(256))
    gmt_updated = Column(String(256))

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
def get_updated():
    db = pymysql.connect(host="192.168.2.99", user="root", password='BOOT-xwork1024', database="spider", port=3306)
    cursor = db.cursor()
    sql = "select record_id from spider_sh_related_medicine_export_sale_prove"
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
def reload(page):
    time.sleep(10)
    data = {
        'currentPage': page,
        'pageSize': '10',
        'groupSize': '8',
        'pageName': 'ypckxszmList',
    }
    url = "http://xuke.yjj.sh.gov.cn/AppRoveManage/selectLicense/selectData"
    response_web = ""
    for IP in range(10):
        try:
            response_web = requests.request(method='post', url=url, data=data, headers=headers, proxies=proxys[-1],
                                            timeout=20)
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
    data = {
        'currentPage': '1',
        'pageSize': '10',
        'groupSize': '8',
        'pageName': 'ypckxszmList',
    }
    url = "http://xuke.yjj.sh.gov.cn/AppRoveManage/selectLicense/selectData"
    response_web = ""
    for IP in range(10):
        try:
            response_web = requests.request(method='post', url=url, data=data, headers=headers, proxies=proxys[-1],
                                            timeout=20)
            # print(response)
            if response_web.status_code == 200:
                response_web = response_web.content.decode('utf8')
                break
        except Exception:
            dl()
    response = json.loads(response_web)
    pages = response.get('totalPage')
    print('数据总数量：{}页！！！'.format(pages))
    time.sleep(8)
    for page in range(1,pages+1):
        data = {
            'currentPage': page,
            'pageSize': '10',
            'groupSize': '8',
            'pageName': 'ypckxszmList',
        }
        url = "http://xuke.yjj.sh.gov.cn/AppRoveManage/selectLicense/selectData"
        response_web = ""
        for IP in range(10):
            try:
                response_web = requests.request(method='post', url=url, data=data, headers=headers, proxies=proxys[-1],
                                                timeout=20)
                # print(response)
                if response_web.status_code == 200:
                    response_web = response_web.content.decode('utf8')
                    break
            except Exception:
                dl()
        response = json.loads(response_web)
        results = response.get('rowData')
        # print(results)
        if len(results) == 1:
            results = reload(page)
            print('跳出reload函数！！！')

        for i in results:
            id = i.get('zsbh')
            license_num = i.get('zsbh')
            company_name = i.get('qymcZw')
            medicine_name = i.get('cpfwZw')
            license_valid_date = i.get('qfrqAsString')
            times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            print((id,license_num,company_name,medicine_name,license_valid_date
                ))
            if id not in bloom:
                zhilian = Medicine(record_id=id,company_name=company_name,medicine_name = medicine_name,license_num=license_num,
                                   license_valid_date=license_valid_date,gmt_created=times, gmt_updated=times)
                sum.append(zhilian)

        time.sleep(8)

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
    main()
