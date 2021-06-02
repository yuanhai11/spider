import requests, pymysql, time
from sqlalchemy import Column, String, create_engine, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import logging
import time, os
import logging.handlers

# 初始化设置
logging.basicConfig(level=logging.INFO, format='%(asctime)s|%(name)-12s: %(levelname)-8s %(message)s')
# 创建
logger = logging.getLogger("spider_industry_information")
logger.setLevel(logging.INFO)

log_file_path = os.path.join(os.path.abspath('.'), 'log')
if not os.path.exists(log_file_path):
    os.mkdir(log_file_path)

# 创建handler
handler1 = logging.FileHandler("{}/空号过滤2.log".format(log_file_path))
handler1.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s|%(name)-12s+ %(levelname)-8s++%(message)s')
handler1.setFormatter(formatter)
handler2 = logging.StreamHandler()
handler2.setLevel(logging.ERROR)
logger.addHandler(handler1)
logger.addHandler(handler2)
'''
通过阿里云提供的空号检测接口进行手机号过滤
'''
# 创建对象的基类:
Base = declarative_base()


# 定义User对象:
class Medicine(Base):
    # 表的名字:
    __tablename__ = 'spider_number_filter'

    # 表的结构:
    id = Column(Integer(), primary_key=True, autoincrement=True)
    company_name = Column(String(256))
    business_status = Column(String(256))
    natural_person = Column(String(256))
    reg_money = Column(String(256))
    apply_date = Column(String(256))
    province = Column(String(256))
    city = Column(String(256))
    xian = Column(String(256))
    email = Column(String(256))
    web = Column(String(256))
    phone = Column(String(256))
    socal_code = Column(String(256))
    insurance_num = Column(String(256))
    company_type = Column(String(256))
    industry = Column(String(256))
    addr = Column(String(256))
    busi_range = Column(String(256))
    filter_result = Column(String(256))


# 初始化数据库连接:
engine = create_engine('mysql+pymysql://root:BOOT-xwork1024@192.168.2.97:3306/spider')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
# 创建session对象:
session = DBSession()

import xlrd


def parse_excle():
    import xlwt
    # 创建一个Wordbook对象，相当于创建了一个Excel文件
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)
    # 创建一个sheet对象，一个sheet对象对应Excel文件中的一张表格
    sheet = book.add_sheet("数仓三", cell_overwrite_ok=True)
    from xlrd import open_workbook
    workbook = open_workbook('个独3-5年服务行业_企查查(52134004).xls')  # 打开excel文件
    sheet2 = workbook.sheets()
    print(sheet2)
    num = 1
    sheet2 = workbook.sheet_by_index(0)
    print(sheet2.nrows)
    tup = []
    for i in range(2, sheet2.nrows):
        # if i < 26709 + 1:
        #     continue
        company_name = sheet2.cell(i, 0).value
        business_status = sheet2.cell(i, 1).value
        natural_person = sheet2.cell(i, 2).value
        reg_money = sheet2.cell(i, 3).value
        apply_date = sheet2.cell(i, 4).value
        hezhun_date = sheet2.cell(i, 5).value
        province = sheet2.cell(i, 6).value
        city = sheet2.cell(i, 7).value
        xian = sheet2.cell(i, 8).value
        phone = sheet2.cell(i, 9).value
        more_phone = sheet2.cell(i, 10).value
        email = sheet2.cell(i, 11).value
        more_email = sheet2.cell(i, 12).value
        socal_code = sheet2.cell(i, 13).value
        nashuiren_code = sheet2.cell(i, 14).value
        register_code = sheet2.cell(i, 15).value
        orangize_code = sheet2.cell(i, 16).value
        insurance_num = sheet2.cell(i, 17).value
        company_type = sheet2.cell(i, 18).value
        industry = sheet2.cell(i, 19).value
        old_name = sheet2.cell(i, 20).value
        english_name = sheet2.cell(i, 21).value
        web = sheet2.cell(i, 22).value
        addr = sheet2.cell(i, 23).value
        year_report_addr = sheet2.cell(i, 24).value
        busi_range = sheet2.cell(i, 25).value
        tup = []

        if '-' not in phone:
            sum = [company_name, business_status, natural_person, reg_money, apply_date,hezhun_date,province, city, xian,
                   phone,email,more_email,socal_code,nashuiren_code,register_code,orangize_code,insurance_num
                , company_type, industry, old_name,english_name,web,addr,year_report_addr,busi_range]
            for index, s in enumerate(sum):
                sheet.write(num, index, s)  #
            tup.append(phone)
            num += 1
        if '-' in more_phone and '；'not in more_phone:
            continue
        if more_phone != '-' and '；' not in more_phone:
            if more_phone not in tup:

                sum = [company_name, business_status, natural_person, reg_money, apply_date, hezhun_date, province, city,
                       xian,
                       more_phone, email,more_email,socal_code,nashuiren_code, register_code, orangize_code, insurance_num
                    , company_type, industry, old_name, english_name, web, addr, year_report_addr, busi_range]
                for index, s in enumerate(sum):
                    sheet.write(num, index, s)  #
                num += 1
                tup.append(more_phone)

        if '；' in more_phone:
            more_phone = more_phone.split('；')
            for m in more_phone:
                if '-' in m:
                    continue
                if m not in tup:

                    sum = [company_name, business_status, natural_person, reg_money, apply_date, hezhun_date, province,
                           city,
                           xian,
                           m, email,more_email,socal_code, nashuiren_code,register_code, orangize_code, insurance_num
                        , company_type, industry, old_name, english_name, web, addr, year_report_addr, busi_range]
                    for index, s in enumerate(sum):
                        sheet.write(num, index, s)  #
                    tup.append(m)
                    num += 1
    book.save("3-5-data.xls")

    #     if ',' in phone:
    #         phone_lists = phone.split(',')
    #         for ph in phone_lists:
    #             print(company_name, business_status, natural_person, reg_money, apply_date, province, city, xian, email,
    #                   web, ph, socal_code, insurance_num
    #                   , company_type, industry, addr, busi_range)
    #             sum = [company_name, business_status, natural_person, reg_money, apply_date, province, city, xian,
    #                    email,
    #                    web, ph, socal_code, insurance_num
    #                 , company_type, industry, addr, busi_range]
    #             for index, s in enumerate(sum):
    #                 sheet.write(num, index, s)  # 其中，"0, 0"指定表中的单元格，"EnglishName"是向该单元格中写入的内容
    #
    #             num += 1
    #             # exit()
    #     else:
    #         print(company_name, business_status, natural_person, reg_money, apply_date, province, city, xian, email,
    #               web, phone, socal_code, insurance_num
    #               , company_type, industry, addr, busi_range)
    #         sum2 = [company_name, business_status, natural_person, reg_money, apply_date, province, city, xian, email,
    #                 web, phone, socal_code, insurance_num
    #             , company_type, industry, addr, busi_range]
    #         for ind, sss in enumerate(sum2):
    #             sheet.write(num, ind, sss)  # 其中，"0, 0"指定表中的单元格，"EnglishName"是向该单元格中写入的内容
    #         num += 1
    #         # exit()
    #
    #     if num > 40000:
    #         book.save("name3.xls")
    #         print(i)
    #         exit()
    #
    # book.save("name3.xls")


