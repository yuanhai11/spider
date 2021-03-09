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
    __tablename__ = 'spider_zj_people_medical_equipment'

    # 表的结构:
    id = Column(Integer(), primary_key=True,autoincrement=True)
    record_id = Column(String(256))
    people_name = Column(String(256))
    belong_company = Column(String(256))
    position = Column(String(256))
    remark = Column(String(256))
    detail_url = Column(String(256))
    gmt_created = Column(String(256))
    gmt_updated = Column(String(256))
# 初始化数据库连接:
engine = create_engine('mysql+mysqlconnector://root:BOOT-xwork1024@192.168.2.99:3306/spider')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
# 创建session对象:
session = DBSession()

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Length': '120',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': 'JSESSIONID=4666C867AF24208B318E1CD46F5E6E06',
    'Host': 'mpa.zjfda.gov.cn',
    'Origin': 'http://mpa.zjfda.gov.cn',
    'Referer': 'http://mpa.zjfda.gov.cn/xzsp!listOfInfoMore.do?search[%27sKey%27]=&search[%27category%27]=yp&search[%27type%27]=CORP',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
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
    sql = "select record_id from spider_zj_people_medical_equipment"
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

def main():
    bloom = get_updated()
    sum = []
    # data = {
    #     "search['sKey']": '',
    #     "search['category']": "qx",
    #     "search['type']": "PERS",
    #     "pAttr2['pageCur']": 1,
    #     "pAttr2['infoSize']": 100
    # }
    # url = "http://mpa.zjfda.gov.cn/xzspajax!listOfInfo.do"
    # response_web = ""
    # for IP in range(10):
    #     try:
    #         response_web = requests.request(method='post', url=url, data=data, headers=headers, proxies=proxys[-1],
    #                                         timeout=10)
    #         # print(response)
    #
    #         if response_web.status_code == 200:
    #             response_web = response_web.content.decode('utf8')
    #             break
    #     except Exception:
    #         dl()
    # # print(response_web)
    # # exit()
    # response = json.loads(response_web)
    # pages = int(response.get('pAttr').get('pageTotal'))
    # print('数据总数：{}页！！！'.format(pages))
    # # exit()
    # time.sleep(3)
    for page in range(1,53):
        data = {
            "search['sKey']": '',
             "search['category']": "qx",
            "search['type']": "PERS",
            "pAttr2['pageCur']": page,
            "pAttr2['infoSize']": 10000
        }
        url = "http://mpa.zjfda.gov.cn/xzspajax!listOfInfo.do"
        response_web = ""
        for IP in range(10):
            try:
                response_web = requests.request(method='post', url=url, data = data,headers=headers,proxies=proxys[-1],
                                                timeout=25)
                # print(response)
                if response_web.status_code == 200:
                    response_web = response_web.content.decode('utf8')
                    break
            except Exception:
                dl()
        response = json.loads(response_web)
        results = response.get('list')
        print(len(results))
        # exit()
        for i in results:
            id = i.get('ID')
            people_name = i.get('NAME')
            position = i.get('NO')

            TNAME = i.get('TNAME')
            url = "http://mpa.zjfda.gov.cn/xzsp!infoDetail.do?id={}&tableNo={}".format(id,TNAME)

            times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            print((id, people_name, position, url))

            if id not in bloom:
                zhilian = Medicine(record_id=id, people_name=people_name,
                                   position=position,
                                   detail_url=url,
                                   gmt_created=times, gmt_updated=times)
                sum.append(zhilian)
        time.sleep(3)

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
