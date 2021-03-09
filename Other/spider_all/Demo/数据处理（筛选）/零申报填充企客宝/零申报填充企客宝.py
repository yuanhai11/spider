from xlrd import open_workbook
import requests,pymysql,time
from sqlalchemy import Column, String, create_engine, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import time,os
import logging.handlers
#初始化设置
logging.basicConfig(level = logging.INFO,format='%(asctime)s|%(name)-12s: %(levelname)-8s %(message)s')
#创建
logger = logging.getLogger("test")
logger.setLevel(logging.INFO)

log_file_path = os.path.join(os.path.abspath('.'),'log')
if not os.path.exists(log_file_path):
    os.mkdir(log_file_path)

#创建handler
handler1=logging.FileHandler("{}/构建空号过滤库.log".format(log_file_path))
handler1.setLevel(logging.INFO)
formatter=logging.Formatter('%(asctime)s|%(name)-12s+ %(levelname)-8s++%(message)s')
handler1.setFormatter(formatter)
handler2=logging.StreamHandler()
handler2.setLevel(logging.ERROR)
logger.addHandler(handler1)
logger.addHandler(handler2)
# 创建对象的基类:
Base = declarative_base()
# 定义User对象:

class Medicine(Base):
    # 表的名字:
    __tablename__ = 'filter_sheet'
    id = Column(Integer(), primary_key=True,autoincrement=True)
    company_name = Column(String(256))
    busi_status = Column(String(256))
    legal_peple = Column(String(256))
    reg_money = Column(String(256))
    apply_date = Column(String(256))
    province = Column(String(256))
    city = Column(String(256))
    area = Column(String(256))
    email = Column(String(256))
    web = Column(String(256))
    phone = Column(String(256))
    social_code = Column(String(256))
    insurance = Column(String(256))
    company_type = Column(String(256))
    industry = Column(String(256))
    addr = Column(String(256))
    busi_range = Column(String(256))
    filter_resule = Column(String(256))

class Medicine_qkb(Base):
    # 表的名字:
    __tablename__ = 'qikebao'
    id = Column(Integer(), primary_key=True,autoincrement=True)
    comoany_name = Column(String(256))
    mob = Column(String(256))

class Medicine_database(Base):
    # 表的名字:
    __tablename__ = 'spider_number_database'
    id = Column(Integer(), primary_key=True,autoincrement=True)
    company_name = Column(String(256))
    phone = Column(String(256))
    result = Column(String(256))

engine = create_engine('mysql+pymysql://root:BOOT-xwork1024@192.168.2.97:3306/spider')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
# 创建session对象:
session = DBSession()

