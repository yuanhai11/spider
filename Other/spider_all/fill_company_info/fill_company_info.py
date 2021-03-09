import time,re,json
from lxml import etree
import requests,pymysql
from sqlalchemy import Column, String, create_engine, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# 创建对象的基类:
Base = declarative_base()
# 定义User对象:
class Medicine(Base):
    # 表的名字:
    __tablename__ = 'Sheet4'

    # 表的结构:
    id = Column(Integer(), primary_key=True, autoincrement=True)
    a = Column(String(256))
    b = Column(String(256))
    c = Column(String(256))
    d = Column(String(256))
    e = Column(String(256))
    f = Column(String(256))
    g = Column(String(256))
    h = Column(String(256))
    company_id = Column(String(256))
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

def select(company):
    db = pymysql.connect(user='root',password='BOOT-xwork1024',host='192.168.2.97',database='spider')
    cursor = db.cursor()
    sql = "select * from company_info where company_name = '{}'".format(company)
    cursor.execute(sql)
    return cursor.fetchone()

def select1(company_id):
    db = pymysql.connect(user='root',password='BOOT-xwork1024',host='192.168.2.97',database='spider')
    cursor = db.cursor()
    sql = "select * from company_business_risk where company_id = {}".format(company_id)
    cursor.execute(sql)
    return cursor.fetchall()

def main1():
    all_data = session.query(Medicine).all()
    print(len(all_data))
    for i in all_data:
        company_name = i.a
        data = select(company_name)
        if data:
            register_date = data[9]
            compan_type = data[15]
            compan_status = data[10]
            hy = data[17]
            print(register_date,compan_type,compan_status,hy)

            i.b = register_date
            i.c = compan_type
            i.d = compan_status
            i.h = hy
            session.commit()

        else:
            continue

def main2():
    all_data = session.query(Medicine).filter(Medicine.b == None).all()
    for i in all_data:
        company_id = i.company_id
        data = select1(company_id)
        if data:
            single = []
            for d in data:
                resons = d[4]
                single.append(resons)
            i.e = '是'
            i.f = str(single)
            session.commit()
            # exit()
        else:
            continue
