import re
import time
import requests
import pymysql
import json
from getCompanyId.get_company_id import get_company_id
from decouple import config
from sqlalchemy import Column, String, create_engine,Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# 创建对象的基类:
Base = declarative_base()
# 定义User对象:
class Medicine(Base):
    '''
    1、数据量小
    2、没有数据更新，更新频率待定
    '''
    # 表的名字:
    __tablename__ = 'spider_sh_company_medical_equipment_network_third_party_platform'

    # 表的结构:
    id = Column(Integer(), primary_key=True,autoincrement=True)
    record_id = Column(String(256))
    record_num = Column(String(256))
    company_name = Column(String(256))
    addr = Column(String(256))
    business_addr = Column(String(256))
    legal_people = Column(String(256))
    company_principal = Column(String(256))
    quality_principal = Column(String(256))
    web_name = Column(String(256))
    web_program_name = Column(String(256))
    domain_name = Column(String(256))
    ip = Column(String(256))
    service_machine_addr = Column(String(256))
    non_profit_internet_service_record_num = Column(String(256))
    record_mechanism = Column(String(256))
    record_date = Column(String(256))
    gmt_created = Column(String(256))
    gmt_updated = Column(String(256))
    company_id = Column(String(256))
# 初始化数据库连接:
engine = create_engine('mysql+pymysql://root:BOOT-xwork1024@192.168.2.99:3306/spider')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
# 创建session对象:
session = DBSession()

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
}
proxys = []
def dl():
    dlurl = config('dlurl')
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
    sql = "select record_num from spider_sh_company_medical_equipment_network_third_party_platform"
    cursor.execute(sql)
    db_data = cursor.fetchall()
    data = [i[0] for i in db_data]
    from pybloom_live import ScalableBloomFilter
    bloom = ScalableBloomFilter(initial_capacity=10000,error_rate=0.001)
    for bl in data:
        bloom.add(bl)
    return bloom
def reload(page):
    time.sleep(10)
    data = {
        'currentPage': page,
        'pageSize': '10',
        'groupSize': '8',
        'pageName': 'ylqxwljyList',
    }
    url = "http://xuke.yjj.sh.gov.cn/AppRoveManage/selectLicense/selectData"
    response_web = ""
    for IP in range(10):
        try:
            response_web = requests.request(method='post', url=url, data=data, headers=headers, proxies=proxys[-1],
                                            timeout=10)
            # print(response)
            if response_web.status_code == 200:
                response_web = response_web.content.decode('utf8')
                break
        except Exception:
            dl()
    response = json.loads(response_web)
    results = response.get('rowData')
    return results

