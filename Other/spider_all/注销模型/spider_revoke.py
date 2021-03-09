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

def get_company_id(keyword):
    time.sleep(0.5)
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
    }
    data = {
        'keyword': keyword,
        "page": 1,
        "pageSize": 20,
        "searchList": ["companyName.keyword"],
    }
    dd = requests.post(url='http://192.168.2.95:18018/api/compass/data/search', headers=headers, json=data).json()
    print(dd)

    list = dd.get('data').get('records')
    if len(list) != 0:
        return list[0]
    else:
        return None


def main():
    '''
    :desc
        1，行政处罚的结果，
    :return:
    '''
    bloom = updated()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
    }
    response = ""
    sum = []
    company_name_lists = []
    # 数据进行了加密，之前的方式只能爬取第一页数据。 加了ids和realid参数，数据筛选前，需要先获取一下新增数据。
    for page in range(2,3):
        try:
            url = "http://www.zjzwfw.gov.cn/zjzw/punish/frontpunish/search_list.do"
            data = {
                'type':1,
                'ids':'330402182020070016_330402182020070016',
                'xzcfws_name': '停业',
                'pageNo': page,
                'webid': 2,
                'bxzcf_type': 0,
                'realid':'0.8407864790200612'
            }
            for IP in range(20):
                try:
                    response = requests.request(method='post', url=url,data=data,headers=headers,timeout=10)
                    if response.status_code == 200:
                        response = response.content.decode('utf-8')
                        break
                except Exception:
                    dl()

            tree = etree.HTML(response)
            detail_url = tree.xpath('//div[@id="xzcf_3"]//tr//a/@href')
            response1 = ''
            for url in detail_url:
                url = 'http://www.zjzwfw.gov.cn' + url
                print(url)
                if url not in bloom and url not in sum:
                    for IP in range(20):
                        try:
                            response1 = requests.request(method='get', url=url, proxies=proxys[-1], headers=headers, timeout=10)
                            if response1.status_code == 200:
                                response1 = response1.content.decode('utf-8')
                                break
                        except Exception:
                            dl()

                    tree1 = etree.HTML(response1)
                    params = ''.join(tree1.xpath('//td[@class="xzcf_jds"]/p//text()'))
                    flag = params.split('行政处罚内容：')[-1].split('\xa0')[0].strip()
                    if '吊销' in flag and '营业执照' in flag:

                        name = re.findall(r'被处罚单位（被处罚人）：</td>.*?<td class="xzcf_xx">(.*?)&nbsp;&nbsp;&nbsp;&nbsp;<span class="xzcf_mc">法定代表人（或单位负责人）',response1,re.S)
                        name1 = re.findall(r'被处罚单位（被处罚人）：</td>.*?<td class="xzcf_xx">(.*?)</td>',response1,re.S)

                        if len(name) !=0:
                            name = name[0]
                        else:
                            name = name1[0]

                        date = re.findall(r'作出行政处罚的日期：</td>.*?<td class="xzcf_xx">(.*?)</td>',response1,re.S)[0]
                        reason = re.findall('行政处罚.*?、依据：(.*?)<br/>',response1,re.S)[0].strip()

                        print('吊销营业执照公司：',name,'时间：',date,'吊销原因：',reason,'page:',page)
                        times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                        if name not in company_name_lists:
                            medicine = Medicine(company_name=name,revoke_date=date,revoke_reason=reason,url=url,gmt_created=times,gmt_updated=times)
                            session.add(medicine)
                            company_name_lists.append(name)
                    else:
                        print('其他处罚内容：',flag)
                else:
                    print('重复数据！')
                    continue
                sum.append(url)
                time.sleep(1)
            session.commit()
        except Exception as e:
            time.sleep(1)
            continue
def updated():
    db = pymysql.connect(host="192.168.2.97", user="root", password='BOOT-xwork1024', database="spider", port=3306)
    cursor = db.cursor()
    sql = "select url from spider_2_company_revoke"
    cursor.execute(sql)
    db_data = cursor.fetchall()
    data = [i[0].strip() for i in db_data]
    bloom = ScalableBloomFilter(initial_capacity=100000, error_rate=0.001)
    for i in data:
        bloom.add(i)
    return bloom

if __name__ == '__main__':
    main()


