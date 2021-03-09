'''
全国：
'''
import re
import time
import requests

from sqlalchemy import Column, String, create_engine,Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# 创建对象的基类:
Base = declarative_base()
# 定义User对象:

class Medicine(Base):
    # 表的名字:
    __tablename__ = 'spider_qualification'
    id = Column(Integer(), primary_key=True,autoincrement=True)
    license_num = Column(String(256))
    company_name = Column(String(256))
    project_name = Column(String(256))
    cover_range = Column(String(256))
    valid_date = Column(String(256))
    invalid_date = Column(String(256))
    area = Column(Integer())

    gmt_created = Column(String(256))
    gmt_updated = Column(String(256))
    company_id = Column(String(256))

# 初始化数据库连接:
engine = create_engine('mysql+pymysql://root:BOOT-xwork1024@192.168.2.97:3306/spider')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
# 创建session对象:
session = DBSession()

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
        'https': resp
    }
    proxys.append(proxy)
    print(proxys[-1])
dl()


def main():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
    }
    url = 'https://ythzxfw.miit.gov.cn/user-center/tbAppSearch/selectResult'
    for page in range(90,4414):
        data = {
            'categoryId': "162",
            'currentPage': page,
            'pageSize': 5,
            'searchContent': ""
        }
        response = ""
        while 1:
            try:
                time.sleep(0.6)
                response = requests.request(method='post', url=url, headers=headers,proxies=proxys[-1], json=data, timeout=10)
                if response.status_code == 200:
                    response = response.json()
                    code = response['code']
                    if code ==200:
                        print('获取信息成功！！！')
                        print('break！！！')
                        break
            except Exception as e:
                print(e)
                dl()
        data = response['params']['tbAppArticle']['list']
        for d in data:
            license_num = d['articleField01']
            company_name = d['articleField02']
            project_name = d['articleField03']
            cover_range = d['articleField04']
            invalid_date = d['articleField05']
            times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            if invalid_date == "":
                invalid_date = None
            print('数据在第',page,'页！',company_name,license_num,project_name,cover_range,invalid_date)
            medicine = Medicine(license_num=license_num,company_name=company_name,project_name=project_name,cover_range=cover_range,invalid_date=invalid_date
                                ,area=36,
                                gmt_created=times,gmt_updated=times,
                                )
            session.add(medicine)
        session.commit()

if __name__ == '__main__':
    main()
