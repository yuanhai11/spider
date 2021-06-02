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
    __tablename__ = 'revoke_model'

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
    time.sleep(2)
    resp = re.sub(r'\n', '', resp)
    proxy = {
        'https': resp
    }
    proxys.append(proxy)
    print(proxys[-1])
dl()

def main3():
    start = 40000
    end = 45000
    with open('hz_data_50000.json', 'r', encoding='utf-8')as fp:
        all_data = json.loads(fp.read())[start:end]
    for index,company_name in enumerate(all_data):
            head = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
                # 'cookie': 'TYCID=435e2b701e3f11eb93fd6b29e729c6c7; ssuid=8413289216; _ga=GA1.2.1495606244.1604454265; __insp_slim=1608615852663; __insp_wid=677961980; __insp_nv=true; __insp_targlpt=5LyB5Lia6K6k6K_BIC0g5aSp55y85p_l; __insp_targlpu=aHR0cHM6Ly93d3cudGlhbnlhbmNoYS5jb20vY2xhaW0vZW50cnkvMjk5MDIxNzc2NA%3D%3D; __insp_norec_sess=true; jsid=SEO-BAIDU-ALL-SY-000001; creditGuide=1; bannerFlag=true; _gid=GA1.2.436903525.1620699332; aliyungf_tc=3443f64845af647fae5240dd087c3ce367a80d76f0485a200d7fa5e91c01f518; csrfToken=gRDH2UvaJ7mjUM88SHcK-7cz; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1619400932,1619597722,1620699336; CT_TYCID=e6ec332b3b5c47d2849f1b41ef6085e5; RTYCID=012c0d988f7a434fa5512883f7b2efeb; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2247184373%22%2C%22first_id%22%3A%22175cea83fe26fa-0ea05bfb98414a-930346c-2073600-175cea83fe3ccd%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%22175cea83fe26fa-0ea05bfb98414a-930346c-2073600-175cea83fe3ccd%22%7D; tyc-user-info={%22claimEditPoint%22:%220%22%2C%22explainPoint%22:%220%22%2C%22vipToMonth%22:%22false%22%2C%22personalClaimType%22:%22none%22%2C%22integrity%22:%2220%25%22%2C%22state%22:%225%22%2C%22score%22:%221748%22%2C%22anonymityLogo%22:%22https://static.tianyancha.com/design/anonymity/anonymity2.png%22%2C%22announcementPoint%22:%220%22%2C%22surday%22:%22246%22%2C%22messageShowRedPoint%22:%220%22%2C%22vipManager%22:%220%22%2C%22monitorUnreadCount%22:%220%22%2C%22discussCommendCount%22:%221%22%2C%22onum%22:%221242%22%2C%22showPost%22:null%2C%22showAnonymityName%22:%22%E5%8C%BF%E5%90%8D%E7%94%A8%E6%88%B72cff9f5%22%2C%22messageBubbleCount%22:%220%22%2C%22claimPoint%22:%220%22%2C%22token%22:%22eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODg2ODcwNzU2MSIsImlhdCI6MTYyMDcwNTg5MiwiZXhwIjoxNjUyMjQxODkyfQ.OriIRZHX4VBtEamHy6wLW3jU0kqdo1745r7CdHA3lVsqLQTwtNEH6Wm31dyEs3y8yVH1UwnEae7QhU7L93L4Iw%22%2C%22schoolAuthStatus%22:%222%22%2C%22userId%22:%2247184373%22%2C%22vipToTime%22:%221641887594846%22%2C%22scoreUnit%22:%22%22%2C%22redPoint%22:%220%22%2C%22myTidings%22:%220%22%2C%22companyAuthStatus%22:%222%22%2C%22originalScore%22:%221748%22%2C%22myAnswerCount%22:%220%22%2C%22myQuestionCount%22:%220%22%2C%22signUp%22:%220%22%2C%22realBossStatus%22:%222%22%2C%22privateMessagePointWeb%22:%220%22%2C%22nickname%22:%22%E6%9D%8E%E5%B2%A9%22%2C%22headPicUrl%22:%22https://cdn.tianyancha.com/design/avatar/v3/man6.png%22%2C%22privateMessagePoint%22:%220%22%2C%22bossStatus%22:%222%22%2C%22isClaim%22:%220%22%2C%22yellowDiamondEndTime%22:%220%22%2C%22isExpired%22:%220%22%2C%22yellowDiamondStatus%22:%22-1%22%2C%22pleaseAnswerCount%22:%220%22%2C%22bizCardUnread%22:%220%22%2C%22vnum%22:%2220%22%2C%22mobile%22:%2218868707561%22%2C%22riskManagement%22:{%22servicePhone%22:null%2C%22mobile%22:18868707561%2C%22title%22:null%2C%22currentStatus%22:null%2C%22lastStatus%22:null%2C%22quickReturn%22:false%2C%22oldVersionMessage%22:null%2C%22riskMessage%22:null}}; tyc-user-info-save-time=1620705893261; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODg2ODcwNzU2MSIsImlhdCI6MTYyMDcwNTg5MiwiZXhwIjoxNjUyMjQxODkyfQ.OriIRZHX4VBtEamHy6wLW3jU0kqdo1745r7CdHA3lVsqLQTwtNEH6Wm31dyEs3y8yVH1UwnEae7QhU7L93L4Iw; tyc-user-phone=%255B%252218868707561%2522%252C%2522188%25203707%25206355%2522%255D; cloud_token=425471dbeeba4278ba37bca54a64c854; searchSessionId=1620705903.65769563; relatedHumanSearchGraphId=3006811449; relatedHumanSearchGraphId.sig=tWonrOcR3-s6D4_uu4Jv9Ie9yejlKqpn3xlpM_asW3E; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1620705943'
            }
            url = 'https://www.tianyancha.com/search?key={}'.format(company_name)
            print(url)
            while 1:
                try:
                    res = requests.request(method='get', url=url,proxies=proxys[-1],headers=head,timeout=10).text

                    print(res)
                    break
                except Exception as e:
                    print(e)
                    dl()


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