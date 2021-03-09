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
        try:
            # if index < 254:
            #     continue
            head = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
            }
            url = 'https://www.tianyancha.com/search?key={}'.format(company_name)
            detail_url = ""
            while 1:
                try:
                    res = requests.request(method='get', url=url,proxies=proxys[-1],headers=head,timeout=10).text
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
                        # check = re.findall(r'<h1 class="name">(.*?)</h1>',text,re.S)[0]
                        break
                    except Exception:
                        time.sleep(2)
                        dl()

                medicine = session.query(Medicine).filter(Medicine.company_name == company_name).first()
                # print(text)
                report_count = re.findall(r'企业年报<span class="itemnumber  -company">(.*?)</span>',data,re.S)
                company_count = re.findall(r'他有<span class=".*?">(.*?)</span>家公司', data, re.S)
                company_count1 = re.findall(r'任职<span class=".*?">(.*?)</span>家', data, re.S)
                reason = re.findall(r'<div>注销原因：(.*?)</div>', data, re.S)
                date = re.findall(r'<div>注销日期：(.*?)</div>', data, re.S)


                reason1 = re.findall(r'<div>吊销原因：(.*?)</div>', data, re.S)
                date1 = re.findall(r'<div>吊销日期：(.*?)</div>', data, re.S)

                print(company_name)
                # print(text)
                if len(report_count) != 0 :
                    # 前三年的年报
                    report_urls = re.findall('年度报告</td><td><a class="link-click" href="(.*?)" target="_blank">详情</a>',data,re.S)[:3]
                    print('{},年报URLS：{}'.format(company_name,report_urls))

                    medicine.is_have_year_report = 1
                    medicine.year_report_url = str(report_urls)

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