def filter_compass():
    import time, requests
    from xlrd import open_workbook
    workbook = open_workbook(
        r'/Demo/name.xls')  # 打开excel文件
    sheet2 = workbook.sheet_by_index(0)
    print(sheet2.nrows)
    # import xlrd  # 导入模块
    # from xlutils.copy import copy  # 导入copy模块
    # rb = xlrd.open_workbook(r'D:\projects\Spider\local_spider\Other\spider_all\Demo\name.xls')  # 打开weng.xls文件
    # wb = copy(rb)  # 利用xlutils.copy下的copy函数复制
    # sheet2 = wb.get_sheet(0)  # 获取表单0

    for i in range(1, sheet2.nrows):
        sheet2.write(1, 17, 1)
        exit()


def compass():
    from xlrd import open_workbook
    workbook = open_workbook('../处理企查查数据/个独1-3年服务行业企查查(52164331).xls')  # 打开excel文件
    sheet2 = workbook.sheet_by_index(0)
    print(sheet2.nrows)
    for i in range(1, sheet2.nrows):
        company_name = sheet2.cell(i, 0).value

        business_status = sheet2.cell(i, 1).value
        natural_person = sheet2.cell(i, 2).value
        reg_money = sheet2.cell(i, 3).value
        apply_date = sheet2.cell(i, 4).value
        province = sheet2.cell(i, 5).value
        city = sheet2.cell(i, 6).value
        xian = sheet2.cell(i, 7).value
        email = sheet2.cell(i, 8).value
        web = sheet2.cell(i, 9).value
        phone = sheet2.cell(i, 10).value
        socal_code = sheet2.cell(i, 11).value
        insurance_num = sheet2.cell(i, 12).value
        company_type = sheet2.cell(i, 13).value
        industry = sheet2.cell(i, 14).value
        addr = sheet2.cell(i, 15).value
        busi_range = sheet2.cell(i, 16).value
        filter_result = sheet2.cell(i, 17).value
        medicine = Medicine(company_name=company_name, business_status=business_status, natural_person=natural_person,
                            reg_money=reg_money, apply_date=apply_date, province=province,
                            city=city, xian=xian, email=email, web=web, phone=phone, socal_code=socal_code,
                            insurance_num=insurance_num, company_type=company_type, industry=industry,
                            addr=addr, busi_range=busi_range, filter_result=filter_result
                            )
        session.add(medicine)
    session.commit()


import re

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
        'http': resp
    }
    proxys.append(proxy)
    print(proxys[-1])


# dl()


# 请求阿里云接口，
def num_filter():
    all_data = session.query(Medicine).filter(Medicine.filter_result == '').all()
    for index, data in enumerate(all_data):
        try:
            if index < 25696:
                continue
            id = data.id
            phone = data.phone
            # if phone == '13758200234':
            #     print(index)
            # continue
            url = 'https://himobile.market.alicloudapi.com/query?number={}'.format(phone)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
                'Authorization': 'APPCODE e0894501ef864abda581ee83234d49f9',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
            }
            time.sleep(1.5)
            res = requests.request(method='get', url=url, headers=headers, proxies=proxys[-1], timeout=10).json()
            print(index)
            logger.info(res)
            co = res['ret']
            if co == 200:
                desc = res['data']['desc']
                medicine = session.query(Medicine).filter(Medicine.id == id).first()
                medicine.filter_result = desc
                session.commit()
        except Exception as e:
            print(e)
            dl()
            time.sleep(5)


if __name__ == '__main__':
    parse_excle()
    # filter_compass()
    # compass()
    # num_filter()
