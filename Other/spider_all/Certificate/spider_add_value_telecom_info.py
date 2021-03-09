#coding:utf-8
'''
反爬：304：加参数解决：
    'If-None-Natch':'',
    'If-Modified-Since':''
}
'''
#coding:utf-8
import json
import shutil
import re
import os
import time
import requests
import pymysql
from lxml import etree
from xlrd import open_workbook
from getCompanyId.get_company_id import get_company_id
from sqlalchemy import Column, String, create_engine,Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# 创建对象的基类:
Base = declarative_base()
# 定义User对象:
class Medicine(Base):
    # 表的名字:
    __tablename__ = 'spider_add_value_telecom_info'

    # 表的结构:
    id = Column(Integer(), primary_key=True,autoincrement=True)
    permit_number = Column(String(256))
    company_name = Column(String(256))
    company_url = Column(String(256))
    domain_info = Column(String(256))
    business_type = Column(String(256))
    customer_service_tel = Column(String(256))
    certificate_valid_date = Column(String(256))
    certificate_invalid_date = Column(String(256))
    file_name = Column(String(256))
    gmt_created = Column(String(256))
    gmt_updated = Column(String(256))
    company_id = Column(String(256))
# 初始化数据库连接:
engine = create_engine('mysql+pymysql://root:BOOT-xwork1024@192.168.2.99:3306/spider')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
# 创建session对象:
session = DBSession()

file_path = os.path.abspath('.')
proxys = []

def dl():
    dlurl = 'http://dps.kdlapi.com/api/getdps/?orderid=969607686104916&num=1&pt=2&sep=1'
    resp = requests.get(dlurl).text
    time.sleep(3)
    resp = re.sub(r'\n', '', resp)
    proxy = {
        'https': resp
    }
    proxys.append(proxy)
    print(proxys[-1])
dl()

def main():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
        'If-None-Natch': '',
        'If-Modified-Since': ''
    }
    sum = []
    url = "http://zjca.miit.gov.cn/n477174/index.html"
    response = ""
    for IP in range(10):
        try:
            response = requests.request(method='get', url=url, headers=headers,proxies=proxys[-1],timeout=10)
            if response.status_code == 200:
                response = response.content.decode('utf8')
                print('获取信息成功！！！')
                print('break！！！')
                break
        except Exception:
            dl()
    tree = etree.HTML(response)
    element_list = tree.xpath('//span[@id="comp_582207"]//ul/li')
    for ele in element_list:
        single = {}
        title = ele.xpath('./a/text()')[0]
        href = ele.xpath('./a/@href')[0][2:]
        if "增值电信业务" in title:
            single['file_name'] = title
            single['file_url'] = 'http://zjca.miit.gov.cn'+href
            times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            single['gmt_created'] = times
            single['gmt_updated'] = times

            response = ""
            for IP in range(10):
                try:
                    response = requests.request(method='get', url=single['file_url'], headers=headers, proxies=proxys[-1],
                                                timeout=10)
                    if response.status_code == 200:
                        response = response.content.decode('utf8')
                        print('获取信息成功！！！')
                        print('break！！！')
                        break
                except Exception:
                    dl()
            tree = etree.HTML(response)
            download_file_url = tree.xpath('//div[@id="content"]//a[@target="_blank"]/@href')[0].split('../')[-1]
            single['download_file_url'] = 'http://zjca.miit.gov.cn/'+download_file_url

            sum.append(single)
            print(single)
    time.sleep(2)
    parse(sum)

def get_updated():
    db = pymysql.connect(host="192.168.2.99", user="root", password='BOOT-xwork1024', database="spider", port=3306)
    cursor = db.cursor()
    sql = "select permit_number from spider_add_value_telecom_info"
    cursor.execute(sql)
    db_data = cursor.fetchall()
    # print(db_data)
    # exit()
    data = [i[0].strip() for i in db_data]
    # print(data)
    # exit()
    from pybloom_live import ScalableBloomFilter
    bloom = ScalableBloomFilter(initial_capacity=10000,error_rate=0.001)
    for bl in data:
        bloom.add(bl)
    return bloom

