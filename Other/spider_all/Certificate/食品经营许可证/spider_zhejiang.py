'''
食品许可证：上海
'''
import re, json
import time
import requests, pymysql
import base64
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pksc1_v1_5
from Crypto.PublicKey import RSA
from sqlalchemy import Column, String, create_engine, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()


# 定义User对象:

class Medicine(Base):
    # 表的名字:
    __tablename__ = 'spider_qualification'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    license_num = Column(String(256))
    company_name = Column(String(256))
    project_name = Column(String(256))
    license_current_status = Column(String(256))
    valid_date = Column(String(256))
    invalid_date = Column(String(256))
    area = Column(Integer())
    addr = Column(String(256))
    busi_addr = Column(String(256))
    reg_authority = Column(String(256))

    gmt_created = Column(String(256))
    gmt_updated = Column(String(256))
    company_id = Column(String(256))
    license_name = Column(String(256))


# 初始化数据库连接:
engine = create_engine('mysql+pymysql://root:BOOT-xwork1024@192.168.2.97:3306/spider')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
# 创建session对象:
session = DBSession()

proxys = []


def dl():
    while 1:
        try:
            dlurl = 'http://api.goubanjia.com/dynamic/get/d490a5d4debefc8980ae6ee4c4148552.html?sep=3'
            resp = requests.get(dlurl).text
            break
        except Exception:
            pass
    time.sleep(3)
    resp = re.sub(r'\n', '', resp)
    proxy = {
        'https': resp
    }
    proxys.append(proxy)
    print(proxys[-1])


dl()


def get_data():
    db = pymysql.connect(host="192.168.2.97", user="root", password='BOOT-xwork1024', database="spider", port=3306)
    cursor = db.cursor()
    sql = "select company_name,business_project from data_wheel where province_code = 'zj'"
    cursor.execute(sql)
    db_data = cursor.fetchall()
    data = [(i[0], i[1]) for i in db_data]
    return data


def get_updated():
    db = pymysql.connect(host="192.168.2.97", user="root", password='BOOT-xwork1024', database="spider", port=3306)
    cursor = db.cursor()
    sql = "select company_name from spider_qualification"
    cursor.execute(sql)
    db_data = cursor.fetchall()
    data = [i[0] for i in db_data]
    from pybloom_live import ScalableBloomFilter
    bloom = ScalableBloomFilter(initial_capacity=1000000, error_rate=0.001)
    for bl in data:
        bloom.add(bl)
    return bloom


