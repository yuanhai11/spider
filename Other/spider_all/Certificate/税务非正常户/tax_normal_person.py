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
    __tablename__ = 'spider_abnormal'

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
    while 1:
        try:
            dlurl = 'http://api.goubanjia.com/dynamic/get/d490a5d4debefc8980ae6ee4c4148552.html?sep=3'
            resp = requests.get(dlurl).text
            break
        except Exception:
            continue
    time.sleep(3)
    resp = re.sub(r'\n', '', resp)
    proxy = {
        'http': resp
    }
    proxys.append(proxy)
    print(proxys[-1])
# dl()

def get_response(url):
    while 1:
        try:
            res = requests.request(method='get',url=url,headers=headers,proxies=proxys[-1],timeout = 8).text
            break
        except Exception as e:
            dl()
    return res

def get_response_content(url):
    while 1:
        try:
            res = requests.request(method='get',url=url,headers=headers,proxies=proxys[-1],timeout = 8).content
            break
        except Exception:
            dl()
    return res
def get_response_code(url):
    while 1:
        try:
            res = requests.request(method='get', url=url, headers=headers, proxies=proxys[-1],timeout = 8)
            break
        except Exception:
            dl()
    return res
def main():
    sql = 'select id,unified_social_credit_code from spider_abnormal where unified_social_credit_code is not null '
    cursor.execute(sql)
    data = cursor.fetchall()
    sum = [[i[0],i[1]] for i in data]
    for index, co in enumerate(sum):
        flag = 1
        code = co[1]
        id = co[0]

        # if code == '913306813440397340':
        #     print(index)
        #     break
        # continue
        if index < 126133+1:
            continue
        while 1:
            try:
                time.sleep(2)
                url = 'https://etax.zhejiang.chinatax.gov.cn/zjgfdacx/kaptcha.jpg?time={}000'.format(int(time.time()))

                data = get_response_content(url)
                with open('1.png', 'wb')as fp:
                    fp.write(data)
                time.sleep(1)
                text = pytesseract.image_to_string(Image.open("1.png"), lang="eng")[:4]
                url = 'https://etax.zhejiang.chinatax.gov.cn/zjgfdacx/checkCaptcha.do?captchaReceived={}'.format(text)
                response = get_response_code(url)
                print(code,response)
                if response.status_code == 200:
                    time.sleep(2)
                    url = 'https://etax.zhejiang.chinatax.gov.cn/zjgfdacx/nsrztcx/query/{}/{}.do'.format(code, text)
                    company_status = json.loads(get_response(url))['resultObj']
                    if len(company_status) == 0:
                        print('查询数据为空,index:{}'.format(index))
                        break
                    else:
                        company_status = company_status[0]['NSRZTMC']

                    medicine = session.query(Medicine).filter(Medicine.id == id).first()
                    medicine.tax_status = company_status
                    print('统一社会信用代码：{}，税务状态：{},index:{}'.format(code,company_status,index))
                    session.commit()
                    break
                else:
                    print('图像识别失败！！！')

            except Exception as e:
                print(e)
                print('获取税务状态失败 | 其他原因！',code)
                time.sleep(5)
                if flag == 10: # 请求10次，break出去
                    break
                flag+=1

if __name__ == '__main__':
    conn = pymysql.connect(user='root',password='BOOT-xwork1024',database='spider',port=3306,host='192.168.2.97')
    cursor = conn.cursor()
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
        'cookie':'yfx_c_g_u_id_10001429=_ck20112513485615521917868414956; yfx_f_l_v_t_10001429=f_t_1606283336551__r_t_1611107880614__v_t_1611107880614__r_c_7; aliyungf_tc=a1dbf30bad53ac7cf68838a7f6b23bda17553c4e94dde422c852603b6e4ee9d8; acw_tc=76b20f8f16124226048952611e7479913f4cb49dff908999aaa65859fbab6f; DTL_SESSION_ID=4defe244-a432-4e86-914f-f17203cf1689',
    }
    main()
