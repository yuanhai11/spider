import pymysql
from sqlalchemy import Column, String, create_engine, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# 创建对象的基类:
Base = declarative_base()
# 定义User对象:
class Medicine(Base):
    # 表的名字:
    __tablename__ = 'spider_model2'

    # 表的结构:
    id = Column(Integer(), primary_key=True, autoincrement=True)
    permit_number = Column(String(256))
    company_name = Column(String(256))
    busi_range = Column(String(256))
    need_permit = Column(String(256))
    certificate_invalid_date = Column(String(256))
    is_new_data = Column(String(256))
    mobile = Column(String(256))
    other_mobiles = Column(String(256))

    company_id = Column(String(256))
# 初始化数据库连接:
engine = create_engine('mysql+pymysql://root:BOOT-xwork1024@192.168.2.99:3306/spider')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
# 创建session对象:
session = DBSession()

def get_table_filter_data(table):
    sql = "select company_name,permit_number from {}".format(table)
    cursor.execute(sql)
    data1 = cursor.fetchall()
    data2 = {}
    for company,permit in data1:
        data2[company] = permit
    keys = list(data2.keys())

    return [data2,keys]

def main():
    '''
    经营范围：基础电信业务
    :return:
    '''
    sql = "select permit_number,company_name,busi_range,certificate_invalid_date,is_new_data,company_id,mobile,other_mobiles from spider_add_value_telecom_info_hz"
    cursor.execute(sql)
    data = cursor.fetchall()
    data = [[i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7]] for i in data]

    industry_data = get_table_filter_data('spider_industry_information')[0]
    industry_keys = get_table_filter_data('spider_industry_information')[1]

    industry_gov_data = get_table_filter_data('spider_industry_information_gov')[0]
    industry_gov_keys = get_table_filter_data('spider_industry_information_gov')[1]
    for i in data:
        single = []
        permit_lists = []
        if i[2] == None:
            continue
        if '基础电信业务' in i[2]:
            single.append('A1,A2')
        if '第一类增值电信业务' in i[2]:
            single.append('B1')
        if '第二类增值电信业务' in i[2]:
            single.append('B2')
        if '互联网新闻信息服务' in i[2]:
            single.append('B2')
        if '药品互联网信息服务' in i[2]:
            single.append('B2')
        if '互联网信息服务' in i[2]:
            single.append('B2')
        if '医疗器械互联网信息服务' in i[2]:
            single.append('B2')
        if '呼叫中心' in i[2]:
            single.append('B2')
        single = list(set(single))

        permit_lists.append(i[0])
        if i[1] in industry_keys:
            print('公司在工信部查到，',i[1])
            permit_lists.append(industry_data[i[1]])

        if i[1] in industry_gov_keys:
            print('公司在国家工信部查到，', i[1])
            permit_lists.append(industry_gov_data[i[1]])

        permit_lists = list(set(permit_lists))

        print(permit_lists,i[1],i[2],single)
        medicine = Medicine(permit_number=str(permit_lists),company_name=str(i[1]),busi_range=str(i[2]),need_permit=str(single),certificate_invalid_date=i[3],is_new_data=i[4],
                            company_id=i[5],mobile=i[6],other_mobiles=i[7])
        session.add(medicine)

    session.commit()
    session.close()


if __name__ == '__main__':
    db = pymysql.connect(host="192.168.2.99", user="root", password='BOOT-xwork1024', database="spider", port=3306)
    cursor = db.cursor()
    main()