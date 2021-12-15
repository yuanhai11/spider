import time, re, json
from lxml import etree
from sqlalchemy import Column, String, create_engine, Integer,and_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import requests
import execjs

# 加入pywintypes，打包成功
import pywintypes
import win32api
import win32con
import win32gui
# 创建对象的基类:
Base = declarative_base()


class Medicine(Base):
    # 表的名字:
    __tablename__ = 'icp_leads'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    site_domain = Column(String(256))
    company_name = Column(String(256))
    main_page = Column(String(256))
    site_license = Column(String(256))
    site_name = Column(String(256))

    company_type = Column(String(256))
    phone = Column(String(256))
    verify_time = Column(String(256))
    dns_provider = Column(String(256))

    eg_capital = Column(String(256))
    social_staff_num = Column(String(256))
    business_scope = Column(String(256))
    company_org_type = Column(String(256))
    phone_source = Column(String(256))
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

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    'cookie':'TYCID=435e2b701e3f11eb93fd6b29e729c6c7; ssuid=8413289216; _ga=GA1.2.1495606244.1604454265; __insp_slim=1608615852663; __insp_wid=677961980; __insp_nv=true; __insp_targlpt=5LyB5Lia6K6k6K_BIC0g5aSp55y85p_l; __insp_targlpu=aHR0cHM6Ly93d3cudGlhbnlhbmNoYS5jb20vY2xhaW0vZW50cnkvMjk5MDIxNzc2NA%3D%3D; __insp_norec_sess=true; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2247184373%22%2C%22first_id%22%3A%22175cea83fe26fa-0ea05bfb98414a-930346c-2073600-175cea83fe3ccd%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%22175cea83fe26fa-0ea05bfb98414a-930346c-2073600-175cea83fe3ccd%22%7D; creditGuide=1; tyc-user-phone=%255B%252218069882328%2522%252C%2522188%25203707%25206355%2522%252C%2522153%25209583%25201367%2522%255D; _bl_uid=p8kXdv0pakeq4hbakedphdz4ywO0; aliyungf_tc=d09840a7aa56823825fb2d9acb3798687b73faa261f70e063a37140d2fc37431; csrfToken=jAoic4Rp0MKRm9vZQ8pY39BK; bannerFlag=true; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1634088403,1635758009; _gid=GA1.2.823123114.1635758009; RTYCID=fc26b95c5e7e4397a9a535e7da3cd1b6; CT_TYCID=05b5a96a365d4f70919b974d8fd951f1; acw_tc=781bad4216358223650144573e50ddab76c69f0be2333352ba75583ec037ec; acw_sc__v2=6180ab1dcde77a65556c2d575628714e095db13d; tyc-user-info-save-time=1635822374934; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODA2OTg4MjMyOCIsImlhdCI6MTYzNTgyMjM3MywiZXhwIjoxNjY3MzU4MzczfQ.kom1B9MFkpyoRdN2s_HCshf35IZAbRp-N5BdlumjhJNVSWNeWmUofydTHUVAZcn5IDnJwzvjD9W8HbH6_DASEA; tyc-user-info={%22isExpired%22:%220%22%2C%22mobile%22:%2218069882328%22%2C%22state%22:%225%22%2C%22vipManager%22:%220%22}; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2247184373%22%2C%22first_id%22%3A%22175cea83fe26fa-0ea05bfb98414a-930346c-2073600-175cea83fe3ccd%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%22175cea83fe26fa-0ea05bfb98414a-930346c-2073600-175cea83fe3ccd%22%7D; cloud_token=fd05a8490c884b78b735f7266d6930e9; cloud_utm=d530866748f84852a8e42525d5b7310b; relatedHumanSearchGraphId=3486767098; relatedHumanSearchGraphId.sig=JI8LutPeOvRWp3-mOuJV8Af-coS9vBZzW_VGXbMDdNw; searchSessionId=1635822806.39474733; _gat_gtag_UA_123487620_1=1; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1635822807'
}
main_company_list = []

