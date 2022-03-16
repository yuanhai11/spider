import json
import time
import requests
from sqlalchemy import Column, String, create_engine,Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# 创建对象的基类:
Base = declarative_base()
# 定义User对象:
class Medicine(Base):
    # 表的名字:
    __tablename__ = 'company_title'

    # 表的结构:
    id = Column(Integer(), primary_key=True,autoincrement=True)
    company_name = Column(String(256))
    company_num = Column(String(256))
    tax_num = Column(String(256))
    reg_addr = Column(String(256))
    phone = Column(String(256))
    bank = Column(String(256))
    bank_card = Column(String(256))

    gmt_created = Column(String(256))
    gmt_updated = Column(String(256))
# 初始化数据库连接:
engine = create_engine('mysql+pymysql://root:BOOT-xwork1024@192.168.2.97:3306/spider')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
# 创建session对象:
session = DBSession()
# exitFlag = 0
#
# class myThread (threading.Thread):
#     def __init__(self, threadID, name, counter):
#         threading.Thread.__init__(self)
#         self.threadID = threadID
#         self.name = name
#         self.counter = counter
#     def run(self):
#         print ("开始线程：" + self.name)
#         print_time(self.name, self.counter, 5)
#         print ("退出线程：" + self.name)
#
# def print_time(threadName, delay, counter):
#     while counter:
#         if exitFlag:
#             threadName.exit()
#         time.sleep(delay)
#         print ("%s: %s" % (threadName, time.ctime(time.time())))
#         counter -= 1
#
# # 创建新线程
# thread1 = myThread(1, "Thread-1", 1)
# thread2 = myThread(2, "Thread-2", 2)
#
# # 开启新线程
# thread1.start()
# thread2.start()
# thread1.join()
# thread2.join()
# print ("退出主线程")


headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
    'cookie':'TYCID=8cb689503de911eca504b7d76c61e034; ssuid=2849981472; sajssdk_2015_cross_new_user=1; bannerFlag=true; _ga=GA1.2.937145053.1636083386; _gid=GA1.2.772698768.1636083386; aliyungf_tc=68b24317138b378bceac4eb90325490d3d3bb05c070e5f7b5b59e1a51caf1cd3; acw_tc=2f6fc10216360834063056653e556628f62f62db6f1c1642417db52de5a475; csrfToken=8Xikfip1fIWD4iHUFJ0-Llap; show_activity_id_16=16; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1636083408; _gat_gtag_UA_123487620_1=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2218837076355%22%2C%22first_id%22%3A%2217cee2b4265a1e-0b7b49aac4b694-57b193e-2073600-17cee2b42665e8%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%2217cee2b4265a1e-0b7b49aac4b694-57b193e-2073600-17cee2b42665e8%22%7D; tyc-user-info={%22state%22:%220%22%2C%22vipManager%22:%220%22%2C%22mobile%22:%2218837076355%22}; tyc-user-info-save-time=1636084882227; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODgzNzA3NjM1NSIsImlhdCI6MTYzNjA4NDg4MSwiZXhwIjoxNjY3NjIwODgxfQ.iE73I69VffB9sx5AIDrL3jrIey1iDeXOJSxTqJFhdB30qcdPYgs1OMU7bRFUQ_9kQN1V4UUnhkJ9523yZTu9tw; tyc-user-phone=%255B%252218837076355%2522%252C%2522153%25209583%25201367%2522%255D; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1636084883'
}
import re,datetime
proxys = []
def dl():
    time.sleep(2)
    try:
        dlurl = 'http://api.ip.data5u.com/dynamic/get.html?order=fba1729fce7d27397dc2db1dc5db9977&random=2&sep=3'
        resp = requests.get(dlurl).text
        resp = re.sub(r'\n', '', resp)
        proxy = {
            'https': resp
        }
        proxys.append(proxy)
        print(proxys[-1])
    except:
        dl()

def add_white():
    while 1:
        try:
            confirm_ip_url = 'http://soft.data5u.com/wl/myip/fba1729fce7d27397dc2db1dc5db9977.html'
            confirm_ip = requests.get(url=confirm_ip_url, headers=headers).text
            white_lists_url = 'http://soft.data5u.com/wl/mywhitelist/fba1729fce7d27397dc2db1dc5db9977.html'
            time.sleep(3)
            white_lists_data = requests.get(url=white_lists_url, headers=headers).text
            if confirm_ip not in white_lists_data:
                add_white_url = 'http://soft.data5u.com/wl/setip/fba1729fce7d27397dc2db1dc5db9977.html?ips={}&clear=true'.format(
                    confirm_ip)
                time.sleep(10)
                res = requests.get(url=add_white_url, headers=headers).text
                print("add white IP success ，please waiting 70 seconds")
                time.sleep(70)
                break
        except Exception:
            time.sleep(2)
            continue

def main():
    dl()
    for u in db_data:
        company_num = u[0]
        company_name = u[1]

        url = 'https://tax.tianyancha.com/cloud-wechat/qrcode.json?gid={}&_=1634088420699'.format(company_num)
        while 1:
            try:
                time.sleep(1.5)
                response = requests.request(method='get', url=url, headers=headers,proxies=proxys[-1],timeout=7)
                if response.status_code == 200:
                    response = response.content.decode('utf-8')
                    break
                elif response.status_code == 500:
                    response = response.content.decode('utf-8')
                    break
                else:
                    dl()
            except Exception as e:
                print(e)
                if 'Tunnel connection failed: 407 Proxy Authentication Required' in str(e):
                    add_white()
                dl()

        if response == '{"error":"系统异常"}':
            print(company_num,company_name,'没有数据。')
            continue
        try:
            c = json.loads(response).get('data')

            gid = c.get('gid')
            name = c.get('name')
            taxnum = c.get('taxnum')
            address = c.get('address')
            phone = c.get('phone')
            bank = c.get('bank')
            bankAccount = c.get('bankAccount')
            times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            medi = Medicine(company_name=name,company_num=gid,tax_num=taxnum,reg_addr=address,phone=phone,bank=bank,bank_card=bankAccount,gmt_created=times,gmt_updated=times)
            print(company_num,company_name,taxnum,address,phone,bank,bankAccount)
            session.add(medi)
            session.commit()
        except:
            continue

def get_bloom():
    import pymysql
    db = pymysql.connect(host="192.168.2.97", user="root", password='BOOT-xwork1024', database="spider", port=3306)
    cursor = db.cursor()
    sql = "select company_num from company_title"
    cursor.execute(sql)
    db_data = cursor.fetchall()
    data = [i[0] for i in db_data]
    from pybloom_live import ScalableBloomFilter
    bloom = ScalableBloomFilter(initial_capacity=100000, error_rate=0.001)
    for bl in data:
        bloom.add(bl)
    db.close()
    return bloom

if __name__ == '__main__':
    with open(r'D:\projects\S_Git_proj\spider\Other\spider_all\税号-浙江省\data-second.txt', encoding='utf-8')as fp:
        content = json.loads(fp.read())
    index = 0
    for index, d in enumerate(content):
        if d[0] == '3019258035': # 3034390094
            print("当前数据的索引位置:{} ".format(index))
            break
    data = content[index + 1:index + 400000]
    print(data)
    bloom = get_bloom()
    db_data = [i for i in data if i[0] not in bloom]
    le = len(db_data)
    print(le)
    main()
