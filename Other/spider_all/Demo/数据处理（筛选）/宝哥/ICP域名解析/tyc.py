'''
新增数据获取
'''
import time, re, json
import requests, pymysql
from lxml import etree
from sqlalchemy import Column, String, create_engine, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy import or_
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()


class Medicine(Base):
    # 表的名字:
    __tablename__ = 'icp_leads'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    company_name = Column(String(256))

    eg_capital = Column(String(256))
    social_staff_num = Column(String(256))
    business_scope = Column(String(256))
    company_org_type = Column(String(256))
    phone = Column(String(256))
    phone_source = Column(String(256))
    dns_provider = Column(String(256))
    gmt_created = Column(String(256))
    gmt_updated = Column(String(256))

# 初始化数据库连接:
engine = create_engine('mysql+pymysql://root:BOOT-xwork1024@192.168.2.97:3306/spider')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
# 创建session对象:
session = DBSession()


class Medicine_company_info(Base):
    # 表的名字:
    __tablename__ = 'company_info'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    company_name = Column(String(256))
    reg_money = Column(String(256))
    insurance_num = Column(String(256))
    business_project = Column(String(256))
    company_type = Column(String(256))

    mobile = Column(String(256))
    mobiles = Column(String(256))

# 创建session对象:
session_company_info = DBSession()

proxys = []

def dl():
    while 1:
        try:
            dlurl = 'http://dps.kdlapi.com/api/getdps/?orderid=922450652890692&num=1&pt=1&sep=1'
            resp = requests.get(dlurl).text
            break
        except Exception:
            pass
    # time.sleep(2)
    resp = re.sub(r'\n', '', resp)
    proxy = {
        'https': resp
    }
    proxys.append(proxy)
    print(proxys[-1])

dl()

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    'cookie':'TYCID=435e2b701e3f11eb93fd6b29e729c6c7; ssuid=8413289216; _ga=GA1.2.1495606244.1604454265; __insp_slim=1608615852663; __insp_wid=677961980; __insp_nv=true; __insp_targlpt=5LyB5Lia6K6k6K_BIC0g5aSp55y85p_l; __insp_targlpu=aHR0cHM6Ly93d3cudGlhbnlhbmNoYS5jb20vY2xhaW0vZW50cnkvMjk5MDIxNzc2NA%3D%3D; __insp_norec_sess=true; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2247184373%22%2C%22first_id%22%3A%22175cea83fe26fa-0ea05bfb98414a-930346c-2073600-175cea83fe3ccd%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%22175cea83fe26fa-0ea05bfb98414a-930346c-2073600-175cea83fe3ccd%22%7D; bannerFlag=true; aliyungf_tc=7f42d88aca6f51b07da5e4a99e5bf451c49194a888d620c847cc2826ce019e52; csrfToken=kVHgVd1shw-Hh0Rv_V5-BLtU; creditGuide=1; relatedHumanSearchGraphId=2964948266; relatedHumanSearchGraphId.sig=VPTfEo08VGIS9p7FAL_65-NzCjGHXU-7dSCHNN4Y0Uk; _gid=GA1.2.1046123012.1635233804; CT_TYCID=e486dcb8091c4b04ad2ca6e8b96ae1d1; RTYCID=119e6b49994645808280c6569ae311e3; searchSessionId=1635322171.75709589; cloud_token=ea69e276ae654560983b5cd3f4ff0e34; tyc-user-info={%22isExpired%22:%220%22%2C%22mobile%22:%2218069882328%22%2C%22state%22:%225%22%2C%22vipManager%22:%220%22}; tyc-user-info-save-time=1635322313961; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODA2OTg4MjMyOCIsImlhdCI6MTYzNTMyMjMxMywiZXhwIjoxNjY2ODU4MzEzfQ.k6rKgtFJBtHY_r5ejoJ2aDZGfVvL6sGaNGQq38SrANTmCXQxhvnIiw4gT9nF6ZIEf7smcqY66lW2Ia8Qerc39A; tyc-user-phone=%255B%252218069882328%2522%252C%2522188%25203707%25206355%2522%252C%2522153%25209583%25201367%2522%255D; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2247184373%22%2C%22first_id%22%3A%22175cea83fe26fa-0ea05bfb98414a-930346c-2073600-175cea83fe3ccd%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%22175cea83fe26fa-0ea05bfb98414a-930346c-2073600-175cea83fe3ccd%22%7D; acw_tc=76b20f8616353829519437886e30332b26eb16e5e9f21dfd26611d538374db; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1634088403; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1635382969; _gat_gtag_UA_123487620_1=1'
}


