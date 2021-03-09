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
        1、无数据更新
        2、更新频率待定
    '''
    # 表的名字:
    __tablename__ = 'spider_sh_company_medical_equipment_entrust_produce'

    # 表的结构:
    id = Column(Integer(), primary_key=True,autoincrement=True)
    record_id = Column(String(256))
    entrust_company_name = Column(String(256))
    entrust_license_num = Column(String(256))
    entrust_legal = Column(String(256))
    entrust_company_principal = Column(String(256))
    entrust_addr = Column(String(256))
    entrust_produce_addr = Column(String(256))
    be_entrust_company_name = Column(String(256))
    be_entrust_license_num = Column(String(256))
    be_entrust_legal = Column(String(256))
    be_entrust_company_principal = Column(String(256))
    be_entrust_addr = Column(String(256))
    be_entrust_produce_addr = Column(String(256))
    entrust_product_name = Column(String(256))
    product_license_num = Column(String(256))
    entrust_date = Column(String(256))
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
def reload(page):
    time.sleep(10)
    data = {
        'currentPage': page,
        'pageSize': '10',
        'groupSize': '8',
        'pageName': 'apparatusWTProdList',
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
            'currentPage':page,
            'pageSize': '10',
            'groupSize': '8',
            'pageName': 'apparatusWTProdList',
        }
        url = "http://xuke.yjj.sh.gov.cn/AppRoveManage/selectLicense/selectData"
        response_web = ""
        for IP in range(10):
            try:
                response_web = requests.request(method='post', url=url, data = data,headers=headers,proxies=proxys[-1],
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
            id = i.get('CPZCH_BAH')
            entrust_company_name =i.get('QYMC')
            entrust_license_num = i.get('XKZBH')
            entrust_legal = i.get('FDDBR')
            entrust_company_principal = i.get('QYFZR')
            entrust_addr = i.get('QYZCDZ')
            entrust_produce_addr = i.get('SCDZ')
            be_entrust_company_name = i.get('SWTQYMC')
            be_entrust_license_num = i.get('SWTQYSCXKZ')
            be_entrust_legal = i.get('SWTFDDBR')
            be_entrust_company_principal = i.get('SWTQYFZR')
            be_entrust_addr = i.get('SWTQYZCDZ')
            be_entrust_produce_addr = i.get('SWTQYSCDZ')
            entrust_product_name = i.get('CPMC')
            product_license_num = i.get('CPZCH_BAH')
            entrust_date = i.get('WTQXRQ')
            record_date = i.get('QFRQ')
            if record_date:
                record_date = get_time(record_date)
            if entrust_date:
                entrust_date = get_time(entrust_date)
            times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            company_id = get_company_id(entrust_company_name)
            if company_id:
                print((id, entrust_company_name, entrust_license_num, entrust_legal, entrust_company_principal,
                       entrust_addr, entrust_produce_addr,
                       be_entrust_company_name, be_entrust_license_num, be_entrust_legal, be_entrust_company_principal,
                       be_entrust_addr,
                       be_entrust_produce_addr, entrust_product_name, product_license_num, record_date, entrust_date,company_id
                       ))
                if product_license_num not in bloom:
                    zhilian = Medicine(record_id=id, entrust_company_name=entrust_company_name,
                                       entrust_license_num=entrust_license_num, entrust_legal=entrust_legal,
                                       entrust_company_principal=entrust_company_principal, entrust_addr=entrust_addr,
                                       entrust_produce_addr=entrust_produce_addr,
                                       be_entrust_company_name=be_entrust_company_name,
                                       be_entrust_license_num=be_entrust_license_num, be_entrust_legal=be_entrust_legal,
                                       be_entrust_company_principal=be_entrust_company_principal,
                                       be_entrust_addr=be_entrust_addr,
                                       be_entrust_produce_addr=be_entrust_produce_addr,
                                       entrust_product_name=entrust_product_name,
                                       product_license_num=product_license_num,
                                       record_date=record_date, entrust_date=entrust_date, gmt_created=times,company_id=company_id,
                                       gmt_updated=times)

                    sum.append(zhilian)
                else:
                    obj_delete = session.query(Medicine).filter(Medicine.product_license_num == product_license_num).all()
                    for i in obj_delete:
                        session.delete(i)
                    zhilian = Medicine(record_id=id, entrust_company_name=entrust_company_name,
                                       entrust_license_num=entrust_license_num, entrust_legal=entrust_legal,
                                       entrust_company_principal=entrust_company_principal, entrust_addr=entrust_addr,
                                       entrust_produce_addr=entrust_produce_addr,
                                       be_entrust_company_name=be_entrust_company_name,
                                       be_entrust_license_num=be_entrust_license_num, be_entrust_legal=be_entrust_legal,
                                       be_entrust_company_principal=be_entrust_company_principal,
                                       be_entrust_addr=be_entrust_addr,
                                       be_entrust_produce_addr=be_entrust_produce_addr,
                                       entrust_product_name=entrust_product_name,
                                       product_license_num=product_license_num,
                                       record_date=record_date, entrust_date=entrust_date, gmt_created=times,
                                       company_id=company_id,
                                       gmt_updated=times)

                    sum.append(zhilian)
                    old_data.append(zhilian)
            else:
                print((id, entrust_company_name, entrust_license_num, entrust_legal, entrust_company_principal,
                       entrust_addr, entrust_produce_addr,
                       be_entrust_company_name, be_entrust_license_num, be_entrust_legal, be_entrust_company_principal,
                       be_entrust_addr,
                       be_entrust_produce_addr, entrust_product_name, product_license_num, record_date, entrust_date,
                       ))
                if product_license_num not in bloom:
                    zhilian = Medicine(record_id=id, entrust_company_name=entrust_company_name,
                                       entrust_license_num=entrust_license_num, entrust_legal=entrust_legal,
                                       entrust_company_principal=entrust_company_principal, entrust_addr=entrust_addr,
                                       entrust_produce_addr=entrust_produce_addr,
                                       be_entrust_company_name=be_entrust_company_name,
                                       be_entrust_license_num=be_entrust_license_num, be_entrust_legal=be_entrust_legal,
                                       be_entrust_company_principal=be_entrust_company_principal,
                                       be_entrust_addr=be_entrust_addr,
                                       be_entrust_produce_addr=be_entrust_produce_addr,
                                       entrust_product_name=entrust_product_name,
                                       product_license_num=product_license_num,
                                       record_date=record_date, entrust_date=entrust_date, gmt_created=times,
                                       gmt_updated=times)

                    sum.append(zhilian)
                else:
                    obj_delete = session.query(Medicine).filter(
                        Medicine.product_license_num == product_license_num).all()
                    for i in obj_delete:
                        session.delete(i)
                    zhilian = Medicine(record_id=id, entrust_company_name=entrust_company_name,
                                       entrust_license_num=entrust_license_num, entrust_legal=entrust_legal,
                                       entrust_company_principal=entrust_company_principal, entrust_addr=entrust_addr,
                                       entrust_produce_addr=entrust_produce_addr,
                                       be_entrust_company_name=be_entrust_company_name,
                                       be_entrust_license_num=be_entrust_license_num, be_entrust_legal=be_entrust_legal,
                                       be_entrust_company_principal=be_entrust_company_principal,
                                       be_entrust_addr=be_entrust_addr,
                                       be_entrust_produce_addr=be_entrust_produce_addr,
                                       entrust_product_name=entrust_product_name,
                                       product_license_num=product_license_num,
                                       record_date=record_date, entrust_date=entrust_date, gmt_created=times,
                                       gmt_updated=times)
                    sum.append(zhilian)
                    old_data.append(zhilian)

        time.sleep(5)

    if len(sum) == 0:
        print('本次无更新数据！！！')
    else:
        print('数据库更新数据：{}条，其中旧数据更新：{}条，新增数据：{}条！！！'.format(len(sum),len(old_data),len(sum)-len(old_data)))
        write_db(sum)

def get_updated():
    db = pymysql.connect(host="192.168.2.99", user="root", password='BOOT-xwork1024', database="spider", port=3306)
    cursor = db.cursor()
    sql = "select product_license_num from spider_sh_company_medical_equipment_entrust_produce"
    cursor.execute(sql)
    db_data = cursor.fetchall()
    data = [i[0] for i in db_data]
    from pybloom_live import ScalableBloomFilter
    bloom = ScalableBloomFilter(initial_capacity=10000, error_rate=0.001)
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
