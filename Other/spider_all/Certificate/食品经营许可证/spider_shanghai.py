'''
食品许可证：上海
'''
import re
import time
import requests,pymysql
import base64
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pksc1_v1_5
from Crypto.PublicKey import RSA
from sqlalchemy import Column, String, create_engine,Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# 创建对象的基类:
Base = declarative_base()
# 定义User对象:

class Medicine(Base):
    # 表的名字:
    __tablename__ = 'spider_qualification'
    id = Column(Integer(), primary_key=True,autoincrement=True)
    license_num = Column(String(256))
    company_name = Column(String(256))
    project_name = Column(String(256))
    cover_range = Column(String(256))
    valid_date = Column(String(256))
    invalid_date = Column(String(256))
    area = Column(Integer())
    addr = Column(Integer())
    busi_addr = Column(Integer())
    reg_authority = Column(Integer())

    gmt_created = Column(String(256))
    gmt_updated = Column(String(256))
    company_id = Column(String(256))
    license_name = Column(String(256))

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
    time.sleep(3)
    resp = re.sub(r'\n', '', resp)
    proxy = {
        'https': resp
    }
    proxys.append(proxy)
    print(proxys[-1])
dl()

def encrpt(password, public_key):
    rsakey = RSA.importKey(public_key)
    cipher = Cipher_pksc1_v1_5.new(rsakey)
    cipher_text = base64.b64encode(cipher.encrypt(password.encode()))
    return cipher_text.decode()

def get_updated():
    db = pymysql.connect(host="192.168.2.97", user="root", password='BOOT-xwork1024', database="spider", port=3306)
    cursor = db.cursor()
    sql = "select license_num from spider_qualification"
    cursor.execute(sql)
    db_data = cursor.fetchall()
    data = [i[0] for i in db_data]
    from pybloom_live import ScalableBloomFilter
    bloom = ScalableBloomFilter(initial_capacity=1000000, error_rate=0.001)
    for bl in data:
        bloom.add(bl)
    return bloom
def main():
    bloom = get_updated()
    url = 'http://xk.scjgj.sh.gov.cn/xzxk_wbjg/query/public/licInfo'
    for page in range(9330,9332): # 219页获取不到
        response = ""
        num = 1
        while 1:
            try:
                time.sleep(1.3)
                sign = str(int(time.time())) + '000'
                password = encrpt(sign, public_key)
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
                    'sign': password,
                    'Cookie': "_gscu_872847596=09224904520vb611; _gscbrs_872847596=1",
                    'Content-Type': 'application/json;charset=UTF-8',
                    'timestamp': sign
                }
                data = {
                    'fzjg': "",
                    'page': page,
                    'rows': 50,
                    'zszl': "00103"
                }
                response = requests.request(method='post', url=url, headers=headers,json=data,proxies=proxys[-1],timeout=10)
                if response.status_code == 200:
                    response = response.json()
                    code = response['code']
                    if code == 200:
                        print('获取信息成功！！！')
                        print('break！！！')
                        data = response['data']['resultList']
                        if data == None:
                            print('error，sign 出现问题！！！')
                            if num == 3:
                                break
                            num+=1
                        else:
                            break
            except Exception as e:
                print(e)
                dl()
        if data == None:
            fail = '三次重试之后，第{}页 数据依旧没有获取到 '.format(page)
            print(fail)
            with open('fail_log_shanghai.txt', 'a', encoding='utf-8')as fp:
                fp.write(fail + '\n')
            continue
        for d in data:
            license_num = d['xkzbh']
            company_name = d['jyzmcASCIIstr']
            addr = d['zs']
            busi_addr = d['jycs']
            reg_authority = d['fzjgmc']
            valid_date = d['yxqq']
            invalid_date = d['yxqz']
            times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            if license_num not in bloom:

                print('数据在第',page,'页！',company_name,license_num,addr,busi_addr,reg_authority,valid_date,invalid_date)
                medicine = Medicine(license_num=license_num,company_name=company_name,addr=addr,busi_addr=busi_addr,invalid_date=invalid_date
                                    ,area=2,reg_authority=reg_authority,valid_date=valid_date,license_name='食品经营许可证',
                                    gmt_created=times,gmt_updated=times,
                                    )
                session.add(medicine)
            else:
                print('重复数据！！！')
        session.commit()

if __name__ == '__main__':
    # key需要修改成自己的
    key = 'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCMFPpXdR/mA3FOyB2L6HaxKRMBDWAPWA2j3qjBdDCu4lTiJ+ip9PwJW3XtaBonyeBdo22AYhMkLjAzfJnoFOFtbOf+oF4Ht4pgR3csXQqJsgvMSPInzexdayTD5Vg/quIgLlWVBLn670O2YOHd9/Ojc2GidoJnUO4D8YlfSd/sEwIDAQAB'
    public_key = '-----BEGIN PUBLIC KEY-----\n' + key + '\n-----END PUBLIC KEY-----'
    main()
