import re
import time
import requests
import pymysql
import json
from getCompanyId.get_company_id import get_company_id
from sqlalchemy import Column, String, create_engine,Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# 创建对象的基类:
Base = declarative_base()
# 定义User对象:

class Medicine(Base):
    # 表的名字:
    __tablename__ = 'spider_sh_related_medicine_produce_license'

    # 表的结构:
    id = Column(Integer(), primary_key=True,autoincrement=True)
    record_id = Column(String(256))
    show_time = Column(String(256))
    license_num = Column(String(256))
    company_name = Column(String(256))
    classifi_code = Column(String(256))
    social_credit_code = Column(String(256))
    addr = Column(String(256))
    legal_people = Column(String(256))
    company_principal = Column(String(256))
    quality_principal = Column(String(256))
    produce_principal = Column(String(256))
    quality_authorize = Column(String(256))
    produce_addr_range = Column(String(256))
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
    # dlurl = 'http://dps.kdlapi.com/api/getdps/?orderid=969607686104916&num=1&pt=2&sep=1'
    dlurl = 'http://api.goubanjia.com/dynamic/get/d490a5d4debefc8980ae6ee4c4148552.html?sep=3'
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
    data = {
        'currentPage': '1',
        'pageSize': '10',
        'groupSize': '8',
        'pageName': 'drugProductList-Time-Limit'
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
    pages = int(response.get('totalPage'))
    print('数据总数：{}页！！！'.format(pages))
    time.sleep(3)
    for page in range(1,pages+1):
        data = {
            'currentPage':page,
            'pageSize': '10',
            'groupSize': '8',
            'pageName': 'drugProductList-Time-Limit'
        }
        url = "http://xuke.smda.sh.cn/AppRoveManage/selectLicense/selectData"
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
        results = response.get('rowData')
        for i in results:
            id = i.get('ZSBH')
            show_time = i.get('RESERVED4')
            license_num = i.get('ZSBH')
            company_name = i.get('QYMC_ZW')
            classifi_code = i.get('CPFWLB')
            social_credit_code = i.get('SHXYDM')
            addr = i.get('ZCDZ_ZW')
            legal_people = i.get('FRMC_ZW')
            company_principal = i.get('QYFZR_ZW')
            quality_principal = i.get('ZLFZR')
            produce_principal = i.get('SCFZR')
            quality_authorize = i.get('ZLSQR')
            produce_addr_range = i.get('CPFW_ZW')

            times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            company_id = get_company_id(company_name)
            if company_id:
                print((id,show_time,license_num,company_name,classifi_code,social_credit_code,addr,legal_people,company_principal,quality_principal,
                       produce_principal,quality_principal,quality_authorize,produce_addr_range,company_id))
                if id not in bloom:
                    zhilian = Medicine(record_id=id,
                                       show_time=show_time, license_num=license_num, company_name=company_name, classifi_code=classifi_code,
                                       social_credit_code=social_credit_code, addr=addr, legal_people=legal_people,company_principal=company_principal,
                                       quality_principal=quality_principal,produce_principal=produce_principal,
                                       quality_authorize=quality_authorize, produce_addr_range=produce_addr_range,
                                       gmt_created=times, gmt_updated=times,company_id=company_id)
                    sum.append(zhilian)
            else:
                print((id, show_time, license_num, company_name, classifi_code, social_credit_code, addr, legal_people,
                       company_principal, quality_principal,
                       produce_principal, quality_principal, quality_authorize, produce_addr_range))

                if id not in bloom:
                    zhilian = Medicine(record_id=id,
                                       show_time=show_time, license_num=license_num, company_name=company_name,
                                       classifi_code=classifi_code,
                                       social_credit_code=social_credit_code, addr=addr, legal_people=legal_people,
                                       company_principal=company_principal,
                                       quality_principal=quality_principal, produce_principal=produce_principal,
                                       quality_authorize=quality_authorize, produce_addr_range=produce_addr_range,
                                       gmt_created=times, gmt_updated=times)
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
    sql = "select record_id from spider_sh_related_medicine_produce_license"
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
