import re
import time
import requests
import pymysql
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
    __tablename__ = 'spider_certificate_js'

    # 表的结构:
    id = Column(Integer(), primary_key=True,autoincrement=True)
    url = Column(String(256))
    license_num = Column(String(256))
    company_name = Column(String(256))
    project_name = Column(String(256))
    valid_date = Column(String(256))
    invalid_date = Column(String(256))

    gmt_created = Column(String(256))
    gmt_updated = Column(String(256))
    company_id = Column(String(256))

# 初始化数据库连接:
engine = create_engine('mysql+pymysql://root:BOOT-xwork1024@192.168.2.97:3306/spider')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
# 创建session对象:
session = DBSession()
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
}
proxys = []
def dl():
    while 1:
        try:
            dlurl = 'http://api.goubanjia.com/dynamic/get/d490a5d4debefc8980ae6ee4c4148552.html?sep=3'
            resp = requests.get(dlurl).text
            break
        except Exception:
            pass
    time.sleep(2)
    resp = re.sub(r'\n', '', resp)
    proxy = {
        'https': resp
    }
    proxys.append(proxy)
    print(proxys[-1])
dl()

def get_response(url):
    time.sleep(0.5)
    response_web = ""
    for IP in range(10):
        try:
            response_web = requests.request(method='get', url=url, headers=headers,proxies=proxys[-1],
                                            timeout=10)
            if response_web.status_code == 200:
                response_web = response_web.content.decode('utf-8')
                break
        except Exception:
            dl()
    return response_web
def main():
    '''
    # 江苏资质类数据
    :return:
    '''
    bloom = get_updated()
    for page in range(778,1500):
        url = 'http://218.94.106.121/zwdtportal/xzxkcfgs.jsi?type=xk&applicantName=&pagenum={}'.format(page)
        time.sleep(0.5)
        response_web = get_response(url)
        if response_web == "":
            continue

        tree = etree.HTML(response_web)
        elemant_lists = tree.xpath('//div[@id="tab1"]//tr')[1:]
        for ele in elemant_lists:

            detail_url = 'http://218.94.106.121' + ele.xpath('./td[2]/a/@href')[0]
            if detail_url not in bloom:
                response_detail = get_response(detail_url)
                if response_detail == "":
                    continue
                tree = etree.HTML(response_detail)
                license_num = ''.join(tree.xpath('//table//tr[1]/td[2]/text()')).strip()
                company_name = ''.join(tree.xpath('//table//tr[5]/td[2]/text()')).strip()
                project_name = ''.join(tree.xpath('//table//tr[2]/td[2]/text()')).strip()
                valid_date = ''.join(tree.xpath('//table//tr[12]/td[2]/text()')).strip()
                invalid_date = ''.join(tree.xpath('//table//tr[13]/td[2]/text()')).strip()
                gmt_created = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                gmt_updated = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


                medicine = Medicine(url=detail_url,company_name=company_name,license_num=license_num,project_name=project_name,valid_date=valid_date,invalid_date=invalid_date,
                                    gmt_created=gmt_created,gmt_updated=gmt_updated)
                print(company_name,license_num,project_name,valid_date,invalid_date,gmt_created,gmt_updated,'page',page)
                session.add(medicine)
        session.commit()

def get_updated():
    db = pymysql.connect(host="192.168.2.97", user="root", password='BOOT-xwork1024', database="spider", port=3306)
    cursor = db.cursor()
    sql = "select url from spider_qualification where area = 10 and license_name like '[%]'"
    cursor.execute(sql)
    db_data = cursor.fetchall()
    data = [i[0] for i in db_data]
    from pybloom_live import ScalableBloomFilter
    bloom = ScalableBloomFilter(initial_capacity=100000,error_rate=0.001)
    for bl in data:
        bloom.add(bl)
    return bloom

if __name__ == '__main__':
    main()
