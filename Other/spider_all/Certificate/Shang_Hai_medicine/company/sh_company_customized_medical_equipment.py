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
    '''
        1、更新机制：无
        2、目前：1条数据
        3、目前为止：无数据更新，不需要更新
    '''
    # 表的名字:
    __tablename__ = 'spider_sh_company_customized_medical_equipment'

    # 表的结构:
    id = Column(Integer(), primary_key=True,autoincrement=True)
    record_id = Column(String(256))
    record_num = Column(String(256))
    product_name = Column(String(256))
    product_description = Column(String(1000))
    application_range = Column(String(1000))
    company_name = Column(String(256))
    addr = Column(String(256))
    produce_addr = Column(String(256))
    tel = Column(String(256))
    register_license_num = Column(String(256))
    license_num = Column(String(256))
    proxy_people = Column(String(256))
    proxy_register_addr = Column(String(256))
    proxy_tel = Column(String(256))
    medicine_mechanism_name = Column(String(256))
    medicine_mechanism_addr = Column(String(256))
    department_name = Column(String(256))
    docter = Column(String(256))
    docter_title = Column(String(256))
    docter_tel = Column(String(256))
    record_mechanism = Column(String(256))
    record_date = Column(String(256))
    updated_message = Column(String(256))
    remove_record_message = Column(String(256))
    remark = Column(String(256))
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
def get_updated():
    db = pymysql.connect(host="192.168.2.99", user="root", password='BOOT-xwork1024', database="spider", port=3306)
    cursor = db.cursor()
    sql = "select record_id from spider_sh_company_customized_medical_equipment"
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
    data = {
        'currentPage': '1',
        'pageSize': '10',
        'groupSize': '8',
        'pageName': 'dzsylqxbaList',
    }
    url = "http://xuke.smda.sh.cn/AppRoveManage/selectLicense/selectData"
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
    pages = response.get('totalPage')
    print('数据总数量：{}页！！！'.format(pages))
    time.sleep(3)
    for page in range(1,pages+1):
        data = {
            'currentPage': page,
            'pageSize': '10',
            'groupSize': '8',
            'pageName': 'dzsylqxbaList',
        }
        url = "http://xuke.smda.sh.cn/AppRoveManage/selectLicense/selectData"
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
        # print(results)

        for i in results:
            id = i.get('ZSID')
            record_num = i.get('ZSBH')
            product_name = i.get('CPMC')
            product_description = i.get('CPMS')
            application_range = i.get('SYFW')

            company_name = i.get('QYMC_ZW')
            addr = i.get('ZSDZ')
            produce_addr = i.get('SCDZXX')
            tel = i.get('LXRJLXDH')
            register_license_num = i.get('ZCZH')
            license_num = i.get('SCXKZH')
            proxy_people = ''
            proxy_register_addr = ''
            proxy_tel = ''
            medicine_mechanism_name = i.get('YLJGMC')
            medicine_mechanism_addr = i.get('YLJGDZ')
            department_name = i.get('ZYKSMC')
            docter = i.get('ZZYS')
            docter_title = i.get('ZZYSZC')
            docter_tel = i.get('YLJGLXRJLXDH')
            record_mechanism = i.get('SLJG')
            record_date = i.get('FZRQ')
            if record_date:
                record_date = get_time(record_date)
            updated_message = ''
            remove_record_message = ''
            remark = ''
            times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            print((id,record_num,product_name,product_description,application_range,company_name,addr,produce_addr,tel,register_license_num,license_num,
                   proxy_people,proxy_register_addr,proxy_tel,medicine_mechanism_name,medicine_mechanism_addr,department_name,
                   docter,docter_title,docter_tel,record_mechanism,record_date,updated_message,remove_record_message,remark))
            # if id not in bloom:
            zhilian = Medicine(record_id=id,record_num=record_num,product_name=product_name,product_description=product_description,application_range=application_range,
                               company_name=company_name,addr=addr,produce_addr=produce_addr,tel=tel,
                               register_license_num=register_license_num,license_num=license_num,proxy_people=proxy_people,
                               proxy_register_addr=proxy_register_addr,proxy_tel=proxy_tel,medicine_mechanism_name=medicine_mechanism_name,
                                medicine_mechanism_addr = medicine_mechanism_addr, department_name = department_name, docter = docter,
                                docter_title = docter_title, docter_tel = docter_tel, record_mechanism = record_mechanism,
                                record_date = record_date, updated_message = updated_message, remove_record_message = remove_record_message,remark=remark,
                               gmt_created=times, gmt_updated=times)
            sum.append(zhilian)

        time.sleep(8)

    # if len(sum) == 0:
    #     print('本次无更新数据！！！')
    # else:
    #     print('本地数据更新了{}条！！！'.format(len(sum)))
    write_db(sum)

def write_db(sum):
    for i in sum:
        session.add(i)
    session.commit()
    session.close()


if __name__ == '__main__':
    main()
