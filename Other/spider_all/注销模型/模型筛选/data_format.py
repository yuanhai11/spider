'''
pass
    将spider_revoke_model里的5万到13万中的数据规范化，字段：经营异常情况
'''

import time,re,json
import threading
from lxml import etree
import requests,pymysql
from sqlalchemy import Column, String, create_engine, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy import or_
from sqlalchemy.ext.declarative import declarative_base
# 创建对象的基类:
Base = declarative_base()
# 定义User对象:
class Medicine(Base):
    # 表的名字:
    __tablename__ = 'spider_2_revoke_model'

    # 表的结构:
    id = Column(Integer(), primary_key=True, autoincrement=True)
    company_name = Column(String(256))
    business_status = Column(String(256))
    connect_company_count = Column(String(256))
    busi_risk_count = Column(String(256))
    busi_abnormal_situation = Column(String(256))
    easy_revoke_end_date = Column(String(256))
    easy_revoke_result = Column(String(256))
    risk_date = Column(String(256))
    risk_reason = Column(String(256))
    is_have_year_report = Column(String(256))
    year_report_url = Column(String(256))
    year_report_busi_status = Column(String(256))
    nineteen_insurance_count = Column(String(256))
    eighteen_insurance_count = Column(String(256))
    seventeen_insurance_count = Column(String(256))
    current_1_busi_status = Column(String(256))
    current_2_busi_status = Column(String(256))
# 初始化数据库连接:
engine = create_engine('mysql+pymysql://root:BOOT-xwork1024@192.168.2.97:3306/spider')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
# 创建session对象:
session = DBSession()
proxys = []
def dl():

    dlurl = 'http://api.goubanjia.com/dynamic/get/d490a5d4debefc8980ae6ee4c4148552.html?sep=3'
    resp = requests.get(dlurl).text
    time.sleep(2)
    resp = re.sub(r'\n', '', resp)
    proxy = {
        'https': resp
    }
    proxys.append(proxy)
    print(proxys[-1])

def main3():
    all_data = session.query(Medicine).offset(50000).limit(80000).all()
    print(len(all_data))
    for index,medi in enumerate(all_data):
        if index<100:
            continue
        # if index == 100:
        #     break

        company_name = medi.company_name
        sum = []

        busi_abnormal_situation = medi.busi_abnormal_situation
        print(company_name,busi_abnormal_situation)
        medicine = session.query(Medicine).filter(Medicine.company_name == company_name).first()
        if not busi_abnormal_situation:
            medicine.busi_abnormal_situation = str(sum)
        else:

            busi_abnormal_situation = eval(busi_abnormal_situation)
            if len(busi_abnormal_situation['列入异常']) != 0:
                for ran in busi_abnormal_situation['列入异常']:
                    single = {}
                    in_date = ran['列入日期']
                    in_reason = ran['列入经营异常名录原因']
                    in_auth = ran['作出决定机关']
                    single['列入日期'] = in_date
                    single['列入原因'] = in_reason
                    single['列入机关'] = in_auth
                    single['移出日期'] = 'None'
                    single['移出原因'] = 'None'
                    single['移出机关'] = 'None'

                    sum.append(single)

            if len(busi_abnormal_situation['移出异常']) != 0:
                for ran in busi_abnormal_situation['移出异常']:

                    single = {}
                    in_date = ran['列入日期']
                    in_reason = ran['列入经营异常名录原因']
                    in_auth = ran['作出决定机关']

                    out_reason = ran['移出经营异常名录原因']
                    out_date = ran['移出日期']
                    single['列入日期'] = in_date
                    single['列入原因'] = in_auth
                    single['列入机关'] = in_reason

                    single['移出日期'] = out_date
                    single['移出原因'] = out_reason
                    single['移出机关'] = in_reason
                    sum.append(single)

            medicine.busi_abnormal_situation = str(sum)

    session.commit()

if __name__ == '__main__':
    main3()