def main():
    dl()
    companys = session.query(Medicine).filter(and_(Medicine.phone == None ,Medicine.eg_capital == None, Medicine.verify_time == local_time , Medicine.company_type != '个人')).all()
    print(len(companys))
    for index, co in enumerate(companys):
        # if index<12:
        #     continue
        company = co.company_name
        company_copy = company.replace('(','').replace(')','').replace('）','').replace('（','')
        if company in main_company_list:
            continue
        # if len(company) < 4:
        #     continue
        # company = '广西梧州市洛英格农业科技有限公司'
        id = co.id
        url = 'https://www.tianyancha.com/search?key={}'.format(company)
        while 1:
            time.sleep(1.5)
            try:
                response = requests.request(method='get', url=url, headers=headers, proxies=proxys[-1], timeout=8)
                # response = requests.request(method='get', url=url, headers=headers,  timeout=10)
                code = response.status_code
                res = response.text
                time.sleep(1.5)
                # print(res)
                # exit()
                if '<title>天眼查校验</title>' not in res:
                    break
                print('search-------login')
                time.sleep(10)
                dl()
            except Exception as e:
                print(e)
                dl()

        tree = etree.HTML(res)
        natural_person = tree.xpath('//div[@id="search_company_0"]')
        if len(natural_person) == 0:
            print(company, '跳过')
            continue
        name = "".join(tree.xpath('//div[@id="search_company_0"]//div[@class="content"]/div[1]/a//text()')).strip().replace('(','').replace(')','').replace('）','').replace('（','')
        if name != company_copy:
            print(company, '跳过')
            continue

        url = "".join(tree.xpath('//div[@id="search_company_0"]//div[@class="content"]/div[1]/a/@href')).split('/')[-1]
        url = "https://www.tianyancha.com/company/{}".format(url)
        get_detail(url, company, id)


def request_data(url):
    while 1:
        try:
            time.sleep(1)
            # response = requests.request(method='get', url=url, headers=headers, timeout=10)
            response = requests.request(method='get', url=url, proxies=proxys[-1], headers=headers, timeout=10)
            code = response.status_code
            res = response.text

            if '<title>天眼查校验</title>' in res:
                print('detail-------login')
                time.sleep(10)
                dl()
                continue
            # print(res)
            tree = etree.HTML(res)
            natural_person = tree.xpath('//div[@id="company_web_top"]')
            if len(natural_person) == 0:
                dl()
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

    medis = session.query(Medicine).filter(Medicine.company_name == company).all()
    for medi in medis:
        medi.eg_capital = reg_capital
        medi.social_staff_num = social_staff_num
        medi.company_org_type = company_org_type
        medi.phone = phone
        medi.phone_source = phone_source
        medi.business_scope = business_scope
        session.commit()
        print(company, reg_capital + '----', social_staff_num + '----', company_org_type + '----', phone + '----',
              phone_source, business_scope)

    main_company_list.append(company)


# 1.从数仓匹配company相等的。
def check_data():
    company_s=[]
    companys = session.query(Medicine).filter(Medicine.verify_time == local_time).all()
    for q in companys:
        sum = []
        name = q.company_name
        if name in company_s:
            continue
        company_info_data = session_company_info.query(Medicine_company_info).filter(
            Medicine_company_info.company_name == name).first()
        if company_info_data == None:
            continue
        mobile = company_info_data.mobile
        mobiles = company_info_data.mobiles
        if mobiles != None:
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
            print(name,'over')
        company_s.append(name)

    session.commit()
    session.close()
    session_company_info.close()


