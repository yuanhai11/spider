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
            叙述： 此代码：零售；  此表包括：批发、零售连锁、零售
    1、更新机制：前5页
    2、没有数据更新,更新频率待定

    '''

    # 表的名字:
    __tablename__ = 'spider_sh_company_medicine_wholesale'

    # 表的结构:
    id = Column(Integer(), primary_key=True,autoincrement=True)
    record_id = Column(String(256))
    company_name = Column(String(256))
    area = Column(String(256))
    addr = Column(String(256))
    street = Column(String(256))
    warehouse = Column(String(256))
    legal_people = Column(String(256))
    company_principal = Column(String(256))
    quality_principal = Column(String(256))
    business_way = Column(String(256))
    business_range = Column(String(256))
    license_num = Column(String(256))
    license_name = Column(String(256))
    license_mechanism = Column(String(256))
    license_status = Column(String(256))
    license_valid_date = Column(String(256))
    license_invalid_date = Column(String(256))
    gsp_license_num = Column(String(256))
    gsp_approve_valid_date = Column(String(256))
    gsp_approve_invalid_date = Column(String(256))
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
def main():
    bloom = get_updated()
    sum = []
    old_data = []
    for page in range(1,6):
        data = {
            'currentPage':page,
            'pageSize': '10',
            'groupSize': '8',
            'pageName': 'durgsList',
            'licenType': 'retail'
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
        for i in results:
            id = i.get('ZSID')
            company_name = i.get('QYMC_ZW')
            area = i.get('ZCDZQX')
            addr = i.get('QYZCDZ')
            street = i.get('ZCDZJD')
            warehouse = i.get('CFDZ')
            legal_people = i.get('FDDBR')
            company_principal = i.get('QYFZR')
            quality_principal = i.get('ZLFZR')
            business_way = i.get('JYFS')
            business_range = i.get('JYFW')
            license_num = i.get('ZSBH')
            license_name = i.get('ZSMC')
            license_mechanism = i.get('FZJG')
            license_status = i.get('ZSZT')

            license_valid_date = i.get('QFRQ')
            if license_valid_date:
                license_valid_date = get_time(license_valid_date)
            license_invalid_date = i.get('YXQZ')
            if license_invalid_date:
                license_invalid_date = get_time(license_invalid_date)

            gsp_license_num = i.get('RZBH')

            gsp_approve_valid_date = i.get('RZSJ')
            if gsp_approve_valid_date:
                gsp_approve_valid_date = get_time(gsp_approve_valid_date)
            gsp_approve_invalid_date = i.get('RZYXQZ')
            if gsp_approve_invalid_date:
                gsp_approve_invalid_date = get_time(gsp_approve_invalid_date)
            times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            company_id = get_company_id(company_name)
            if company_id:
                print((id,company_name,area,addr,street,warehouse,legal_people,company_principal,quality_principal,business_way,business_range,
                       license_num,license_name,license_mechanism,license_status,license_valid_date,license_invalid_date,gsp_license_num,gsp_approve_valid_date,gsp_approve_invalid_date,
                       company_id))
                if license_num not in bloom:
                    zhilian = Medicine(record_id=id,company_name=company_name,area=area,addr=addr,street=street,warehouse=warehouse,
                                   legal_people=legal_people,company_principal=company_principal,
                                   quality_principal=quality_principal,business_way=business_way,business_range=business_range,
                                   license_num=license_num,license_name=license_name,license_mechanism=license_mechanism,license_status=license_status,
                                   license_valid_date=license_valid_date,license_invalid_date=license_invalid_date,gsp_license_num=gsp_license_num,
                                   gsp_approve_valid_date=gsp_approve_valid_date,gsp_approve_invalid_date=gsp_approve_invalid_date,
                                   gmt_created=times, gmt_updated=times,company_id=company_id)

                    sum.append(zhilian)
                else:
                    obj_delete = session.query(Medicine).filter(Medicine.license_num == license_num).all()
                    for i in obj_delete:
                        session.delete(i)
                    zhilian = Medicine(record_id=id, company_name=company_name, area=area, addr=addr, street=street,
                                       warehouse=warehouse,
                                       legal_people=legal_people, company_principal=company_principal,
                                       quality_principal=quality_principal, business_way=business_way,
                                       business_range=business_range,
                                       license_num=license_num, license_name=license_name,
                                       license_mechanism=license_mechanism, license_status=license_status,
                                       license_valid_date=license_valid_date, license_invalid_date=license_invalid_date,
                                       gsp_license_num=gsp_license_num,
                                       gsp_approve_valid_date=gsp_approve_valid_date,
                                       gsp_approve_invalid_date=gsp_approve_invalid_date,
                                       gmt_created=times, gmt_updated=times, company_id=company_id)

                    sum.append(zhilian)
                    old_data.append(zhilian)
            else:
                print((id, company_name, area, addr, street, warehouse, legal_people, company_principal,
                       quality_principal, business_way, business_range,
                       license_num, license_name, license_mechanism, license_status, license_valid_date,
                       license_invalid_date, gsp_license_num, gsp_approve_valid_date, gsp_approve_invalid_date))
                if license_num not in bloom:
                    zhilian = Medicine(record_id=id, company_name=company_name, area=area, addr=addr, street=street,
                                       warehouse=warehouse,
                                       legal_people=legal_people, company_principal=company_principal,
                                       quality_principal=quality_principal, business_way=business_way,
                                       business_range=business_range,
                                       license_num=license_num, license_name=license_name,
                                       license_mechanism=license_mechanism, license_status=license_status,
                                       license_valid_date=license_valid_date, license_invalid_date=license_invalid_date,
                                       gsp_license_num=gsp_license_num,
                                       gsp_approve_valid_date=gsp_approve_valid_date,
                                       gsp_approve_invalid_date=gsp_approve_invalid_date,
                                       gmt_created=times, gmt_updated=times)
                    sum.append(zhilian)
                else:
                    obj_delete = session.query(Medicine).filter(Medicine.license_num == license_num).all()
                    for i in obj_delete:
                        session.delete(i)
                    zhilian = Medicine(record_id=id, company_name=company_name, area=area, addr=addr, street=street,
                                       warehouse=warehouse,
                                       legal_people=legal_people, company_principal=company_principal,
                                       quality_principal=quality_principal, business_way=business_way,
                                       business_range=business_range,
                                       license_num=license_num, license_name=license_name,
                                       license_mechanism=license_mechanism, license_status=license_status,
                                       license_valid_date=license_valid_date, license_invalid_date=license_invalid_date,
                                       gsp_license_num=gsp_license_num,
                                       gsp_approve_valid_date=gsp_approve_valid_date,
                                       gsp_approve_invalid_date=gsp_approve_invalid_date,
                                       gmt_created=times, gmt_updated=times)
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
    sql = "select license_num from spider_sh_company_medicine_wholesale"
    cursor.execute(sql)
    db_data = cursor.fetchall()
    # print(db_data)
    # exit()
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
