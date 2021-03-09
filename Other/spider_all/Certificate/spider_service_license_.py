import re
import time
import requests
import pymysql
from getCompanyId.get_company_id import get_company_id
from sqlalchemy import Column, String, create_engine,Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# 创建对象的基类:
Base = declarative_base()
# 定义User对象:

class Medicine(Base):
    # 表的名字:
    __tablename__ = 'spider_service_license'

    # 表的结构:
    id = Column(Integer(), primary_key=True,autoincrement=True)
    company_name = Column(String(256))
    register_position = Column(String(256))
    connect_people = Column(String(256))
    connect_tel = Column(String(256))
    business_license_number = Column(String(256))
    license_authority = Column(String(256))
    valid_date = Column(String(256))
    year_business_report = Column(String(256))

    gmt_created = Column(String(256))
    gmt_updated = Column(String(256))
    company_id = Column(String(256))

# 初始化数据库连接:
engine = create_engine('mysql+mysqlconnector://root:BOOT-xwork1024@192.168.2.99:3306/spider')
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
    print(proxys[-1])
dl()
def main():
    bloom = get_updated()
    sum = []
    data = {
        '_currpage': 1,
        '_pagelines': 20,
        '_rowcount': 56,
        '_selectpage': 1
    }
    url = "http://rsz.zjhz.hrss.gov.cn/jyhptweb/cycx/queryLwpqxkdw.action;jsessionid=5pN8HiGEIhh85GYcbqG_ldLunPVxbSP_viiSnSz35dxeS8LGMRY5!1300760266"
    response_web = ""
    for IP in range(10):
        try:
            response_web = requests.request(method='post', url=url, headers=headers, data=data, proxies=proxys[-1],
                                            timeout=15)
            # print(response)
            if response_web.status_code == 200:
                response_web = response_web.content.decode('utf8')
                break
            time.sleep(2)
        except Exception:
            dl()
            time.sleep(1.5)
    results = int(re.findall(r"<font color='red'>(.*?)</font>页", response_web, re.S)[-1])
    for page in range(1,results+1):
        data = {
            '_currpage': page,
            '_pagelines': 20,
            '_rowcount': 56,
            '_selectpage': page
        }
        url = "http://rsz.zjhz.hrss.gov.cn/jyhptweb/cycx/queryLwpqxkdw.action;jsessionid=5pN8HiGEIhh85GYcbqG_ldLunPVxbSP_viiSnSz35dxeS8LGMRY5!1300760266"
        response_web = ""
        for IP in range(10):
            try:
                response_web = requests.request(method='post', url=url, headers=headers, data=data, proxies=proxys[-1],
                                                timeout=15)
                # print(response)
                if response_web.status_code == 200:
                    response_web = response_web.content.decode('utf8')
                    break
                time.sleep(2)
            except Exception:
                dl()
                time.sleep(1.5)

        results = re.findall(r'javascript:toGetInfo(.*?);',response_web,re.S)
        print(results)
        for j in results:
            keyword = j.split('(')[-1].split(')')[0]
            url = 'http://rsz.zjhz.hrss.gov.cn/jyhptweb/cycx/checkLwpqxkdw.action?dwid={}'.format(keyword)
            response = ""
            for IP in range(10):
                try:
                    response = requests.request(method='post', url=url, headers=headers, data=data,
                                                    proxies=proxys[-1],
                                                    timeout=15)
                    # print(response)
                    if response.status_code == 200:
                        response = response.content.decode('utf8')
                        break
                    time.sleep(2)
                except Exception:
                    dl()
                    time.sleep(1.5)
            company_name = re.findall(r'<h4>(.*?)</h4>',response,re.S)[0]
            register_position = re.findall(r'注册地址：.*?<td>(.*?)&nbsp;</td>',response,re.S)[0]
            connect_people = re.findall(r'联系人：.*?<td >(.*?)&nbsp;</td>',response,re.S)[0]
            connect_tel = re.findall(r'联系电话：.*?<td>(.*?)&nbsp;</td>',response,re.S)[0]
            business_license_number = re.findall(r'劳务派遣经营许可证号码：.*?<td >(.*?)&nbsp;</td>',response,re.S)[0]
            license_authority = re.findall(r'许可机关.*?<td >(.*?)&nbsp;</td>',response,re.S)[0]
            valid_date = re.findall(r'有效期：.*?<td >(.*?)&nbsp;</td>',response,re.S)[0]
            year_business_report = re.findall(r'提交年度经营报告情况.*?<td >(.*?)&nbsp;</td>',response,re.S)[0]

            times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            if business_license_number not in bloom:

                company_id = get_company_id(company_name)
                if company_id:
                    print((company_name, register_position, connect_people, connect_tel, business_license_number, license_authority
                           , valid_date,year_business_report, company_id))
                    zhilian = Medicine(company_name=company_name, register_position=register_position, connect_people=connect_people,
                                       connect_tel=connect_tel, business_license_number=business_license_number,
                                       license_authority=license_authority, valid_date=valid_date,
                                       year_business_report=year_business_report,
                                       gmt_created=times, gmt_updated=times, company_id=company_id)

                    sum.append(zhilian)
                else:
                    print((company_name, register_position, connect_people, connect_tel, business_license_number,
                           license_authority
                           , valid_date, year_business_report))
                    zhilian = Medicine(company_name=company_name, register_position=register_position,
                                       connect_people=connect_people,
                                       connect_tel=connect_tel, business_license_number=business_license_number,
                                       license_authority=license_authority, valid_date=valid_date,
                                       year_business_report=year_business_report,
                                       gmt_created=times, gmt_updated=times)
                    sum.append(zhilian)

            time.sleep(0.5)

    if len(sum) == 0:
        print('此次没有数据更新！！！')
    else:
        print('此次更新数据有{}条！！！'.format(len(sum)))
        write_db(sum)

def get_updated():
    db = pymysql.connect(host="192.168.2.99", user="root", password='BOOT-xwork1024', database="spider", port=3306)
    cursor = db.cursor()
    sql = "select business_license_number from spider_service_license"
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
