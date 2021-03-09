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
    __tablename__ = 'spider_zj_company_medical_equipment'

    # 表的结构:
    id = Column(Integer(), primary_key=True,autoincrement=True)
    record_id = Column(String(256))
    detail_url = Column(String(256))
    company_name = Column(String(256))
    type = Column(String(256))
    content = Column(String(256))

    gmt_created = Column(String(256))
    gmt_updated = Column(String(256))
# 初始化数据库连接:
engine = create_engine('mysql+mysqlconnector://root:BOOT-xwork1024@192.168.2.99:3306/spider')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
# 创建session对象:
session = DBSession()

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Length': '120',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': 'JSESSIONID=4666C867AF24208B318E1CD46F5E6E06',
    'Host': 'mpa.zjfda.gov.cn',
    'Origin': 'http://mpa.zjfda.gov.cn',
    'Referer': 'http://mpa.zjfda.gov.cn/xzsp!listOfInfoMore.do?search[%27sKey%27]=&search[%27category%27]=yp&search[%27type%27]=CORP',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
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
def get_updated():
    db = pymysql.connect(host="192.168.2.99", user="root", password='BOOT-xwork1024', database="spider", port=3306)
    cursor = db.cursor()
    sql = "select record_id from spider_zj_company_medical_equipment"
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

