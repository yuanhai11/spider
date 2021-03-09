'''
非正常户数据，进行税务查询，获取最近的税务状态。
'''
import pymysql
import pytesseract
from PIL import Image
import time,re,json
import requests
from sqlalchemy import Column, String, create_engine, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# 创建对象的基类:
Base = declarative_base()
# 定义User对象:
class Medicine(Base):
    # 表的名字:
    __tablename__ = 'spider_abnormal_per_hz'

    # 表的结构:
    id = Column(Integer(), primary_key=True, autoincrement=True)
    unified_social_credit_code = Column(String(256))
    tax_status = Column(String(256))

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
    time.sleep(3)
    resp = re.sub(r'\n', '', resp)
    proxy = {
        'https': resp
    }
    proxys.append(proxy)
    print(proxys[-1])

def main():
    sql = 'select * from spider_abnormal_per_hz where company_id is not null'
    cursor.execute(sql)
    data = cursor.fetchall()
    sum = [i[2] for i in data  if i[2] != 'none' ]

    for index, code in enumerate(sum):
        if index < 5000:
            continue
        # if index == 5000:
        #     session.commit()
            # exit()

        while 1:
            try:
                time.sleep(2)
                url = 'https://etax.zhejiang.chinatax.gov.cn/zjgfdacx/kaptcha.jpg?time={}000'.format(int(time.time()))
                data = requests.get(url, headers=headers).content
                with open('1.png', 'wb')as fp:
                    fp.write(data)
                time.sleep(1)
                text = pytesseract.image_to_string(Image.open("1.png"), lang="eng")[:4]
                url = 'https://etax.zhejiang.chinatax.gov.cn/zjgfdacx/checkCaptcha.do?captchaReceived={}'.format(text)
                response = requests.get(url=url, headers=headers)
                print(response)
                if response.status_code == 200:
                    time.sleep(2)
                    url = 'https://etax.zhejiang.chinatax.gov.cn/zjgfdacx/nsrztcx/query/{}/{}.do'.format(code, text)
                    company_status = json.loads(requests.request(method='get',url=url, headers=headers).text)['resultObj']
                    if len(company_status) == 0:
                        print('查询数据为空')
                        break
                    else:
                        company_status = company_status[0]['NSRZTMC']

                    medicine = session.query(Medicine).filter(Medicine.unified_social_credit_code == code).first()
                    medicine.tax_status = company_status
                    print('统一社会信用代码：{}，税务状态：{}'.format(code,company_status))
                    break
                else:
                    print('图像识别失败！！！')

            except Exception:
                print('获取税务状态失败 | 其他原因！')
                time.sleep(5)
    session.commit()


if __name__ == '__main__':
    conn = pymysql.connect(user='root',password='BOOT-xwork1024',database='spider',port=3306,host='192.168.2.97')
    cursor = conn.cursor()
    dic = {}
    sum = []
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
        'cookie':'yfx_c_g_u_id_10001429=_ck20112513485615521917868414956; yfx_f_l_v_t_10001429=f_t_1606283336551__r_t_1606283336551__v_t_1606283336551__r_c_0; aliyungf_tc=AQAAAMdIjBAXRQsA+fB3fZPv5CK0UqWx; acw_tc=707c9f9e16065255862145021e0fa20a30d37a518e9f5d5753070dab38e6ea; DTL_SESSION_ID=af62148d-d35e-44ba-879b-a2fed8a2e9b5'
    }
    main()
