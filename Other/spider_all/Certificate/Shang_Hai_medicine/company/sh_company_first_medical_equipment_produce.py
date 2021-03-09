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
    1、更新机制：前10页
    2、目前发现数据有点无规则，新增数据较少，更新频率：2周
    '''
    # 表的名字:
    __tablename__ = 'spider_sh_company_first_medical_equipment_produce'

    # 表的结构:
    id = Column(Integer(), primary_key=True,autoincrement=True)
    record_id = Column(String(256))
    company_name = Column(String(256))
    legal_people = Column(String(256))
    company_principal = Column(String(256))
    record_num = Column(String(256))
    recent_record_date = Column(String(256))
    record_mechanism = Column(String(256))
    business_range = Column(String(256))
    home_addr = Column(String(256))
    busi_addr = Column(String(256))
    produce_info = Column(String(10000))
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
    sql = "select record_num from spider_sh_company_first_medical_equipment_produce"
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
        'pageName': 'apparatusProdBackList',
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

    for page in range(1,11):
        data = {
            'currentPage': page,
            'pageSize': '10',
            'groupSize': '8',
            'pageName': 'apparatusProdBackList',
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
            company_name = i.get('QYMC_ZW')
            legal_people = i.get('FRMC_ZW')
            company_principal = i.get('QYFZR_ZW')

            recent_record_date = i.get('QFRQ')
            if recent_record_date:
                recent_record_date = get_time(recent_record_date)

            record_mechanism = i.get('FZJG')

            business_range = ""
            fw1 = i.get('CPFW_ZW')
            if fw1:
                r =  '【原《分类目录》分类编码区】：'+fw1
                business_range +=r
            else:
                r = '【原《分类目录》分类编码区】：无'
                business_range += r

            fw2 = i.get('CPFW_YW')
            if fw2:
                r =  '【新《分类目录》分类编码区】：'+fw2
                business_range +=r
            else:
                r = '【新《分类目录》分类编码区】：无'
                business_range += r

            home_addr = i.get('ZCDZ_ZW')
            record_num = i.get('ZSBH')

            business_addr_list = i.get('scdzList')
            busi_addr = ""
            if business_addr_list:
                if len(business_addr_list)!=0:
                    for aa in business_addr_list:
                        addr = aa.get('SCDZ')
                        busi_addr += addr

            produce_info = str(i.get('cpxxList'))
            times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            company_id = get_company_id(company_name)
            if company_id:
                print((id,company_name,legal_people,company_principal,record_num,recent_record_date,record_mechanism,business_range,
                       home_addr,busi_addr,produce_info,company_id))
                if record_num not in bloom:
                    zhilian = Medicine(record_id=id,company_name=company_name,legal_people=legal_people,company_principal=company_principal,record_num=record_num,
                                       recent_record_date=recent_record_date,record_mechanism=record_mechanism,business_range=business_range,company_id=company_id,
                                       home_addr=home_addr,busi_addr=busi_addr,produce_info=produce_info,gmt_created=times, gmt_updated=times)
                    sum.append(zhilian)
                else:
                    obj_delete = session.query(Medicine).filter(Medicine.record_num == record_num).all()
                    for i in obj_delete:
                        session.delete(i)
                    zhilian = Medicine(record_id=id, company_name=company_name, legal_people=legal_people,
                                       company_principal=company_principal, record_num=record_num,
                                       recent_record_date=recent_record_date, record_mechanism=record_mechanism,
                                       business_range=business_range,
                                       home_addr=home_addr, busi_addr=busi_addr, produce_info=produce_info,company_id=company_id,
                                       gmt_created=times, gmt_updated=times)
                    sum.append(zhilian)
                    old_data.append(zhilian)
            else:
                print((id, company_name, legal_people, company_principal, record_num, recent_record_date,
                       record_mechanism, business_range,
                       home_addr, busi_addr, produce_info))
                if record_num not in bloom:
                    zhilian = Medicine(record_id=id, company_name=company_name, legal_people=legal_people,
                                       company_principal=company_principal, record_num=record_num,
                                       recent_record_date=recent_record_date, record_mechanism=record_mechanism,
                                       business_range=business_range,
                                       home_addr=home_addr, busi_addr=busi_addr, produce_info=produce_info,
                                       gmt_created=times, gmt_updated=times)
                    sum.append(zhilian)
                else:
                    obj_delete = session.query(Medicine).filter(Medicine.record_num == record_num).all()
                    for i in obj_delete:
                        session.delete(i)
                    zhilian = Medicine(record_id=id, company_name=company_name, legal_people=legal_people,
                                       company_principal=company_principal, record_num=record_num,
                                       recent_record_date=recent_record_date, record_mechanism=record_mechanism,
                                       business_range=business_range,
                                       home_addr=home_addr, busi_addr=busi_addr, produce_info=produce_info,
                                       gmt_created=times, gmt_updated=times)
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
