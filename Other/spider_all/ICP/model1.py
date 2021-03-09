from pybloom_live import ScalableBloomFilter
import pymysql
from sqlalchemy import Column, String, create_engine, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# 创建对象的基类:
Base = declarative_base()
# 模型一
# 定义User对象:
class Medicine(Base):
    # 表的名字:
    __tablename__ = 'spider_model1'

    # 表的结构:
    id = Column(Integer(), primary_key=True, autoincrement=True)
    company_name = Column(String(256))
    mobile = Column(String(256))
    other_mobiles = Column(String(256))
    reg_money = Column(String(256))
    business_status = Column(String(256))
    company_type = Column(String(256))
    insurance_num = Column(String(256))

    gmt_created = Column(String(256))
    gmt_updated = Column(String(256))
    company_id = Column(String(256))
# 初始化数据库连接:
engine = create_engine('mysql+pymysql://root:BOOT-xwork1024@192.168.2.99:3306/spider')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
# 创建session对象:
session = DBSession()

def model1_filter_data(table):
    sql = 'select company_name from {} where permit_number is not null ;'.format(table)
    cursor.execute(sql)
    permit_data = cursor.fetchall()
    permit_data = [i[0] for i in permit_data]
    return permit_data

def main():
    '''
    有icp edi 域名备案
    :return:
    '''
    db = pymysql.connect(host="192.168.2.99", user="root", password='BOOT-xwork1024', database="spider", port=3306)
    cursor = db.cursor()
    sql = 'select distinct (company_name) from spider_company_icp;'
    cursor.execute(sql)
    domain_data = cursor.fetchall()
    domain_data = [i[0] for i in domain_data]
    # print(domain_data)
    print('icp 域名备案 ---- count：{}'.format(len(domain_data)))
    '''
    没有icp edi 许可证
    :return:
    '''
    add_value_telecom_lists = model1_filter_data('spider_add_value_telecom_info_hz')
    industry_lists = model1_filter_data('spider_industry_information')
    industry_gov_lists = model1_filter_data('spider_industry_information_gov')

    p = add_value_telecom_lists + industry_lists + industry_gov_lists
    bloom = ScalableBloomFilter(initial_capacity=1000000,error_rate=0.001)
    for i in p:
        bloom.add(i)
    sum = []
    for company in domain_data:
        if company not in bloom:
            sum.append(company)
        else:
            print('具有ICp许可证',company)
    print('icp 域名备案 ,没有icp许可证的公司 ----- count:{}'.format(len(sum)))
    print(sum)
    for i in sum:
        medicine = Medicine(company_name=i)
        session.add(medicine)

    session.commit()
    session.close()

if __name__ == '__main__':
    db = pymysql.connect(host="192.168.2.99", user="root", password='BOOT-xwork1024', database="spider", port=3306)
    cursor = db.cursor()
    main()