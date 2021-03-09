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
handler1=logging.FileHandler("{}/构建空号过滤库.log".format(log_file_path))
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
    __tablename__ = 'Sheet1'

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

from xlrd import open_workbook
# 解析excle 到数据库
def parse_excle():
    workbook = open_workbook('注销模型-空号过滤.xlsx')  # 打开excel文件
    sheet2 = workbook.sheet_by_index(0)
    sum = []
    for i in range(1, sheet2.nrows):
        company_name = sheet2.cell(i, 1).value
        peple = sheet2.cell(i, 2).value
        tel = sheet2.cell(i, 3).value
        other_tel = sheet2.cell(i, 4).value
        medicine = Medicine(company_name=company_name,peple=peple,tel=tel,other_tel=other_tel)
        session.add(medicine)
    session.commit()

def main():
    # data = session.query(Medicine).all()
    data = session.query(Medicine).filter(Medicine.id > 3159).all()
    for index,d in enumerate(data):
        try:
            if index < 1946+20:
                continue
            id = d.id
            ph = d.ph
            time.sleep(1.5)
            url = 'https://himobile.market.alicloudapi.com/query?number={}'.format(ph)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
                'Authorization': 'APPCODE e0894501ef864abda581ee83234d49f9',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
            }
            res = requests.request(method='get', url=url, headers=headers).json()
            logger.info(res)
            co = res['ret']
            print('index:',index)
            if co == 200:
                code = res['data']['code']
                desc = res['data']['desc']
                if code == 1:
                    medicine = session.query(Medicine).filter(Medicine.id == id).first()
                    medicine.is_valid_type = desc
                    print('desc:{} , index:{}'.format(desc,index))
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