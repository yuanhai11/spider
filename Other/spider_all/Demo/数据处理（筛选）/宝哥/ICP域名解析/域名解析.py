from lxml import etree
from sqlalchemy import Column, String, create_engine, Integer, and_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from ctypes import windll
from model.table import table_icp_leads, table_company_info
from apscheduler.schedulers.blocking import BlockingScheduler

import time, re, json, os
import requests
import datetime
# 加入pywintypes，打包成功
import pywintypes
import win32api
import win32con
import win32gui


class Operation():

    def __init__(self, local_time):
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
            'cookie':'TYCID=435e2b701e3f11eb93fd6b29e729c6c7; ssuid=8413289216; _ga=GA1.2.1495606244.1604454265; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2247184373%22%2C%22first_id%22%3A%22175cea83fe26fa-0ea05bfb98414a-930346c-2073600-175cea83fe3ccd%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%22175cea83fe26fa-0ea05bfb98414a-930346c-2073600-175cea83fe3ccd%22%7D; tyc-user-phone=%255B%252218069882328%2522%252C%2522188%25203707%25206355%2522%252C%2522153%25209583%25201367%2522%255D; _bl_uid=p8kXdv0pakeq4hbakedphdz4ywO0; aliyungf_tc=d09840a7aa56823825fb2d9acb3798687b73faa261f70e063a37140d2fc37431; csrfToken=jAoic4Rp0MKRm9vZQ8pY39BK; bannerFlag=true; __insp_wid=677961980; __insp_slim=1636082473876; __insp_nv=true; __insp_targlpu=aHR0cHM6Ly93d3cudGlhbnlhbmNoYS5jb20vY2xhaW0vZW50cnkvNTAxNjMyMTQy; __insp_targlpt=5LyB5Lia6K6k6K_BIC0g5aSp55y85p_l; __insp_norec_sess=true; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1635758009,1635823826; creditGuide=1; relatedHumanSearchGraphId=5243947963; relatedHumanSearchGraphId.sig=UowRes9NMOYd5w0jBpNGvhEcnawcmbNcdc0dwISQF3I; _gid=GA1.2.2008545.1637542812; searchSessionId=1637542812.63712088; RTYCID=2f6ad8f6f8484131963d98fad4295c36; CT_TYCID=878dbde8452c4594bb1af6f8c09649b5; acw_tc=2f6fc12116375480750016628e66daae71c04e567eb8828e168762e307b21f; tyc-user-info={%22isExpired%22:%220%22%2C%22mobile%22:%2218069882328%22%2C%22state%22:%225%22%2C%22vipManager%22:%220%22}; tyc-user-info-save-time=1637548092390; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODA2OTg4MjMyOCIsImlhdCI6MTYzNzU0ODA4OSwiZXhwIjoxNjY5MDg0MDg5fQ.8CEfYg-5DtJ9laknykTY9dhQWdtgtfYvyp8NFzRex6ERHrz-ZFdDdP7QmD-2z99ACACnR_PnkzL5wrLl9cep9w; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2247184373%22%2C%22first_id%22%3A%22175cea83fe26fa-0ea05bfb98414a-930346c-2073600-175cea83fe3ccd%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%22175cea83fe26fa-0ea05bfb98414a-930346c-2073600-175cea83fe3ccd%22%7D; cloud_token=8fef4f037b2242a4866d2fb265de5d9f; cloud_utm=1a4987e9349a4e41abaf4835214f8606; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1637548094'
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
            and_(table_icp_leads.phone == None, table_icp_leads.eg_capital == None,table_icp_leads.id>14150,
                 table_icp_leads.company_type != '个人')).all()
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
                    if '<title>天眼查校验</title>' in res:
                        print('-------触发了login，请等待1min之内更换cookie')
                        time.sleep(60)
                        continue
                    if 'setCookie(name,value)' in res:
                        self.dl()
                        continue
                    break
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
                    print('-------触发了login，请等待1min之内更换cookie')
                    time.sleep(60)
                    self.dl()
                    continue
                if 'setCookie(name,value)' in res:
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

    def get_detail(self,url, company, id):
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
            print(id,company, reg_capital + '----', social_staff_num + '----', company_org_type + '----', phone + '----',
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
                    if mobiles == None:
                        i.phone_source = ''
                    else:
                        i.phone_source = str(mobiles)
                    print(name, 'over')
                company_s.append(name)
            except Exception:
                continue

        self.session.commit()

    '''
    解析每天从UIBOT中获取的数据，以时间为分割，每天只能执行一次，
    '''

    def icp_lists(self):
        with open(r"C:\Users\20945\Desktop\Uibot_project\ICP\data\2.txt", 'r', encoding='utf-8')as fp:
            con = fp.read().replace('\n', '').replace(' ', '').replace('][', '----').replace("[", "").replace("]",
                                                                                                              '').split(
                '----')
        merge_sum = []
        for i in con:
            sum = i.replace('"', "").split(',')

            site_domain = sum[0]
            company_name = sum[1]
            company_type = sum[2]
            main_page = sum[5]
            site_license = sum[3]
            site_name = sum[4]
            verify = sum[6]

            merge = company_name + site_license + verify

            if verify != local_time or merge in merge_sum:
                continue

            times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            medi = table_icp_leads(site_domain=site_domain, company_name=company_name, company_type=company_type,
                                   main_page=main_page, site_license=site_license, site_name=site_name,
                                   verify_time=verify, gmt_created=times, gmt_updated=times)

            self.session.add(medi)

            print(sum)
            merge_sum.append(merge)

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
        driver = webdriver.Chrome(executable_path=r'E:\Environment\chromedriver_win32\chromedriver.exe')
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
               Object.defineProperty(navigator, 'webdriver', {
                 get: () => undefined
               })
         """
        })
        companys = self.session.query(table_icp_leads).filter(
            and_(table_icp_leads.verify_time == self.local_time, table_icp_leads.site_domain != None,
                 table_icp_leads.dns_provider == None)).all()
        for company in companys:
            try:
                id = company.id
                try:
                    domain = "https://whois.chinaz.com/" + company.site_domain
                    driver.get(domain)
                    time.sleep(7)
                    ele_lists = driver.find_element_by_xpath('//div[@class="block ball"]/span')
                    text = ele_lists.text
                    print(domain, text)
                except Exception:
                    continue
                con = self.session.query(table_icp_leads).filter(table_icp_leads.id == id).first()
                con.dns_provider = text
                self.session.commit()
            except Exception:
                print("断网保护，休眠100s")
                time.sleep(100)

        self.session.close()
        driver.close()

    '''
    唤起uibot 并执行
    '''

    def call_uibot(self):
        print("执行uibot程序")
        source_path = r"C:\Users\20945\Desktop\locked.txt"
        if not os.path.exists(source_path):
            with open(source_path, mode='w', encoding="utf-8") as f:
                f.write("1")

        windows_type = "Chrome_WidgetWin_1"
        windows_name = "UiBot Creator"
        MAP_KEYS = windll.user32.MapVirtualKeyA
        h_wnd = win32gui.FindWindow(windows_type, windows_name)
        win32gui.ShowWindow(h_wnd, win32con.SW_RESTORE)
        time.sleep(.5)
        win32gui.SetActiveWindow(h_wnd)
        time.sleep(.5)
        win32gui.SetForegroundWindow(h_wnd)
        time.sleep(.5)
        win32api.keybd_event(win32con.VK_F5, MAP_KEYS(116, 0), 0, 0)  # 按下 F5
        win32api.keybd_event(win32con.VK_F5, MAP_KEYS(116, 0), win32con.WM_KEYUP, 0)

def start_job():
    local_time = time.strftime("%Y-%m-%d", time.localtime())
    # local_time = '2021-12-14'
    print("开始入库：时间====》{} ".format(local_time))
    operation = Operation(local_time)
    operation.call_uibot()
    if not os.path.exists(r"C:\Users\20945\Desktop\locked.txt"):
        operation.icp_lists()
        operation.check_data()
        operation.web()
        # operation.tyc_data_match()
        print("时间：{} --- 结束".format(local_time))
        # scheduler.remove_job("start_job")

if __name__ == '__main__':
    global local_time
    # BlockingScheduler
    scheduler = BlockingScheduler()
    scheduler.add_job(start_job,'cron',id="start_job",day='1-31', hour=22, minute=0)
    # scheduler.add_job(start_job,'interval',seconds=5)
    scheduler.start()
    print("你好啊")