def main():

    workbook = open_workbook(r'C:\Users\20945\Desktop\table\零申报数据（待洗）-已筛选.xlsx')  # 打开excel文件
    sum = []
    flag = ''
    sheet2 = workbook.sheet_by_index(0)
    print(sheet2.nrows)
    lig = False
    qkb_phone = []
    for i in range(1, sheet2.nrows):
        # if i == 500:
        #     session.commit()
        #     exit()
        # if i<835:
        #     continue
        company_name = sheet2.cell(i, 0).value
        busi_status = sheet2.cell(i, 1).value
        legal_peple = sheet2.cell(i, 2).value
        reg_money = sheet2.cell(i, 3).value
        apply_date = sheet2.cell(i, 4).value
        province = sheet2.cell(i, 5).value
        city = sheet2.cell(i, 6).value
        area = sheet2.cell(i, 7).value
        email = sheet2.cell(i, 8).value
        web = sheet2.cell(i, 9).value
        phone = sheet2.cell(i, 10).value
        social_code = sheet2.cell(i, 11).value
        insurance = sheet2.cell(i, 12).value
        company_type = sheet2.cell(i, 13).value
        industry = sheet2.cell(i, 14).value
        addr = sheet2.cell(i, 15).value
        busi_range = sheet2.cell(i, 16).value
        filter_resule = sheet2.cell(i, 17).value

        if flag!=company_name:

            for ph in qkb_phone:
                if ph !='':
                    filter_resule_test = number_identify(ph)
                    me = Medicine(company_name=company_name_test, busi_status=busi_status_test, legal_peple=legal_peple_test,
                                  reg_money=reg_money_test, apply_date=apply_date_test, province=province_test,
                                  city=city_test, area=area_test, email=email_test, web=web_test, phone=ph, social_code=social_code_test,
                                  insurance=insurance_test, company_type=company_type_test, industry=industry_test,
                                  addr=addr_test, busi_range=busi_range_test, filter_resule=filter_resule_test
                                  )
                    session.add(me)
                    print(company_name_test,'新增了一个信息')
                    qkb_phone = []
            data = session.query(Medicine_qkb).filter(Medicine_qkb.comoany_name == company_name).first()
            if data:
                # print(company_name, '在企客保里有数据！！！')
                company_name_test = company_name
                busi_status_test = busi_status
                legal_peple_test = legal_peple
                reg_money_test = reg_money
                apply_date_test = apply_date
                province_test = province
                city_test = city
                area_test = area
                email_test = email
                web_test = web
                social_code_test = social_code
                insurance_test = insurance
                company_type_test = company_type
                industry_test = industry
                addr_test = addr
                busi_range_test = busi_range

                qkb_phone = data.mob.split(',')
                # print(qkb_phone)
                if phone in qkb_phone:
                    qkb_phone.remove(phone)

            flag = company_name
        else:
            if phone in qkb_phone:
                qkb_phone.remove(phone)

        me = Medicine(company_name=company_name,busi_status=busi_status,legal_peple=legal_peple,reg_money=reg_money,apply_date=apply_date,province=province,
                 city=city,area=area,email=email,web=web,phone=phone,social_code=social_code,insurance=insurance,company_type=company_type,industry=industry,
                 addr=addr,busi_range=busi_range,filter_resule=filter_resule
                 )
        session.add(me)

    session.commit()

def number_identify(number):
    '''
    对手机号进行识别，进行实号过滤
    :return:
    '''
    url = 'https://himobile.market.alicloudapi.com/query?number={}'.format(number)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'Authorization': 'APPCODE e0894501ef864abda581ee83234d49f9',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }
    res = requests.request(method='get', url=url, headers=headers).json()
    logger.info(res)
    co = res['ret']
    if co == 200:
        desc = res['data']['desc']
        return desc

def number_identify_all():
    '''
    将 数据中filter_result 为空的数据进行空号过滤
    :return:
    '''
    all_data = session.query(Medicine).filter(Medicine.filter_resule == '').all()
    for index,data in enumerate(all_data):
        try:
            if index<1461:
                continue
            id = data.id
            number = data.phone
            # if number == '15162649974':
            #     print(index)
            # continue
            url = 'https://himobile.market.alicloudapi.com/query?number={}'.format(number)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
                'Authorization': 'APPCODE e0894501ef864abda581ee83234d49f9',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
            }
            time.sleep(1.5)
            res = requests.request(method='get', url=url, headers=headers).json()
            print(index)
            logger.info(res)
            co = res['ret']
            if co == 200:
                desc = res['data']['desc']
                medicine = session.query(Medicine).filter(Medicine.id == id).first()
                medicine.filter_resule = desc
                session.commit()
        except Exception as e :
            print(e)
            time.sleep(3)

def insert():
    workbook = open_workbook(r'C:\Users\20945\Desktop\table\零申报数据（待洗）-已筛选.xlsx')  # 打开excel文件
    sheet2 = workbook.sheet_by_index(0)
    print(sheet2.nrows)
    for i in range(1, sheet2.nrows):
        company_name = sheet2.cell(i, 0).value
        phone = sheet2.cell(i, 10).value
        filter_resule = sheet2.cell(i, 17).value
        me = Medicine_database(company_name=company_name, phone=phone,result=filter_resule)
        session.add(me)
    session.commit()
if __name__ == '__main__':
    # main()
    # number_identify_all()
    insert()