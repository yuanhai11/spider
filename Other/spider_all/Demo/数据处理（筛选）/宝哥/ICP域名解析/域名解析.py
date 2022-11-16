import pymysql
from lxml import etree
from sqlalchemy import Column, String, create_engine, Integer, and_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from ctypes import windll
from model.table import table_icp_leads,table_company_info,table_company_contact,table_data_wheel

import time, re, json,os
import requests
import datetime
# 加入pywintypes，打包成功
import pywintypes
# import win32api
# import win32con
# import win32gui


class Operation():

    def __init__(self,local_time):
        # 创建对象的基类:
        self.Base = declarative_base()
        # 初始化数据库连接:
        self.engine = create_engine('mysql+pymysql://root:BOOT-xwork1024@192.168.2.97:3306/spider')
        # 创建DBSession类型:
        self.DBSession = sessionmaker(bind=self.engine)
        # 创建session对象:
        self.session = self.DBSession()

        self.proxys = []
        self.main_company_list = []
        self.local_time = local_time

        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
            'cookie': 'TYCID=435e2b701e3f11eb93fd6b29e729c6c7; ssuid=8413289216; _ga=GA1.2.1495606244.1604454265; __insp_slim=1608615852663; __insp_wid=677961980; __insp_nv=true; __insp_targlpt=5LyB5Lia6K6k6K_BIC0g5aSp55y85p_l; __insp_targlpu=aHR0cHM6Ly93d3cudGlhbnlhbmNoYS5jb20vY2xhaW0vZW50cnkvMjk5MDIxNzc2NA%3D%3D; __insp_norec_sess=true; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2247184373%22%2C%22first_id%22%3A%22175cea83fe26fa-0ea05bfb98414a-930346c-2073600-175cea83fe3ccd%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%22175cea83fe26fa-0ea05bfb98414a-930346c-2073600-175cea83fe3ccd%22%7D; creditGuide=1; tyc-user-phone=%255B%252218069882328%2522%252C%2522188%25203707%25206355%2522%252C%2522153%25209583%25201367%2522%255D; _bl_uid=p8kXdv0pakeq4hbakedphdz4ywO0; aliyungf_tc=d09840a7aa56823825fb2d9acb3798687b73faa261f70e063a37140d2fc37431; csrfToken=jAoic4Rp0MKRm9vZQ8pY39BK; bannerFlag=true; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1634088403,1635758009; _gid=GA1.2.823123114.1635758009; RTYCID=fc26b95c5e7e4397a9a535e7da3cd1b6; CT_TYCID=05b5a96a365d4f70919b974d8fd951f1; acw_tc=781bad4216358223650144573e50ddab76c69f0be2333352ba75583ec037ec; acw_sc__v2=6180ab1dcde77a65556c2d575628714e095db13d; tyc-user-info-save-time=1635822374934; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODA2OTg4MjMyOCIsImlhdCI6MTYzNTgyMjM3MywiZXhwIjoxNjY3MzU4MzczfQ.kom1B9MFkpyoRdN2s_HCshf35IZAbRp-N5BdlumjhJNVSWNeWmUofydTHUVAZcn5IDnJwzvjD9W8HbH6_DASEA; tyc-user-info={%22isExpired%22:%220%22%2C%22mobile%22:%2218069882328%22%2C%22state%22:%225%22%2C%22vipManager%22:%220%22}; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2247184373%22%2C%22first_id%22%3A%22175cea83fe26fa-0ea05bfb98414a-930346c-2073600-175cea83fe3ccd%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%22175cea83fe26fa-0ea05bfb98414a-930346c-2073600-175cea83fe3ccd%22%7D; cloud_token=fd05a8490c884b78b735f7266d6930e9; cloud_utm=d530866748f84852a8e42525d5b7310b; relatedHumanSearchGraphId=3486767098; relatedHumanSearchGraphId.sig=JI8LutPeOvRWp3-mOuJV8Af-coS9vBZzW_VGXbMDdNw; searchSessionId=1635822806.39474733; _gat_gtag_UA_123487620_1=1; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1635822807'
        }

    '''
    请求代理 
    '''

    def dl(self):
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
        self.proxys.append(proxy)
        print(self.proxys[-1])

    '''
     从天眼查中获取多个手机号
     '''

    def tyc_data_match(self):
        self.dl()
        companys = self.session.query(table_icp_leads).filter(
            and_(table_icp_leads.phone == None, table_icp_leads.eg_capital == None,
                 table_icp_leads.verify_time == local_time, table_icp_leads.company_type != '个人')).all()
        print(len(companys))
        for index, co in enumerate(companys):
            # if index<12:
            #     continue
            company = co.company_name
            company_copy = company.replace('(', '').replace(')', '').replace('）', '').replace('（', '')
            if company in self.main_company_list:
                continue
            # if len(company) < 4:
            #     continue
            # company = '广西梧州市洛英格农业科技有限公司'
            id = co.id
            url = 'https://www.tianyancha.com/search?key={}'.format(company)
            while 1:
                time.sleep(1.5)
                try:
                    response = requests.request(method='get', url=url, headers=self.headers, proxies=self.proxys[-1],
                                                timeout=8)
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
                    self.dl()
                except Exception as e:
                    print(e)
                    self.dl()

            tree = etree.HTML(res)
            natural_person = tree.xpath('//div[@id="search_company_0"]')
            if len(natural_person) == 0:
                print(company, '跳过')
                continue
            name = "".join(
                tree.xpath('//div[@id="search_company_0"]//div[@class="content"]/div[1]/a//text()')).strip().replace(
                '(', '').replace(')', '').replace('）', '').replace('（', '')
            if name != company_copy:
                print(company, '跳过')
                continue

            url = "".join(tree.xpath('//div[@id="search_company_0"]//div[@class="content"]/div[1]/a/@href')).split('/')[
                -1]
            url = "https://www.tianyancha.com/company/{}".format(url)
            self.get_detail(url, company, id)

    '''
     请求数据，返回tree
     '''

    def request_data(self, url):
        while 1:
            try:
                time.sleep(1)
                # response = requests.request(method='get', url=url, headers=headers, timeout=10)
                response = requests.request(method='get', url=url, proxies=self.proxys[-1], headers=self.headers,
                                            timeout=10)
                code = response.status_code
                res = response.text

                if '<title>天眼查校验</title>' in res:
                    print('detail-------login')
                    time.sleep(10)
                    self.dl()
                    continue
                # print(res)
                tree = etree.HTML(res)
                natural_person = tree.xpath('//div[@id="company_web_top"]')
                if len(natural_person) == 0:
                    self.dl()
                    continue
                break
            except Exception as e:
                print(e)
                self.dl()

        return tree

    '''
     获取详情页，进行解析并入库
     '''

    def get_detail(url, company, id, self):
        response = self.request_data(url)
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

        medis = self.session.query(table_icp_leads).filter(table_icp_leads.company_name == company).all()
        for medi in medis:
            medi.eg_capital = reg_capital
            medi.social_staff_num = social_staff_num
            medi.company_org_type = company_org_type
            medi.phone = phone
            medi.phone_source = phone_source
            medi.business_scope = business_scope
            self.session.commit()
            print(company, reg_capital + '----', social_staff_num + '----', company_org_type + '----', phone + '----',
                  phone_source, business_scope)

        self.main_company_list.append(company)

    '''
    从数仓中进行手机号匹配，通过company_name。
    '''

    def check_data(self):
        company_s = []
        companys = self.session.query(table_icp_leads).filter(table_icp_leads.verify_time == self.local_time).all()
        for q in companys:
            try:
                sum = []
                name = q.company_name
                if name in company_s:
                    continue
                company_info_data = self.session.query(table_company_info).filter(
                    table_company_info.company_name == name).first()
                if company_info_data == None:
                    continue
                mobile = company_info_data.mobile
                mobiles = company_info_data.mobiles
                if mobiles != None:
                    mobiles = json.loads(company_info_data.mobiles)
                    sum = [m['pN'] for m in mobiles]

                reg_money = company_info_data.reg_money
                if reg_money:
                    reg_money = reg_money.replace("万",'').\
                        replace("人",'')\
                        .replace("民",'')\
                        .replace("币",'')\
                        .replace("美元",'')\
                        .replace("港元",'')

                insurance_num = company_info_data.insurance_num
                business_project = company_info_data.business_project
                company_type = company_info_data.company_type

                if mobile != None:
                    sum.append(mobile)
                sum = ','.join(list(set(sum)))

                icp = self.session.query(table_icp_leads).filter(table_icp_leads.company_name == name).all()
                for i in icp:

                    i.eg_capital = reg_money
                    i.social_staff_num = insurance_num
                    i.business_scope = business_project
                    i.company_org_type = company_type
                    i.phone = sum
                    if sum=='':
                        i.phone = None
                    if mobiles == None:
                        i.phone_source = None
                    else:
                        i.phone_source = str(mobiles)
                    print(name, 'over')
                company_s.append(name)
            except Exception:
                continue

        self.session.commit()

    def match_peer(self):
        companys = self.session.query(table_icp_leads).filter(and_(
            table_icp_leads.verify_time == self.local_time,
            table_icp_leads.phone != None
        )).all()

        match = self.session.query(table_company_contact).filter(table_company_contact.match_peer==1).all()
        res = ','.join([i.tel for i in match])
        for q in companys:
            phone = str(q.phone)
            ph_lists = phone.split(',')
            for p in ph_lists:
                if p not in res:
                    print("no")
                    continue
                q.match_peer = 1
                print("dhaoif",q.company_name)
                break

        self.session.commit()

        for q in companys:

            match = self.session.query(table_data_wheel).filter(and_(
                table_data_wheel.is_peer_number == 1,
                table_data_wheel.company_name == q.company_name
            )).all()
            if match:
                q.match_peer = 1
                print("dhaoif",q.company_name)
                # break
        self.session.commit()


    '''
     获取dns_provider字段
     '''

    def web(self):
        '''
        识别图片中的文字
        '''

        options = Options()
        # 下面代码为设置端口、忽略证书错误以及指定文件夹
        # options.add_argument(('--proxy-server=127.0.0.1:8080'))
        # options.add_argument("--ignore-certificate-errors")
        # options.add_argument('--user-data-dir=C:\\Users\\20945\\Desktop\\data')
        # 下面代码为避免网站对selenium的屏蔽
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        # 以设定好的方式打开谷歌浏览器
        driver = webdriver.Chrome(
            executable_path=r'C:\Users\20945\Downloads\Compressed\chromedriver_win32_4\chromedriver.exe',
            options=options)
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
               Object.defineProperty(navigator, 'webdriver', {
                 get: () => undefined
               })
         """
        })
        companys = self.session.query(table_icp_leads).filter(
            and_(table_icp_leads.verify_time == self.local_time, table_icp_leads.site_domain != None
                 ,table_icp_leads.phone != None,
                 table_icp_leads.social_staff_num > 2,
                 table_icp_leads.eg_capital > 100
                 )).all()

        for company in companys:
            id = company.id
            domain = "https://whois.chinaz.com/" + company.site_domain
            driver.get(domain)
            time.sleep(3)
            try:
                ele_lists = driver.find_element_by_xpath('//div[@class="block ball"]/span')
                text = ele_lists.text
                print(domain, text)
            except Exception:
                continue
            con = self.session.query(table_icp_leads).filter(table_icp_leads.id == id).first()
            con.dns_provider = text
            self.session.commit()

        companys = self.session.query(table_icp_leads).filter(
            and_(table_icp_leads.verify_time == self.local_time, table_icp_leads.site_domain != None
                 ,table_icp_leads.dns_provider == None,
                 )).all()
        for company in companys:
            id = company.id
            domain = "https://whois.chinaz.com/" + company.site_domain
            driver.get(domain)
            time.sleep(3)
            try:
                ele_lists = driver.find_element_by_xpath('//div[@class="block ball"]/span')
                text = ele_lists.text
                print(domain, text)
            except Exception:
                continue
            con = self.session.query(table_icp_leads).filter(table_icp_leads.id == id).first()
            con.dns_provider = text
            self.session.commit()
        self.session.close()
        driver.close()


    def icp_lists(self):
        head = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
            'cookie':'cz_statistics_visitor=b843c099-69ba-6c07-2bcb-7d8c63e0471a; qHistory=aHR0cDovL3dob2lzLmNoaW5hei5jb20vX1dob2lz5p+l6K+ifGh0dHA6Ly9pcC50b29sLmNoaW5hei5jb21fSVAvSVB2Nuafpeivou+8jOacjeWKoeWZqOWcsOWdgOafpeivog==; __bid_n=183d631626e89a08254207; .AspNetCore.Antiforgery.2htDGZ9yTBg=CfDJ8AdiD4ZOsAtHkpahMRR1T64-nwoMoAIpJwWd41AkLWFQlUDaPn34kYIrQtGh9xVKH_EdObQcxjQbxJ3EkUVrHtcO2YHawCA9pQVjwhbiGNgeXpWZ8cUzXaM-l8Cx5BmzVWFiKButy7F04SgqadmY_3c; Hm_lvt_ca96c3507ee04e182fb6d097cb2a1a4c=1665745823,1666086142,1667455427,1667878035; ucvalidate=fa6b7674-7028-6493-011a-ad0007cd90d6; toolUserGrade=F4378AC40164ECEFBBA722273EBE9DB3052713BC5A8D18DB025214970CFEF4E8FAA7BF2E1230AFC6017487F075E3D2DBCDDF6344EF96CCB1; bbsmax_user=221a7c9c-b0a9-dfd3-7dbc-7e01bff41813; .AspNetCore.Antiforgery.ZLR_yHWNBdY=CfDJ8DeKtxYi9PZDlMLEsemar02Hfu1tR8zl01DDKK7Zpx6CaOLSibmF6n7zbOAD3089bkcaCZ2rZopSAgdGAg92_u-uWXO25X31BslXHDycLjtJH-RRDEkFVqzZw8zHtNSQuYg4Q9kqwQECtjPa-cBOo98; Hm_lpvt_ca96c3507ee04e182fb6d097cb2a1a4c=1667878116'
        }
        # 循环100次，因为最大限制100
        for page in range(1,101):
            data = {
                'pageNo': page,
                'pageSize': 20,
                # day 代表当天
                'day':1
            }
            time.sleep(5)
            while 1:
                try:
                    tex = requests.post(url="http://icp.chinaz.com/Provinces/PageData",data=data,headers=head).json().get("data")
                    print(tex)
                    break
                except Exception:
                    print("page:【{}】 be in trouble".format(page))
                    time.sleep(8)
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

                if verify != self.local_time or merge in merge_sum:
                    continue

                times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                medi = table_icp_leads(
                    site_domain=site_domain,company_name=company_name,company_type=company_type,main_page=main_page,site_license=site_license,site_name=site_name,verify_time=verify,gmt_created=times,gmt_updated=times
                    ,match_peer=0)
                self.session.add(medi)
                merge_sum.append(merge)

            self.session.commit()
            self.session.close()


def main():
    local_time = time.strftime("%Y-%m-%d", time.localtime())
    # local_time = "2022-11-15"

    # 每天下午4点开始。
    operation = Operation(local_time)
    try:
        operation.icp_lists()
    except Exception:
        pass
    operation.check_data()
    operation.match_peer()
    operation.web()



if __name__ == '__main__':

    from apscheduler.schedulers.blocking import BlockingScheduler
    scheduler = BlockingScheduler()
    scheduler.add_job(main, 'cron', day ='1-31', hour=17, minute=42)
    # scheduler.add_job(main, 'cron', day ='1-31', hour=9, minute=2)
    scheduler.start()