def main():
    companys = session.query(Medicine).filter(Medicine.phone == None).all()
    print(len(companys))

    for index, co in enumerate(companys):
        # if index<140:
        #     continue
        company = co.company_name
        if len(company) < 4:
            continue
        # company = '广西梧州市洛英格农业科技有限公司'
        id = co.id
        url = 'https://tax.tianyancha.com/search/{}'.format(company)
        while 1:
            time.sleep(1)
            try:
                response = requests.request(method='get', url=url, headers=headers, proxies=proxys[-1], timeout=8)
                # response = requests.request(method='get', url=url, headers=headers,  timeout=10)
                code = response.status_code
                res = response.text
                if '<title>天眼查校验</title>' not in res:
                    break
                print('search-------login')
                dl()
            except Exception as e:
                print(e)
                dl()
        # print(response)
        tree = etree.HTML(res)
        natural_person = tree.xpath('//div[@id="search_company_0"]/div[@class="content"]/div[1]')
        if len(natural_person) == 0:
            print(company, '跳过')
            continue
        name = "".join(tree.xpath('//div[@id="search"]/div[@class="content"]/div[1]//a/@title')).strip()
        if name != company:
            print(company, '跳过')
            continue

        url = "".join(tree.xpath('//div[@id="search"]/div[@class="content"]/div[1]//a/@href')).split('/')[-1]
        url = "https://www.tianyancha.com/company/{}".format(url)
        get_detail(url, company, id)

def request_data(url):
    time.sleep(1)
    while 1:
        try:
            # response = requests.request(method='get', url=url, headers=headers, timeout=10)
            response = requests.request(method='get', url=url, proxies=proxys[-1], headers=headers, timeout=10)
            code = response.status_code
            res = response.text

            if '<title>天眼查校验</title>' in res:
                print('detail-------login')
                dl()
                continue
            # print(res)
            tree = etree.HTML(res)
            natural_person = tree.xpath('//div[@id="company_web_top"]')
            if len(natural_person) == 0:
                # dl()
                continue
            break
        except Exception as e:
            print(e)
            dl()

    return tree

def get_detail(url, company, id):
    response = request_data(url)
    reg_capital = ''.join(
        response.xpath('//table[@class="table -striped-col -breakall"]/tbody/tr[3]/td[last()]//text()'))
    social_staff_num = ''.join(
        response.xpath('//table[@class="table -striped-col -breakall"]/tbody/tr[8]/td[2]//text()'))
    business_scope = ''.join(
        response.xpath('//table[@class="table -striped-col -breakall"]/tbody/tr[last()]/td[last()]//text()'))
    company_org_type = ''.join(
        response.xpath('//table[@class="table -striped-col -breakall"]/tbody/tr[7]/td[2]//text()'))
    phone = response.xpath(
        '//div[@class="in-block sup-ie-company-header-child-1 copy-info-box"]//span[@class="hidden"]//text()')
    phone_source = ''.join(phone)
    if len(phone) == 0:
        phone = ''
    else:
        phones = json.loads(phone[0])
        p = []
        for ph in phones:
            p.append(ph['phoneNumber'])
        phone = ','.join(list(set(p)))

    medi = session.query(Medicine).filter(Medicine.id == id).first()
    medi.reg_capital = reg_capital
    medi.social_staff_num = social_staff_num
    medi.company_org_type = company_org_type
    medi.phone = phone
    medi.phone_source = phone_source
    medi.business_scope = business_scope
    session.commit()
    print(company, reg_capital + '----', social_staff_num + '----', company_org_type + '----', phone + '----',
          phone_source, business_scope)

# 1.从数仓匹配company相等的。
def check_data():
    companys = session.query(Medicine).all()
    for q in companys:
        sum = []
        name = q.company_name

        company_info_data = session_company_info.query(Medicine_company_info).filter(Medicine_company_info.company_name == name).first()
        if company_info_data == None:
            continue
        mobile = company_info_data.mobile
        mobiles = company_info_data.mobiles
        if mobiles!=None:
            mobiles = json.loads(company_info_data.mobiles)
            sum = [m['pN'] for m in mobiles]

        reg_money = company_info_data.reg_money
        insurance_num = company_info_data.insurance_num
        business_project = company_info_data.business_project
        company_type = company_info_data.company_type

        if mobile != None:
            sum.append(mobile)
        sum = ','.join(list(set(sum)))

        icp = session.query(Medicine).filter(Medicine.company_name == name).all()
        for i in icp:
            i.eg_capital = reg_money
            i.social_staff_num = insurance_num
            i.business_scope = business_project
            i.company_org_type = company_type
            i.phone = sum
            if mobiles == None:
                i.phone_source = ''
            else:
                i.phone_source = str(mobiles)
            session.commit()
            print('over')
    session.close()
    session_company_info.close()



if __name__ == '__main__':
    main()
    # check_data()