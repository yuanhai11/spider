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
    __tablename__ = 'spider_zj_company_medicine'

    # 表的结构:
    id = Column(Integer(), primary_key=True,autoincrement=True)
    record_id = Column(String(256))
    company_name = Column(String(256))

    medicine_name = Column(String(256))
    medicine_approve_num = Column(String(256))
    medicine_approve_num_origin = Column(String(256))
    medicine_approve_num_origin_invalid = Column(String(256))

    register_addr = Column(String(256))
    license = Column(String(256))
    business_addr = Column(String(256))
    license_mechanism = Column(String(256))
    business_range = Column(String(256))
    legal_people = Column(String(256))
    company_principal = Column(String(256))
    quality_principal = Column(String(256))
    license_valid_date = Column(String(256))
    license_invalid_date = Column(String(256))
    gsp_license_num = Column(String(256))
    gsp_approve_valid_date = Column(String(256))
    gsp_approve_invalid_date = Column(String(256))
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
    time.sleep(2)
    dlurl = 'http://dps.kdlapi.com/api/getdps/?orderid=969607686104916&num=1&pt=2&sep=1'
    resp = requests.get(dlurl).text
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
    sql = "select record_id from spider_zj_company_medicine"
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
    '''
    网站含有 5种及以上的文本格式，字段不同，无法全部入库，进行数据筛选入库，
    '''
    bloom = get_updated()
    sum = []
    data = {
        "search['sKey']": '',
        "search['category']": "yp",
        "search['type']": "CORP",
        "pAttr2['pageCur']": 1,
        "pAttr2['infoSize']": 100
    }
    url = "http://mpa.zjfda.gov.cn/xzspajax!listOfInfo.do"
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
    pages = int(response.get('pAttr').get('pageTotal'))
    print('数据总数：{}页！！！'.format(pages))
    # exit()
    time.sleep(3)
    for page in range(500,pages+1):
        # if page == 500:
        #     break
        data = {
            "search['sKey']": '',
             "search['category']": "yp",
            "search['type']": "CORP",
            "pAttr2['pageCur']": page,
            "pAttr2['infoSize']": 100
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
                time.sleep(1.5)
                dl()
        response = json.loads(response_web)

        results = response.get('list')
        for i in results:
            id = i.get('ID')
            t_name = i.get('TNAME')
            url = "http://mpa.zjfda.gov.cn/xzsp!infoDetail.do?id={}&tableNo={}".format(id,t_name)
            print(url)
            head = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
            }
            response_web = ""
            for IP in range(10):
                try:
                    response_web = requests.request(method='get', url=url, headers=head,
                                                    proxies=proxys[-1],
                                                    timeout=10)
                    # print(response)
                    if response_web.status_code == 200:
                        response_web = response_web.content.decode('utf8')
                        print('break！！！')
                        break
                except Exception:
                    time.sleep(1.5)
                    dl()

            sign1 = re.findall(r'GSP证号:</td>.*?<td>(.*?)</td>', response_web, re.S)
            sign2 = re.findall(r'生产许可证:</td>.*?<td>(.*?)</td>', response_web, re.S)
            sign3 = re.findall(r'食品名称:</td>.*?<td>(.*?)</td>', response_web, re.S)
            try:
                if len(sign1) !=0:
                    company_name = re.findall(r'企业名称:</td>.*?<td>(.*?)</td>', response_web,re.S)[0].strip()
                    register_addr = re.findall(r'注册地址:</td>.*?<td>(.*?)</td>', response_web,re.S)[0].strip()
                    license = re.findall(r'药品经营（零售）许可证:</td>.*?<td>(.*?)</td>', response_web,re.S)
                    if len(license)!=0:
                        license = license[0].strip()
                    else:
                        license = re.findall(r'药品经营（批发）许可证:</td>.*?<td>(.*?)</td>', response_web,re.S)[0].strip()

                    business_addr = re.findall(r'经营地址:</td>.*?<td>(.*?)</td>', response_web,re.S)[0].strip()
                    license_mechanism = re.findall(r'证书发放部门:</td>.*?<td>(.*?)</td>', response_web,re.S)[0].strip()
                    business_range = re.findall(r'经营范围:</td>.*?<td>(.*?)</td>', response_web,re.S)[0].strip()
                    legal_people = re.findall(r'法定代表人:</td>.*?<td>(.*?)</td>', response_web,re.S)[0].strip()
                    company_principal = re.findall(r'企业负责人:</td>.*?<td>(.*?)</td>', response_web,re.S)[0].strip()
                    quality_principal = re.findall(r'质量负责人:</td>.*?<td>(.*?)</td>', response_web,re.S)[0].strip()
                    license_valid_date = re.findall(r'经营许可证书发放日期:</td>.*?<td>(.*?)</td>', response_web,re.S)
                    if len(license_valid_date)!=0:
                        license_valid_date = license_valid_date[0].strip()
                    else:
                        license_valid_date = re.findall(r'经营许可证发放日期:</td>.*?<td>(.*?)</td>', response_web,re.S)[0].strip()
                    license_invalid_date = re.findall(r'经营许可证书有效期:</td>.*?<td>(.*?)</td>', response_web,re.S)
                    if len(license_invalid_date)!=0:
                        license_invalid_date = license_invalid_date[0].replace('\t','').replace('\r','').replace('\n','')
                    else:
                        license_invalid_date = re.findall(r'经营许可证有效期:</td>.*?<td>(.*?)</td>', response_web,re.S)[0].replace('\t','').replace('\r','').replace('\n','')

                    gsp_license_num = re.findall(r'GSP证号:</td>.*?<td>(.*?)</td>', response_web,re.S)[0].strip()
                    gsp_approve_valid_date = re.findall(r'GSP证书发放日期:</td>.*?<td>(.*?)</td>', response_web,re.S)[0].strip()
                    gsp_approve_invalid_date = re.findall(r'GSP证书有效期:</td>.*?<td>(.*?)</td>', response_web,re.S)[0].replace('\t','').replace('\r','').replace('\n','')
                    times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    print((id,company_name,register_addr,license,business_addr,license_mechanism,business_range,legal_people,
                           company_principal,quality_principal,license_valid_date,license_invalid_date,gsp_license_num,gsp_approve_valid_date,
                           gsp_approve_invalid_date ))
                    if id not in bloom:
                        zhilian = Medicine(record_id=id,company_name=company_name,register_addr=register_addr,license=license,business_addr=business_addr
                                           ,license_mechanism=license_mechanism,legal_people=legal_people,
                                           business_range=business_range,company_principal=company_principal,
                                           quality_principal=quality_principal,
                                           license_valid_date=license_valid_date,license_invalid_date=license_invalid_date,gsp_license_num=gsp_license_num,
                                           gsp_approve_valid_date=gsp_approve_valid_date,gsp_approve_invalid_date=gsp_approve_invalid_date,
                                           gmt_created=times, gmt_updated=times)
                        sum.append(zhilian)
                elif len(sign2)!=0:
                    company_name = re.findall(r'企业名称:</td>.*?<td>(.*?)</td>', response_web, re.S)[0].strip()
                    register_addr = re.findall(r'注册地址:</td>.*?<td>(.*?)</td>', response_web, re.S)[0].strip()
                    license = re.findall(r'生产许可证:</td>.*?<td>(.*?)</td>', response_web, re.S)[0].strip()
                    business_addr = re.findall(r'生产地址及范围:</td>.*?<td>(.*?)</td>', response_web, re.S)[0].strip()
                    license_mechanism = re.findall(r'证书发放部门:</td>.*?<td>(.*?)</td>', response_web, re.S)[0].strip()
                    legal_people = re.findall(r'法定代表人:</td>.*?<td>(.*?)</td>', response_web, re.S)[0].strip()
                    company_principal = re.findall(r'企业负责人:</td>.*?<td>(.*?)</td>', response_web, re.S)[0].strip()
                    quality_principal = re.findall(r'质量负责人:</td>.*?<td>(.*?)</td>', response_web, re.S)[0].strip()
                    license_valid_date = re.findall(r'证书发放日期:</td>.*?<td>(.*?)</td>', response_web, re.S)[0].strip()
                    license_invalid_date = re.findall(r'证书有效期:</td>.*?<td>(.*?)</td>', response_web, re.S)[0].replace(
                        '\t', '').replace('\r', '').replace('\n', '')
                    times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    print((id, company_name, register_addr, license, business_addr, license_mechanism,
                           legal_people,
                           company_principal, quality_principal, license_valid_date, license_invalid_date))
                    if id not in bloom:
                        zhilian = Medicine(record_id=id, company_name=company_name, register_addr=register_addr,
                                           license=license, business_addr=business_addr
                                           , license_mechanism=license_mechanism, legal_people=legal_people,
                                          company_principal=company_principal,
                                           quality_principal=quality_principal,
                                           license_valid_date=license_valid_date, license_invalid_date=license_invalid_date,
                                           gmt_created=times, gmt_updated=times)
                        sum.append(zhilian)
                elif len(sign3)!=0:
                        company_name = re.findall(r'企业名称:</td>.*?<td>(.*?)</td>', response_web, re.S)[0].strip()
                        medicine_name = re.findall(r'食品名称:</td>.*?<td>(.*?)</td>', response_web, re.S)[0].strip()
                        medicine_approve_num = re.findall(r'食品批准文号:</td>.*?<td>(.*?)</td>', response_web, re.S)[0].strip()
                        medicine_approve_num_origin = re.findall(r'原广告批准文号:</td>.*?<td>(.*?)</td>', response_web, re.S)[0].strip()
                        medicine_approve_num_origin_invalid = re.findall(r'原广告批准文号有效期至:</td>.*?<td>(.*?)</td>', response_web, re.S)[0].strip()
                        times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                        print((id, company_name,medicine_name,medicine_approve_num,medicine_approve_num_origin,medicine_approve_num_origin_invalid))
                        if id not in bloom:
                            zhilian = Medicine(record_id=id, company_name=company_name, medicine_approve_num=medicine_approve_num,
                                               medicine_name=medicine_name, medicine_approve_num_origin=medicine_approve_num_origin
                                               , medicine_approve_num_origin_invalid=medicine_approve_num_origin_invalid,
                                               gmt_created=times, gmt_updated=times)
                            sum.append(zhilian)
            except Exception as e:
                continue
            time.sleep(1.5)
        time.sleep(2.5)

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
