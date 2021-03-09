import requests,pymysql,time
from sqlalchemy import Column, String, create_engine, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import logging
import time,os
import logging.handlers
#初始化设置
logging.basicConfig(level = logging.INFO,format='%(asctime)s|%(name)-12s: %(levelname)-8s %(message)s')
#创建
logger = logging.getLogger("spider_industry_information")
logger.setLevel(logging.INFO)

log_file_path = os.path.join(os.path.abspath('.'),'log')
if not os.path.exists(log_file_path):
    os.mkdir(log_file_path)

#创建handler
handler1=logging.FileHandler("{}/空号过滤3.log".format(log_file_path))
handler1.setLevel(logging.INFO)
formatter=logging.Formatter('%(asctime)s|%(name)-12s+ %(levelname)-8s++%(message)s')
handler1.setFormatter(formatter)
handler2=logging.StreamHandler()
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
    __tablename__ = 'Sheet4'

    # 表的结构:
    id = Column(Integer(), primary_key=True, autoincrement=True)
    ph = Column(String(256))
    is_valid = Column(Integer())
    is_valid_type = Column(String(256))

# 初始化数据库连接:
engine = create_engine('mysql+pymysql://root:BOOT-xwork1024@192.168.2.97:3306/spider')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
# 创建session对象:
session = DBSession()
proxys = []
def dl():
    import re
    dlurl = 'http://api.goubanjia.com/dynamic/get/d490a5d4debefc8980ae6ee4c4148552.html?sep=3'
    resp = requests.get(dlurl).text
    time.sleep(2)
    resp = re.sub(r'\n', '', resp)
    proxy = {
        'https': resp
    }
    proxys.append(proxy)
    print(proxys[-1])
dl()
def main():
    data = session.query(Medicine).all()
    for index,d in enumerate(data):
        try:
            if index < 1026:
                continue
            id = d.id
            ph = d.ph
            time.sleep(1)
            url = 'https://himobile.market.alicloudapi.com/query?number={}'.format(ph)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
                'Authorization': 'APPCODE e0894501ef864abda581ee83234d49f9',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
            }
            while 1:
                try:
                    res = requests.request(method='get', url=url, headers=headers,proxies=proxys[-1],timeout=8).json()
                    break
                except Exception:
                    dl()
                    continue
            logger.info(res)
            co = res['ret']
            print('index:',index)
            if co == 200:
                code = res['data']['code']
                desc = res['data']['desc']
                if code == 1:
                    medicine = session.query(Medicine).filter(Medicine.id == id).first()
                    medicine.is_valid_type = desc
                    print('desc:{} , index:{}'.format(desc, index))
                    session.commit()

                elif code == 2:
                    medicine = session.query(Medicine).filter(Medicine.id == id).first()
                    medicine.is_valid_type = desc

                    print('desc:{} , index:{}'.format(desc, index))
                    session.commit()
                elif code == 5:
                    medicine = session.query(Medicine).filter(Medicine.id == id).first()
                    medicine.is_valid_type = desc

                    print('desc:{} , index:{}'.format(desc, index))
                    session.commit()

                elif code == 4:
                    medicine = session.query(Medicine).filter(Medicine.id == id).first()
                    medicine.is_valid_type = desc

                    print('desc:{} , index:{}'.format(desc, index))
                    session.commit()

        except Exception as e:
            print(e)
            time.sleep(3)
            continue

if __name__ == '__main__':
    main()