'''
每天爬取的数据，以时间为分割，每天只能执行一次，
'''
def icp_lists():
    head = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'cookie':'toolbox_words=www.meshplus.cn; cz_statistics_visitor=230cb358-83e2-a7fc-e7e9-6293fc07ca4a; toolbox_urls=cjpa.top|www.github.com|www.easywork.cc; UM_distinctid=17d0342bc42beb-07b7c8107a287d-57b193e-1fa400-17d0342bc43cf4; Hm_lvt_ca96c3507ee04e182fb6d097cb2a1a4c=1637913968,1638002217,1638147469,1638252492; qHistory=aHR0cDovL3Rvb2wuY2hpbmF6LmNvbS9pcHdob2lzL19JUCBXSE9JU+afpeivonxodHRwOi8vd2hvaXMuY2hpbmF6LmNvbS9zdWZmaXhf5pyA5paw5rOo5YaM5Z+f5ZCN5p+l6K+ifGh0dHA6Ly90b29sLmNoaW5hei5jb21f56uZ6ZW/5bel5YW3fGh0dHA6Ly93aG9pcy5jaGluYXouY29tL19XaG9pc+afpeivonxodHRwOi8vaXAudG9vbC5jaGluYXouY29tL3NpdGVpcC9fSVDmiYDlnKjlnLDmibnph4/mn6Xor6J8aHR0cDovL2lwLnRvb2wuY2hpbmF6LmNvbS9pcGJhdGNoL19JUOaJuemHj+afpeivonxodHRwOi8vaXAudG9vbC5jaGluYXouY29tX0lQL0lQdjbmn6Xor6LvvIzmnI3liqHlmajlnLDlnYDmn6Xor6I=; bbsmax_user=f6df12f1-e09a-a25d-63a7-ab2053091f8d; .AspNetCore.Antiforgery.2htDGZ9yTBg=CfDJ8AWLYhGeXVlJiV3by1LjtiI_IC8k_ToxRLUK6NBjvjytXQvwl2G7W3aZB344czrtcHGM5RZfdh-5Yf4ve809EInD77X2z-2AXqINiWr0anAnHnekCCgCDxcajLtuUY9j3Mw0oG5QLODB0zFx0LQ2UOw; .AspNetCore.Session=CfDJ8AWLYhGeXVlJiV3by1LjtiK5oRPr4RGsjrPVxS855Nd1cSfc4UuW2YvCTV0vpwAKI89%2B3DCWVswOqVNJbzBsBJN5ASqz%2Fh3u1KbukQsanKyvIr7H1sq%2Fs%2FB4RlwPJyMvRsKIbCEIW1PYPDfMSyRWNVNIw1GCq9d%2BLUIonT3hB1e0; Hm_lpvt_ca96c3507ee04e182fb6d097cb2a1a4c=1639530550; CNZZDATA5082706=cnzz_eid%3D503046556-1635288334-http%253A%252F%252Ftool.chinaz.com%252F%26ntime%3D1639527414'
    }
    # 循环100次，因为最大限制100
    for page in range(34,101):
        data = {
            'pageNo': page,
            'pageSize': 20,
            # day 代表当天
            'day':1
        }
        time.sleep(10)
        while 1:
            try:
                tex = requests.post(url="http://icp.chinaz.com/Provinces/PageData",data=data,headers=head,proxies=proxys[-1]).json().get("data")
                print(tex)
                break
            except Exception:
                time.sleep(5)
                dl()
                continue

        if len(tex)==0:
            time.sleep(10)
            continue
        merge_sum = []

        for sum in tex:
            site_domain = sum.get("host")
            company_name =sum.get("comName")
            company_type =sum.get("typ")
            main_page ="".join(sum.get("lstHp")).replace("[","").replace("]","")
            site_license =sum.get("permit")
            site_name =sum.get("webName")
            verify =sum.get("verifyTime")

            merge = company_name+site_license+verify

            if verify != local_time or merge in merge_sum:
                continue

            times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            medi = Medicine(site_domain=site_domain,company_name=company_name,company_type=company_type,main_page=main_page,site_license=site_license,site_name=site_name,verify_time=verify,gmt_created=times,gmt_updated=times)

            session.add(medi)
            merge_sum.append(merge)

        session.commit()
        session.close()

def dns_provider():
    head = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    }
    domains = ['xinnet.com',
    'jdtop.com.cn',
    'h110.cn',
    'yszhylyun.cn',
    'nmgthsy.com',
    'isotopesystem.com',
    'cczszh.com']

    for domain in domains:
        print(domain)
        token = get_js(domain)
        data = {
            'host': domain,
            'isUp': False,
            'token': token

        }
        tex = requests.post(url="https://whois.chinaz.com/getWhoisInfo.ashx",data=data,headers=head).json()
        print(tex)
        time.sleep(3)

def get_js(domain):
    f = open("a.js", 'r', encoding='UTF-8')
    line = f.readline()
    htmlstr = ''
    while line:
        htmlstr = htmlstr + line
        line = f.readline()
    ctx = execjs.compile(htmlstr)
    return str(ctx.call('generateHostKey', domain))

if __name__ == '__main__':
    local_time = time.strftime("%Y-%m-%d", time.localtime())
    local_time = '2021-12-14'
    icp_lists()

    # dns_provider()
    # 2.
    # check_data()
    # 4.
    # main()
