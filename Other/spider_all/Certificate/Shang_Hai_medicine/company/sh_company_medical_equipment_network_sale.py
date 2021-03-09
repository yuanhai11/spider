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
        2、存在旧数据更新问题，
            解决：删除旧数据，增加新数据
        3、频率：2周
       '''
    # 表的名字:
    __tablename__ = 'spider_sh_company_medical_equipment_network_sale'

    # 表的结构:
    id = Column(Integer(), primary_key=True,autoincrement=True)
    record_id = Column(String(256))
    company_name = Column(String(256))
    legal_people = Column(String(256))
    company_principal = Column(String(256))
    home_addr = Column(String(256))
    business_addr = Column(String(256))
    business_type = Column(String(256))
    record_date = Column(String(256))
    internet_sold_type = Column(String(256))
    social_credit_code = Column(String(256))
    business_license_num = Column(String(256))
    main_business = Column(String(256))
    business_range = Column(String(256))
    plat_form_info = Column(String(256))
    gmt_created = Column(String(256))
    gmt_updated = Column(String(256))
    other_info = Column(String(1000))
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
def main():

    bloom = get_updated()
    sum = []
    old_data = []
    for page in range(1,15):
        url = "http://wlxsba.smda.sh.cn/openApi/getRecordPage?search=false&nd=1600149091958&rows=20&page={}&sidx=&sord=desc&totalrows=2000".format(page)
        response_web = ""
        for IP in range(10):
            try:
                response_web = requests.request(method='get', url=url, headers=headers,proxies=proxys[-1],
                                                timeout=15)
                # print(response)
                if response_web.status_code == 200:
                    response_web = response_web.content.decode('utf8')
                    break
            except Exception:
                dl()
        # print(response_web)
        response = json.loads(response_web)
        results = response.get('rows')

        for i in results:
            detail = i.get('ylqxEnp')
            if not detail:
                continue

            company_name = detail.get('baQymc')
            legal_people = detail.get('baFddbr')
            company_principal = detail.get('baQyfzr')
            home_addr = detail.get('baQyzcdz')
            business_addr = detail.get('baJycsdz')
            business_type =detail.get('baJyfs')
            business_range = detail.get('baJyfwzw')
            internet_sold_type = '入驻类'
            social_credit_code = detail.get('enpId')

            record_num = detail.get('baZsbh')
            license_num = detail.get('licNo')
            if record_num and not license_num:
                business_license_num = record_num
            elif license_num and not record_num:
                business_license_num = license_num
            else:
                business_license_num = ",".join([record_num, license_num])

            id = i.get('riId')
            response = ""
            url = 'http://wlxsba.smda.sh.cn/openApi/getRecordDetailData?recordId={}&isOpen=1&_=1600151345630'.format(id)
            print(url)
            for IP in range(10):
                try:
                    response = requests.request(method='get', url=url, headers=headers, proxies=proxys[-1],
                                                    timeout=15)
                    # print(response)
                    if response.status_code == 200:
                        response = response.content.decode('utf8')
                        break
                except Exception:
                    dl()
            response = json.loads(response)

            flag = response.get('recordInfo').get('ylqxEnpJson')
            flag = json.loads(flag)
            if not company_name:
                company_name =flag.get('baQymc')
                if not company_name:
                    company_name = flag.get('enpName')
            if not legal_people:
                legal_people = flag.get('baFddbr')
                if not legal_people:
                    legal_people = flag.get('fddbr')
            if not company_principal:
                company_principal = flag.get('baQyfzr')
                if not company_principal:
                    company_principal = flag.get('qyfzr')
            if not home_addr:
                home_addr = flag.get('baQyzcdz')
                if not home_addr:
                    home_addr = flag.get('homeAddr')
            if not business_addr:
                business_addr = flag.get('baJycsdz')
                if not business_addr:
                    business_addr = flag.get('registerAddr')
            if not business_type:
                business_type = flag.get('baJyfs')
                if not business_type:
                    business_type = flag.get('jyfsStr')
            if not business_range:
                business_range = flag.get('baJyfwzw')
                if not business_range:
                    business_range = flag.get('jyfw')
            if not social_credit_code:
                social_credit_code = flag.get('enpId')

            main_business = response.get('boornetParameter').get('paraName')
            record_date = response.get('recordInfo').get('completeTime')
            if not record_date:
                record_date = response.get('recordInfo').get('createtime')

            other_info = response.get('recordInfo').get('ylqxEnpJson')

            lis =response.get('enterRecordInfoList')
            plat_form_info = []
            if lis:
                for i in lis:
                    sing = {}
                    join_platform_name =i.get('svPfName')
                    platform_license_num =i.get('svRecodeNum')
                    plat_form_domain =i.get('wsDomainName')
                    plat_form_shop_add = i.get('wsShopName')
                    sing['join_platform_name'] = join_platform_name
                    sing['platform_license_num'] = platform_license_num
                    sing['plat_form_domain'] = plat_form_domain
                    sing['plat_form_shop_add'] = plat_form_shop_add
                    plat_form_info.append(sing)
            company_id = get_company_id(company_name)
            if company_id:
                print((id,company_name,legal_people,company_principal,home_addr,business_addr,business_type,
                       record_date,internet_sold_type,social_credit_code,business_license_num,main_business,business_range,plat_form_info,other_info,company_id))
                times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                if social_credit_code not in bloom:
                    zhilian = Medicine(record_id=id,company_name=company_name,legal_people=legal_people,company_principal=company_principal
                                       ,home_addr=home_addr,business_addr=business_addr,business_type=business_type,record_date=record_date,
                                       internet_sold_type=internet_sold_type,social_credit_code=social_credit_code,
                                       business_license_num=business_license_num,main_business=main_business,company_id=company_id
                                       ,business_range=business_range,plat_form_info=str(plat_form_info),gmt_created=times, gmt_updated=times,other_info = other_info)
                else:
                    obj_delete = session.query(Medicine).filter(Medicine.social_credit_code == social_credit_code).all()
                    for i in obj_delete:
                        session.delete(i)
                    zhilian = Medicine(record_id=id, company_name=company_name, legal_people=legal_people,
                                       company_principal=company_principal
                                       , home_addr=home_addr, business_addr=business_addr, business_type=business_type,
                                       record_date=record_date,
                                       internet_sold_type=internet_sold_type, social_credit_code=social_credit_code,
                                       business_license_num=business_license_num, main_business=main_business
                                       , business_range=business_range, plat_form_info=str(plat_form_info),
                                       gmt_created=times, gmt_updated=times, other_info=other_info,company_id=company_id)
                sum.append(zhilian)
                old_data.append(zhilian)
            else:
                print((id, company_name, legal_people, company_principal, home_addr, business_addr, business_type,
                       record_date, internet_sold_type, social_credit_code, business_license_num, main_business,
                       business_range, plat_form_info, other_info))
                times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                if social_credit_code not in bloom:
                    zhilian = Medicine(record_id=id, company_name=company_name, legal_people=legal_people,
                                       company_principal=company_principal
                                       , home_addr=home_addr, business_addr=business_addr, business_type=business_type,
                                       record_date=record_date,
                                       internet_sold_type=internet_sold_type, social_credit_code=social_credit_code,
                                       business_license_num=business_license_num, main_business=main_business
                                       , business_range=business_range, plat_form_info=str(plat_form_info),
                                       gmt_created=times, gmt_updated=times, other_info=other_info)

                    sum.append(zhilian)
                else:
                    obj_delete = session.query(Medicine).filter(Medicine.social_credit_code == social_credit_code).all()
                    for i in obj_delete:
                        session.delete(i)
                    zhilian = Medicine(record_id=id, company_name=company_name, legal_people=legal_people,
                                       company_principal=company_principal
                                       , home_addr=home_addr, business_addr=business_addr, business_type=business_type,
                                       record_date=record_date,
                                       internet_sold_type=internet_sold_type, social_credit_code=social_credit_code,
                                       business_license_num=business_license_num, main_business=main_business
                                       , business_range=business_range, plat_form_info=str(plat_form_info),
                                       gmt_created=times, gmt_updated=times, other_info=other_info)
                    sum.append(zhilian)
                    old_data.append(zhilian)
            time.sleep(1.5)

    if len(sum) == 0:
        print('本次无更新数据！！！')
    else:
        print('数据库更新数据：{}条，其中旧数据更新：{}条，新增数据：{}条！！！'.format(len(sum),len(old_data),len(sum)-len(old_data)))
        write_db(sum)

def get_updated():
    db = pymysql.connect(host="192.168.2.99", user="root", password='BOOT-xwork1024', database="spider", port=3306)
    cursor = db.cursor()
    sql = "select social_credit_code from spider_sh_company_medical_equipment_network_sale"
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
