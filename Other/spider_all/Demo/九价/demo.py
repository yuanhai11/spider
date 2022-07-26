#coding:utf-8
import re
import time,pymysql
import requests
from lxml import etree
from sqlalchemy import Column, String, create_engine,Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pybloom_live import ScalableBloomFilter
# 创建对象的基类:
Base = declarative_base()
# 定义User对象:
class Medicine(Base):
    # 表的名字:
    __tablename__ = 'spider_2_company_revoke'

    # 表的结构:
    id = Column(Integer(), primary_key=True,autoincrement=True)
    url = Column(String(256))
    company_name = Column(String(256))
    revoke_date = Column(String(256))
    revoke_reason = Column(String(256))
    gmt_created = Column(String(256))
    gmt_updated = Column(String(256))
# 初始化数据库连接:
engine = create_engine('mysql+pymysql://root:BOOT-xwork1024@192.168.2.97:3306/spider')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
# 创建session对象:
session = DBSession()

proxys = []
def dl():
    dlurl = 'http://api.goubanjia.com/dynamic/get/d490a5d4debefc8980ae6ee4c4148552.html?sep=3'
    resp = requests.get(dlurl).text
    time.sleep(6)
    resp = re.sub(r'\n', '', resp)
    proxy = {
        'https': resp
    }
    proxys.append(proxy)
    print(proxys[-1])


"""
1.请求不同城市的九价医院列表   
 "https://cloud.cn2030.com/sc/wx/HandlerSubscribe.ashx?act=CustomerList&city=%5B%22%E6%B2%B3%E5%8D%97%E7%9C%81%22%2C%22%E9%83%91%E5%B7%9E%E5%B8%82%22%2C%22%22%5D&lat=30.27415&lng=120.15515&id=0&cityCode=410100&product=25"
2.登录认证
POST /sc/wx/HandlerSubscribe.ashx?act=auth&code=003gkQml2CDWS84HIXml2dPQI21gkQmV HTTP/1.1
3.获取用户
GET /sc/wx/HandlerSubscribe.ashx?act=User HTTP/1.1
3.请求所在医院疫苗列表  
GET /sc/wx/HandlerSubscribe.ashx?act=CustomerProduct&id=1921&lat=30.27415&lng=120.15515 HTTP/1.1

4.请求九价接口  
GET /sc/wx/HandlerSubscribe.ashx?act=GetCustSubscribeDateAll&pid=1&id=1921&month=202203 HTTP/1.1
"""

def main():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
        'Referer': 'https://servicewechat.com/wx2c7f0f3c30d99445/92/page-frame.html',
        # 'zftsl':'2a0aebcff233b9fc93e52b5323a92db2'
    }
    url = "https://cloud.cn2030.com/sc/wx/HandlerSubscribe.ashx?"
    url="https://cloud.cn2030.com/sc/wx/HandlerSubscribe.ashx?act=CustomerList&city=%5B%22%E6%B2%B3%E5%8D%97%E7%9C%81%22%2C%22%E9%83%91%E5%B7%9E%E5%B8%82%22%2C%22%22%5D&lat=30.27415&lng=120.15515&id=0&cityCode=410100&product=25"
    data = {
        "act",	"CustomerList",
        "city",	'["河南省","郑州市",""]',
        "lat",	30.27415,
        "lng",	120.15515,
        "id",	0,
        "cityCode",	410100,
        "product",	25
    }
    # response = requests.request(method='get', url=url, data=data, headers=headers, timeout=10,verify=False)
    response = requests.request(method='get', url=url, headers=headers, timeout=10,verify=False)
    print(response.text)


if __name__ == '__main__':
    main()


