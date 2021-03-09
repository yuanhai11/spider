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
    __tablename__ = 'spider_sh_product_medical_traditional_chinese_medicine'

    # 表的结构:
    id = Column(Integer(), primary_key=True,autoincrement=True)
    record_id = Column(String(256))
    chinese_medicine_name = Column(String(256))
    record_num = Column(String(256))
    medical_mechanism = Column(String(256))
    preparation_company_name = Column(String(256))
    preparation_addr = Column(String(256))
    record_date = Column(String(256))
    preparation_way = Column(String(256))
    dosage_form = Column(String(256))
    descrip = Column(String(256))
    valid_date = Column(String(256))
    record_type = Column(String(256))
    executive_standard = Column(String(256))
    medical_mechanism_regis_addr = Column(String(256))
    gmt_created = Column(String(256))
    gmt_updated = Column(String(256))
# 初始化数据库连接:
engine = create_engine('mysql+mysqlconnector://root:BOOT-xwork1024@192.168.2.99:3306/spider')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
# 创建session对象:
session = DBSession()

headers = {
    'Cookie': 'JSESSIONID=187FC5A453FA0B0A8BC90F3C451F0209; _gscu_1119681443=001357537oh62u53; zh_choose=s; _pk_ref.2.f8ac=%5B%22%22%2C%22%22%2C1600657300%2C%22http%3A%2F%2Fhdcx.smda.sh.cn%3A8088%2Fsfda%2Ftype.do%3Fmethod%3Dshow%26type%3D2%22%5D; _pk_id.2.f8ac=56e7611fcf71cdc0.1600148457.21.1600657300.1600657300.; _pk_ses.2.f8ac=*',
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
def reload(page):
    time.sleep(10)
    data = {
        'currentPage': page,
        'pageSize': '10',
        'groupSize': '8',
        'pageName': 'chinMediRecordList',
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
        'pageName': 'chinMediRecordList',
    }
    url = "http://xuke.yjj.sh.gov.cn/AppRoveManage/selectLicense/selectData"
    response_web = ""
    for IP in range(10):
        try:
            response_web = requests.request(method='post', url=url, data=data, headers=headers, proxies=proxys[-1],
                                            timeout=20)
            # print(response_web)
            if response_web.status_code == 200:
                response_web = response_web.content.decode('utf8')
                break
        except Exception:
            dl()
    response = json.loads(response_web)
    pages = int(response.get('totalPage'))
    print('数据总数：{}页！！！'.format(pages))
    time.sleep(3)
    for page in range(1,pages+1):
        data = {
            'currentPage':page,
            'pageSize': '10',
            'groupSize': '8',
            'pageName': 'chinMediRecordList',
        }
        url = "http://xuke.yjj.sh.gov.cn/AppRoveManage/selectLicense/selectData"
        response_web = ""
        for IP in range(10):
            try:
                response_web = requests.request(method='post', url=url, data = data,headers=headers,proxies=proxys[-1],
                                                timeout=20)
                # print(response)
                if response_web.status_code == 200:
                    response_web = response_web.content.decode('utf8')
                    break
            except Exception:
                dl()
        response = json.loads(response_web)
        results = response.get('rowData')
        if len(results) == 1:
            results = reload(page)
            print('跳出reload函数！！！')

        for i in results:
            id = i.get('ZSID')
            chinese_medicine_name =i.get('ZJ_TYMC')
            record_num = i.get('ZSBH')
            medical_mechanism = i.get('NAME')
            preparation_company_name = i.get('PZDW')
            preparation_addr = i.get('PZDZ')
            record_date = i.get('QFRQ')
            if record_date:
                record_date = get_time(record_date)
            preparation_way = i.get('GYLX')
            preparation_way = "".join(re.findall(r'[\u4e00-\u9fa5]',preparation_way,re.S))
            record_type = i.get('ZSZT')
            if record_type == '10':
                record_type = '已备案'
            dosage_form = i.get('ZJ_JX')
            descrip = i.get('ZJ_GG')
            valid_date = i.get('ZJ_YXQ')
            executive_standard = i.get('NKBZBH')
            medical_mechanism_regis_addr = i.get('ADDRESS')

            times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            print((id,chinese_medicine_name,record_num,medical_mechanism,preparation_company_name,preparation_addr,record_date,preparation_way,
                   dosage_form,descrip,valid_date,executive_standard,medical_mechanism_regis_addr,record_type
                   ))

            if id not in bloom:
                zhilian = Medicine(record_id=id,chinese_medicine_name=chinese_medicine_name,record_num=record_num,medical_mechanism=medical_mechanism,
                                   preparation_company_name=preparation_company_name,preparation_addr=preparation_addr,record_date=record_date,
                   preparation_way=preparation_way, dosage_form=dosage_form, descrip=descrip,record_type=record_type,
                                   valid_date=valid_date, executive_standard=executive_standard,
                   medical_mechanism_regis_addr=medical_mechanism_regis_addr,gmt_created=times, gmt_updated=times)

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
    sql = "select record_id from spider_sh_product_medical_traditional_chinese_medicine"
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
