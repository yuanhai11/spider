import requests,pymysql,re,time
from sqlalchemy import Column, String, create_engine, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import threading
from queue import Queue
# 创建对象的基类:
Base = declarative_base()
# 定义User对象:
class Medicine(Base):
    # 表的名字:
    __tablename__ = 'spider_company_icp'

    # 表的结构:
    id = Column(Integer(), primary_key=True, autoincrement=True)
    company_id = Column(String(256))
    company_name = Column(String(256))
    web_domain = Column(String(256))
    web_index = Column(String(256))
    is_web_valid = Column(String(256))
    ip_addr_area = Column(String(256))
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
            time.sleep(1)
            continue
    time.sleep(2)
    resp = re.sub(r'\n', '', resp)
    proxy = {
        'https': resp
    }
    proxys.append(proxy)
    print(proxys[-1])

def thre(queue):
    session = DBSession()
    while 1:
        if queue.empty():
            break
        d = queue.get()
        domain = d.web_domain
        index = 'http://' + d.web_index
        company_name = d.company_name
        # if ind < 70:
        #     continue
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        }
        form_data = {
            'ip': domain
        }
        url = 'http://ip.tool.chinaz.com/'
        time.sleep(0.5)
        while 1:
            try:
                res = requests.request(method='post', url=url, data=form_data, headers=headers, proxies=proxys[-1],timeout=15).text
                addr = re.findall(r'<span class="Whwtdhalf w50-0">(.*?)</span>', res, re.S)
                break
            except Exception as e:
                dl()
                print(e)

        if len(addr) !=0:
            # lock.acquire()
            medicine = session.query(Medicine).filter(Medicine.web_domain == domain).first()
            from lxml import etree
            tree = etree.HTML(res)
            ip_addr = ''.join(tree.xpath('//span[@class="Whwtdhalf w30-0 lh24 tl ml80"]/p/text()'))
            print(ip_addr)
            medicine.ip_addr_area = ip_addr
            try:
                res = requests.request(method='get', url=index, headers=headers,timeout=15)
                if res.status_code == 200:
                    print(company_name, 'success')
                    medicine = session.query(Medicine).filter(Medicine.web_domain == domain).first()
                    medicine.is_web_valid = 1
                    session.commit()

            except Exception:
                print(company_name,'有IP地址，但网站访问不了。')
                session.commit()
        else:
            print(company_name,'no data')
def main():
    data = session.query(Medicine).all()[76525:]
    for i in data:
        print(i.company_name)
    # exit()
    queue = Queue(100000)
    dl()
    # lock = threading.Lock()
    for d in data:
        queue.put(d)
    print(queue.qsize())
    thread1 = threading.Thread(target=thre, args=(queue, ))
    thread2 = threading.Thread(target=thre, args=(queue, ))
    thread3 = threading.Thread(target=thre, args=(queue, ))
    thread4 = threading.Thread(target=thre, args=(queue, ))
    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()

if __name__ == '__main__':
    main()

