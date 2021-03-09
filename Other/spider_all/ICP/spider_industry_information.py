#coding:utf-8
import re
import time
import requests
import pymysql
from lxml import etree
from getCompanyId.get_company_id import get_company_id
from sqlalchemy import Column, String, create_engine,Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import logging
import time,os
import logging.handlers
#初始化设置
logging.basicConfig(level = logging.INFO,format='%(asctime)s|%(name)-12s: %(levelname)-8s %(message)s')
#创建
logger = logging.getLogger("spider_industry_information")
logger.setLevel(logging.INFO)

log_file_path = os.path.join(os.path.abspath('.'),'log')
if not os.path.exists(log_file_path):
    os.mkdir(log_file_path)

#创建handler
handler1=logging.FileHandler("{}/spider_industry_information.log".format(log_file_path))
handler1.setLevel(logging.INFO)
formatter=logging.Formatter('%(asctime)s|%(name)-12s+ %(levelname)-8s++%(message)s')
handler1.setFormatter(formatter)
handler2=logging.StreamHandler()
handler2.setLevel(logging.ERROR)
logger.addHandler(handler1)
logger.addHandler(handler2)
# 创建对象的基类:
Base = declarative_base()
# 定义User对象:
class Medicine(Base):
    # 表的名字:
    __tablename__ = 'spider_industry_information'

    # 表的结构:
    id = Column(Integer(), primary_key=True,autoincrement=True)
    company_name = Column(String(256))
    application_matters = Column(String(256))
    permit_number = Column(String(256))
    business_type = Column(String(256))
    batch = Column(String(256))
    release_date = Column(String(256))
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
    dlurl = 'http://api.goubanjia.com/dynamic/get/d490a5d4debefc8980ae6ee4c4148552.html?sep=3'
    resp = requests.get(dlurl).text
    time.sleep(2)
    resp = re.sub(r'\n', '', resp)
    proxy = {
        'https': resp
    }
    proxys.append(proxy)
    logger.info(proxys[-1])
dl()

def main():
    bloom = get_updated()
    sum = []
    for i in range(1,2):
        url = "https://tsm.miit.gov.cn/telecom-manage/web/notice/list/1/{}".format(i)
        response = ""
        for IP in range(10):
            try:
                response = requests.request(method='get', url=url, headers=headers,proxies=proxys[-1],timeout=10,verify=False)
                if response.status_code == 200:
                    response = response.content.decode('utf8')
                    logger.info('获取信息成功！！！')
                    logger.info('break！！！')
                    break
            except Exception:
                dl()
        if not response:
            raise ValueError('代理出现问题！！！')

        tree = etree.HTML(response)
        element_list = tree.xpath('//ul[@id="noticelist1"]/li')
        for ele in element_list:
            title = ele.xpath('./a/span/text()')[0].strip()
            number = ele.xpath('./a/span/@onclick')[0].split(',')[1].split(')')[0]
            release_date = ele.xpath('./span/text()')[0]
            if '《中华人民共和国增值电信业务经营许可证》' in title:
                url = 'https://tsm.miit.gov.cn/telecom-manage/web/notice/0/{}.html'.format(number)
                times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

                if title not in bloom:
                    response=""
                    time.sleep(1)
                    for IP in range(10):
                        try:
                            response = requests.request(method='get', url=url, headers=headers, proxies=proxys[-1],
                                                        timeout=10,
                                                        verify=False)
                            if response.status_code == 200:
                                response = response.content.decode('utf8')
                                logger.info('获取信息成功！！！')
                                logger.info('break！！！')
                                break
                        except Exception:
                            dl()
                    tree = etree.HTML(response)
                    element_list = tree.xpath('//table[@class="MsoNormalTable ke-zeroborder"]/tbody/tr[position()>1]')
                    if len(element_list) == 0:
                        element_list = tree.xpath('//table[@class="ke-zeroborder"]/tbody/tr[position()>1]')

                    business_type = ""
                    for ele in element_list:
                        flag = ele.xpath('./td')
                        if len(flag) < 3:
                            business_type = ele.xpath('./td[1]/p/b/span[1]/text()')
                            if len(business_type) == 0:
                                business_type = ele.xpath('./td[1]/p/span[1]/text()')
                        else:
                            company_name = ele.xpath('./td[2]/p/span[1]/text()')
                            if len(company_name) == 0:
                                continue
                            application_matter = "".join(ele.xpath('./td[3]/p/span[1]//text()'))
                            permit_number = "".join(ele.xpath('./td[4]/p//span//text()'))

                            company_name = company_name[0]
                            application_matter = application_matter
                            permit_number = permit_number
                            batch = title
                            release_date = release_date

                            company_id = get_company_id(company_name)
                            logger.info((company_name, application_matter, permit_number, business_type[0], batch,company_id,
                                   release_date))
                            zhilian = Medicine(company_name=company_name, application_matters=application_matter,
                                               permit_number=permit_number,
                                               business_type=business_type[0], batch=batch,company_id=company_id
                                               , release_date=release_date,
                                               gmt_created=times, gmt_updated=times)
                            sum.append(zhilian)

    if len(sum) == 0:
        logger.info('本次无更新数据！！！')
    else:
        logger.info('本地数据更新了{}条！！！'.format(len(sum)))
        write_db(sum)

def get_updated():
    db = pymysql.connect(host="192.168.2.97", user="root", password='BOOT-xwork1024', database="spider", port=3306)
    cursor = db.cursor()
    sql = "select batch from spider_industry_information group by batch"
    cursor.execute(sql)
    db_data = cursor.fetchall()
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
