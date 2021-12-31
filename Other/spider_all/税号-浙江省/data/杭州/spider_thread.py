import time
from queue import Queue
import requests
from threading import Thread, Lock
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

headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
     'cookie':'TYCID=8cb689503de911eca504b7d76c61e034; ssuid=2849981472; sajssdk_2015_cross_new_user=1; bannerFlag=true; _ga=GA1.2.937145053.1636083386; _gid=GA1.2.772698768.1636083386; aliyungf_tc=68b24317138b378bceac4eb90325490d3d3bb05c070e5f7b5b59e1a51caf1cd3; acw_tc=2f6fc10216360834063056653e556628f62f62db6f1c1642417db52de5a475; csrfToken=8Xikfip1fIWD4iHUFJ0-Llap; show_activity_id_16=16; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1636083408; _gat_gtag_UA_123487620_1=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2218837076355%22%2C%22first_id%22%3A%2217cee2b4265a1e-0b7b49aac4b694-57b193e-2073600-17cee2b42665e8%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%2217cee2b4265a1e-0b7b49aac4b694-57b193e-2073600-17cee2b42665e8%22%7D; tyc-user-info={%22state%22:%220%22%2C%22vipManager%22:%220%22%2C%22mobile%22:%2218837076355%22}; tyc-user-info-save-time=1636084882227; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODgzNzA3NjM1NSIsImlhdCI6MTYzNjA4NDg4MSwiZXhwIjoxNjY3NjIwODgxfQ.iE73I69VffB9sx5AIDrL3jrIey1iDeXOJSxTqJFhdB30qcdPYgs1OMU7bRFUQ_9kQN1V4UUnhkJ9523yZTu9tw; tyc-user-phone=%255B%252218837076355%2522%252C%2522153%25209583%25201367%2522%255D; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1636084883'

}
import re,datetime
proxys = []
def dl():
    time.sleep(2)
    dlurl = 'http://dps.kdlapi.com/api/getdps/?orderid=922450652890692&num=1&pt=1&sep=1'
    resp = requests.get(dlurl).text
    if '今日' not in resp:
        resp = re.sub(r'\n', '', resp)
        proxy = {
            'https': resp
        }
        proxies_queue.put(proxy)
        logger.info(proxy)
        # proxys.append(proxy)
        # print(proxys[-1])
    else:
        t = datetime.datetime.replace(datetime.datetime.now() + datetime.timedelta(days=1), hour=9, minute=0, second=0)
        logger.info("休眠中，！！！明天9点运行》")
        time.sleep((t - datetime.datetime.now()).total_seconds())
        proxies_queue.put({'https':'117.43.52.160:21604'})

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

def get_log():
    import logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s|%(name)-6s|%(threadName)-6s|%(levelname)-8s|%(message)s')
    logger = logging.getLogger("spider")
    logger.setLevel(logging.INFO)

    # 创建handler
    handler1 = logging.FileHandler("spider.log")
    handler1.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s|%(name)-12s+ %(threadName)-8s +%(levelname)-8s++%(message)s')
    handler1.setFormatter(formatter)
    logger.addHandler(handler1)
    return logger

def add_white_ip():
    url = 'https://dev.kdlapi.com/api/getmyip?orderid=922450652890692&signature=p2u9t67sss8qlqx54aq9bchr1nfso2m4'
    local_ip = requests.get(url, headers=headers).json()['data']['ip']
    time.sleep(1)
    url = 'https://dev.kdlapi.com/api/getipwhitelist?orderid=922450652890692&signature=p2u9t67sss8qlqx54aq9bchr1nfso2m4'
    ipwhitelist = requests.get(url, headers=headers).json()['data']['ipwhitelist']
    if local_ip not in ipwhitelist:
        url = 'https://dev.kdlapi.com/api/setipwhitelist?orderid=922450652890692&signature=p2u9t67sss8qlqx54aq9bchr1nfso2m4&iplist='
        res = requests.get(url, headers=headers).json()
        logger.info(res)
        time.sleep(0.8)
        url = 'https://dev.kdlapi.com/api/setipwhitelist?orderid=922450652890692&signature=p2u9t67sss8qlqx54aq9bchr1nfso2m4'
        res = requests.get(url, headers=headers).json()
        logger.info(res)
        time.sleep(120)


