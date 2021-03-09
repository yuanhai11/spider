import time,re,json
import requests
from lxml import etree
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from sqlalchemy import Column, String, create_engine, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# 创建对象的基类:
Base = declarative_base()
# 定义User对象:
class Medicine(Base):
    # 表的名字:
    __tablename__ = 'spider_busi_range_standard_test'

    # 表的结构:
    id = Column(Integer(), primary_key=True, autoincrement=True)
    code = Column(String(256))
    busi_range_descrip = Column(String(256))
    economic_industry_classifi = Column(String(256))
    permit_situation = Column(String(256))
    scope_id = Column(String(256))
    ac = Column(String(256))
    description = Column(String(256))
    related_activity = Column(String(256))
    remarks = Column(String(256))
    related_matters = Column(String(256))
    related_lawer = Column(String(256))
    product_prohibit = Column(String(256))
    related_major = Column(String(256))
    related_feedback = Column(String(256))
    gmt_created = Column(String(256))
    gmt_updated = Column(String(256))
# 初始化数据库连接:
engine = create_engine('mysql+pymysql://root:BOOT-xwork1024@192.168.2.99:3306/spider')
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
        'http': resp
    }
    proxys.append(proxy)
    print(proxys[-1])

def main1():
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
    }
    city_code = ['110000', '120000', '130000', '140000', '150000', '210000', '220000', '230000', '310000', '320000', '330000',
     '340000', '350000', '360000', '370000', '410000', '420000', '430000', '440000', '450000', '460000', '500000',
     '510000', '520000', '530000', '540000', '610000', '620000', '630000', '640000', '650000', '670000', '810000',
     '820000']
    url = 'https://api.jyfwyun.com/cloud-service/cross/search'
    for cd in city_code:
        code_data = {
            "pageNum": 1, "ac": cd
        }
        response = ""
        for i in range(10):
            try:
                response = requests.post(url, json=code_data, headers=headers, proxies=proxys[-1])
                if response.status_code == 200:
                    response = response.json()
                    break
            except Exception:
                dl()
        all_pages = response.get('result').get('data').get('pages')
        time.sleep(1)
        for page in range(1,int(all_pages)+1):
            data = {
                "pageNum": page, "ac": cd
            }
            print(data)
            response_t = ""
            for i in range(10):
                try:
                    response_t = requests.post(url,json=data,headers=headers,proxies=proxys[-1])
                    if response_t.status_code == 200:
                        response_t = response_t.json()
                        break
                except Exception:
                    dl()

            data_lists = response_t.get('result').get('data').get('records')
            for d in data_lists:

                code = d.get('scopeCode')
                scopeId = d.get('scopeId')
                ac = cd
                busi_range_descrip = d.get('standardItem')
                economic_industry_classifi = d.get('gbName')
                type = d.get('permitType')
                permit_situation = ""
                if type==0:
                    permit_situation = '一般事项'
                elif type == 1:
                    permit_situation = '前置许可'
                elif type==2:
                    permit_situation = '后置许可'
                elif type == 3:
                    permit_situation = '许可事项'
                elif type == 4:
                    permit_situation = '一般事项（需备案）'
                times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

                ss = session.query(Medicine).filter(Medicine.code==code).first()
                if ss:
                    print('重复数据！！！')
                else:
                    print('第{}页 - 发现新数据：{}，{}，{}，{}'.format(page,code,busi_range_descrip,economic_industry_classifi,permit_situation))
                    zhilian = Medicine(code=code,busi_range_descrip=busi_range_descrip,economic_industry_classifi=economic_industry_classifi,permit_situation=permit_situation,
                                       scope_id=scopeId,ac=ac,gmt_created=times,gmt_updated=times)
                    session.add(zhilian)
                    # session.commit()

            time.sleep(1.5)
        time.sleep(1)
    session.commit()
    session.close()

def get_detail(scope_id,ac):
    time.sleep(2)
    head = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
    }
    data = {
        "scopeId":scope_id,
        "ac":ac
    }
    url = 'https://api.jyfwyun.com/cloud-service/cross/details'
    res = requests.request(method='post',url=url,json=data,headers=head,proxies=proxys[-1],timeout=10).json()
    return res
def main2():
    data = session.query(Medicine).filter(Medicine.permit_situation != '一般事项').all()
    print(len(data))

    for index,i in enumerate(data):
        print(index)
        if index < 231:
            continue
        code = i.code
        permit_situation = i.permit_situation
        scope_id = i.scope_id
        ac = i.ac
        detail = get_detail(scope_id,ac)

        description = detail['result']['description']
        includedItems = detail['result']['includedItems']
        remarks = detail['result']['remarks']
        others = detail['result']['otherInfo']

        related_matters_lists = others['busiApprovalList']
        related_matters = []
        for i in related_matters_lists:
            single = {}
            aName = i.get('aName')
            aTypeText = i.get('aTypeText')
            availableArea = i.get('availableArea')
            supervisorDep = i.get('supervisorDep')
            busiSection = i.get('busiSection')
            reformMode = i.get('reformMode')
            single['aName'] = aName
            single['aTypeText'] = aTypeText
            single['availableArea'] = availableArea
            single['supervisiorDep'] = supervisorDep
            single['busiSection'] = busiSection
            single['reformMode'] = reformMode
            related_matters.append(single)
        related_matters = str(related_matters)

        related_lawer = str(others['busiPolicyList'])
        product_prohibit = str(others['busiTraitList'])
        related_major = str(others['busiGuideList'])
        related_feedback = str([])

        medicine = session.query(Medicine).filter(Medicine.code==code).first()
        medicine.description = description
        medicine.related_activity = includedItems
        medicine.remarks = remarks
        medicine.related_matters = related_matters
        medicine.related_lawer = related_lawer
        medicine.product_prohibit = product_prohibit
        medicine.related_major = related_major
        medicine.related_feedback = related_feedback

        session.commit()
        # exit()

if __name__ == '__main__':
    dl()
    # main1()
    main2()
# 0(一般事项) 1(前置许可)  2(后置许可)  3(许可事项)  4(一般事项（需备案）)
# 可以获取到所有的全国所有区的ac 亦或者 获取全国省份的ac

