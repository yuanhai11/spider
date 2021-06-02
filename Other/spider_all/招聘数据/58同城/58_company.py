# coding:utf-8
import time
import re,os
import json
import logging
import requests, pymysql
from lxml import etree
from sqlalchemy import Column, String, create_engine, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from requests.auth import HTTPProxyAuth
# 创建对象的基类:
Base = declarative_base()


# 定义User对象:

class Medicine(Base):
    # 表的名字:
    __tablename__ = 'spider_58_company'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    company = Column(String(256))
    city = Column(String(256))
    business = Column(String(256))
    tags = Column(String(256))


# 初始化数据库连接:
engine = create_engine('mysql+pymysql://root:BOOT-xwork1024@192.168.2.97:3306/spider')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
# 创建session对象:
session = DBSession()

proxys = []

def dl():
    while 1:
        try:
            dlurl = 'http://api.goubanjia.com/dynamic/get/d490a5d4debefc8980ae6ee4c4148552.html?sep=3'
            resp = requests.get(dlurl).text
            time.sleep(3.6)
            resp = re.sub(r'\n', '', resp)
            proxy = {
                'https': resp
            }
            proxys.append(proxy)
            print(proxys[-1])
            break
        except:
            time.sleep(2)
            continue

dl()


def get_logger():
    logging.basicConfig(level = logging.INFO,format='%(asctime)s|%(name)-s: %(levelname)-s %(message)s')
    logger = logging.getLogger("spider")
    logger.setLevel(logging.INFO)

    log_file_path = os.path.join(os.path.abspath('.'),'log')
    if not os.path.exists(log_file_path):
        os.mkdir(log_file_path)

    #创建handler
    handler1=logging.FileHandler("{}/58_spider.log".format(log_file_path),encoding='utf-8')
    handler1.setLevel(logging.INFO)
    formatter=logging.Formatter('%(asctime)s|%(name)-s+ %(levelname)-s++%(message)s')
    handler1.setFormatter(formatter)
    handler2=logging.StreamHandler()
    handler2.setLevel(logging.ERROR)
    logger.addHandler(handler1)
    logger.addHandler(handler2)
    return logger

def get_url():
    import requests
    from requests.auth import HTTPProxyAuth

    s = requests.Session()
    s.auth = HTTPProxyAuth('msha0723@163.com', 'msha0723')
    url = 'https://bj.58.com/job/?PGTID=0d302408-016b-f183-b8e6-ac34b3d6824f&ClickID=1'
    time.sleep(1.3)
    response = s.get(url, headers=headers, timeout=15).text
    from lxml import etree
    tree = etree.HTML(response)
    url_lists = tree.xpath('//div[@class="sub_area clearfix"]/a/@href')
    print(url_lists)


# def get_response():
'''
    urls = ['https://hz.58.com/zhuce/','https://bj.58.com/zhuce/','https://sh.58.com/zhuce/','https://gz.58.com/zhuce/','https://sz.58.com/zhuce/','https://cd.58.com/zhuce/',
    'https://nj.58.com/zhuce/','https://tj.58.com/zhuce/','https://wh.58.com/zhuce/','https://cq.58.com/zhuce/']
    citys = ['杭州','北京','上海','广州','深圳','成都','南京','天津','武汉','重庆']
    
    urls = ['https://zs.58.com/zhuce/','https://zh.58.com/zhuce/','https://sjz.58.com/zhuce/','https://yt.58.com/zhuce/',
    'https://qd.58.com/zhuce/','https://jn.58.com/zhuce/','https://xm.58.com/zhuce/']
    citys = ['中山','珠海','石家庄','烟台','青岛','济南','厦门']
    
'''

def get_sum():
    data = session.query(Medicine).all()
    return list(set([d.company for d in data]))

def main():
    sum = get_sum()
    logger = get_logger()
    s = requests.Session()
    # s.proxies = {"http": proxys[-1], "https": proxys[-1]}
    s.auth = HTTPProxyAuth('msha0723@163.com', 'msha0723')

    urls = ['https://yt.58.com/zhuce/',
    'https://qd.58.com/zhuce/','https://jn.58.com/zhuce/','https://xm.58.com/zhuce/']
    citys = ['烟台','青岛','济南','厦门']

    gaga = False
    for city,url in zip(citys,urls):
        url = url + '?PGTID=0d30007d-0047-8f45-156c-5485d5dfbd91&ClickID=1'
        while 1:
            try:
                time.sleep(1.3)
                response = s.get(url, headers=headers, proxies=proxys[-1], timeout=15).text
                tree = etree.HTML(response)
                areas = tree.xpath('//dd[@id="local"]/a/@href')[1:-1]
                areas1 = tree.xpath('//dd[@id="local"]/a/@href')[0]
                logger.info('{}下 >> {}个区'.format(city,len(areas)))
                break
            except Exception as e:
                print(e)
                dl()
        for index,a in enumerate(areas):
            # if city=='烟台':
            #     if index<9:
            #         continue
            u = url.replace('/zhuce/',a).replace('?PGTID=0d30007d-0047-8f45-156c-5485d5dfbd91&ClickID=1','pn{}/?PGTID=0d30007d-0047-8f45-156c-5485d5dfbd91&ClickID=1')
            for page in range(1,71):
                if gaga:
                    break
                ur = u.format(page)
                logger.info(ur)
                # continue
                while 1:
                    try:
                        time.sleep(1.3)
                        response = s.get(ur, headers=headers, proxies=proxys[-1],timeout=15).text
                        tree = etree.HTML(response)
                        flag = tree.xpath('//section[@id="selection"]')[0]
                        data_eles = tree.xpath('//div[@id="infolist"]//td[@class="t"]')

                        if len(data_eles) == 0:
                            gaga = True
                        break
                    except Exception as e:
                        print(e)
                        dl()
                for data in data_eles:
                    try:
                        company = ''.join(data.xpath('.//p[@class="seller"]/text()')).strip().replace(r'\r','').replace(r'\t','')
                        business = ''.join(data.xpath('.//a/div//text()')).strip().replace(r'\r','').replace(r'\t','')
                        tag = ','.join(data.xpath('.//p[@class="item-tags"]/span/text()')).strip().replace(r'\r','').replace(r'\t','')
                        logger.info('公司：{}++   '.format(company)+'经营范围：{}++  '.format(business)+'标签：{}++  '.format(tag))
                        if company not in sum:
                            me = Medicine(company=company,city=city,business=business,tags=tag)
                            session.add(me)
                            sum.append(company)
                    except Exception:
                        continue
            session.commit()
            gaga = False


if __name__ == '__main__':
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
    }
    main()
