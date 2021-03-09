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
    __tablename__ = 'spider_sh_product_first_medical_equipment_product'

    # 表的结构:
    id = Column(Integer(), primary_key=True,autoincrement=True)
    record_id = Column(String(256))
    record_company = Column(String(256))
    organization_code = Column(String(256))
    regis_addr = Column(String(256))
    produce_addr = Column(String(256))
    proxy_people = Column(String(256))
    proxy_regis_addr = Column(String(256))
    standard = Column(String(256))
    descrip = Column(String(256))
    effect = Column(String(256))
    remark = Column(String(256))
    change = Column(String(256))
    product_name = Column(String(256))
    record_mechanism = Column(String(256))
    record_num = Column(String(256))
    structure = Column(String(256))
    classifi_code = Column(String(256))
    record_deal_people = Column(String(256))
    first_change_cancel_date = Column(String(256))
    packaging_standard = Column(String(256))
    product_valid_date = Column(String(256))
    main_ingredient = Column(String(256))
    type = Column(String(256))
    change_count = Column(String(256))
    record_type = Column(String(256))
    medical_record_num = Column(String(256))
    is_record_certificate_product = Column(String(256))
    gmt_created = Column(String(256))
    gmt_updated = Column(String(256))
    company_id = Column(String(256))
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
def reload(page):
    time.sleep(10)
    data = {
        'currentPage': page,
        'pageSize': '10',
        'groupSize': '8',
        'pageName': 'prodBackLicense',
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
        'pageName': 'prodBackLicense',
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
            'pageName': 'prodBackLicense',
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
            record_company = i.get('QYMC_ZW')
            organization_code = i.get('SHXYDM')
            regis_addr = i.get('BARZCDZ_ZW')
            produce_addr = i.get('SCDZ_ZW')
            proxy_people = i.get('CPDLRMC')
            proxy_regis_addr = i.get('CPDLRZCDZ')
            standard = i.get('GGXH')
            descrip = i.get('CPMS')
            effect = i.get('YQYT')
            remark = i.get('REMARK')
            change = i.get('BGQK')
            product_name = i.get('CPMC_ZW')
            record_mechanism = i.get('SLJG')
            record_num = i.get('ZSBH')
            structure = i.get('JGTZZW')
            classifi_code = i.get('FLBM')
            record_deal_people = i.get('BABLR')
            first_change_cancel_date = i.get('QFRQZW')
            packaging_standard = i.get('BZGG')
            product_valid_date = i.get('CPYXQ')
            main_ingredient = i.get('ZYZCCF')
            type = i.get('ZSZT')
            change_count = i.get('DJCBG')
            record_type = i.get('SQLX')
            medical_record_num = i.get('SCBAH')
            is_record_certificate_product = i.get('CPBZ')
            # from Other.post_es import get_company_id
            # company_id = get_company_id(record_company)
            # time.sleep(1)
            times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            print((id,record_company,organization_code,regis_addr,produce_addr,proxy_people,proxy_regis_addr,standard,descrip,effect,remark,change,product_name,record_mechanism,
                   record_num,structure,classifi_code,record_deal_people,first_change_cancel_date,packaging_standard,product_valid_date,main_ingredient,type,
                   change_count,record_type,medical_record_num,is_record_certificate_product
                   ))

            if id not in bloom:
                zhilian = Medicine(record_id=id,record_company=record_company,organization_code=organization_code,regis_addr=regis_addr,produce_addr=produce_addr,
                                   proxy_people=proxy_people,proxy_regis_addr=proxy_regis_addr,standard=standard,descrip=descrip,effect=effect,remark=remark,
                                   change=change,product_name=product_name,record_mechanism=record_mechanism,
                   record_num=record_num,structure=structure,classifi_code=classifi_code,record_deal_people=record_deal_people,first_change_cancel_date=first_change_cancel_date
                                   ,packaging_standard=packaging_standard,product_valid_date=product_valid_date,main_ingredient=main_ingredient,type=type,
                   change_count=change_count,record_type=record_type,medical_record_num=medical_record_num,is_record_certificate_product=is_record_certificate_product,gmt_created=times, gmt_updated=times,
                                   )

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
    sql = "select record_id from spider_sh_product_first_medical_equipment_product"
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
