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


# 定义User对象:
class Medicine(Base):
    # 表的名字:
    __tablename__ = 'spider_company_info'

    # 表的结构:
    id = Column(Integer(), primary_key=True, autoincrement=True)
    company_num = Column(String(256))
    company_name = Column(String(256))
    natural_person = Column(String(256))
    contacts = Column(String(256))
    mobile = Column(String(256))
    history_name = Column(String(256))
    eng_name = Column(String(256))
    reg_money = Column(String(256))
    apply_date = Column(String(256))
    business_status = Column(String(256))
    reg_num = Column(String(256))
    unified_social_credit_code = Column(String(256))
    organization_code = Column(String(256))
    tax_num = Column(String(256))
    company_type = Column(String(256))
    business_term = Column(String(256))
    industry = Column(String(256))
    tax_qualification = Column(String(256))
    audit_date = Column(String(256))
    paid_money = Column(String(256))
    staff_size = Column(String(256))
    insurance_num = Column(String(256))
    reg_authority = Column(String(256))
    reg_addr = Column(String(256))
    business_project = Column(String(256))
    mobiles = Column(String(256))
    net = Column(String(256))
    emails = Column(String(256))

    gmt_created = Column(String(256))
    gmt_updated = Column(String(256))
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
    time.sleep(2)
    resp = re.sub(r'\n', '', resp)
    proxy = {
        'https': resp
    }
    proxys.append(proxy)
    print(proxys[-1])
dl()

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    # 'cookie': 'TYCID=435e2b701e3f11eb93fd6b29e729c6c7; ssuid=8413289216; _ga=GA1.2.1495606244.1604454265; jsid=SEM-BAIDU-PZ-SY-20201109-BIAOTI; tyc-user-info={%22claimEditPoint%22:%220%22%2C%22vipToMonth%22:%22false%22%2C%22explainPoint%22:%220%22%2C%22personalClaimType%22:%22none%22%2C%22integrity%22:%2210%25%22%2C%22state%22:%220%22%2C%22score%22:%2296%22%2C%22announcementPoint%22:%220%22%2C%22messageShowRedPoint%22:%220%22%2C%22bidSubscribe%22:%22-1%22%2C%22vipManager%22:%220%22%2C%22onum%22:%220%22%2C%22monitorUnreadCount%22:%220%22%2C%22discussCommendCount%22:%220%22%2C%22showPost%22:null%2C%22messageBubbleCount%22:%220%22%2C%22claimPoint%22:%220%22%2C%22token%22:%22eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODgzNzA3NjM1NSIsImlhdCI6MTYwNzY2NTY3MSwiZXhwIjoxNjM5MjAxNjcxfQ.8vTjN_t0do4-kc7o2qO5O7f6ujh3J4Ek7jHHSXtjv_YiGQ6jTyS_aRrKUv4i9kN2DIKZcDvrk_gthbsLfP7ZjA%22%2C%22schoolAuthStatus%22:%222%22%2C%22userId%22:%2235705210%22%2C%22scoreUnit%22:%22%22%2C%22redPoint%22:%220%22%2C%22myTidings%22:%220%22%2C%22companyAuthStatus%22:%222%22%2C%22originalScore%22:%2296%22%2C%22myAnswerCount%22:%220%22%2C%22myQuestionCount%22:%220%22%2C%22signUp%22:%220%22%2C%22privateMessagePointWeb%22:%220%22%2C%22nickname%22:%22%E5%B8%8C%E6%8B%89%E7%91%9E%C2%B7%E8%BE%BE%E8%8A%99%22%2C%22privateMessagePoint%22:%220%22%2C%22bossStatus%22:%222%22%2C%22isClaim%22:%220%22%2C%22yellowDiamondEndTime%22:%220%22%2C%22yellowDiamondStatus%22:%22-1%22%2C%22pleaseAnswerCount%22:%220%22%2C%22bizCardUnread%22:%220%22%2C%22vnum%22:%220%22%2C%22mobile%22:%2218837076355%22%2C%22riskManagement%22:{%22servicePhone%22:null%2C%22mobile%22:18837076355%2C%22title%22:null%2C%22currentStatus%22:null%2C%22lastStatus%22:null%2C%22quickReturn%22:false%2C%22oldVersionMessage%22:null%2C%22riskMessage%22:null}}; tyc-user-info-save-time=1607665672908; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODgzNzA3NjM1NSIsImlhdCI6MTYwNzY2NTY3MSwiZXhwIjoxNjM5MjAxNjcxfQ.8vTjN_t0do4-kc7o2qO5O7f6ujh3J4Ek7jHHSXtjv_YiGQ6jTyS_aRrKUv4i9kN2DIKZcDvrk_gthbsLfP7ZjA; tyc-user-phone=%255B%252218837076355%2522%252C%2522188%25206870%25207561%2522%255D; _gid=GA1.2.587846859.1608514528; csrfToken=ikfObrQXnonOui442CFKI9ck; bannerFlag=true; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1607997927,1608097031,1608194729,1608520205; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22175cea83fe26fa-0ea05bfb98414a-930346c-2073600-175cea83fe3ccd%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%22175cea83fe26fa-0ea05bfb98414a-930346c-2073600-175cea83fe3ccd%22%7D; CT_TYCID=abe3455306be44b3bea3846a0f8ceb13; __insp_wid=677961980; __insp_nv=true; __insp_slim=1608520356369; __insp_targlpu=aHR0cHM6Ly93d3cudGlhbnlhbmNoYS5jb20vY2xhaW0vZW50cnkvMzQ4NzAzMDE0NT9mcm9tPWYz; __insp_targlpt=5LyB5Lia6K6k6K_BIC0g5aSp55y85p_l; RTYCID=f0834d5ff1d2453bad56c12d775320db; acw_tc=2760777a16086052659794735e3a58a0812a9726928bc80306e19d147edf52; cloud_token=006cb75d084543d1b8b1076a43dc812d; cloud_utm=98c3f9d6326c434693293265082fd7d0; token=657a577c3e0d4fd2a271b8cae43ed791; _utm=bd52d9cc1574441c9f8ca42a8e8587c3; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1608605287'
}

