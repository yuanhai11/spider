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
    1、更新频率：2周
    '''
    # 表的名字:
    __tablename__ = 'spider_sh_company_medicine_produce'

    # 表的结构:
    id = Column(Integer(), primary_key=True,autoincrement=True)
    record_id = Column(String(256))
    company_name = Column(String(256))
    license_num = Column(String(256))
    license_invalid_date = Column(String(256))
    classifi_num = Column(String(256))
    social_credit_code = Column(String(256))
    legal_people = Column(String(256))
    company_principal = Column(String(256))
    register_addr = Column(String(256))
    produce_addr_and_range = Column(String(1000))
    quality_principal = Column(String(256))
    produce_principal = Column(String(256))
    quality_authorization = Column(String(10000))
    recent_update_date = Column(String(10000))
    gmt_created = Column(String(256))
    gmt_updated = Column(String(256))
    license_type = Column(String(256))
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
    sql = "select social_credit_code from spider_sh_company_medicine_produce"
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

def reload(page):
    time.sleep(10)
    data = {
        'currentPage': page,
        'pageSize': '10',
        'groupSize': '8',
        'pageName': 'drugProductList',
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
            'pageName': 'drugProductList',
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
            id = i.get('ZSBH')
            company_name = i.get('QYMC_ZW')
            license_num = i.get('ZSBH')
            classifi_num =  i.get('CPFWLB')
            social_credit_code = i.get('SHXYDM')
            license_invalid_date = i.get('YXQZ')
            recent_update_date = i.get('QFRQ')

            legal_people = i.get('FRMC_ZW')
            company_principal = i.get('QYFZR_ZW')
            register_addr = i.get('ZCDZ_ZW')
            produce_addr_and_range = i.get('CPFW_ZW')

            quality_principal = i.get('ZLFZR')
            produce_principal = i.get('SCFZR')
            quality_authorization = i.get('ZLSQR')
            license_type = i.get('ZSZT')
            if license_type == '10':
                license_type = '有效'
            else:
                license_type = '注销'

            times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            company_id = get_company_id(company_name)
            if company_id:
                print((id, company_name, license_num, classifi_num, social_credit_code, license_invalid_date,
                       recent_update_date, legal_people, company_principal,
                       register_addr, produce_addr_and_range, quality_principal, produce_principal,
                       quality_authorization, license_type,company_id
                       ))
                if social_credit_code not in bloom:
                    zhilian = Medicine(record_id=id, company_name=company_name, license_num=license_num,
                                       legal_people=legal_people, company_principal=company_principal,
                                       license_invalid_date=license_invalid_date, recent_update_date=recent_update_date,
                                       register_addr=register_addr,
                                       classifi_num=classifi_num, social_credit_code=social_credit_code,
                                       produce_addr_and_range=produce_addr_and_range,
                                       quality_principal=quality_principal, produce_principal=produce_principal,
                                       quality_authorization=quality_authorization,company_id=company_id,
                                       license_type=license_type, gmt_created=times, gmt_updated=times)
                    sum.append(zhilian)
                else:
                    obj_delete = session.query(Medicine).filter(Medicine.social_credit_code == social_credit_code).all()
                    for i in obj_delete:
                        session.delete(i)
                    zhilian = Medicine(record_id=id, company_name=company_name, license_num=license_num,
                                       legal_people=legal_people, company_principal=company_principal,
                                       license_invalid_date=license_invalid_date, recent_update_date=recent_update_date,
                                       register_addr=register_addr,
                                       classifi_num=classifi_num, social_credit_code=social_credit_code,
                                       produce_addr_and_range=produce_addr_and_range,
                                       quality_principal=quality_principal, produce_principal=produce_principal,
                                       quality_authorization=quality_authorization, company_id=company_id,
                                       license_type=license_type, gmt_created=times, gmt_updated=times)
                    sum.append(zhilian)
                    old_data.append(zhilian)
            else:
                print((id, company_name, license_num, classifi_num, social_credit_code, license_invalid_date,
                       recent_update_date, legal_people, company_principal,
                       register_addr, produce_addr_and_range, quality_principal, produce_principal,
                       quality_authorization, license_type,
                       ))
                if social_credit_code not in bloom:
                    zhilian = Medicine(record_id=id, company_name=company_name, license_num=license_num,
                                       legal_people=legal_people, company_principal=company_principal,
                                       license_invalid_date=license_invalid_date, recent_update_date=recent_update_date,
                                       register_addr=register_addr,
                                       classifi_num=classifi_num, social_credit_code=social_credit_code,
                                       produce_addr_and_range=produce_addr_and_range,
                                       quality_principal=quality_principal, produce_principal=produce_principal,
                                       quality_authorization=quality_authorization,
                                       license_type=license_type, gmt_created=times, gmt_updated=times)
                    sum.append(zhilian)
                else:
                    obj_delete = session.query(Medicine).filter(Medicine.social_credit_code == social_credit_code).all()
                    for i in obj_delete:
                        session.delete(i)
                    zhilian = Medicine(record_id=id, company_name=company_name, license_num=license_num,
                                       legal_people=legal_people, company_principal=company_principal,
                                       license_invalid_date=license_invalid_date, recent_update_date=recent_update_date,
                                       register_addr=register_addr,
                                       classifi_num=classifi_num, social_credit_code=social_credit_code,
                                       produce_addr_and_range=produce_addr_and_range,
                                       quality_principal=quality_principal, produce_principal=produce_principal,
                                       quality_authorization=quality_authorization,
                                       license_type=license_type, gmt_created=times, gmt_updated=times)
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