def main():
    bloom = get_updated()
    sum = []

    for page in range(100,108): # 60 - 80
        # if page ==90:
        #     break
        data = {
            "search['sKey']": '',
             "search['category']": "qx",
            "search['type']": "CORP",
            "pAttr2['pageCur']": page,
            "pAttr2['infoSize']": 1000
        }
        url = "http://mpa.zjfda.gov.cn/xzspajax!listOfInfo.do"
        response_web = ""
        for IP in range(20):
            try:
                response_web = requests.request(method='post', url=url, data = data,headers=headers,proxies=proxys[-1],
                                                timeout=10)
                if response_web.status_code == 200:
                    response_web = response_web.content.decode('utf8')
                    break
            except Exception:
                time.sleep(2)
                dl()
        response = json.loads(response_web)
        results = response.get('list')

        for i in results:
            company_name = i.get('NAME')
            type = i.get('CHNTABLE')

            id = i.get('ID')
            t_name = i.get('TNAME')
            url = "http://mpa.zjfda.gov.cn/xzsp!infoDetail.do?id={}&tableNo={}".format(id,t_name)
            print(url)

            head = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
            }
            response_web = ""
            for IP in range(10):
                try:
                    response_web = requests.request(method='get', url=url, headers=head,
                                                    proxies=proxys[-1],
                                                    timeout=10)
                    # print(response)
                    if response_web.status_code == 200:
                        response_web = response_web.content.decode('utf8')
                        print('break！！！')
                        break
                except Exception:
                    time.sleep(2)
                    dl()

            if type == "器械经营企业":
                register_addr = re.findall(r'注册地址:</td>.*?<td>(.*?)</td>', response_web, re.S)[0].strip()
                license = re.findall(r'药品经营（批发）许可证:</td>.*?<td>(.*?)</td>', response_web, re.S)[0].strip()
                business_addr = re.findall(r'经营地址:</td>.*?<td>(.*?)</td>', response_web, re.S)[0].strip()
                license_mechanism = re.findall(r'证书发放部门:</td>.*?<td>(.*?)</td>', response_web, re.S)[0].strip()
                business_range = re.findall(r'经营范围:</td>.*?<td>(.*?)</td>', response_web, re.S)[0].strip()
                legal_people = re.findall(r'法定代表人:</td>.*?<td>(.*?)</td>', response_web, re.S)[0].strip()
                company_principal = re.findall(r'企业负责人:</td>.*?<td>(.*?)</td>', response_web, re.S)[0].strip()
                quality_principal = re.findall(r'质量负责人:</td>.*?<td>(.*?)</td>', response_web, re.S)[0].strip()
                license_valid_date = re.findall(r'经营许可证发放日期:</td>.*?<td>(.*?)</td>', response_web, re.S)[0].strip()
                license_invalid_date = re.findall(r'经营许可证有效期:</td>.*?<td>(.*?)</td>', response_web, re.S)[0].replace(
                    '\t', '').replace('\r', '').replace('\n', '')
                status = re.findall(r'状态:</td>.*?<td>(.*?)</td>', response_web, re.S)[0].replace('\t', '').replace('\r',
                                                                                                                 '').replace(
                    '\n', '').strip()
                gsp_license_num = re.findall(r'GSP证号:</td>.*?<td>(.*?)</td>', response_web, re.S)[0].strip()
                gsp_approve_valid_date = re.findall(r'GSP证书发放日期:</td>.*?<td>(.*?)</td>', response_web, re.S)[0].strip()
                gsp_approve_invalid_date = re.findall(r'GSP证书有效期:</td>.*?<td>(.*?)</td>', response_web, re.S)[
                    0].replace('\t', '').replace('\r', '').replace('\n', '')
                single = {}
                single['register_addr']=register_addr
                single['license']=license
                single['business_addr']=business_addr
                single['license_mechanism']=license_mechanism
                single['legal_people']=legal_people
                single['company_principal']=company_principal
                single['quality_principal']=quality_principal
                single['license_valid_date']=license_valid_date
                single['license_invalid_date']=license_invalid_date
                single['status']=status
                single['gsp_license_num']=gsp_license_num
                single['gsp_approve_valid_date']=gsp_approve_valid_date
                single['gsp_approve_invalid_date']=gsp_approve_invalid_date
                single['business_range']=business_range
                times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                content = json.dumps(single,ensure_ascii=False)
                print((id, url, company_name,type,content))
                if id not in bloom:
                    zhilian = Medicine(record_id=id, company_name=company_name,detail_url=url,
                                       type=type,content=content,
                                       gmt_created=times, gmt_updated=times)
                    sum.append(zhilian)
                time.sleep(1.5)

            elif type == "器械广告备案":
                medical_equipment_name = re.findall(r'医疗器械名称:</td>.*?<td>(.*?)</td>', response_web, re.S)[0].strip()
                medical_equipment_approval_num = re.findall(r'医疗器械批准文号:</td>.*?<td>(.*?)</td>', response_web, re.S)[0].strip()
                advertise_approval_num = re.findall(r'原广告批准文号:</td>.*?<td>(.*?)</td>', response_web, re.S)[0].strip()
                advertise_time = re.findall(r'广告时长:</td>.*?<td>(.*?)</td>', response_web, re.S)[0].strip()
                advertise_type = re.findall(r'广告类型:</td>.*?<td>(.*?)</td>', response_web, re.S)[0].strip()
                advertise_approval_num_invalid = re.findall(r'原广告批准文号有效期至:</td>.*?<td>(.*?)</td>', response_web, re.S)[0].strip()
                record_date = re.findall(r'备案日期:</td>.*?<td>(.*?)</td>', response_web, re.S)[0].strip()
                times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

                single = {}
                single['medical_equipment_name'] = medical_equipment_name
                single['medical_equipment_approval_num'] = medical_equipment_approval_num
                single['advertise_approval_num'] = advertise_approval_num
                single['advertise_time'] = advertise_time
                single['advertise_type'] = advertise_type
                single['advertise_approval_num_invalid'] = advertise_approval_num_invalid
                single['record_date'] = record_date
                content = json.dumps(single, ensure_ascii=False)

                print((id, company_name, type, url, content))
                if id not in bloom:
                    zhilian = Medicine(record_id=id, company_name=company_name,
                                       type=type, content=content, detail_url=url,
                                       gmt_created=times, gmt_updated=times)
                    sum.append(zhilian)
                time.sleep(1.5)

            elif type == "二类备案信息":
                home_addr = re.findall(r'住         所:</td>.*?<td>(.*?)</td>', response_web, re.S)[0].strip()
                business_type = re.findall(r'经营方式:</td>.*?<td>(.*?)</td>', response_web, re.S)[0].strip()
                business_addr = re.findall(r'经营场所:</td>.*?<td>(.*?)</td>', response_web, re.S)[0].strip()
                cangku_addr = re.findall(r'库房地址:</td>.*?<td>(.*?)</td>', response_web, re.S)[0].strip()
                business_range = re.findall(r'经营范围:</td>.*?<td>(.*?)</td>', response_web, re.S)[0].strip()
                legal_people = re.findall(r'法定代表人:</td>.*?<td>(.*?)</td>', response_web, re.S)[0].strip()
                charge_person = re.findall(r'企业负责人:</td>.*?<td>(.*?)</td>', response_web, re.S)[0].strip()
                record_num = re.findall(r'备案号:</td>.*?<td>(.*?)</td>', response_web, re.S)[0].strip()
                record_addr = re.findall(r'备案地点:</td>.*?<td>(.*?)</td>', response_web, re.S)[0].strip()
                record_time = re.findall(r'备案时间:</td>.*?<td>(.*?)</td>', response_web, re.S)[0].strip()

                times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                single = {}
                single['home_addr'] = home_addr
                single['business_type'] = business_type
                single['business_addr'] = business_addr
                single['cangku_addr'] = cangku_addr
                single['business_range'] = business_range
                single['legal_people'] = legal_people
                single['charge_person'] = charge_person
                single['record_num'] = record_num
                single['record_addr'] = record_addr
                single['record_time'] = record_time
                content = json.dumps(single, ensure_ascii=False)

                print((id, company_name, type, url, content))
                if id not in bloom:
                    zhilian = Medicine(record_id=id, company_name=company_name,
                                       type=type,content=content,detail_url=url,
                                       gmt_created=times, gmt_updated=times)
                    sum.append(zhilian)
                time.sleep(1.5)

            elif type == "医疗器械产品出口销售证明":

                license = re.findall(r'证书编号:</td>.*?<td>(.*?)</td>', response_web,re.S)[0].strip()
                produce_addr = re.findall(r'生产地址:</td>.*?<td>(.*?)</td>', response_web,re.S)[0].strip()
                license_mechanism = re.findall(r'发证机关:</td>.*?<td>(.*?)</td>', response_web,re.S)[0].strip()
                legal_people = re.findall(r'法定代表人:</td>.*?<td>(.*?)</td>', response_web, re.S)[0].strip()
                connect_person = re.findall(r'联系人:</td>.*?<td>(.*?)</td>', response_web, re.S)[0].strip()
                license_valid_date = re.findall(r'发证日期:</td>.*?<td>(.*?)</td>', response_web, re.S)[0].strip()
                license_invalid_date = re.findall(r'证书有效期:</td>.*?<td>(.*?)</td>', response_web, re.S)[0].strip()
                times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

                single = {}
                single['license'] = license
                single['produce_addr'] = produce_addr
                single['license_mechanism'] = license_mechanism
                single['legal_people'] = legal_people
                single['connect_person'] = connect_person
                single['license_valid_date'] = license_valid_date
                single['license_invalid_date'] = license_invalid_date
                content = json.dumps(single,ensure_ascii=False)

                print((id,company_name,type,url,content))
                if id not in bloom:
                    zhilian = Medicine(record_id=id,company_name=company_name,
                                       type=type,detail_url=url,content=content,
                                       gmt_created=times, gmt_updated=times)
                    sum.append(zhilian)
                time.sleep(1.5)

            elif type == "器械生产企业":

                register_addr = re.findall(r'注册地址:</td>.*?<td>(.*?)</td>', response_web,re.S)[0].strip()
                produce_license_num = re.findall(r'生产许可证:</td>.*?<td>(.*?)</td>', response_web,re.S)[0].strip()
                produce_addr = re.findall(r'生产地址:</td>.*?<td>(.*?)</td>', response_web,re.S)[0].strip()
                produce_range = re.findall(r'生产范围:</td>.*?<td>(.*?)</td>', response_web,re.S)[0].strip()

                legal_people = re.findall(r'法定代表人:</td>.*?<td>(.*?)</td>', response_web, re.S)[0].strip()
                charge_person = re.findall(r'企业负责人:</td>.*?<td>(.*?)</td>', response_web, re.S)[0].strip()
                quality_principal = re.findall(r'质量负责人:</td>.*?<td>(.*?)</td>', response_web, re.S)[0].strip()
                license_mechanism = re.findall(r'证书发放部门:</td>.*?<td>(.*?)</td>', response_web,re.S)[0].strip()
                license_valid_date = re.findall(r'证书发放日期:</td>.*?<td>(.*?)</td>', response_web, re.S)[0].replace('\t', '').replace('\r', '').replace('\n', '')
                license_invalid_date = re.findall(r'证书有效期:</td>.*?<td>(.*?)</td>', response_web, re.S)[0].replace('\t', '').replace('\r', '').replace('\n', '')
                times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

                single = {}
                single['register_addr'] = register_addr
                single['produce_license_num'] = produce_license_num
                single['produce_addr'] = produce_addr
                single['produce_range'] = produce_range
                single['legal_people'] = legal_people
                single['charge_person'] = charge_person
                single['quality_principal'] = quality_principal
                single['license_mechanism'] = license_mechanism
                single['license_valid_date'] = license_valid_date
                single['license_invalid_date'] = license_invalid_date
                content = json.dumps(single,ensure_ascii=False)

                print((id,company_name,type,url,content))
                if id not in bloom:
                    zhilian = Medicine(record_id=id,company_name=company_name,
                                       type=type,detail_url=url,content=content,
                                       gmt_created=times, gmt_updated=times)
                    sum.append(zhilian)
                time.sleep(1.5)

            else:
                time.sleep(1)
                continue
            # write_db(sum)
            # exit()
        time.sleep(2)


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
