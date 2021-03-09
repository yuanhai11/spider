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
    business_term = Column(String(256))
    connect_company_count = Column(String(256))
    busi_risk_count = Column(String(256))
    busi_abnormal_situation = Column(String(256))
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
    current_1_busi_status = Column(String(256))
    current_2_busi_status = Column(String(256))
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
    all_data = session.query(Medicine).offset(160000).limit(10000).all() # 180000 .  10000   之后140000 ~ 200000 重新检索一边  140000- 160000 170000-180000 180000-200000
    print(len(all_data))
    for index,medi in enumerate(all_data):
        company_name = medi.company_name
        busi_abnormal_situation = medi.busi_abnormal_situation
        if busi_abnormal_situation == None or busi_abnormal_situation == '':
            # if company_name == '杭州君唐科技有限公司':
            #     print(index)
            # continue
            try:
                # if index < 4556-start:
                #     continue
                head = {
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
                    # 'cookie':"TYCID=435e2b701e3f11eb93fd6b29e729c6c7; ssuid=8413289216; _ga=GA1.2.1495606244.1604454265; jsid=SEM-BAIDU-PZ-SY-20201109-BIAOTI; __insp_slim=1606196162867; __insp_wid=677961980; __insp_nv=true; __insp_targlpt=5LyB5Lia6K6k6K_BIC0g5aSp55y85p_l; __insp_targlpu=aHR0cHM6Ly93d3cudGlhbnlhbmNoYS5jb20vY2xhaW0vZW50cnkvNDAzNDM3NDI5NT9mcm9tPWYz; __insp_norec_sess=true; csrfToken=gZ0eQTIgj1gpio11orxrPRgx; bannerFlag=true; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1606485479,1607046294,1607070791,1607589227; _gid=GA1.2.71257741.1607589228; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22175cea83fe26fa-0ea05bfb98414a-930346c-2073600-175cea83fe3ccd%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%22175cea83fe26fa-0ea05bfb98414a-930346c-2073600-175cea83fe3ccd%22%7D; RTYCID=2fd3ee666c1c4082a7e6454b803e32d0; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1607665614; _gat_gtag_UA_123487620_1=1; token=3ec10a866f1743618f32e0e612f1030a; _utm=9d0f83c741944fe98cc553523025c79e; tyc-user-info={%22claimEditPoint%22:%220%22%2C%22vipToMonth%22:%22false%22%2C%22explainPoint%22:%220%22%2C%22personalClaimType%22:%22none%22%2C%22integrity%22:%2210%25%22%2C%22state%22:%220%22%2C%22score%22:%2296%22%2C%22announcementPoint%22:%220%22%2C%22messageShowRedPoint%22:%220%22%2C%22bidSubscribe%22:%22-1%22%2C%22vipManager%22:%220%22%2C%22onum%22:%220%22%2C%22monitorUnreadCount%22:%220%22%2C%22discussCommendCount%22:%220%22%2C%22showPost%22:null%2C%22messageBubbleCount%22:%220%22%2C%22claimPoint%22:%220%22%2C%22token%22:%22eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODgzNzA3NjM1NSIsImlhdCI6MTYwNzY2NTY3MSwiZXhwIjoxNjM5MjAxNjcxfQ.8vTjN_t0do4-kc7o2qO5O7f6ujh3J4Ek7jHHSXtjv_YiGQ6jTyS_aRrKUv4i9kN2DIKZcDvrk_gthbsLfP7ZjA%22%2C%22schoolAuthStatus%22:%222%22%2C%22userId%22:%2235705210%22%2C%22scoreUnit%22:%22%22%2C%22redPoint%22:%220%22%2C%22myTidings%22:%220%22%2C%22companyAuthStatus%22:%222%22%2C%22originalScore%22:%2296%22%2C%22myAnswerCount%22:%220%22%2C%22myQuestionCount%22:%220%22%2C%22signUp%22:%220%22%2C%22privateMessagePointWeb%22:%220%22%2C%22nickname%22:%22%E5%B8%8C%E6%8B%89%E7%91%9E%C2%B7%E8%BE%BE%E8%8A%99%22%2C%22privateMessagePoint%22:%220%22%2C%22bossStatus%22:%222%22%2C%22isClaim%22:%220%22%2C%22yellowDiamondEndTime%22:%220%22%2C%22yellowDiamondStatus%22:%22-1%22%2C%22pleaseAnswerCount%22:%220%22%2C%22bizCardUnread%22:%220%22%2C%22vnum%22:%220%22%2C%22mobile%22:%2218837076355%22%2C%22riskManagement%22:{%22servicePhone%22:null%2C%22mobile%22:18837076355%2C%22title%22:null%2C%22currentStatus%22:null%2C%22lastStatus%22:null%2C%22quickReturn%22:false%2C%22oldVersionMessage%22:null%2C%22riskMessage%22:null}}; tyc-user-info-save-time=1607665672908; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODgzNzA3NjM1NSIsImlhdCI6MTYwNzY2NTY3MSwiZXhwIjoxNjM5MjAxNjcxfQ.8vTjN_t0do4-kc7o2qO5O7f6ujh3J4Ek7jHHSXtjv_YiGQ6jTyS_aRrKUv4i9kN2DIKZcDvrk_gthbsLfP7ZjA; tyc-user-phone=%255B%252218837076355%2522%252C%2522188%25206870%25207561%2522%255D"
                }
                url = 'https://www.tianyancha.com/search?key={}'.format(company_name)
                detail_url = ""
                while 1:
                    try:
                        res = requests.request(method='get', url=url,proxies=proxys[-1],headers=head,timeout=10).text
                        # res = requests.request(method='get', url=url,headers=head,timeout=10).text
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
                        print(e)
                        time.sleep(2)
                        dl()
                print(detail_url)
                if detail_url == "":
                    time.sleep(1)
                    print(company_name,'天眼查查询不到，跳过')
                else:

                    time.sleep(1)
                    detail_url = detail_url[0]
                    data = ''
                    while 1:
                        try:
                            data = requests.request(method='get', url=detail_url, proxies=proxys[-1],headers=head, timeout=10).text
                            # data = requests.request(method='get', url=detail_url, headers=head, timeout=10).text
                            check = re.findall(r'<h1 class="name">(.*?)</h1>',data,re.S)   # 作为获取成功数据的标志，因为获取的页面可能是login in
                            if len(check)==0:
                                check1 = re.findall(r'<h2 class="name">(.*?)</h2>',data,re.S)[0]   # 作为获取成功数据的标志，因为获取的页面可能是login in

                            break
                        except Exception as e:
                            print(e)
                            time.sleep(2)
                            dl()

                    medicine = session.query(Medicine).filter(Medicine.company_name == company_name).first()
                    # print(text)
                    business_status = re.findall(r'经营状态</td>.*?>(.*?)</td>', data, re.S)
                    business_term = re.findall(r'<td>营业期限</td>.*?<span>(.*?)</span></td>', data, re.S)

                    report_count = re.findall(r'企业年报<span class="itemnumber  -company">(.*?)</span>',data,re.S)
                    company_count = re.findall(r'他有<span class=".*?">(.*?)</span>家公司', data, re.S)
                    company_count1 = re.findall(r'任职<span class=".*?">(.*?)</span>家', data, re.S)
                    reason = re.findall(r'<div>注销原因：(.*?)</div>', data, re.S)
                    date = re.findall(r'<div>注销日期：(.*?)</div>', data, re.S)

                    reason1 = re.findall(r'<div>吊销原因：(.*?)</div>', data, re.S)
                    date1 = re.findall(r'<div>吊销日期：(.*?)</div>', data, re.S)

                    busi_except = re.findall(r'<span class="data-title">经营异常</span><span class="data-count -warn">(.*?)</span>', data, re.S)
                    print('经营异常数量：', busi_except)
                    s = []
                    try:
                        if len(busi_except) != 0:
                            busi_risk_count = busi_except[0]
                            tr22 = etree.HTML(data)
                            tr_list1 = tr22.xpath('//div[@id="_container_abnormalPut"]//tbody/tr')
                            tr_list2 = tr22.xpath('//div[@id="_container_abnormalRemove"]//tbody/tr')

                            for t1 in tr_list1:
                                s1 = {}
                                put_date = t1.xpath('./td[2]/text()')[0]
                                anthori = t1.xpath('./td[3]/text()')[0]
                                rea = t1.xpath('./td[4]//div[@class="detail-content"]/text()')[0].strip()
                                s1['列入日期'] = put_date
                                s1['列入原因'] = rea
                                s1['列入机关'] = anthori
                                s1['移出日期'] = 'None'
                                s1['移出原因'] = 'None'
                                s1['移出机关'] = 'None'
                                s.append(s1)

                            for t2 in tr_list2:
                                s2 = {}
                                put_date1 = t2.xpath('./td[2]/text()')[0]
                                rea1 = t2.xpath('./td[3]/text()')[0]
                                anthori1 = t2.xpath('./td[4]/text()')[0]
                                remove_date1 = t2.xpath('./td[5]/text()')[0]
                                remove_rea = t2.xpath('./td[6]//div[@class="detail-content"]/text()')[0].strip()
                                s2['列入日期'] = put_date1
                                s2['列入原因'] = rea1
                                s2['列入机关'] = anthori1
                                s2['移出日期'] = remove_date1
                                s2['移出原因'] = remove_rea
                                s2['移出机关'] = anthori1
                                s.append(s2)

                            print('经营异常数量：{}经营异常：{}'.format(busi_risk_count, s))
                            medicine.busi_abnormal_situation = str(s)
                            medicine.busi_risk_count = busi_risk_count

                        else:
                            medicine.busi_abnormal_situation = str(s)
                    except Exception as e:
                        print(e)
                    print(company_name)

                    if len(business_status) !=0:
                        business_status = ''.join(business_status)
                        medicine.business_status = business_status
                        print('经营状态：',business_status)
                    if len(business_term) !=0:
                        business_term = ''.join(business_term).replace('&nbsp;','').replace(' ','').strip()
                        medicine.business_term = business_term
                        print('经营截至期限：',business_term)

                    if len(reason) !=0 and len(date) !=0:
                        reason = reason[0]
                        date = date[0]
                        print('注销原因：{},注销日期：{}'.format(reason,date))

                        medicine.risk_reason = reason
                        medicine.risk_date = date
                    elif len(reason1) !=0 and len(date1) !=0:
                        reason1 = reason1[0]
                        date1 = date1[0]
                        print('吊销原因：{},吊销日期：{}'.format(reason1,date1))

                        medicine.risk_reason = reason1
                        medicine.risk_date = date1

                    if len(company_count) !=0:
                        company_count = company_count[0]
                        print('法人名下有{}家公司：'.format(company_count))

                        medicine.connect_company_count = str(company_count)
                    elif len(company_count1) !=0:
                        company_count1 = company_count1[0]
                        print('法人名下有{}家公司：'.format(company_count1))

                        medicine.connect_company_count = str(company_count1)

                    # if len(report_count) != 0 :
                    #     # 前三年的年报
                    #     report_urls = re.findall('年度报告</td><td><a class="link-click" href="(.*?)" target="_blank">详情</a>',data,re.S)[:3]
                    #     print('{},年报URLS：{}'.format(company_name,report_urls))
                    #     for i, report_url in enumerate(report_urls):
                    #         time.sleep(0.5)
                    #         report_content = ''
                    #         while 1:
                    #             try:
                    #                 report_content = requests.request(method='get', url=report_url, proxies=proxys[-1], headers=head,timeout=10).text
                    #                 # report_content = requests.request(method='get', url=report_url,headers=head,timeout=10).text
                    #                 year = re.findall(r'<title>.*?_(.*?)年报_企业年报查询 - 天眼查'.format(company_name), report_content, re.S)[0]
                    #
                    #                 break
                    #             except Exception as e:
                    #                 print(e)
                    #                 dl()
                    #
                    #         year = re.findall(r'<title>.*?_(.*?)年报_企业年报查询 - 天眼查'.format(company_name), report_content, re.S)[0]
                    #
                    #         busi_status = ''
                    #         if i == 0:
                    #             busi_status = re.findall(r'<td>企业经营状态</td><td>(.*?)</td>'.format(), report_content, re.S)[0]
                    #             medicine.current_1_busi_status = busi_status
                    #         if i == 1:
                    #             busi_status = re.findall(r'<td>企业经营状态</td><td>(.*?)</td>'.format(), report_content, re.S)[0]
                    #             medicine.current_2_busi_status = busi_status
                    #
                    #         insurance_count = re.findall(r'城镇职工基本养老保险</td><td .*?">(.*?)</td>'.format(), report_content, re.S)
                    #         if len(insurance_count) == 0:
                    #             insurance_count = '无社保信息'
                    #         else:
                    #             insurance_count = insurance_count[0]
                    #
                    #         if '2019' == year:
                    #             medicine.nineteen_insurance_count = insurance_count
                    #         elif '2018' == year:
                    #             medicine.eighteen_insurance_count = insurance_count
                    #         elif '2017' == year:
                    #             medicine.seventeen_insurance_count = insurance_count
                    #
                    #         print('--公司：{}---年报:{}---社保人数：{}---最近第{}年经营状态：{}'.format(company_name, year, insurance_count,i+1,busi_status))
                    #
                    #     medicine.is_have_year_report = 1
                    #     medicine.year_report_url = str(report_urls)

                    if 'brief_cancel_announcements_data' in data:
                        try:
                            easy_revoke_msg_date = re.findall(r'"announcement_end_date":"(.*?)"',data,re.S)[0]
                            easy_revoke_msg_result = re.findall(r'"brief_cancel_result":"(.*?)"',data,re.S)[0]

                            print('注销截至日期：{}'.format(easy_revoke_msg_date))
                            print('注销结果：{}'.format(easy_revoke_msg_result))

                            medicine.easy_revoke_end_date= easy_revoke_msg_date
                            medicine.easy_revoke_result = easy_revoke_msg_result
                        except Exception:
                            session.commit()
                            continue
                    session.commit()
                    print('**********************************************************************************')

            except Exception as e:
                print('捕获到了未知的异常，',e)
                continue
if __name__ == '__main__':
    main3()