def request_data(url):
    time.sleep(1.2)
    while 1:
        try:
            # response = requests.request(method='get', url=url, proxies=proxys[-1], headers=headers, timeout=10).text
            response = requests.request(method='get', url=url, headers=headers, timeout=10).text
            check = re.findall(r'<h1 class="name">(.*?)</h1>', response, re.S)  # 作为获取成功数据的标志，因为获取的页面可能是login in
            if len(check) == 0:
                check1 = re.findall(r'<h2 class="name">(.*?)</h2>', response, re.S)[0]  # 作为获取成功数据的标志，因为获取的页面可能是login in
            break
        except Exception as e:
            print(e)
            dl()
    return response

def format_data(data):
    if len(data) != 0:
        data = ''.join(data)
        if data == '-':
            data = None
    else:
        data = None
    return data

def main3():
    one_url = 'https://www.tianyancha.com/company/2790512155'
    company_num = one_url.split('/')[-1]
    response = request_data(one_url)
    with open('{}.html'.format(company_num), 'w', encoding='utf-8')as fp:
        fp.write(response)
    tree = etree.HTML(response)
    company_num = company_num
    company_name = '浙江中禄财务咨询有限公司'
    natural_person = tree.xpath('//div[@class="humancompany"]//a[@class="link-click"]/text()')
    natural_person = format_data(natural_person)

    contacts = ''

    history_name = tree.xpath('//table[@class="table -striped-col -breakall"]/tbody/tr[9]/td[2]//text()')
    history_name = format_data(history_name)

    eng_name = tree.xpath('//table[@class="table -striped-col -breakall"]/tbody/tr[9]/td[4]//text()')
    eng_name = format_data(eng_name)

    reg_money = tree.xpath('//table[@class="table -striped-col -breakall"]/tbody/tr[3]/td[2]//text()')
    reg_money = format_data(reg_money)

    apply_date = tree.xpath('//table[@class="table -striped-col -breakall"]/tbody/tr[2]/td[2]//text()')
    apply_date = format_data(apply_date)

    business_status = tree.xpath('//table[@class="table -striped-col -breakall"]/tbody/tr[1]/td[4]//text()')
    business_status = format_data(business_status)

    reg_num = tree.xpath('//table[@class="table -striped-col -breakall"]/tbody/tr[4]/td[4]//text()')
    reg_num = format_data(reg_num)

    unified_social_credit_code = tree.xpath('//table[@class="table -striped-col -breakall"]/tbody/tr[5]/td[2]//text()')
    unified_social_credit_code = format_data(unified_social_credit_code)

    organization_code = tree.xpath('//table[@class="table -striped-col -breakall"]/tbody/tr[5]/td[6]//text()')
    organization_code = format_data(organization_code)

    tax_num = tree.xpath('//table[@class="table -striped-col -breakall"]/tbody/tr[5]/td[4]//text()')
    tax_num = format_data(tax_num)

    company_type = tree.xpath('//table[@class="table -striped-col -breakall"]/tbody/tr[7]/td[2]//text()')
    company_type = format_data(company_type)

    business_term = tree.xpath('//table[@class="table -striped-col -breakall"]/tbody/tr[6]/td[2]//text()')
    business_term = format_data(business_term)

    industry = tree.xpath('//table[@class="table -striped-col -breakall"]/tbody/tr[7]/td[4]//text()')
    industry = format_data(industry)

    tax_qualification = tree.xpath('//table[@class="table -striped-col -breakall"]/tbody/tr[6]/td[4]//text()')
    tax_qualification = format_data(tax_qualification)

    audit_date = tree.xpath('//table[@class="table -striped-col -breakall"]/tbody/tr[6]/td[6]//text()')
    audit_date = format_data(audit_date)

    paid_money = tree.xpath('//table[@class="table -striped-col -breakall"]/tbody/tr[4]/td[4]//text()')
    paid_money = format_data(paid_money)

    staff_size = tree.xpath('//table[@class="table -striped-col -breakall"]/tbody/tr[7]/td[6]//text()')
    staff_size = format_data(staff_size)

    insurance_num = tree.xpath('//table[@class="table -striped-col -breakall"]/tbody/tr[8]/td[2]//text()')
    insurance_num = format_data(insurance_num)

    reg_authority = tree.xpath('//table[@class="table -striped-col -breakall"]/tbody/tr[8]/td[4]//text()')
    reg_authority = format_data(reg_authority)

    reg_addr = tree.xpath('//table[@class="table -striped-col -breakall"]/tbody/tr[10]/td[2]//text()')
    if len(reg_addr) != 0:
        reg_addr = reg_addr[0]
        if reg_addr == '-':
            reg_addr = None
    else:
        reg_addr = None

    business_project = tree.xpath('//table[@class="table -striped-col -breakall"]/tbody/tr[11]/td[2]//text()')
    business_project = format_data(business_project)

    gmt_created = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    gmt_updated = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    report_count = re.findall(r'企业年报<span class="itemnumber  -company">(.*?)</span>', response, re.S)
    sum = []
    if len(report_count) != 0:
        report_urls = re.findall('年度报告</td><td><a class="link-click" href="(.*?)" target="_blank">详情</a>', response,
                                 re.S)
        print('{},年报URLS：{}'.format(company_name, report_urls))
        for i, report_url in enumerate(report_urls):
            single = {}
            time.sleep(0.5)
            while 1:
                try:
                    # report_content = requests.request(method='get', url=report_url, proxies=proxys[-1], headers=headers,timeout=10).text
                    report_content = requests.request(method='get', url=report_url, headers=headers, timeout=10).text
                    year = re.findall(r'<title>.*?_(.*?)_企业年报查询 - 天眼查'.format(company_name), report_content, re.S)[0]
                    break
                except Exception as e:
                    print(e)
                    dl()

            year_report_mobile = re.findall(r'<td>企业联系电话</td><td>(.*?)</td>'.format(), report_content, re.S)
            year_report_mobile = format_data(year_report_mobile)
            if not year_report_mobile:
                continue
            single['sS'] = year
            single['pN'] = year_report_mobile

            sum.append(single)

    mobiles = sum

    net = tree.xpath('//div[@class="f0 clearfix mb0"]/div[1]/a[last()]/text()')
    net = format_data(net)

    emails = tree.xpath('//div[@class="f0"]/div[2]/span[@class="email"]/text()')
    emails_lists = tree.xpath('//div[@class="f0"]/div[2]/span[last()]/script/text()')
    if len(emails) !=0:
        emails = emails
        if len(emails_lists) !=0:
            emails = emails_lists
    else:
        emails = None
    mobile = ''

    print(company_num, company_name, natural_person, contacts, mobile, history_name, eng_name, reg_money, apply_date,
          business_status, reg_num, unified_social_credit_code, organization_code,
          tax_num, company_type, business_term, industry, tax_qualification, audit_date, paid_money, staff_size,
          insurance_num, reg_authority, reg_addr, business_project, gmt_created, gmt_updated,
          mobiles, net, emails)


if __name__ == '__main__':
    main3()