def main():
    bloom = get_updated()
    sum = []
    old_data = []
    for page in range(1,3):
        data = {
            'currentPage': page,
            'pageSize': '10',
            'groupSize': '8',
            'pageName': 'ylqxwljyList',
        }
        url = "http://xuke.yjj.sh.gov.cn/AppRoveManage/selectLicense/selectData"
        response_web = ""
        for IP in range(10):
            try:
                response_web = requests.request(method='post', url=url, data=data, headers=headers, proxies=proxys[-1],
                                                timeout=10)
                # print(response)
                if response_web.status_code == 200:
                    response_web = response_web.content.decode('utf8')
                    break
            except Exception:
                dl()
        response = json.loads(response_web)
        results = response.get('rowData')
        # print(results)
        if len(results) == 1:
            results = reload(page)
            print('跳出reload函数！！！')
        for i in results:
            id = i.get('ZSID')

            record_num = i.get('ZSBH')
            company_name = i.get('QYMC_ZW')
            addr = i.get('ZCDZ_ZW')
            business_addr = i.get('SCDZ_ZW')
            legal_people = i.get('FRMC_ZW')
            company_principal = i.get('QYFZR_ZW')
            quality_principal = i.get('ZLAQGLR')
            web_name = i.get('WZMC')
            web_program_name = i.get('WLKHD')
            domain_name = i.get('WZYM')
            ip = i.get('WZIPDZ')
            service_machine_addr = i.get('FWQCFDZ')
            non_profit_internet_service_record_num = i.get('FJYXHLWXXBABH')
            record_mechanism = i.get('FZJG')
            record_date = i.get('QFRQ')
            if record_date:
                record_date = get_time(record_date)

            times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            company_id = get_company_id(company_name)
            if company_id:
                print((id, record_num, company_name, addr, business_addr, legal_people, company_principal,
                       quality_principal, web_name, web_program_name,
                       domain_name, ip, service_machine_addr, non_profit_internet_service_record_num, record_mechanism,
                       record_date,company_id
                       ))
                if record_num not in bloom:
                    zhilian = Medicine(record_id=id, record_num=record_num, company_name=company_name, addr=addr,
                                       business_addr=business_addr, legal_people=legal_people,
                                       company_principal=company_principal,
                                       quality_principal=quality_principal, web_name=web_name,
                                       web_program_name=web_program_name, domain_name=domain_name, ip=ip,
                                       service_machine_addr=service_machine_addr,
                                       non_profit_internet_service_record_num=non_profit_internet_service_record_num,
                                       record_mechanism=record_mechanism, record_date=record_date, gmt_created=times,company_id=company_id,
                                       gmt_updated=times)
                    sum.append(zhilian)
                else:
                    obj_delete = session.query(Medicine).filter(Medicine.record_num == record_num).all()
                    for i in obj_delete:
                        session.delete(i)
                    zhilian = Medicine(record_id=id, record_num=record_num, company_name=company_name, addr=addr,
                                       business_addr=business_addr, legal_people=legal_people,
                                       company_principal=company_principal,
                                       quality_principal=quality_principal, web_name=web_name,
                                       web_program_name=web_program_name, domain_name=domain_name, ip=ip,
                                       service_machine_addr=service_machine_addr,
                                       non_profit_internet_service_record_num=non_profit_internet_service_record_num,
                                       record_mechanism=record_mechanism, record_date=record_date, gmt_created=times,
                                       company_id=company_id,
                                       gmt_updated=times)
                    sum.append(zhilian)
                    old_data.append(zhilian)
            else:
                print((id, record_num, company_name, addr, business_addr, legal_people, company_principal,
                       quality_principal, web_name, web_program_name,
                       domain_name, ip, service_machine_addr, non_profit_internet_service_record_num, record_mechanism,
                       record_date,
                       ))
                if record_num not in bloom:
                    zhilian = Medicine(record_id=id, record_num=record_num, company_name=company_name, addr=addr,
                                       business_addr=business_addr, legal_people=legal_people,
                                       company_principal=company_principal,
                                       quality_principal=quality_principal, web_name=web_name,
                                       web_program_name=web_program_name, domain_name=domain_name, ip=ip,
                                       service_machine_addr=service_machine_addr,
                                       non_profit_internet_service_record_num=non_profit_internet_service_record_num,
                                       record_mechanism=record_mechanism, record_date=record_date, gmt_created=times,
                                       gmt_updated=times)
                    sum.append(zhilian)
                else:
                    obj_delete = session.query(Medicine).filter(Medicine.record_num == record_num).all()
                    for i in obj_delete:
                        session.delete(i)
                    zhilian = Medicine(record_id=id, record_num=record_num, company_name=company_name, addr=addr,
                                       business_addr=business_addr, legal_people=legal_people,
                                       company_principal=company_principal,
                                       quality_principal=quality_principal, web_name=web_name,
                                       web_program_name=web_program_name, domain_name=domain_name, ip=ip,
                                       service_machine_addr=service_machine_addr,
                                       non_profit_internet_service_record_num=non_profit_internet_service_record_num,
                                       record_mechanism=record_mechanism, record_date=record_date, gmt_created=times,
                                       gmt_updated=times)
                    sum.append(zhilian)
                    old_data.append(zhilian)
        time.sleep(8)

    if len(sum) == 0:
        print('本次无更新数据！！！')
    else:
        print('数据库更新数据：{}条，其中旧数据更新：{}条，新增数据：{}条！！！'.format(len(sum),len(old_data),len(sum)-len(old_data)))
        write_db(sum)

def write_db(sum):
    for i in sum:
        session.add(i)
    session.commit()
    session.close()


if __name__ == '__main__':
    main()
