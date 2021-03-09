'''
食品许可证：上海
'''
import re
import time
import requests,pymysql
import base64
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pksc1_v1_5
from Crypto.PublicKey import RSA
from sqlalchemy import Column, String, create_engine,Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# 创建对象的基类:
Base = declarative_base()
# 定义User对象:

class Medicine(Base):
    # 表的名字:
    __tablename__ = 'spider_qualification'
    id = Column(Integer(), primary_key=True,autoincrement=True)
    license_num = Column(String(256))
    company_name = Column(String(256))
    valid_date = Column(String(256))
    invalid_date = Column(String(256))
    area = Column(Integer())
    license_current_status = Column(String(256))

    gmt_created = Column(String(256))
    gmt_updated = Column(String(256))
    company_id = Column(String(256))
    license_name = Column(String(256))

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
            break
        except Exception:
            pass
    time.sleep(3)
    resp = re.sub(r'\n', '', resp)
    proxy = {
        'https': resp
    }
    proxys.append(proxy)
    print(proxys[-1])
dl()

def get_updated():
    db = pymysql.connect(host="192.168.2.97", user="root", password='BOOT-xwork1024', database="spider", port=3306)
    cursor = db.cursor()
    sql = "select license_num from spider_qualification"
    cursor.execute(sql)
    db_data = cursor.fetchall()
    data = [i[0] for i in db_data]
    from pybloom_live import ScalableBloomFilter
    bloom = ScalableBloomFilter(initial_capacity=1000000, error_rate=0.001)
    for bl in data:
        bloom.add(bl)
    return bloom

def main():
    # bloom = get_updated()
    # url = 'http://mpa.zjfda.gov.cn/xzsp!ylqxjyxkz.do'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
    }
    # data = {
    #     'pAttr3.infoSize': 20000,
    #     'pAttr3.pageCur': 1,
    # }
    # response = requests.request(method='post', url=url, headers=headers,data=data,timeout=30).text
    # codes = re.findall(r'<input type="button" value="详情" .*?onclick="spGotourl(.*?)" />.*?</td>',response,re.S)
    import json
    with open('mechine_codes.json','r',encoding='utf-8')as fp:
        # fp.write(json.dumps(codes,ensure_ascii=False))
        codes = json.loads(fp.read())
        # exit()
    for index,code in enumerate(codes):
        code = code.split(',')[-1].replace(')"','')[:-1][1:-1]
        # if code == 'E4D3AF82539148B49B6BD9E246F69160':
        #     print(index)
        #     exit()
        # continue
        url = "http://mpa.zjfda.gov.cn/xzsp!ylqxjyxkzDetail.do?id={}".format(code)
        print(url,'索引：',index)
        if index < 17191+1:
            continue
        response_web = ""
        while 1:
            try:
                time.sleep(4)
                response_web = requests.request(method='get', url=url, headers=headers,proxies=proxys[-1],timeout=10)
                if response_web.status_code == 200:
                    response_web = response_web.content.decode('utf-8')
                    break
            except Exception:
                dl()
        if response_web == "":
            continue
        from lxml import etree
        tree = etree.HTML(response_web)
        company_name = ''.join(tree.xpath('//div[@class="xinxiLeft"]//tr[1]/td[2]/text()')).strip().replace(' ','')
        if company_name==None:
            continue
        license_num = ''.join(tree.xpath('//div[@class="xinxiRight"]//tr[2]/td[2]/text()')).strip().replace(' ','')
        invalid_date = ''.join(tree.xpath('//div[@class="xinxiRight"]//tr[5]/td[2]/text()')).strip().replace(' ','')
        valid_date = ''.join(tree.xpath('//div[@class="xinxiRight"]//tr[4]/td[2]/text()')).strip().replace(' ','')
        license_current_status = ''.join(tree.xpath('//div[@class="xinxiLeft"]//tr[6]/td[2]/text()')).strip().replace(' ','')
        area = 9
        license_name = '医疗器械经营许可证'
        times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        print(company_name,license_num,license_current_status,valid_date,invalid_date,license_name,area)
        medicine = Medicine(license_num=license_num,company_name=company_name,license_name=license_name,valid_date=valid_date,invalid_date=invalid_date,area=area,
                 license_current_status=license_current_status,
                 gmt_created=times,gmt_updated=times)

        session.add(medicine)
        session.commit()

if __name__ == '__main__':
    main()
