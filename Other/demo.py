# 查看浙江和上海数据量

'''''
# import pymysql
# db = pymysql.connect(host="192.168.2.99", user="root", password='BOOT-xwork1024', database="spider", port=3306)
# cursor = db.cursor()
#
#
# sql = "show tables"
#
# cursor.execute(sql)
# data = cursor.fetchall()
#
# data = [i[0] for i in data if 'spider_zj' in i[0]]
# print('上海市药监局spider表：{}'.format(data))
# print('上海市药监局spider表总量：{}'.format(len(data)))
# sum =0
# for s in data:
#     sql = 'select count(*) from {}'.format(s)
#     cursor.execute(sql)
#     count = cursor.fetchall()[0][0]
#     sum +=count
# print('上海药监局总数据：{}'.format(sum))
'''


# 上海某个网站的更新机制设计

'''

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
    # 只需前100页数据获取新鲜数据即可
    for page in range(2,3):
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
                    obj_delete = session.query(Medicine).filter(Medicine.social_credit_code == social_credit_code).first()
                    session.delete(obj_delete)
                    session.commit()
                    zhilian = Medicine(record_id=id, company_name=company_name, legal_people=legal_people,
                                       company_principal=company_principal
                                       , home_addr=home_addr, business_addr=business_addr, business_type=business_type,
                                       record_date=record_date,
                                       internet_sold_type=internet_sold_type, social_credit_code=social_credit_code,
                                       business_license_num=business_license_num, main_business=main_business
                                       , business_range=business_range, plat_form_info=str(plat_form_info),
                                       gmt_created=times, gmt_updated=times, other_info=other_info,company_id=company_id)
                sum.append(zhilian)
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
                    obj_delete = session.query(Medicine).filter(
                        Medicine.social_credit_code == social_credit_code).first()
                    session.delete(obj_delete)
                    session.commit()
                    zhilian = Medicine(record_id=id, company_name=company_name, legal_people=legal_people,
                                       company_principal=company_principal
                                       , home_addr=home_addr, business_addr=business_addr, business_type=business_type,
                                       record_date=record_date,
                                       internet_sold_type=internet_sold_type, social_credit_code=social_credit_code,
                                       business_license_num=business_license_num, main_business=main_business
                                       , business_range=business_range, plat_form_info=str(plat_form_info),
                                       gmt_created=times, gmt_updated=times, other_info=other_info)
                    sum.append(zhilian)
            time.sleep(1.5)

    if len(sum) == 0:
        print('本次无更新数据！！！')
    else:
        print('本地数据更新了{}条！！！'.format(len(sum)))
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

'''


# 测试布隆过滤器
#   布隆过滤器下的 1 和 '1' 结果是一样的
#    注意：加入布隆过滤器的尽量用 **字符串**

'''

from pybloom_live import ScalableBloomFilter
bloom = ScalableBloomFilter(initial_capacity=10000, error_rate=0.001)
data = [i for i in range(1,10000)]

for bl in data:
    bloom.add(bl)
print(0 not in bloom)
print(1  in bloom)
print(5  in bloom)
print(10000 in bloom)
if 1 not in bloom:
    print('数字')
elif '1'  in bloom:
    print('字符串型数字')
else:
    print('其他')
'''


# hashlib的md5加密,产生32位的不可逆字符串

'''
import hashlib
md5 = hashlib.md5()
md5.update('1'.encode())
print(md5.hexdigest())
'''

# 不定时的依据company_info 更新spider表中的company_id 字段

import pymysql
import time
from getCompanyId.get_company_id import get_company_id
conn = pymysql.connect(host='192.168.2.99',password='BOOT-xwork1024',database='spider',user='root')
cursor = conn.cursor()
# sql = "show tables"
# cursor.execute(sql)
# data = cursor.fetchall()
# sum = []
# for i in data:
#     if 'spider'  in i[0] and 'spider_sh' not in i[0] and 'spider_zj' not in i[0]:
#         print(i)
#         sum.append(i[0])
# print(sum)

# ['spider_add_value_telecom_info', 'spider_busi_range_standard', 'spider_company_city_level_makerspace', 'spider_company_honor_data', 'spider_company_province_level_makerspace', 'spider_company_province_tech_incubator', 'spider_company_related_park', 'spider_culture_business_license', 'spider_high_talent', 'spider_industry_information',  'spider_outstand_talent', 'spider_radio_show_business_license', 'spider_service_license', 'spider_talent_room']

# data = [i[0] for i in data]
# print(data)

all_tables = [
    'spider_add_value_telecom_info', 'spider_company_city_level_makerspace',
              'spider_company_honor_data', 'spider_company_province_level_makerspace',
              'spider_company_province_tech_incubator',
              'spider_culture_business_license', 'spider_industry_information',
              'spider_outstand_talent', 'spider_radio_show_business_license', 'spider_service_license',
              'spider_high_talent','spider_talent_room'
              ]
                # ,'spider_company_related_park']
for table in all_tables:
    sql = '''select id,company_name from {} where company_id is NULL '''.format(table)
    cursor.execute(sql)
    single_data = cursor.fetchall()
    print(single_data)
    for i in single_data:
        id = i[0]
        company_name = i[1]
        company_id = get_company_id(company_name)
        if company_id:
            update_sql = '''update {} set company_id = {} where id = {}'''.format(table,company_id,id)
            cursor.execute(update_sql)
            print('{}表中，公司{}新增了company_id字段'.format(table,company_name))
        else:
            continue
        # time.sleep(0.5)
    # break

conn.commit()
conn.close()

