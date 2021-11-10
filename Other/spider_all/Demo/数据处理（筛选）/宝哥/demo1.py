import re
import time,json
import requests,pymysql
import base64
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pksc1_v1_5
from Crypto.PublicKey import RSA
from sqlalchemy import Column, String, create_engine,Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# 创建对象的基类:
Base = declarative_base()
# 定义User对象:

class Medicine(Base):
    # 表的名字:
    __tablename__ = 'data_wheel'
    id = Column(Integer(), primary_key=True,autoincrement=True)

    mobiles = Column(String(600))
    province = Column(String(64))
    city_code = Column(String(64))
    city = Column(String(64))

# 初始化数据库连接:
engine = create_engine('mysql+pymysql://root:BOOT-xwork1024@192.168.2.97:3306/spider')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
# 创建session对象:
session = DBSession()
'''
北京 重庆   杭州  武汉      苏州  南京  郑州    东莞   沈阳   青岛   佛山  
'''
def main():
    # data = session.query(Medicine).filter(Medicine.city_code == 'qingdao').all()
    data = session.query(Medicine).filter(Medicine.city == '沈阳市').all()
    print(len(data))
    sum = []
    for i in data:
        mobiles = i.mobiles
        if mobiles == None:
            continue
        phone = json.loads(mobiles)
        if len(phone)!=0:
            for p in phone:
                pho = p.get("pN").replace('"','')
                sum.append(pho)

        else:
            continue

    s = list(set(sum))
    s = [k for k in s if k.startswith('1') and len(k)==11 and '-' not in k]
    for ss in s:
        with open('沈阳.txt','a',encoding='utf-8')as fp:
            fp.write(ss + '\n')



def get_time(t):
    import time
    t = int(str(t)[:-3])
    time_local = time.localtime(t)
    dt = time.strftime("%Y-%m-%d", time_local)
    return dt


if __name__ == '__main__':
    main()













