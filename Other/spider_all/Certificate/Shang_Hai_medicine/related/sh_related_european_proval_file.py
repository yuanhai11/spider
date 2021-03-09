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
    __tablename__ = 'spider_sh_related_european_proval_file'

    # 表的结构:
    id = Column(Integer(), primary_key=True,autoincrement=True)
    record_id = Column(String(256))
    prove_file_num = Column(String(256))
    company_name = Column(String(256))
    export_medicine_name = Column(String(256))
    china_approve_num = Column(String(256))
    file_issue_date = Column(String(256))
    file_valid_date = Column(String(256))
    gmt_created = Column(String(256))
    gmt_updated = Column(String(256))
# 初始化数据库连接:
engine = create_engine('mysql+mysqlconnector://root:BOOT-xwork1024@192.168.2.99:3306/spider')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
# 创建session对象:
session = DBSession()

headers = {
    'cookie':'JSESSIONID=5B5FE5C70C40D5FDC5191F843CE07DC8; zh_choose=s; _pk_ref.2.8c15=%5B%22%22%2C%22%22%2C1600251367%2C%22http%3A%2F%2Fxuke.yjj.sh.gov.cn%2FAppRoveManage%2FselectLicense%2Fzww%3FpageName%3DapparatusProdBackList%22%5D; _pk_id.2.8c15=1c50b8bddf2e2c19.1599717248.2.1600251380.1600251367.; AlteonP=AEH5UaHgEqz1pm1I+2XzRQ$$',
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

    url = "http://hdcx.smda.sh.cn:8088/sfda/table.do?method=search&page=1&Id=96"
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

    response = re.findall(r'共(.*?)页',response_web,re.S)[0]
    pages = int(response)
    print('数据总数：{}页！！！'.format(pages))
    time.sleep(3)

    for page in range(1,pages+1):
        url = "http://hdcx.smda.sh.cn:8088/sfda/table.do?method=search&page={}&Id=96".format(page)
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
        tree = etree.HTML(response_web)
        ele_list = tree.xpath('//table[@bgcolor="#CCCCCC"]/tbody/tr')[1:-1]
        for ele in ele_list:
            detail_url = 'http://hdcx.smda.sh.cn:8088/sfda/' + ele.xpath('./td[5]/a/@href')[0]
            response_web = ""
            for IP in range(10):
                try:
                    response_web = requests.request(method='get', url=detail_url, headers=headers, proxies=proxys[-1],
                                                    timeout=10)
                    # print(response)
                    if response_web.status_code == 200:
                        response_web = response_web.content.decode('utf8')
                        break
                except Exception:
                    dl()
            tree = etree.HTML(response_web)
            ele_li = tree.xpath('//table[@bgcolor="#CCCCCC"]/tbody')
            for e in ele_li:
                record_id = detail_url
                prove_file_num = e.xpath('./tr[1]/td[2]/text()')
                if len(prove_file_num) == 0:
                    prove_file_num = ""
                else:
                    prove_file_num = prove_file_num[0]
                company_name = e.xpath('./tr[2]/td[2]/text()')
                if len(company_name) == 0:
                    company_name = ""
                else:
                    company_name = company_name[0]

                export_medicine_name = e.xpath('./tr[3]/td[2]/text()')
                if len(export_medicine_name) == 0:
                    export_medicine_name = ""
                else:
                    export_medicine_name = export_medicine_name[0]
                china_approve_num= e.xpath('./tr[4]/td[2]/text()')
                if len(china_approve_num) == 0:
                    china_approve_num = ""
                else:
                    china_approve_num= china_approve_num[0]
                file_issue_date = e.xpath('./tr[5]/td[2]/text()')
                if len(file_issue_date) == 0:
                    file_issue_date = ""
                else:
                    file_issue_date = file_issue_date[0]
                file_valid_date = e.xpath('./tr[6]/td[2]/text()')
                if len(file_valid_date) == 0:
                    file_valid_date = ""
                else:
                    file_valid_date = file_valid_date[0]
                times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

                print((record_id,prove_file_num,company_name,export_medicine_name,china_approve_num,file_issue_date,file_valid_date,
                       ))

                if id not in bloom:
                    zhilian = Medicine(record_id=record_id,company_name=company_name,prove_file_num=prove_file_num,export_medicine_name=export_medicine_name,
                                       china_approve_num=china_approve_num,file_issue_date=file_issue_date,
                                       file_valid_date=file_valid_date,
                       gmt_created=times, gmt_updated=times)
                    sum.append(zhilian)

            time.sleep(0.8)
        time.sleep(3)
    if len(sum) == 0:
        print('本次无更新数据！！！')
    else:
        print('本地数据更新了{}条！！！'.format(len(sum)))
        write_db(sum)

def get_updated():
    db = pymysql.connect(host="192.168.2.99", user="root", password='BOOT-xwork1024', database="spider", port=3306)
    cursor = db.cursor()
    sql = "select record_id from spider_sh_related_european_proval_file"
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