def main():
    '''
    浙江数据保存本地
    :return:
    '''
    # 将浙江数据保存本地

    # data = get_data()
    # sum = []
    # for d in data:
    #     business_project = d[1]
    #     company_name = d[0]
    #     print(business_project)
    #     if business_project == None:
    #         continue
    #     if '食品互联网销售（销售预包装食品）' in business_project:
    #         sum.append(company_name)
    #     elif '食品互联网销售' in business_project:
    #         sum.append(company_name)
    #     elif '餐饮服务' in business_project:
    #         sum.append(company_name)
    #     elif '餐饮服务（不产生油烟、异味、废气）' in business_project:
    #         sum.append(company_name)
    #     elif '食品经营' in business_project:
    #         sum.append(company_name)
    #     elif '食品经营（销售预包装食品）' in business_project:
    #         sum.append(company_name)
    #     elif '食品经营（销售散装食品）' in business_project:
    #         sum.append(company_name)
    #     elif '婴幼儿配方乳粉销售' in business_project:
    #         sum.append(company_name)
    #     elif '酒吧服务（不含演艺娱乐活动）' in business_project:
    #         sum.append(company_name)
    #     elif '特殊医学用途配方食品销售' in business_project:
    #         sum.append(company_name)
    # print(len(sum))
    # with open('浙江-data.json','w',encoding='utf-8')as fp:
    #     fp.write(json.dumps(sum,ensure_ascii=False))
    # exit()
    # bloom = get_updated()
    with open('浙江-data.json', encoding='utf-8')as fp:
        data = json.loads(fp.read())[650000:700000]
    print(len(data))

    for index, company_name in enumerate(data):
        # if company_name == '海宁市斜桥镇杨宇水果店':
        #     print(index)
        #     exit()
        # continue
        # if company_name not in bloom:
        flag = 0
        # if index < 36383 + 1:  # 从这开始
        #     continue
        url = 'http://223.4.77.249:8050/SearchHandler.ashx?Flag=getSearchDataList&tabid=2E398671-CA45-BFF7-DF09-5884E0288432&page=1&keyword={}'.format(
            company_name)
        response = ""
        while 1:
            try:
                time.sleep(4.5)
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
                }
                response = requests.request(method='get', url=url, headers=headers, proxies=proxys[-1], timeout=10,
                                            allow_redirects=False)
                if response.status_code == 200:
                    response = response.json()
                    # print('search 获取信息成功！！！')
                    break
            except Exception as e:
                print(e)
                if flag > 10:
                    with open('fail_log_zhejiang.txt', 'a', encoding='utf-8')as fp:
                        fp.write(json.dumps(company_name, ensure_ascii=False))
                    exit()
                flag += 1
                dl()
        try:
            rowdata = response[0]['rowdata']
        except Exception:
            continue
        if rowdata == []:
            print(company_name, 'no data , index:{}'.format(index))
            continue
        for row in rowdata:
            name = row['str_2'].replace("%", "\\").encode("utf-8").decode("unicode_escape")
            if company_name == name:
                data_id = row['data_id']
                detail_url = 'http://223.4.77.249:8050/SearchHandler.ashx?Flag=getSearchData&tabid=2E398671-CA45-BFF7-DF09-5884E0288432&dataid={}'.format(
                    data_id)
                while 1:
                    try:
                        time.sleep(3)
                        headers = {
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
                        }
                        response_deta = requests.request(method='get', url=detail_url, proxies=proxys[-1],
                                                         headers=headers, timeout=10, allow_redirects=False)
                        if response_deta.status_code == 200:
                            response_deta = response_deta.json()
                            # print('detail 获取信息成功！！！')
                            break
                    except Exception as e:
                        print(e)
                        dl()
                company_name = response_deta[0]['rowdata'][0]['str_2'].replace("%", "\\").encode("utf-8").decode(
                    "unicode_escape")
                license_num = response_deta[0]['rowdata'][0]['str_7'].replace("%", "\\").encode("utf-8").decode(
                    "unicode_escape")
                addr = response_deta[0]['rowdata'][0]['str_5'].replace("%", "\\").encode("utf-8").decode(
                    "unicode_escape")
                busi_addr = response_deta[0]['rowdata'][0]['str_6'].replace("%", "\\").encode("utf-8").decode(
                    "unicode_escape")
                reg_authority = response_deta[0]['rowdata'][0]['str_11'].replace("%", "\\").encode("utf-8").decode(
                    "unicode_escape")
                valid_date = response_deta[0]['rowdata'][0]['str_10'].replace("%", "\\").encode("utf-8").decode(
                    "unicode_escape")
                invalid_date = response_deta[0]['rowdata'][0]['str_14'].replace("%", "\\").encode("utf-8").decode(
                    "unicode_escape")
                license_current_status = response_deta[0]['rowdata'][0]['str_15'].replace("%", "\\").encode(
                    "utf-8").decode("unicode_escape")
                times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

                print(company_name, license_num, addr, busi_addr, reg_authority, valid_date, invalid_date, '食品经营许可证',
                      license_current_status, 'index:{}'.format(index))
                medicine = Medicine(company_name=company_name, license_num=license_num, addr=addr, busi_addr=busi_addr,
                                    reg_authority=reg_authority, valid_date=valid_date, invalid_date=invalid_date,
                                    license_current_status=license_current_status, area=9, license_name='食品经营许可证',
                                    gmt_created=times, gmt_updated=times
                                    )
                session.add(medicine)
                break
        session.commit()
    # else:
    #     print(company_name,'重复数据')


if __name__ == '__main__':
    main()
