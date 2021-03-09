import re
import time
import requests
import pymysql
import json
from lxml import etree
from getCompanyId.get_company_id import get_company_id
from sqlalchemy import Column, String, create_engine,Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# 创建对象的基类:
Base = declarative_base()
# 定义User对象:

class Medicine(Base):
    # 表的名字:
    __tablename__ = 'spider_radio_show_business_license'

    # 表的结构:
    id = Column(Integer(), primary_key=True,autoincrement=True)
    license_number = Column(String(256))
    company_name = Column(String(256))
    social_credit_code = Column(String(256))
    legal_people = Column(String(256))
    company_addr = Column(String(256))
    company_id = Column(String(256))

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
def main():
    bloom = get_updated()
    url = "http://gdj.zj.gov.cn/module/search/index.jsp?field=field_561854:1,field_561855:1,field_561856:1,field_561857:1,field_561858:1&i_columnid=style_1016&field_561854=&field_561855=&field_561856=&field_561857=&field_561858=&currpage=1"
    response = ""
    for IP in range(10):
        try:
            response = requests.request(method='get', url=url, headers=headers, proxies=proxys[-1], timeout=15)
            if response.status_code == 200:
                response = response.content.decode('utf8')
                print('break！！！')
                break
        except Exception:
            dl()
    results = int(re.findall(r"共&nbsp;(.*?)&nbsp;页", response, re.S)[0])
    print('目标数据总页数：{}'.format(results))
    sum = []
    for page in range(1,results+1):
        if page == 20: # 数据更新以 前30页数据为基准；
            break
        url = "http://gdj.zj.gov.cn/module/search/index.jsp?field=field_561854:1,field_561855:1,field_561856:1,field_561857:1,field_561858:1&i_columnid=style_1016&field_561854=&field_561855=&field_561856=&field_561857=&field_561858=&currpage={}".format(page)
        response_web = ""
        for IP in range(10):
            try:
                response_web = requests.request(method='get', url=url, headers=headers,proxies=proxys[-1],timeout=15)
                # print(response)
                if response_web.status_code == 200:
                    response_web = response_web.content.decode('utf8')
                    print('break！！！')
                    break
            except Exception:
                dl()
        license_number = re.findall(r'<td align="center" width="170" bgcolor="#FFFFFF">(.*?)</td>', response_web, re.S)
        company_name = re.findall(r'<td align="center" width="310" bgcolor="#FFFFFF">(.*?)</td>', response_web, re.S)
        social_credit_code = re.findall(r'<td align="center" width="186" bgcolor="#FFFFFF">(.*?)</td>', response_web, re.S)
        legal_people = re.findall(r'<td align="center" width="100" bgcolor="#FFFFFF">(.*?)</td>', response_web, re.S)
        company_addr = re.findall(r'<td align="center" width="300" bgcolor="#FFFFFF">(.*?)</td>', response_web, re.S)

        res = zip(license_number,company_name,social_credit_code,legal_people,company_addr)
        for i in res:
            license_number = i[0]
            company_name = i[1]
            social_credit_code = i[2]
            legal_people = i[3]
            company_addr = i[4]
            times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            if social_credit_code not in bloom:
                company_id = get_company_id(company_name)
                if company_id:
                    print((license_number,company_name,social_credit_code,legal_people,company_addr,company_id))
                    zhilian = Medicine(license_number=license_number, company_name=company_name, social_credit_code=social_credit_code,
                                       legal_people=legal_people,
                                       company_addr=company_addr, company_id=company_id,
                                       gmt_created=times, gmt_updated=times)
                    sum.append(zhilian)
                else:
                    print((license_number,company_name,social_credit_code,legal_people,company_addr))
                    zhilian = Medicine(license_number=license_number, company_name=company_name,
                                       social_credit_code=social_credit_code,
                                       legal_people=legal_people,
                                       company_addr=company_addr,
                                       gmt_created=times, gmt_updated=times)
                    sum.append(zhilian)

        time.sleep(1.7)
    if len(sum) == 0:
        print('此次没有数据更新！！！')
    else:
        print('此次更新数据有{}条！！！'.format(len(sum)))
        write_db(sum)

def get_updated():
    db = pymysql.connect(host="192.168.2.99", user="root", password='BOOT-xwork1024', database="spider", port=3306)
    cursor = db.cursor()
    sql = "select social_credit_code from spider_radio_show_business_license"
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
