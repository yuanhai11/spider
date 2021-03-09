import requests,pymysql,time
from sqlalchemy import Column, String, create_engine, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class Medicine(Base):
    # 表的名字:
    __tablename__ = 'spider_number_filter'
    id = Column(Integer(), primary_key=True,autoincrement=True)
    company_name = Column(String(256))
    phone = Column(String(256))
    filter_result = Column(String(256))

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

def updated():
    db = pymysql.connect(host="192.168.2.97", user="root", password='BOOT-xwork1024', database="spider", port=3306)
    cursor = db.cursor()
    sql = "select phone from spider_number_database"
    cursor.execute(sql)
    db_data = cursor.fetchall()
    data = [i[0] for i in db_data]
    from pybloom_live import ScalableBloomFilter
    bloom = ScalableBloomFilter(initial_capacity=100000, error_rate=0.001)
    for bl in data:
        bloom.add(bl)
    return bloom

def main():
    bloom = updated()
    data = session.query(Medicine).all()
    for d in data:
        phone = d.phone
        company_name = d.company_name
        filter_result = d.filter_result
        if phone not in bloom:
            me = Medicine_database(company_name=company_name,phone=phone,result=filter_result)
            print(company_name)
            session.add(me)

    session.commit()

if __name__ == '__main__':
    main()