def main(proxiess,thread_name):
    session = DBSession()
    while 1:
        if company_queue.empty():
            logger.info("线程--{}---结束".format(thread_name))
            break
        u = company_queue.get()
        company_num = u[0]
        company_name = u[1]
        url = 'https://tax.tianyancha.com/cloud-wechat/qrcode.json?gid={}&_=1634088420699'.format(company_num)
        while 1:
            try:
                time.sleep(2)
                response = requests.request(method='get', url=url, headers=headers,proxies=proxiess,timeout=7)
                if response.status_code == 200:
                    response = response.content.decode('utf-8')
                    break
                elif response.status_code == 500:
                    response = response.content.decode('utf-8')
                    break
                else:
                    dl()
                    proxiess = proxies_queue.get()
            except Exception as e:
                logger.info(e)
                if 'Tunnel connection failed: 407 White IP Failed' in str(e):

                    lock.acquire()
                    add_white_ip()
                    dl()
                    proxiess = proxies_queue.get()
                    lock.release()

                else:
                    dl()
                    proxiess = proxies_queue.get()

        if response == '{"error":"系统异常"}':
            logger.info("{} -- {} 显示系统异常，没有数据".format(company_num,company_name))
            continue
        try:
            c = json.loads(response).get('data')
            gid = c.get('gid')
            name = c.get('name')
            taxnum = c.get('taxnum')
            address = c.get('address').strip()
            phone = c.get('phone')
            bank = c.get('bank')
            bankAccount = c.get('bankAccount')
            times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        except Exception:
            logger.info("解析response时出现异常：{}".format(response))
            continue
        try:
            medi = Medicine(company_name=name,company_num=gid,tax_num=taxnum,reg_addr=address,phone=phone,bank=bank,bank_card=bankAccount,gmt_created=times,gmt_updated=times)
            logger.info('{} ----- {}-{}-{}-{}-{}-{}-{}-{}'.format(thread_name,str(proxiess),company_num,company_name,taxnum,address,phone,bank,bankAccount))
            session.add(medi)

            session.commit()
        except Exception:
            logger.info("数据库中断，重新连接")
            session = DBSession()


if __name__ == '__main__':
    logger = get_log()
    lock = Lock()
    proxies_queue = Queue(maxsize=5)
    company_queue = Queue(maxsize=1000000)
    # Tunnel connection failed: 407 White IP Failed
    import json
    with open(r'D:\projects\S_Git_proj\spider\Other\spider_all\税号-浙江省\data-second.txt', encoding='utf-8')as fp:
        content = json.loads(fp.read())
    index = 0
    for index, d in enumerate(content):
        if d[0] == '3278408489': #  下波数据 832339646
            logger.info("当前数据的索引位置:{} ".format(index))
            break

    data = content[index + 1:index + 400000]
    print(data)
    bloom = get_bloom()
    db_data = [i for i in data if i[0] not in bloom]
    le = len(db_data)
    logger.info("剩余公司数量：{}".format(le))
    # print(db_data)
    # exit()


    for q in db_data:
        company_queue.put(q)
    import threading
    dl()
    proxiess = proxies_queue.get()
    thread1 = threading.Thread(target=main, args=(proxiess,'thread-1'))
    thread2 = threading.Thread(target=main, args=(proxiess,'thread-2'))
    thread3 = threading.Thread(target=main, args=(proxiess,'thread-3'))
    thread4 = threading.Thread(target=main, args=(proxiess,'thread-4'))
    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()







