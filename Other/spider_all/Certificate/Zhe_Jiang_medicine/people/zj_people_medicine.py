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
    __tablename__ = 'spider_zj_people_medicine'

    # 表的结构:
    id = Column(Integer(), primary_key=True,autoincrement=True)
    record_id = Column(String(256))
    detail_url = Column(String(256))
    name = Column(String(256))
    company = Column(String(256))
    person_type = Column(String(256))
    content = Column(String(256))
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
    sql = "select detail_url from spider_zj_people_medicine"
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
    for page in range(36,37):
        # if page == 36:
        #     break
        data = {
            "search['sKey']": '',
             "search['category']": "yp",
            "search['type']": "PERS",
            "pAttr2['pageCur']": page,
            "pAttr2['infoSize']": 10000
        }
        url = "http://mpa.zjfda.gov.cn/xzspajax!listOfInfo.do"
        response_web = ""
        for IP in range(10):
            try:
                response_web = requests.request(method='post', url=url, data = data,headers=headers,proxies=proxys[-1],
                                                timeout=10)
                # print(response)
                if response_web.status_code == 200:
                    response_web = response_web.content.decode('utf8')
                    break
            except Exception:
                dl()
        response = json.loads(response_web)

        results = response.get('list')
        for i in results:
            person_type = i.get('CHNTABLE')
            id = i.get('ID')
            TNAME = i.get('TNAME')
            detail_url = "http://mpa.zjfda.gov.cn/xzsp!infoDetail.do?id={}&tableNo={}".format(id, TNAME)

            if person_type == "药品零售人员":
                name = i.get('NAME')
                company = i.get('ADDRESS')
                person_type = '药品零售人员'

                # 非共同字段
                station = i.get('NO')

                single = {}
                single['station'] = station
                content = json.dumps(single,ensure_ascii=False)

                times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

                print((id,detail_url,name,company,person_type,content))
                if detail_url not in bloom:
                    zhilian = Medicine(record_id=id,name=name,company=company,content=content,
                                       person_type=person_type,detail_url=detail_url,
                                       gmt_created=times, gmt_updated=times)
                    sum.append(zhilian)
            elif person_type == "执业药师人员":
                head = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
                }
                response_web = ""
                for IP in range(15):
                    try:
                        response_web = requests.request(method='get', url=detail_url, headers=head,
                                                        proxies=proxys[-1],
                                                        timeout=10)
                        # print(response)
                        if response_web.status_code == 200:
                            response_web = response_web.content.decode('utf8')
                            print('break！！！')
                            break
                    except Exception:
                        dl()

                name = re.findall(r'姓名:</td>.*?<td>(.*?)</td>', response_web, re.S)[0].strip()
                company = re.findall(r'工作单位:</td>.*?<td>(.*?)</td>', response_web, re.S)[0].strip()
                person_type = "执业药师人员"

                # 非共同字段
                register_license_num = re.findall(r'注册证号:</td>.*?<td>(.*?)</td>', response_web, re.S)[0].strip()
                register_license_invalid = re.findall(r'注册证有效期:</td>.*?<td>(.*?)</td>', response_web, re.S)[0].strip()
                type = re.findall(r'状态:</td>.*?<td>(.*?)</td>', response_web, re.S)[0].strip()

                single = {}
                single['register_license_num']=register_license_num
                single['register_license_invalid']=register_license_invalid
                single['type']=type
                content = json.dumps(single,ensure_ascii=False)

                times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

                print((id, detail_url, name, company, person_type, content))
                if detail_url not in bloom:
                    zhilian = Medicine(record_id=id, name=name, company=company,
                                       content=content,
                                       person_type=person_type, detail_url=detail_url,
                                       gmt_created=times, gmt_updated=times)
                    sum.append(zhilian)
                time.sleep(1)
            elif person_type == "从业药师人员":
                head = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
                }
                response_web = ""
                for IP in range(15):
                    try:
                        response_web = requests.request(method='get', url=detail_url, headers=head,
                                                        proxies=proxys[-1],
                                                        timeout=10)
                        # print(response)
                        if response_web.status_code == 200:
                            response_web = response_web.content.decode('utf8')
                            print('break！！！')
                            break
                    except Exception:
                        dl()

                name = re.findall(r'姓名:</td>.*?<td>(.*?)</td>', response_web, re.S)[0].strip()
                company = re.findall(r'原报考单位:</td>.*?<td>(.*?)</td>', response_web, re.S)[0].strip()
                person_type = "从业药师人员"

                # 非共同字段
                work_category = re.findall(r'从业类别:</td>.*?<td>(.*?)</td>', response_web, re.S)[0].strip()
                license_valid = re.findall(r'发证日期:</td>.*?<td>(.*?)</td>', response_web, re.S)[0].strip()
                type = re.findall(r'状态:</td>.*?<td>(.*?)</td>', response_web, re.S)[0].strip()

                single = {}
                single['work_category'] = work_category
                single['license_valid'] = license_valid
                single['type'] = type
                content = json.dumps(single,ensure_ascii=False)

                times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

                print((id, detail_url, name, company, person_type, content))
                if detail_url not in bloom:
                    zhilian = Medicine(record_id=id, name=name, company=company,
                                       content=content,
                                       person_type=person_type, detail_url=detail_url,
                                       gmt_created=times, gmt_updated=times)
                    sum.append(zhilian)
                time.sleep(1)
            elif person_type == "药品批发人员":
                name = i.get('NAME')
                company = i.get('ADDRESS')
                person_type = '药品批发人员'

                # 非共同字段
                station = i.get('NO')

                single = {}
                single['station'] = station
                content = json.dumps(single, ensure_ascii=False)

                times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

                print((id, detail_url, name, company, person_type, content))
                if detail_url not in bloom:
                    zhilian = Medicine(record_id=id, name=name, company=company, content=content,
                                       person_type=person_type, detail_url=detail_url,
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
