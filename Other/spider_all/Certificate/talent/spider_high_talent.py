import re
import time
import requests
import pymysql
from lxml import etree
from sqlalchemy import Column, String, create_engine, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from decouple import config
import logging,os,sys


logging.basicConfig(level = logging.INFO,format='%(asctime)s|%(name)-12s: %(levelname)-8s %(message)s')
logger = logging.getLogger("spider")
logger.setLevel(logging.INFO)

log_file_path = os.path.join(os.path.abspath('.'),'log')
if not os.path.exists(log_file_path):
    os.mkdir(log_file_path)

#创建handler
handler1=logging.FileHandler("{}/spdier.log".format(log_file_path))
handler1.setLevel(logging.INFO)
formatter=logging.Formatter('%(asctime)s|%(name)-12s+ %(levelname)-8s++%(message)s')
handler1.setFormatter(formatter)
handler2=logging.StreamHandler()
handler2.setLevel(logging.ERROR)
logger.addHandler(handler1)
logger.addHandler(handler2)

D_URL = config('D_URL')

# 创建对象的基类:
Base = declarative_base()


# 定义User对象:
class Medicine(Base):
    '''
    1、更新机制：获取前30页数据
    2、频率：1周
    '''
    # 表的名字:
    __tablename__ = 'spider_high_talent'

    # 表的结构:
    id = Column(Integer(), primary_key=True, autoincrement=True)
    title_url = Column(String(256))
    name = Column(String(256))
    department = Column(String(256))
    company_name = Column(String(256))
    birth = Column(String(256))
    talent_type = Column(String(256))
    reason = Column(String(256))
    content = Column(String(256))
    release_date = Column(String(256))
    gmt_created = Column(String(256))
    gmt_updated = Column(String(256))


# 初始化数据库连接:
engine = create_engine('mysql+pymysql://root:BOOT-xwork1024@192.168.2.97:3306/spider')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
# 创建session对象:
session = DBSession()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
}
proxys = []


def dl():
    while 1:
        try:
            resp = requests.get(D_URL).text
            break
        except Exception:
            time.sleep(1)
    time.sleep(3)
    resp = re.sub(r'\n', '', resp)
    proxy = {
        'https': resp
    }
    proxys.append(proxy)
    logger.info(proxys[-1])


dl()


def get_updated():
    db = pymysql.connect(host="192.168.2.97", user="root", password='BOOT-xwork1024', database="spider", port=3306)
    cursor = db.cursor()
    sql = "select title_url from spider_high_talent"
    cursor.execute(sql)
    db_data = cursor.fetchall()
    data = [i[0] for i in db_data]
    from pybloom_live import ScalableBloomFilter
    bloom = ScalableBloomFilter(initial_capacity=100000, error_rate=0.001)
    for bl in data:
        bloom.add(bl)
    return bloom



def main():
    bloom = get_updated()
    for page in range(13, 201):  # 根据更新频率，正常情况下一周统一更新一次，以前30页为准

        url = 'https://rc.hzrs.hangzhou.gov.cn/articles/2/page/{}.html'.format(page)
        response_web = ""
        while 1:
            try:
                response_web = requests.request(method='get', url=url, headers=headers, proxies=proxys[-1],
                                                timeout=15)
                logger.info(response_web)
                if response_web.status_code == 200:
                    response_web = response_web.content.decode('utf-8')
                    break
                else:
                    dl()
            except Exception:
                dl()
        if IP == 19:
            logger.error('IP:{},page:{}'.format(IP,page))
            sys.exit()

        tree = etree.HTML(response_web)
        if page == 1:
            ele_ments_list = tree.xpath('//div[@class="index-art-list01"]//li[position()>3]')
        else:
            ele_ments_list = tree.xpath('//div[@class="index-art-list01"]//li')

        time.sleep(1.5)

        for e in ele_ments_list:
            release_date = e.xpath('./span/text()')[0]
            detail_url = 'http://rc.zjhz.hrss.gov.cn' + e.xpath('./a/@href')[0]
            response_web = ""
            for IP in range(1,20):
                try:
                    response_web = requests.request(method='get', url=detail_url, headers=headers, proxies=proxys[-1],
                                                    timeout=15)
                    logger.info('detail:{}'.format(response_web))
                    if response_web.status_code == 200:
                        response_web = response_web.content.decode('utf-8')
                        break
                    else:
                        dl()
                except Exception:
                    dl()

            if IP == 19:
                logger.error('IP:{},page:{}'.format(IP, page))
                sys.exit()
            tree = etree.HTML(response_web)
            data = tree.xpath('//div[@class="articel-detail-con mgtop20"]/p[1]')[0]
            name = data.xpath('./span[1]/text()')
            if len(name) != 0:
                name = name[0].strip()
            else:
                name = ''
            company_name = data.xpath('./span[2]/text()')
            if len(company_name) != 0:
                company_name = company_name[0].strip()
            else:
                company_name = ''
            talent_type = data.xpath('./span[3]/text()')
            if len(talent_type) != 0:
                talent_type = talent_type[0].strip()
            else:
                talent_type = ''
            reason = data.xpath('./span[4]/text()')
            if len(reason) != 0:
                reason = reason[0].strip()
            else:
                reason = ''
            text_data = "".join(tree.xpath('//div[@class="articel-detail-con mgtop20"]/p[1]/text()')).strip()
            department = re.findall(r'（所属部门：(.*?)；', text_data, re.S)
            if len(department) != 0:
                department = department[0].strip()
            else:
                department = ''
            birth = re.findall(r'，19(.*?)出生', text_data, re.S)
            if len(birth) != 0:
                birth = '19' + birth[0].strip()
            else:
                birth = ''
            content = "".join(tree.xpath('//div[@class="articel-detail-con mgtop20"]/p[1]//text()'))

            times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            con = 'detail_url:{}'.format(detail_url),'name:{}'.format(name),'company_name:{}'.format(company_name)
            logger.info(con)
            logger.info('爬取到第{}页！！！'.format(page))
            if detail_url not in bloom:
                zhilian = Medicine(title_url=detail_url, name=name, company_name=company_name, talent_type=talent_type,
                                   reason=reason,
                                   department=department, birth=birth, content=content, release_date=release_date,
                                   gmt_created=times, gmt_updated=times)
                session.add(zhilian)
                session.commit()
            else:
                logger.info('公司：{}，已经存在！！！'.format(company_name))

            time.sleep(2)
        time.sleep(5)


if __name__ == '__main__':
    main()