def parse(data):
    bloom = get_updated()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
        'If-None-Natch': '',
        'If-Modified-Since': ''
    }
    f = os.path.join(file_path, 'files')
    shutil.rmtree(f)
    if not os.path.exists(f):
        os.mkdir(f)
    sum = []
    for i in data:
        url = i.get('download_file_url')
        name = i.get('file_name')
        if url.endswith('xls'):
            file_name = '{}/{}.xls'.format(f,name)
        else:
            file_name = '{}/{}.xlsx'.format(f,name)

        response = requests.request(method='get', url=url, headers=headers).content
        with open(file_name,'wb')as fP:
            fP.write(response)
    for i in data:
        url = i.get('download_file_url')
        name = i.get('file_name')
        if url.endswith('xls'):
            file_name = '{}/{}.xls'.format(f, name)
        else:
            file_name = '{}/{}.xlsx'.format(f, name)

        workbook = open_workbook(file_name)  # 打开excel文件
        sheet2 = workbook.sheet_by_index(0)
        all_rows = sheet2.row_values(1)
        for index,i in enumerate(all_rows):
            if i.endswith('称'):
                num = index
                break
        for i in range(2, sheet2.nrows):
            permit_number = sheet2.cell(i, 0).value.strip()
            if '不予' in permit_number and '浙' in permit_number:
                permit_number= ''.join(permit_number.split('不予许可')).strip()
                permit_number= ''.join(permit_number.split('不予受理')).strip()
            if permit_number in bloom:
                print(permit_number,name)

                continue

            company_name = sheet2.cell(i, num).value.strip()

            headers = {
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Connection': 'keep-alive',
                'Content-Length': '332',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Cookie': 'asopSearchUserName=C0E6C927-A7FA-F8E8-197C-339630838038; lastAccessTime=1599630838038; JSESSIONID=5E36F6AD6962754A4EF96AE3E5BBE0BE; lastLoginTime=1599634000115',
                'Host': '202.106.121.52:8580',
                'Origin': 'http://202.106.121.52:8580',
                'Referer': 'http://202.106.121.52:8580/searchweb/query.jsp',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
                'X-Requested-With': 'XMLHttpRequest'
            }
            post_url = "http://202.106.121.52:8580/searchweb/search"
            data = {
                'pageSize': '10',
                'pageNow': '1',
                'zjbh': permit_number,
                'sortType': '0',
                'searchType': '0',
                'titleFoldBegin': '-1',
                'titleFoldPage': '-1',
                'urls': 'zjca.miit.gov.cn/n477169/n477283/'  # 关键字段
            }
            response = json.loads(requests.post(post_url, data=data, headers=headers, proxies=proxys[-1], timeout=10).text).get('array')

            if not response:
                times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                print('公司数据目前查询不到！！！')
                print(company_name,permit_number,name)
                zhilian = Medicine(company_name=company_name, permit_number=permit_number, file_name=name,
                                   gmt_created=times, gmt_updated=times)
                sum.append(zhilian)
                continue

            detail_url = [i.get('url') for i in response][0]
            head = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
                'If-None-Natch': '',
                'If-Modified-Since': ''
            }
            response = ""
            for IP in range(10):
                try:
                    response = requests.request(method='get', url=detail_url, headers=head, proxies=proxys[-1],
                                                timeout=10, )
                    if response.status_code == 200:
                        response = response.content.decode('utf-8')
                        print('获取信息成功！！！')
                        print('break！！！')
                        break
                except Exception:
                    dl()
            tree = etree.HTML(response)
            element_list = tree.xpath('//table[@class="table_biaoge"]/tbody')
            for ele in element_list:
                permit_number = ele.xpath('./tr[2]/td[2]/a/text()')[0].strip()
                company_name = ele.xpath('./tr[3]/td[2]/a/text()')[0].strip()
                domain_info = ele.xpath('./tr[4]/td[2]/a/text()')[0]
                if '$content' in domain_info:
                    domain_info = '数据显示错误'
                business_type = ele.xpath('./tr[5]/td[2]/a/text()')[0]
                customer_service_tel = ele.xpath('./tr[6]/td[2]/a/text()')[0]
                if '$content' in customer_service_tel:
                    customer_service_tel = '数据显示错误'
                certificate_valid_date = ele.xpath('./tr[7]/td[2]/a/text()')[0]
                certificate_invalid_date = ele.xpath('./tr[8]/td[2]/a/text()')[0]

                times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                company_id = get_company_id(company_name)
                if company_id:
                    print((permit_number, company_name, domain_info, business_type, customer_service_tel,
                           certificate_valid_date, certificate_invalid_date, name, detail_url
                           , company_id))
                    zhilian = Medicine(company_name=company_name, permit_number=permit_number,
                                       domain_info=domain_info, business_type=business_type,
                                       customer_service_tel=customer_service_tel,
                                       certificate_valid_date=certificate_valid_date,
                                       certificate_invalid_date=certificate_invalid_date
                                       , file_name=name, company_id=company_id, company_url=detail_url,
                                       gmt_created=times, gmt_updated=times)
                    sum.append(zhilian)
                else:
                    print((permit_number, company_name, domain_info, business_type, customer_service_tel,
                           certificate_valid_date, certificate_invalid_date, name, detail_url))
                    zhilian = Medicine(company_name=company_name, permit_number=permit_number,
                                       domain_info=domain_info, business_type=business_type,
                                       customer_service_tel=customer_service_tel,
                                       certificate_valid_date=certificate_valid_date,
                                       certificate_invalid_date=certificate_invalid_date
                                       , file_name=name,company_url=detail_url,
                                       gmt_created=times, gmt_updated=times)
                    sum.append(zhilian)

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

