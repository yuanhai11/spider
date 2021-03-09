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
    __tablename__ = 'spider_sh_company_medical_equipment_license_invalid'

    # 表的结构:
    id = Column(Integer(), primary_key=True,autoincrement=True)
    record_id = Column(String(256))
    company_name = Column(String(256))
    license_num = Column(String(256))
    legal_people = Column(String(256))
    company_principal = Column(String(256))
    license_valid_date = Column(String(256))
    license_invalid_date = Column(String(256))
    produce_range = Column(String(256))
    addr = Column(String(256))
    produce_addr = Column(String(256))
    produce_info = Column(String(10000))
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
    sql = "select license_num from spider_sh_company_medical_equipment_license_invalid"
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
        'pageName': 'apparatusProdOTList',
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
            'pageName': 'apparatusProdOTList',
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
        # print(results)
        if len(results) == 1:
            results = reload(page)
            print('跳出reload函数！！！')

        for i in results:
            id = i.get('ZSID')
            company_name = i.get('QYMC_ZW')
            legal_people = i.get('FRMC_ZW')
            license_num = i.get('ZSBH')
            company_principal = i.get('QYFZR_ZW')

            license_valid_date = i.get('QFRQ')
            if license_valid_date:
                license_valid_date = get_time(license_valid_date)
            license_invalid_date = i.get('YXQZ')
            if license_invalid_date:
                license_invalid_date = get_time(license_invalid_date)

            produce_range = ""
            fw1 = i.get('CPFW_ZW')
            if fw1:
                r =  '【原《分类目录》分类编码区】：'+fw1
                produce_range +=r
            else:
                r = '【原《分类目录》分类编码区】：无'
                produce_range += r

            fw2 = i.get('CPFW_YW')
            if fw2:
                r =  '【新《分类目录》分类编码区】：'+fw2
                produce_range +=r
            else:
                r = '【新《分类目录》分类编码区】：无'
                produce_range += r

            addr = i.get('ZCDZ_ZW')
            produce_addr_list = i.get('scdzList')
            produce_addr = ""
            if produce_addr_list:
                if len(produce_addr_list)!=0:
                    for aa in produce_addr_list:
                        ad = aa.get('SCDZ')
                        produce_addr += ad

            produce_info = str(i.get('cpxxList'))

            times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            company_id = get_company_id(company_name)
            if company_id:
                print((id, company_name, legal_people, license_num, company_principal, license_valid_date,
                       license_invalid_date, produce_range, addr,
                       produce_addr, produce_info,company_id))
                if license_num not in bloom:
                    zhilian = Medicine(record_id=id, license_num=license_num, company_name=company_name,
                                       legal_people=legal_people, company_principal=company_principal,
                                       license_valid_date=license_valid_date, license_invalid_date=license_invalid_date,
                                       produce_range=produce_range,company_id=company_id,
                                       addr=addr, produce_addr=produce_addr, produce_info=produce_info,
                                       gmt_created=times, gmt_updated=times, license_type='已过期')
                    sum.append(zhilian)
                else:
                    obj_delete = session.query(Medicine).filter(Medicine.license_num == license_num).all()
                    for i in obj_delete:
                        session.delete(i)
                    zhilian = Medicine(record_id=id, license_num=license_num, company_name=company_name,
                                       legal_people=legal_people, company_principal=company_principal,
                                       license_valid_date=license_valid_date, license_invalid_date=license_invalid_date,
                                       produce_range=produce_range, company_id=company_id,
                                       addr=addr, produce_addr=produce_addr, produce_info=produce_info,
                                       gmt_created=times, gmt_updated=times, license_type='已过期')
                    sum.append(zhilian)
                    old_data.append(zhilian)
            else:
                print((id, company_name, legal_people, license_num, company_principal, license_valid_date,
                       license_invalid_date, produce_range, addr,
                       produce_addr, produce_info,))
                if license_num not in bloom:
                    zhilian = Medicine(record_id=id, license_num=license_num, company_name=company_name,
                                       legal_people=legal_people, company_principal=company_principal,
                                       license_valid_date=license_valid_date, license_invalid_date=license_invalid_date,
                                       produce_range=produce_range,
                                       addr=addr, produce_addr=produce_addr, produce_info=produce_info,
                                       gmt_created=times, gmt_updated=times, license_type='已过期')
                    sum.append(zhilian)
                else:
                    obj_delete = session.query(Medicine).filter(Medicine.license_num == license_num).all()
                    for i in obj_delete:
                        session.delete(i)
                    zhilian = Medicine(record_id=id, license_num=license_num, company_name=company_name,
                                       legal_people=legal_people, company_principal=company_principal,
                                       license_valid_date=license_valid_date, license_invalid_date=license_invalid_date,
                                       produce_range=produce_range,
                                       addr=addr, produce_addr=produce_addr, produce_info=produce_info,
                                       gmt_created=times, gmt_updated=times, license_type='已过期')
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
