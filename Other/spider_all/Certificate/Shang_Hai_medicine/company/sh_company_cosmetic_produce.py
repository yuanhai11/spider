import re
import time
import requests
import pymysql
import json
from decouple import config
from getCompanyId.get_company_id import get_company_id
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
    __tablename__ = 'spider_sh_company_cosmetic_produce'

    # 表的结构:
    id = Column(Integer(), primary_key=True,autoincrement=True)
    record_id = Column(String(256))
    area_mechainsm = Column(String(256))
    license_num = Column(String(256))
    company_name = Column(String(256))
    addr = Column(String(256))
    produce_addr = Column(String(1000))
    social_credit_code = Column(String(256))
    legal_people = Column(String(256))
    company_principal = Column(String(256))
    quality_principal = Column(String(256))
    allow_project_range = Column(String(256))
    license_valid_date = Column(String(256))
    license_invalid_date = Column(String(256))
    change_cancel_record = Column(String(256))
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
    sql = "select social_credit_code from spider_sh_company_cosmetic_produce"
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
        'pageName': 'hzpList',
    }
    url = "http://xuke.smda.sh.cn/AppRoveManage/selectLicense/selectData"
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
            'pageName': 'hzpList',
        }
        url = "http://xuke.smda.sh.cn/AppRoveManage/selectLicense/selectData"
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
        if len(results) == 1:
            results = reload(page)
            print('跳出reload函数！！！')

        for i in results:
            id = i.get('ZSBH')
            area_mechainsm =  i.get('RCJGJG')
            license_num = i.get('ZSBH')
            company_name = i.get('QYMC_ZW')
            addr = i.get('ZCDZ_ZW')
            produce_addr= i.get('SCDZ_ZW')
            social_credit_code = i.get('SHXYDM')
            legal_people = i.get('FRMC_ZW')
            company_principal = i.get('QYFZR_ZW')
            quality_principal = i.get('ZLFZR')
            allow_project_range = i.get('CPFW_ZW')

            license_valid_date = i.get('QFRQ')
            if license_valid_date:
                license_valid_date = get_time(license_valid_date)
            license_invalid_date = i.get('YXQZ')
            if license_invalid_date:
                license_invalid_date = get_time(license_invalid_date)
            change_cancel_record = ''

            times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            company_id = get_company_id(company_name)
            if company_id:
                print((id,area_mechainsm,license_num,company_name,addr,produce_addr,social_credit_code,legal_people,company_principal,
                       quality_principal,allow_project_range,license_valid_date,license_invalid_date,change_cancel_record,company_id
                       ))
                if social_credit_code not in bloom:
                    zhilian = Medicine(record_id=id,company_name=company_name,license_num=license_num,legal_people=legal_people,company_principal=company_principal,
                                       license_invalid_date=license_invalid_date,license_valid_date=license_valid_date,change_cancel_record=change_cancel_record,
                                       produce_addr=produce_addr,social_credit_code=social_credit_code,addr=addr,
                                       quality_principal=quality_principal,allow_project_range=allow_project_range,company_id=company_id,
                                       area_mechainsm=area_mechainsm,gmt_created=times, gmt_updated=times)
                    sum.append(zhilian)
                else:
                    obj_delete = session.query(Medicine).filter(Medicine.social_credit_code == social_credit_code).all()
                    for i in obj_delete:
                        session.delete(i)
                    zhilian = Medicine(record_id=id, company_name=company_name, license_num=license_num,
                                       legal_people=legal_people, company_principal=company_principal,
                                       license_invalid_date=license_invalid_date, license_valid_date=license_valid_date,
                                       change_cancel_record=change_cancel_record,
                                       produce_addr=produce_addr, social_credit_code=social_credit_code, addr=addr,
                                       quality_principal=quality_principal, allow_project_range=allow_project_range,
                                       company_id=company_id,
                                       area_mechainsm=area_mechainsm, gmt_created=times, gmt_updated=times)
                    sum.append(zhilian)
                    old_data.append(zhilian)
            else:
                print((id, area_mechainsm, license_num, company_name, addr, produce_addr, social_credit_code,
                       legal_people, company_principal,
                       quality_principal, allow_project_range, license_valid_date, license_invalid_date,
                       change_cancel_record,
                       ))
                if social_credit_code not in bloom:
                    zhilian = Medicine(record_id=id, company_name=company_name, license_num=license_num,
                                       legal_people=legal_people, company_principal=company_principal,
                                       license_invalid_date=license_invalid_date, license_valid_date=license_valid_date,
                                       change_cancel_record=change_cancel_record,
                                       produce_addr=produce_addr, social_credit_code=social_credit_code, addr=addr,
                                       quality_principal=quality_principal, allow_project_range=allow_project_range,
                                       area_mechainsm=area_mechainsm, gmt_created=times, gmt_updated=times)
                    sum.append(zhilian)
                else:
                    obj_delete = session.query(Medicine).filter(Medicine.social_credit_code == social_credit_code).all()
                    for i in obj_delete:
                        session.delete(i)
                    zhilian = Medicine(record_id=id, company_name=company_name, license_num=license_num,
                                       legal_people=legal_people, company_principal=company_principal,
                                       license_invalid_date=license_invalid_date, license_valid_date=license_valid_date,
                                       change_cancel_record=change_cancel_record,
                                       produce_addr=produce_addr, social_credit_code=social_credit_code, addr=addr,
                                       quality_principal=quality_principal, allow_project_range=allow_project_range,
                                       area_mechainsm=area_mechainsm, gmt_created=times, gmt_updated=times)
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
