import re
import time
import requests
import pymysql
from getCompanyId.get_company_id import get_company_id
from sqlalchemy import Column, String, create_engine,Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# 创建对象的基类:
Base = declarative_base()
# 定义User对象:

class Medicine(Base):
    # 表的名字:
    __tablename__ = 'spider_qualification'

    # 表的结构:
    id = Column(Integer(), primary_key=True,autoincrement=True)
    company_name = Column(String(256))
    project_name = Column(String(256))
    license_name = Column(String(256))

# 初始化数据库连接:
engine = create_engine('mysql+pymysql://root:BOOT-xwork1024@192.168.2.97:3306/spider')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
# 创建session对象:
session = DBSession()
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
}
def main():
    data = session.query(Medicine).filter(Medicine.id<100028).all()
    for index,d in enumerate(data):
        if index < 2000:
            continue
        sum = []
        id = d.id
        company_name = d.company_name
        project_name = d.project_name
        license_name = d.license_name
        if '码号' == project_name:
            print('码号，过')
            continue
        if '信息服务业务（仅限互联网信息服务）' in project_name:
            sum.append('ICP许可证')
        if '在线数据处理与交易处理业务' in project_name:
            sum.append('EDI许可证')
        if '互联网数据中心业务（仅限互联网资源协作服务） ' in project_name or '互联网数据中心业务（不含互联网资源协作服务）' in project_name:
            sum.append('IDC许可证')
        if '内容分发网络业务' in project_name:
            sum.append('CDN许可证')
        if '互联网接入服务业务（不含网站接入）' in project_name or '互联网接入服务业务（含网站接入）' in project_name:
            sum.append('ISP许可证')
        if '信息服务业务（不含互联网信息服务）' in project_name:
            sum.append('SP许可证')
        print(sum)
        medicine = session.query(Medicine).filter(Medicine.id==id).first()
        medicine.license_name = str(sum)
        session.commit()

if __name__ == '__main__':
    main()
