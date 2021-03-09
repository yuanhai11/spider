import re
import time
import requests
import pymysql
import json
from getCompanyId.get_company_id import get_company_id
from sqlalchemy import Column, String, create_engine,Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# 创建对象的基类:
Base = declarative_base()
# 定义User对象:
class Medicine(Base):
    '''
        1、更新机制：获取前14页数据
        2、目前：38864条数据（存在无效数据）
        3、目前为止：无数据更新，更新频率待定
    '''
    # 表的名字:
    __tablename__ = 'spider_sh_company_medical_equipment_business'

    # 表的结构:
    id = Column(Integer(), primary_key=True,autoincrement=True)
    record_id = Column(String(256))
    area = Column(String(256))
    company_name = Column(String(256))
    license_name = Column(String(256))
    license_num = Column(String(256))
    business_type = Column(String(256))
    supervision_classification = Column(String(256))
    supervision_sort = Column(String(256))
    legal_people = Column(String(256))
    company_principal = Column(String(256))
    addr = Column(String(256))
    business_addr = Column(String(256))
    warehouse_addr = Column(String(256))
    business_way = Column(String(256))
    third_business_range = Column(String(256))
    license_valid_date = Column(String(256))
    license_invalid_date = Column(String(256))
    two_business_range = Column(String(256))
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
    dlurl = 'http://api.goubanjia.com/dynamic/get/d490a5d4debefc8980ae6ee4c4148552.html?sep=3'
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
    sql = "select license_num from spider_sh_company_medical_equipment_business"
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
        'pageName': 'apparatusDealList',
    }
    url = "http://xuke.yjj.sh.gov.cn/AppRoveManage/selectLicense/selectData"
    response_web = ""
    for IP in range(10):
        try:
            response_web = requests.request(method='post', url=url, data=data, headers=headers, proxies=proxys[-1],
                                            timeout=20)
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
    for page in range(1,6):
        data = {
            'currentPage': page,
            'pageSize': '10',
            'groupSize': '8',
            'pageName': 'apparatusDealList',
        }
        url = "http://xuke.yjj.sh.gov.cn/AppRoveManage/selectLicense/selectData"
        response_web = ""
        for IP in range(10):
            try:
                response_web = requests.request(method='post', url=url, data=data, headers=headers, proxies=proxys[-1],
                                                timeout=20)
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
            area = i.get('JYDZQX')
            company_name = i.get('QYMC_ZW')
            license_name = i.get('ZSMC')
            license_num = i.get('ZSBH')
            business_type = i.get('JYMS')
            supervision_classification = i.get('FLJGJB')
            supervision_sort = i.get('ZDJGLB')
            legal_people = i.get('FDDBR')
            company_principal = i.get('QYFZR')
            addr = i.get('QYZSDZ')
            business_addr = i.get('JYCS')
            warehouse_addr = i.get('CFDZ')
            business_way = i.get('JYFS')

            third_business_range = ""
            fw1 = i.get('JYFW')
            if fw1:
                r = '【原《分类目录》分类编码区】：' + fw1
                third_business_range += r
            else:
                r = '【原《分类目录》分类编码区】：无'
                third_business_range += r

            fw2 = i.get('CPFW_YW')
            if fw2:
                r = '【新《分类目录》分类编码区】：' + fw2
                third_business_range += r
            else:
                r = '【新《分类目录》分类编码区】：无'
                third_business_range += r

            license_valid_date = i.get('QFRQ')
            if license_valid_date:
                license_valid_date = get_time(license_valid_date)
            license_invalid_date = i.get('YXQZ')
            if license_invalid_date:
                license_invalid_date = get_time(license_invalid_date)
            two_business_range = i.get('BAJYFW')
            record_date = i.get('BAQFRQ')
            if record_date:
                record_date = get_time(record_date)
            times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            company_id = get_company_id(company_name)
            if company_id:
                print((id, area, company_name, license_name, license_num, business_type, supervision_classification,
                       supervision_sort,
                       legal_people, company_principal, addr, business_addr, warehouse_addr, business_way,
                       third_business_range,
                       license_valid_date, license_invalid_date, two_business_range, record_date,company_id))
                if license_num not in bloom:
                    zhilian = Medicine(record_id=id,area=area,company_name=company_name,license_name = license_name,license_num=license_num,business_type=business_type,
                                       supervision_classification=supervision_classification,supervision_sort=supervision_sort,legal_people=legal_people,
                                       company_principal=company_principal,addr=addr,business_addr=business_addr,warehouse_addr=warehouse_addr,
                                       business_way=business_way,third_business_range=third_business_range,
                                       license_valid_date=license_valid_date,license_invalid_date=license_invalid_date,two_business_range=two_business_range,
                                       record_date=record_date,gmt_created=times, gmt_updated=times,company_id=company_id)
                    sum.append(zhilian)
                else:
                    obj_delete = session.query(Medicine).filter(Medicine.license_num == license_num).all()
                    for i in obj_delete:
                        session.delete(i)
                    zhilian = Medicine(record_id=id, area=area, company_name=company_name, license_name=license_name,
                                       license_num=license_num, business_type=business_type,
                                       supervision_classification=supervision_classification,
                                       supervision_sort=supervision_sort, legal_people=legal_people,
                                       company_principal=company_principal, addr=addr, business_addr=business_addr,
                                       warehouse_addr=warehouse_addr,
                                       business_way=business_way, third_business_range=third_business_range,
                                       license_valid_date=license_valid_date, license_invalid_date=license_invalid_date,
                                       two_business_range=two_business_range,
                                       record_date=record_date, gmt_created=times, gmt_updated=times,
                                       company_id=company_id)
                    sum.append(zhilian)
                    old_data.append(zhilian)
            else:
                print((id, area, company_name, license_name, license_num, business_type, supervision_classification,
                       supervision_sort,
                       legal_people, company_principal, addr, business_addr, warehouse_addr, business_way,
                       third_business_range,
                       license_valid_date, license_invalid_date, two_business_range, record_date))
                if license_num not in bloom:
                    zhilian = Medicine(record_id=id, area=area, company_name=company_name, license_name=license_name,
                                       license_num=license_num, business_type=business_type,
                                       supervision_classification=supervision_classification,
                                       supervision_sort=supervision_sort, legal_people=legal_people,
                                       company_principal=company_principal, addr=addr, business_addr=business_addr,
                                       warehouse_addr=warehouse_addr,
                                       business_way=business_way, third_business_range=third_business_range,
                                       license_valid_date=license_valid_date, license_invalid_date=license_invalid_date,
                                       two_business_range=two_business_range,
                                       record_date=record_date, gmt_created=times, gmt_updated=times)
                    sum.append(zhilian)
                else:
                    obj_delete = session.query(Medicine).filter(Medicine.license_num == license_num).all()
                    for i in obj_delete:
                        session.delete(i)
                    zhilian = Medicine(record_id=id, area=area, company_name=company_name, license_name=license_name,
                                       license_num=license_num, business_type=business_type,
                                       supervision_classification=supervision_classification,
                                       supervision_sort=supervision_sort, legal_people=legal_people,
                                       company_principal=company_principal, addr=addr, business_addr=business_addr,
                                       warehouse_addr=warehouse_addr,
                                       business_way=business_way, third_business_range=third_business_range,
                                       license_valid_date=license_valid_date, license_invalid_date=license_invalid_date,
                                       two_business_range=two_business_range,
                                       record_date=record_date, gmt_created=times, gmt_updated=times)
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