def main3():
    all_data = session.query(Medicine).filter(Medicine.b == None).all()
    for index,data in enumerate(all_data):
        if index < 14:
            continue
        company_name = data.a
        print(company_name)
        head = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
            'cookie':'TYCID=435e2b701e3f11eb93fd6b29e729c6c7; ssuid=8413289216; _ga=GA1.2.1495606244.1604454265; aliyungf_tc=AQAAAInD9UpPvAUATvTrevDjN9EcHL76; csrfToken=afsKAVVvJskVjmuHrJtCT7FT; jsid=SEM-BAIDU-PZ-SY-20201109-BIAOTI; show_activity_id_6=6; bannerFlag=true; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1604454265,1604893628,1605234542; _gid=GA1.2.1957823725.1605234542; RTYCID=e34509ee7f3d4f26a9fd21534a060ad7; CT_TYCID=2a5f9587504b42189fbc7823d3acf47d; relatedHumanSearchGraphId=138976244; relatedHumanSearchGraphId.sig=DhJI6PmqLXfZylOhYEubWcZEfhO6J-V0dnucijWLHGM; tyc-user-info={%22claimEditPoint%22:%220%22%2C%22vipToMonth%22:%22false%22%2C%22explainPoint%22:%220%22%2C%22personalClaimType%22:%22none%22%2C%22integrity%22:%2210%25%22%2C%22state%22:%220%22%2C%22score%22:%2257%22%2C%22announcementPoint%22:%220%22%2C%22messageShowRedPoint%22:%220%22%2C%22bidSubscribe%22:%22-1%22%2C%22vipManager%22:%220%22%2C%22onum%22:%220%22%2C%22monitorUnreadCount%22:%220%22%2C%22discussCommendCount%22:%220%22%2C%22showPost%22:null%2C%22messageBubbleCount%22:%220%22%2C%22claimPoint%22:%220%22%2C%22token%22:%22eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODgzNzA3NjM1NSIsImlhdCI6MTYwNTI0OTU4NiwiZXhwIjoxNjM2Nzg1NTg2fQ.1MdQQv9rq6XCueICGPoFAPZcIgEWqs2qAM6XK9Gp9Cz7gKPGSxl7evG2xPYto5-YI8IRwc6ms5SO3JK7pr8-yQ%22%2C%22schoolAuthStatus%22:%222%22%2C%22userId%22:%2235705210%22%2C%22scoreUnit%22:%22%22%2C%22redPoint%22:%220%22%2C%22myTidings%22:%220%22%2C%22companyAuthStatus%22:%222%22%2C%22originalScore%22:%2257%22%2C%22myAnswerCount%22:%220%22%2C%22myQuestionCount%22:%220%22%2C%22signUp%22:%220%22%2C%22privateMessagePointWeb%22:%220%22%2C%22nickname%22:%22%E5%B8%8C%E6%8B%89%E7%91%9E%C2%B7%E8%BE%BE%E8%8A%99%22%2C%22privateMessagePoint%22:%220%22%2C%22bossStatus%22:%222%22%2C%22isClaim%22:%220%22%2C%22yellowDiamondEndTime%22:%220%22%2C%22yellowDiamondStatus%22:%22-1%22%2C%22pleaseAnswerCount%22:%220%22%2C%22bizCardUnread%22:%220%22%2C%22vnum%22:%220%22%2C%22mobile%22:%2218837076355%22}; tyc-user-info-save-time=1605249587905; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODgzNzA3NjM1NSIsImlhdCI6MTYwNTI0OTU4NiwiZXhwIjoxNjM2Nzg1NTg2fQ.1MdQQv9rq6XCueICGPoFAPZcIgEWqs2qAM6XK9Gp9Cz7gKPGSxl7evG2xPYto5-YI8IRwc6ms5SO3JK7pr8-yQ; tyc-user-phone=%255B%252218837076355%2522%255D; token=5f171c273fa7465687e016ea11950657; _utm=e0ab41abd86e42e48ac3f46de1c72813; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1605249590; cloud_token=8dc69e577bf34738aef7ebfb7c703bf4; cloud_utm=01cc7bb1e51e4161be0041c75f22b9cd; _gat_gtag_UA_123487620_1=1'
        }
        url = 'https://www.tianyancha.com/search?key={}'.format(company_name)
        detail_url = ""
        for i in range(20):
            try:
                res = requests.request(method='get', url=url, headers=head, proxies=proxys[-1],timeout=10).text
                tree = etree.HTML(res)

                n = tree.xpath('//div[@class="no-result-right"]')
                if len(n) != 0:
                    print(company_name,'查询不到数据')
                    break
                name = tree.xpath('//div[@class="header"]/a//text()')[0]
                if name == company_name:
                    detail_url = tree.xpath('//div[@class="header"]/a/@href')
                break
            except Exception as e:
                time.sleep(2)
                dl()
        print(detail_url)
        if detail_url == "":
            time.sleep(3)
            print(company_name,'contitue')
            continue
        else:
            time.sleep(3.5)
            detail_url = detail_url[0]
            for i in range(20):
                try:
                    text = requests.request(method='get', url=detail_url,  proxies=proxys[-1],headers=head, timeout=10).text
                    tree = etree.HTML(text)
                    element = tree.xpath('//table[@class="table -striped-col -breakall"]/tbody')
                    if len(element)!=0:
                        element = element[0]
                    else:
                        element = tree.xpath('//table[@class="table -striped-col"]/tbody')[0]
                    g = element.xpath('./tr[1]//span[@class="num-company-distributed num-toco"]/text()')[0]
                    b = element.xpath('./tr[2]/td[2]/text()')[0]
                    c = element.xpath('./tr[8]/td[2]/text()')[0]
                    d = element.xpath('./tr[1]/td[4]/text()')[0]
                    h = element.xpath('./tr[8]/td[4]/text()')[0]

                    single = []
                    element_list1 = tree.xpath('//div[@id="_container_abnormalPut"]//tbody/tr')
                    element_list2 = tree.xpath('//div[@id="_container_abnormalRemove"]//tbody/tr')
                    for gaga in element_list1:
                        reson = gaga.xpath('./td[4]/text()')[0]
                        single.append(reson)
                    for gaga1 in element_list2:
                        reson1 = gaga1.xpath('./td[3]/text()')[0]
                        single.append(reson1)

                    if single == []:
                        e = '否'
                        single = None
                    else:
                        e = '是'
                        single = str(single)
                    data.b = b
                    data.c = c
                    data.d = d
                    data.e = e
                    data.f = single
                    data.g = g
                    data.h = h

                    session.commit()
                    break
                except Exception:
                    time.sleep(2)
                    dl()
            print(company_name,b,c,d,e,single,g,h)
            time.sleep(10)

if __name__ == '__main__':
    dl()
    # main1()
    # main2()
    main3()