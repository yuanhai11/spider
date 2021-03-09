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
    risk_in = Column(String(256))
    risk_out = Column(String(256))
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
    time.sleep(3)
    resp = re.sub(r'\n', '', resp)
    proxy = {
        'https': resp
    }
    proxys.append(proxy)
    print(proxys[-1])
dl()

def main3():
    all_data = []
    data = session.query(Medicine).limit(50000).all()
    for i in data:
        if i.is_have_year_report and not i.year_report_busi_status:
            company_name = i.company_name
            year_report_url = eval(i.year_report_url)
            year_report_url.append(company_name)

            all_data.append(year_report_url)

    print('总数：',len(all_data))
    start = 800
    end = 1600
    all_data = all_data[start:end]
    print('本次执行数量：',len(all_data))

    for index,report_urls in enumerate(all_data):
        company_name = report_urls.pop()
        try:
            # if index < 2467-start:
            #     continue
            head = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
                # 'cookie':'TYCID=435e2b701e3f11eb93fd6b29e729c6c7; ssuid=8413289216; _ga=GA1.2.1495606244.1604454265; jsid=SEM-BAIDU-PZ-SY-20201109-BIAOTI; tyc-user-phone=%255B%252218837076355%2522%255D; __insp_slim=1606196162867; __insp_wid=677961980; __insp_nv=true; __insp_targlpt=5LyB5Lia6K6k6K_BIC0g5aSp55y85p_l; __insp_targlpu=aHR0cHM6Ly93d3cudGlhbnlhbmNoYS5jb20vY2xhaW0vZW50cnkvNDAzNDM3NDI5NT9mcm9tPWYz; __insp_norec_sess=true; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22175cea83fe26fa-0ea05bfb98414a-930346c-2073600-175cea83fe3ccd%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%22175cea83fe26fa-0ea05bfb98414a-930346c-2073600-175cea83fe3ccd%22%7D; bannerFlag=true; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1606271066,1606367491,1606440321,1606485479; tyc-user-info-save-time=1606697802233; tyc-user-info={%22claimEditPoint%22:%220%22%2C%22vipToMonth%22:%22false%22%2C%22explainPoint%22:%220%22%2C%22personalClaimType%22:%22none%22%2C%22integrity%22:%2210%25%22%2C%22state%22:%220%22%2C%22score%22:%2275%22%2C%22announcementPoint%22:%220%22%2C%22messageShowRedPoint%22:%220%22%2C%22bidSubscribe%22:%22-1%22%2C%22vipManager%22:%220%22%2C%22onum%22:%220%22%2C%22monitorUnreadCount%22:%220%22%2C%22discussCommendCount%22:%220%22%2C%22showPost%22:null%2C%22messageBubbleCount%22:%220%22%2C%22claimPoint%22:%220%22%2C%22token%22:%22eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODgzNzA3NjM1NSIsImlhdCI6MTYwNjY5NzgwMCwiZXhwIjoxNjM4MjMzODAwfQ.RqZkrx3pFnlZ82_MsbiZ2ePJdtyZWo180EhXWgfUaLk1XvN-Znv42OrBlBQJV0t4CLNhzrAwstbe4B-VnupNUA%22%2C%22schoolAuthStatus%22:%222%22%2C%22userId%22:%2235705210%22%2C%22scoreUnit%22:%22%22%2C%22redPoint%22:%220%22%2C%22myTidings%22:%220%22%2C%22companyAuthStatus%22:%222%22%2C%22originalScore%22:%2275%22%2C%22myAnswerCount%22:%220%22%2C%22myQuestionCount%22:%220%22%2C%22signUp%22:%220%22%2C%22privateMessagePointWeb%22:%220%22%2C%22nickname%22:%22%E5%B8%8C%E6%8B%89%E7%91%9E%C2%B7%E8%BE%BE%E8%8A%99%22%2C%22privateMessagePoint%22:%220%22%2C%22bossStatus%22:%222%22%2C%22isClaim%22:%220%22%2C%22yellowDiamondEndTime%22:%220%22%2C%22yellowDiamondStatus%22:%22-1%22%2C%22pleaseAnswerCount%22:%220%22%2C%22bizCardUnread%22:%220%22%2C%22vnum%22:%220%22%2C%22mobile%22:%2218837076355%22%2C%22riskManagement%22:{%22servicePhone%22:null%2C%22mobile%22:18837076355%2C%22title%22:null%2C%22currentStatus%22:null%2C%22lastStatus%22:null%2C%22quickReturn%22:false%2C%22oldVersionMessage%22:null%2C%22riskMessage%22:null}}; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODgzNzA3NjM1NSIsImlhdCI6MTYwNjY5NzgwMCwiZXhwIjoxNjM4MjMzODAwfQ.RqZkrx3pFnlZ82_MsbiZ2ePJdtyZWo180EhXWgfUaLk1XvN-Znv42OrBlBQJV0t4CLNhzrAwstbe4B-VnupNUA; csrfToken=kPPzpX88n8s1Ul6WLmg_RE0u; Hm_lvt_4b2d8422d27558696ac691372d8e6e98=1606446680,1606719440; RTYCID=1c77d1d5a3094fe5877aa36047a30652; _gid=GA1.2.2106028816.1606870618; CT_TYCID=93cf7f0c22d841c9ab7507d657cbe792; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1606892412; cloud_token=e6bd9b1679dc4365af68a7d27f4e191a; Hm_lpvt_4b2d8422d27558696ac691372d8e6e98=1606892425'
            }
            medicine = session.query(Medicine).filter(Medicine.company_name == company_name).first()

            for i,url in enumerate(report_urls):
                time.sleep(0.5)
                data = ''
                while 1:
                    try:
                        data = requests.request(method='get', url=url,proxies=proxys[-1],headers=head,timeout=10).text
                        year = re.findall(r'<title>.*?_(.*?)年报_企业年报查询 - 天眼查'.format(company_name), data, re.S)[0]

                        break
                    except Exception as e:
                        print(e)
                        dl()
                        continue

                year = re.findall(r'<title>.*?_(.*?)年报_企业年报查询 - 天眼查'.format(company_name), data, re.S)[0]

                if i ==0:
                    busi_status = re.findall(r'<td>企业经营状态</td><td>(.*?)</td>'.format(), data, re.S)[0]
                    medicine.year_report_busi_status = year + '：' + busi_status

                insurance_count = re.findall(r'城镇职工基本养老保险</td><td .*?">(.*?)</td>'.format(), data, re.S)
                if len(insurance_count) == 0:
                    insurance_count = '无社保信息'
                else:
                    insurance_count = insurance_count[0]

                if '2019' == year:
                    medicine.nineteen_insurance_count = insurance_count
                elif '2018' == year:
                    medicine.eighteen_insurance_count = insurance_count
                elif '2017' == year:
                    medicine.seventeen_insurance_count = insurance_count

                print('---公司：{}----年报:{}----社保人数：{}'.format(company_name,year,insurance_count))

            session.commit()
            print('**********************************************************************************')
            time.sleep(1.5)
        except Exception as e:
            continue
if __name__ == '__main__':
    main3()

    # proxys1 = []
    # proxys2 = []
    # proxys3 = []
    # proxys4 = []
    # # t1 = threading.Thread(target=main3,args=(proxys1,9000,9100))
    # # t2 = threading.Thread(target=main3,args=(proxys2,9100,9200))
    # # t3 = threading.Thread(target=main3,args=(proxys3,9200,9300))
    # # t4 = threading.Thread(target=main3,args=(proxys4,9300,9400))
    # t1 = threading.Thread(target=main3,args=(proxys1,0,2))
    # t2 = threading.Thread(target=main3,args=(proxys2,2,4))
    # t3 = threading.Thread(target=main3,args=(proxys3,4,6))
    # t4 = threading.Thread(target=main3,args=(proxys4,6,9))
    # t1.start()
    # time.sleep(1)
    # t2.start()
    # time.sleep(1)
    # t3.start()
    # time.sleep(1)
    # t4.start()
    # exe_2 = ThreadPoolExecutor(max_workers=4)
    # tasks = []
    # for i in range(4):
    #     tasks.append(exe_2.submit(main3,0,2))
    # for task in tasks:
    #     print(task.done())