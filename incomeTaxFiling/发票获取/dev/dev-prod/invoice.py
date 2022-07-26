#encoding=utf-8
import random,re
import logging.config
import time
from ctypes import windll
# 加入pywintypes，打包成功
from threading import Lock

from Crypto.Cipher import AES
# 导入config里的变量信息
from decouple import config
from kafka import KafkaConsumer
from logger_manager import LoggerManager
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, create_engine, Integer
from sqlalchemy.orm import sessionmaker

import requests, json
# kafka server conf
KAFKA_SERVER = config("KAFKA_SERVER").split(",")
KAFKA_TOPIC = config("KAFKA_TOPIC")


CALL_BACK_HOST = config('CALL_BACK_HOST')
CALL_BACK_URL = config('CALL_BACK_URL')
LOGIN_API = config('LOGIN_API')
MAP_KEYS = windll.user32.MapVirtualKeyA

LoggerManager.init_logging("logs/invoice.log", need_mail=False, need_console=True)
logger = logging.getLogger('loggerManager')
logger.setLevel(logging.DEBUG)

# 创建对象的基类:
Base = declarative_base()
# 定义User对象:
class Medicine(Base):
    # 表的名字:
    __tablename__ = 'tax_invoice_kafka'
    # 表的结构:
    id = Column(Integer(), primary_key=True, autoincrement=True)
    company_name = Column(String(256))
    date = Column(String(256))

# 初始化数据库连接:
# engine = create_engine('mysql+pymysql://root:BOOT-xwork1024@192.168.2.96:3306/dev_spider')

engine = create_engine('mysql+pymysql://root:BOOT-xwork1024@192.168.2.99:3306/prod_spider')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
# 创建session对象:
session = DBSession()

def dl(proxys):
    time.sleep(1)
    try:
        dlurl = 'http://api.ip.data5u.com/dynamic/get.html?order=fba1729fce7d27397dc2db1dc5db9977&random=2&sep=3'
        resp = requests.get(dlurl).text
        resp = re.sub(r'\n', '', resp)
        proxy = {
            'https': resp
        }
        proxys[0] = proxy
        logger.info(proxys)
    except Exception as e:
        dl(proxys)

def main():
    from concurrent.futures import ThreadPoolExecutor
    executor = ThreadPoolExecutor(max_workers=5)
    result_list = []
    # consumer
    logger.info("kafka server is {},topic is [{}]".format(KAFKA_SERVER, KAFKA_TOPIC))
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_SERVER,
        group_id='group_1',
        auto_offset_reset='earliest',
        enable_auto_commit=False,
        consumer_timeout_ms=3 * 1000,
        max_poll_interval_ms=3000000
    )

    logger.info("rpa worker started!")

    while 1:
        if len(result_list) >= 5:
            for index, i in enumerate(result_list):
                if i.done():
                    result_list.remove(result_list[index])
            time.sleep(1)
            continue
        try:
            # message = consumer.poll()
            message = next(consumer)
            consumer.commit()
            # logger.info(message)
            # continue
            message_str = message.value.decode("utf-8").replace(" ", "").replace("\t", "")
            logger.info("receive message: {}".format(message_str))
            message_dict = json.loads(message_str)
            l = [message_dict["taxAccount"], message_dict["taxPwd"],
                 message_dict["handleTaxName"], message_dict["handleTaxPwd"],
                 message_dict["companyId"], message_dict["companyName"],
                 message_dict["tenant_code"],message_dict['localDate']
                 ]

            company_name = message_dict["companyName"]
            date = message_dict["localDate"]
            # while 1:
            #     try:
            #         s = session.query(Medicine).filter(Medicine.company_name==company_name,Medicine.date==date).first()
            #         break
            #     except Exception as e:
            #         session = DBSession()
            #
            # if s:
            #     logger.info(company_name + "该公司已经执行过了！")
            #     continue
            result = executor.submit(handle_message, l)
            result_list.append(result)
            # me = Medicine(company_name=company_name, date=date)
            # session.add(me)
            # session.commit()

        except StopIteration as se:
            time.sleep(2)
        except Exception as e:
            logger.error(e)


def handle_message(l):

    proxys = [{'https':'114.97.184.243:47916'}]

    data = {
        "handleTaxName": l[2],
        "handleTaxPwd": l[3],
        "taxAccount": l[0],
        "taxPwd": l[1]
    }
    import_data = {
        "company_id": l[4],
        "company_name": l[5],
        "tenant_code": l[6],
        "localDate":l[7]
    }
    cookie = None
    for i in range(6):
        response = get_login_cookie(data)
        if not response or response['data']['name'] != '0':
            logger.info("{}获取cookie中失败,retry{}次".format(l[5],i))
            continue
        else:
            cookie = response['data']['value'][7:]
            break

    if cookie:
        spider(cookie, import_data,proxys)


def get_login_cookie(data):
    url = LOGIN_API
    headers2 = {
        'Content-Type': 'application/json;charset=UTF-8',
        'Host': CALL_BACK_HOST,
        'Connection': 'close',
    }
    try:
        time.sleep(1)
        response = requests.post(url=url, json=data, headers=headers2, timeout=10)
    except Exception:
        return None

    aaa = response.text
    response.close()
    return json.loads(aaa)

def spider(cookie, import_data,proxys):
    company_id = import_data['company_id']
    company_name = import_data['company_name']
    tenant_code = import_data['tenant_code']
    localDate = import_data['localDate'].replace("-","")

    for types,names in [
        ['tydzfp','浙江省通用电子发票'],
        ['zzsdzfp','增值税电子普通发票'],
        ['zzsptfp','增值税普通发票'],
        ['zzszyfp','增值税专用发票'],
        ['zzsdzzp','增值税电子专票'],
        ['tyjdfp','通用机打发票'],
        ['jdcxsfp','机动车销售发票'],
        ['escfp','二手车发票'],
        ['sghdfp','手工核定发票'],
        ['czcfp','出租车发票'],
        ]:

        for se in ['SPF','KPF']:

            select_type = se
            headers = {
                'Content-Type': 'application/json;charset=UTF-8',
                'Cookie': cookie,
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
            }
            start = localDate[:6]
            data = {
                'rqq': localDate,
                'rqz': localDate,
                'fplx': types,
                'cxfs': select_type
            }
            time.sleep(0.5)
            result = get_data_by_proxy(headers,data,types,select_type,localDate,proxys)
            logger.info("{},{},{},{},{}".format(company_name,proxys,names,se,result))
            if result == None or result==[]:
                continue
            sss = []
            for re in result:
                ss = {}

                HJ = except_deal(re,"HJ")
                WLFPH = except_deal(re,"WLFPH")
                HWMC = except_deal(re,"HWMC")
                KPRQ = except_deal(re,"KPRQ")
                KPR = except_deal(re,"KPR")
                FPHM = except_deal(re,"FPHM")
                SE = except_deal(re, "SE")
                FPDM = except_deal(re, "FPDM")
                MC = except_deal(re, "MC")
                SBH = except_deal(re, "SBH")
                BZ = except_deal(re, "BZ")
                SL = except_deal(re, "SL")
                FPZL = names

                ss['invoice_amount'] = HJ
                ss['network_invoice_number'] = WLFPH
                ss['goods_name'] = HWMC
                ss['invoice_date'] = KPRQ
                ss['invoice_user'] = KPR
                ss['invoice_number'] = FPHM
                ss['tax_amount'] = SE
                ss['invoice_code'] = FPDM

                ss['invoice_status'] = BZ
                ss['tax_rate'] = SL
                ss['invoice_type'] = FPZL
                ss['tenant_code'] = tenant_code
                ss['company_id'] = company_id
                ss['company_name'] = company_name
                ss['tax_date'] = start
                ss['is_deleted'] = 0
                ss['declaration_id'] = 0

                if select_type == "KPF":
                    ss['select_type'] = 0
                    ss['buyer_name'] = MC
                    ss['buyer_id'] = SBH
                    ss['seller_name'] = None
                    ss['seller_id'] = None

                else:
                    ss['select_type'] = 1
                    ss['buyer_name'] = None
                    ss['buyer_id'] = None
                    ss['seller_name'] = MC
                    ss['seller_id'] = SBH

                sss.append(ss)

            # res = callback_saas(sss)
            # logger.info(res)

def add_white():
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
    }
    while 1:
        try:
            confirm_ip_url = 'http://soft.data5u.com/wl/myip/fba1729fce7d27397dc2db1dc5db9977.html'
            confirm_ip = requests.get(url=confirm_ip_url, headers=headers).text
            white_lists_url = 'http://soft.data5u.com/wl/mywhitelist/fba1729fce7d27397dc2db1dc5db9977.html'
            time.sleep(1)
            white_lists_data = requests.get(url=white_lists_url, headers=headers).text
            if confirm_ip not in white_lists_data:
                add_white_url = 'http://soft.data5u.com/wl/setip/fba1729fce7d27397dc2db1dc5db9977.html?ips={}&clear=true'.format(
                    confirm_ip)
                time.sleep(3)
                res = requests.get(url=add_white_url, headers=headers).text
                logger.info("add white IP success ，please waiting 70 seconds")
                time.sleep(100)
            break
        except Exception:
            time.sleep(2)
            continue


def get_data_by_proxy(headers,data,types,select_type,localDate,proxys):

    for rr in range(20):
        try:
            result = requests.get(
                'https://etax.zhejiang.chinatax.gov.cn/zjgfdacx/fpxxcx/query.do?rqq={}&rqz={}&fplx={}&cxfs={}&kpfxx=&fpdm=&fphm='.format(
                    localDate,localDate, types, select_type)
                , data=data,
                headers=headers, proxies = proxys[-1],timeout=8
            ).json()['resultObj']
            break
        except Exception as e:
            logger.info("get_data error")
            if rr >= 19:
                result = None
                break
            if 'Tunnel connection failed: 407 Proxy Authentication Required' in str(e):
                lock.acquire()
                add_white()
                lock.release()

            dl(proxys)

    return result


def callback_saas(data):
    headers2 = {
        'Content-Type': 'application/json;charset=UTF-8',
        'Host': CALL_BACK_HOST,
        'Connection': 'close',
    }
    data = {
        "data": data
    }

    purl = CALL_BACK_URL

    try:
        response = requests.post(url=purl, json=data, headers=headers2, timeout=10)
        aaa = response.text
        response.close()
    except Exception as  e:
        aaa = "error"

    return aaa

def except_deal(re,field):
    try:
        ff = re[field]
    except Exception:
        ff = ''

    return ff


if __name__ == '__main__':
    # data = [{'invoice_amount': '99000', 'network_invoice_number': '', 'goods_name': '*交通管制设备*机动车远光灯光学检测仪', 'invoice_date': '2021-10-20 17:39:01.0', 'invoice_user': '', 'invoice_number': '29319068', 'tax_amount': '11389.38', 'invoice_code': '033002000711', 'invoice_status': '正常', 'tax_rate': '0.13', 'invoice_type': '增值税电子普通发票', 'tenant_code': 'ZH-383-20191217145410', 'company_id': '345', 'company_name': '浙江安谐智能科技有限公司', 'tax_date': '202110', 'is_deleted': 0, 'declaration_id': 0, 'select_type': 0, 'buyer_name': '徐州市公安局交通警察支队', 'buyer_id': '11320300014051773Q', 'seller_name': None, 'seller_id': None}, {'invoice_amount': '99000', 'network_invoice_number': '', 'goods_name': '*交通管制设备*高清卡口抓拍机', 'invoice_date': '2021-10-20 17:39:01.0', 'invoice_user': '', 'invoice_number': '29319068', 'tax_amount': '11389.38', 'invoice_code': '033002000711', 'invoice_status': '正常', 'tax_rate': '0.13', 'invoice_type': '增值税电子普通发票', 'tenant_code': 'ZH-383-20191217145410', 'company_id': '345', 'company_name': '浙江安谐智能科技有限公司', 'tax_date': '202110', 'is_deleted': 0, 'declaration_id': 0, 'select_type': 0, 'buyer_name': '徐州市公安局交通警察支队', 'buyer_id': '11320300014051773Q', 'seller_name': None, 'seller_id': None}, {'invoice_amount': '88500', 'network_invoice_number': '', 'goods_name': '*交通管制设备*主控箱', 'invoice_date': '2021-10-20 18:02:10.0', 'invoice_user': '', 'invoice_number': '29319069', 'tax_amount': '10181.42', 'invoice_code': '033002000711', 'invoice_status': '正常', 'tax_rate': '0.13', 'invoice_type': '增值税电子普通发票', 'tenant_code': 'ZH-383-20191217145410', 'company_id': '345', 'company_name': '浙江安谐智能科技有限公司', 'tax_date': '202110', 'is_deleted': 0, 'declaration_id': 0, 'select_type': 0, 'buyer_name': '徐州市公安局交通警察支队', 'buyer_id': '11320300014051773Q', 'seller_name': None, 'seller_id': None}, {'invoice_amount': '88500', 'network_invoice_number': '', 'goods_name': '*交通管制设备*杆件及基础', 'invoice_date': '2021-10-20 18:02:10.0', 'invoice_user': '', 'invoice_number': '29319069', 'tax_amount': '10181.42', 'invoice_code': '033002000711', 'invoice_status': '正常', 'tax_rate': '0.13', 'invoice_type': '增值税电子普通发票', 'tenant_code': 'ZH-383-20191217145410', 'company_id': '345', 'company_name': '浙江安谐智能科技有限公司', 'tax_date': '202110', 'is_deleted': 0, 'declaration_id': 0, 'select_type': 0, 'buyer_name': '徐州市公安局交通警察支队', 'buyer_id': '11320300014051773Q', 'seller_name': None, 'seller_id': None}, {'invoice_amount': '88500', 'network_invoice_number': '', 'goods_name': '*交通管制设备*施工及辅材', 'invoice_date': '2021-10-20 18:02:10.0', 'invoice_user': '', 'invoice_number': '29319069', 'tax_amount': '10181.42', 'invoice_code': '033002000711', 'invoice_status': '正常', 'tax_rate': '0.13', 'invoice_type': '增值税电子普通发票', 'tenant_code': 'ZH-383-20191217145410', 'company_id': '345', 'company_name': '浙江安谐智能科技有限公司', 'tax_date': '202110', 'is_deleted': 0, 'declaration_id': 0, 'select_type': 0, 'buyer_name': '徐州市公安局交通警察支队', 'buyer_id': '11320300014051773Q', 'seller_name': None, 'seller_id': None}, {'invoice_amount': '88500', 'network_invoice_number': '', 'goods_name': '*交通管制设备*常亮补光灯', 'invoice_date': '2021-10-20 18:02:10.0', 'invoice_user': '', 'invoice_number': '29319069', 'tax_amount': '10181.42', 'invoice_code': '033002000711', 'invoice_status': '正常', 'tax_rate': '0.13', 'invoice_type': '增值税电子普通发票', 'tenant_code': 'ZH-383-20191217145410', 'company_id': '345', 'company_name': '浙江安谐智能科技有限公司', 'tax_date': '202110', 'is_deleted': 0, 'declaration_id': 0, 'select_type': 0, 'buyer_name': '徐州市公安局交通警察支队', 'buyer_id': '11320300014051773Q', 'seller_name': None, 'seller_id': None}, {'invoice_amount': '88500', 'network_invoice_number': '', 'goods_name': '*交通管制设备*爆闪灯', 'invoice_date': '2021-10-20 18:02:10.0', 'invoice_user': '', 'invoice_number': '29319069', 'tax_amount': '10181.42', 'invoice_code': '033002000711', 'invoice_status': '正常', 'tax_rate': '0.13', 'invoice_type': '增值税电子普通发票', 'tenant_code': 'ZH-383-20191217145410', 'company_id': '345', 'company_name': '浙江安谐智能科技有限公司', 'tax_date': '202110', 'is_deleted': 0, 'declaration_id': 0, 'select_type': 0, 'buyer_name': '徐州市公安局交通警察支队', 'buyer_id': '11320300014051773Q', 'seller_name': None, 'seller_id': None}, {'invoice_amount': '88500', 'network_invoice_number': '', 'goods_name': '*交通管制设备*移动警务终端', 'invoice_date': '2021-10-20 18:02:10.0', 'invoice_user': '', 'invoice_number': '29319069', 'tax_amount': '10181.42', 'invoice_code': '033002000711', 'invoice_status': '正常', 'tax_rate': '0.13', 'invoice_type': '增值税电子普通发票', 'tenant_code': 'ZH-383-20191217145410', 'company_id': '345', 'company_name': '浙江安谐智能科技有限公司', 'tax_date': '202110', 'is_deleted': 0, 'declaration_id': 0, 'select_type': 0, 'buyer_name': '徐州市公安局交通警察支队', 'buyer_id': '11320300014051773Q', 'seller_name': None, 'seller_id': None}, {'invoice_amount': '103500', 'network_invoice_number': '', 'goods_name': '*交通管制设备*流媒体转发服务单元', 'invoice_date': '2021-10-20 18:08:42.0', 'invoice_user': '', 'invoice_number': '29319070', 'tax_amount': '11907.08', 'invoice_code': '033002000711', 'invoice_status': '正常', 'tax_rate': '0.13', 'invoice_type': '增值税电子普通发票', 'tenant_code': 'ZH-383-20191217145410', 'company_id': '345', 'company_name': '浙江安谐智能科技有限公司', 'tax_date': '202110', 'is_deleted': 0, 'declaration_id': 0, 'select_type': 0, 'buyer_name': '徐州市公安局交通警察支队', 'buyer_id': '11320300014051773Q', 'seller_name': None, 'seller_id': None}, {'invoice_amount': '69000', 'network_invoice_number': '', 'goods_name': '*交通管制设备*流媒体转发服务单元', 'invoice_date': '2021-10-20 18:10:00.0', 'invoice_user': '', 'invoice_number': '29319071', 'tax_amount': '7938.05', 'invoice_code': '033002000711', 'invoice_status': '正常', 'tax_rate': '0.13', 'invoice_type': '增值税电子普通发票', 'tenant_code': 'ZH-383-20191217145410', 'company_id': '345', 'company_name': '浙江安谐智能科技有限公司', 'tax_date': '202110', 'is_deleted': 0, 'declaration_id': 0, 'select_type': 0, 'buyer_name': '徐州市公安局交通警察支队', 'buyer_id': '11320300014051773Q', 'seller_name': None, 'seller_id': None}, {'invoice_amount': '100000', 'network_invoice_number': '', 'goods_name': '*交通管制设备*分布式大数据分析系统', 'invoice_date': '2021-10-20 18:11:22.0', 'invoice_user': '', 'invoice_number': '29319072', 'tax_amount': '11504.42', 'invoice_code': '033002000711', 'invoice_status': '正常', 'tax_rate': '0.13', 'invoice_type': '增值税电子普通发票', 'tenant_code': 'ZH-383-20191217145410', 'company_id': '345', 'company_name': '浙江安谐智能科技有限公司', 'tax_date': '202110', 'is_deleted': 0, 'declaration_id': 0, 'select_type': 0, 'buyer_name': '徐州市公安局交通警察支队', 'buyer_id': '11320300014051773Q', 'seller_name': None, 'seller_id': None}, {'invoice_amount': '100000', 'network_invoice_number': '', 'goods_name': '*交通管制设备*分布式大数据分析系统', 'invoice_date': '2021-10-20 18:11:40.0', 'invoice_user': '', 'invoice_number': '29319073', 'tax_amount': '11504.42', 'invoice_code': '033002000711', 'invoice_status': '正常', 'tax_rate': '0.13', 'invoice_type': '增值税电子普通发票', 'tenant_code': 'ZH-383-20191217145410', 'company_id': '345', 'company_name': '浙江安谐智能科技有限公司', 'tax_date': '202110', 'is_deleted': 0, 'declaration_id': 0, 'select_type': 0, 'buyer_name': '徐州市公安局交通警察支队', 'buyer_id': '11320300014051773Q', 'seller_name': None, 'seller_id': None}, {'invoice_amount': '100000', 'network_invoice_number': '', 'goods_name': '*交通管制设备*分布式大数据分析系统', 'invoice_date': '2021-10-20 18:11:56.0', 'invoice_user': '', 'invoice_number': '29319074', 'tax_amount': '11504.42', 'invoice_code': '033002000711', 'invoice_status': '正常', 'tax_rate': '0.13', 'invoice_type': '增值税电子普通发票', 'tenant_code': 'ZH-383-20191217145410', 'company_id': '345', 'company_name': '浙江安谐智能科技有限公司', 'tax_date': '202110', 'is_deleted': 0, 'declaration_id': 0, 'select_type': 0, 'buyer_name': '徐州市公安局交通警察支队', 'buyer_id': '11320300014051773Q', 'seller_name': None, 'seller_id': None}, {'invoice_amount': '100000', 'network_invoice_number': '', 'goods_name': '*交通管制设备*分布式大数据分析系统', 'invoice_date': '2021-10-20 18:16:27.0', 'invoice_user': '', 'invoice_number': '29319075', 'tax_amount': '11504.42', 'invoice_code': '033002000711', 'invoice_status': '正常', 'tax_rate': '0.13', 'invoice_type': '增值税电子普通发票', 'tenant_code': 'ZH-383-20191217145410', 'company_id': '345', 'company_name': '浙江安谐智能科技有限公司', 'tax_date': '202110', 'is_deleted': 0, 'declaration_id': 0, 'select_type': 0, 'buyer_name': '徐州市公安局交通警察支队', 'buyer_id': '11320300014051773Q', 'seller_name': None, 'seller_id': None}, {'invoice_amount': '100000', 'network_invoice_number': '', 'goods_name': '*交通管制设备*分布式大数据分析系统', 'invoice_date': '2021-10-20 18:16:43.0', 'invoice_user': '', 'invoice_number': '29319076', 'tax_amount': '11504.42', 'invoice_code': '033002000711', 'invoice_status': '正常', 'tax_rate': '0.13', 'invoice_type': '增值税电子普通发票', 'tenant_code': 'ZH-383-20191217145410', 'company_id': '345', 'company_name': '浙江安谐智能科技有限公司', 'tax_date': '202110', 'is_deleted': 0, 'declaration_id': 0, 'select_type': 0, 'buyer_name': '徐州市公安局交通警察支队', 'buyer_id': '11320300014051773Q', 'seller_name': None, 'seller_id': None}, {'invoice_amount': '100000', 'network_invoice_number': '', 'goods_name': '*交通管制设备*分布式大数据分析系统', 'invoice_date': '2021-10-20 18:17:04.0', 'invoice_user': '', 'invoice_number': '29319077', 'tax_amount': '11504.42', 'invoice_code': '033002000711', 'invoice_status': '正常', 'tax_rate': '0.13', 'invoice_type': '增值税电子普通发票', 'tenant_code': 'ZH-383-20191217145410', 'company_id': '345', 'company_name': '浙江安谐智能科技有限公司', 'tax_date': '202110', 'is_deleted': 0, 'declaration_id': 0, 'select_type': 0, 'buyer_name': '徐州市公安局交通警察支队', 'buyer_id': '11320300014051773Q', 'seller_name': None, 'seller_id': None}, {'invoice_amount': '101000', 'network_invoice_number': '', 'goods_name': '*交通管制设备*视频分析存储节点', 'invoice_date': '2021-10-20 18:17:54.0', 'invoice_user': '', 'invoice_number': '29319078', 'tax_amount': '11619.47', 'invoice_code': '033002000711', 'invoice_status': '正常', 'tax_rate': '0.13', 'invoice_type': '增值税电子普通发票', 'tenant_code': 'ZH-383-20191217145410', 'company_id': '345', 'company_name': '浙江安谐智能科技有限公司', 'tax_date': '202110', 'is_deleted': 0, 'declaration_id': 0, 'select_type': 0, 'buyer_name': '徐州市公安局交通警察支队', 'buyer_id': '11320300014051773Q', 'seller_name': None, 'seller_id': None}, {'invoice_amount': '101000', 'network_invoice_number': '', 'goods_name': '*交通管制设备*视频分析存储节点', 'invoice_date': '2021-10-20 18:18:13.0', 'invoice_user': '', 'invoice_number': '29319079', 'tax_amount': '11619.47', 'invoice_code': '033002000711', 'invoice_status': '正常', 'tax_rate': '0.13', 'invoice_type': '增值税电子普通发票', 'tenant_code': 'ZH-383-20191217145410', 'company_id': '345', 'company_name': '浙江安谐智能科技有限公司', 'tax_date': '202110', 'is_deleted': 0, 'declaration_id': 0, 'select_type': 0, 'buyer_name': '徐州市公安局交通警察支队', 'buyer_id': '11320300014051773Q', 'seller_name': None, 'seller_id': None}, {'invoice_amount': '101000', 'network_invoice_number': '', 'goods_name': '*交通管制设备*视频分析存储节点', 'invoice_date': '2021-10-20 18:18:30.0', 'invoice_user': '', 'invoice_number': '29319080', 'tax_amount': '11619.47', 'invoice_code': '033002000711', 'invoice_status': '正常', 'tax_rate': '0.13', 'invoice_type': '增值税电子普通发票', 'tenant_code': 'ZH-383-20191217145410', 'company_id': '345', 'company_name': '浙江安谐智能科技有限公司', 'tax_date': '202110', 'is_deleted': 0, 'declaration_id': 0, 'select_type': 0, 'buyer_name': '徐州市公安局交通警察支队', 'buyer_id': '11320300014051773Q', 'seller_name': None, 'seller_id': None}, {'invoice_amount': '97000', 'network_invoice_number': '', 'goods_name': '*交通管制设备*远光灯终端服务器（含软件基础模块）', 'invoice_date': '2021-10-20 18:40:00.0', 'invoice_user': '', 'invoice_number': '29319081', 'tax_amount': '11159.29', 'invoice_code': '033002000711', 'invoice_status': '正常', 'tax_rate': '0.13', 'invoice_type': '增值税电子普通发票', 'tenant_code': 'ZH-383-20191217145410', 'company_id': '345', 'company_name': '浙江安谐智能科技有限公司', 'tax_date': '202110', 'is_deleted': 0, 'declaration_id': 0, 'select_type': 0, 'buyer_name': '徐州市公安局交通警察支队', 'buyer_id': '11320300014051773Q', 'seller_name': None, 'seller_id': None}, {'invoice_amount': '97000', 'network_invoice_number': '', 'goods_name': '*交通管制设备*光学采集联动模块', 'invoice_date': '2021-10-20 18:40:00.0', 'invoice_user': '', 'invoice_number': '29319081', 'tax_amount': '11159.29', 'invoice_code': '033002000711', 'invoice_status': '正常', 'tax_rate': '0.13', 'invoice_type': '增值税电子普通发票', 'tenant_code': 'ZH-383-20191217145410', 'company_id': '345', 'company_name': '浙江安谐智能科技有限公司', 'tax_date': '202110', 'is_deleted': 0, 'declaration_id': 0, 'select_type': 0, 'buyer_name': '徐州市公安局交通警察支队', 'buyer_id': '11320300014051773Q', 'seller_name': None, 'seller_id': None}, {'invoice_amount': '80000', 'network_invoice_number': '', 'goods_name': '*交通管制设备*光学采集联动模块', 'invoice_date': '2021-10-20 18:48:26.0', 'invoice_user': '', 'invoice_number': '29319082', 'tax_amount': '9203.54', 'invoice_code': '033002000711', 'invoice_status': '正常', 'tax_rate': '0.13', 'invoice_type': '增值税电子普通发票', 'tenant_code': 'ZH-383-20191217145410', 'company_id': '345', 'company_name': '浙江安谐智能科技有限公司', 'tax_date': '202110', 'is_deleted': 0, 'declaration_id': 0, 'select_type': 0, 'buyer_name': '徐州市公安局交通警察支队', 'buyer_id': '11320300014051773Q', 'seller_name': None, 'seller_id': None}, {'invoice_amount': '80000', 'network_invoice_number': '', 'goods_name': '*交通管制设备*违法车辆锁定跟踪技术模块', 'invoice_date': '2021-10-20 18:53:22.0', 'invoice_user': '', 'invoice_number': '29319083', 'tax_amount': '9203.54', 'invoice_code': '033002000711', 'invoice_status': '正常', 'tax_rate': '0.13', 'invoice_type': '增值税电子普通发票', 'tenant_code': 'ZH-383-20191217145410', 'company_id': '345', 'company_name': '浙江安谐智能科技有限公司', 'tax_date': '202110', 'is_deleted': 0, 'declaration_id': 0, 'select_type': 0, 'buyer_name': '徐州市公安局交通警察支队', 'buyer_id': '11320300014051773Q', 'seller_name': None, 'seller_id': None}, {'invoice_amount': '80000', 'network_invoice_number': '', 'goods_name': '*交通管制设备*违法车辆锁定跟踪技术模块', 'invoice_date': '2021-10-20 18:54:13.0', 'invoice_user': '', 'invoice_number': '29319084', 'tax_amount': '9203.54', 'invoice_code': '033002000711', 'invoice_status': '正常', 'tax_rate': '0.13', 'invoice_type': '增值税电子普通发票', 'tenant_code': 'ZH-383-20191217145410', 'company_id': '345', 'company_name': '浙江安谐智能科技有限公司', 'tax_date': '202110', 'is_deleted': 0, 'declaration_id': 0, 'select_type': 0, 'buyer_name': '徐州市公安局交通警察支队', 'buyer_id': '11320300014051773Q', 'seller_name': None, 'seller_id': None}, {'invoice_amount': '80000', 'network_invoice_number': '', 'goods_name': '*交通管制设备*车牌对比标记技术模块', 'invoice_date': '2021-10-20 18:54:13.0', 'invoice_user': '', 'invoice_number': '29319084', 'tax_amount': '9203.54', 'invoice_code': '033002000711', 'invoice_status': '正常', 'tax_rate': '0.13', 'invoice_type': '增值税电子普通发票', 'tenant_code': 'ZH-383-20191217145410', 'company_id': '345', 'company_name': '浙江安谐智能科技有限公司', 'tax_date': '202110', 'is_deleted': 0, 'declaration_id': 0, 'select_type': 0, 'buyer_name': '徐州市公安局交通警察支队', 'buyer_id': '11320300014051773Q', 'seller_name': None, 'seller_id': None}, {'invoice_amount': '80000', 'network_invoice_number': '', 'goods_name': '*交通管制设备*车牌对比标记技术模块', 'invoice_date': '2021-10-20 18:55:31.0', 'invoice_user': '', 'invoice_number': '29319085', 'tax_amount': '9203.54', 'invoice_code': '033002000711', 'invoice_status': '正常', 'tax_rate': '0.13', 'invoice_type': '增值税电子普通发票', 'tenant_code': 'ZH-383-20191217145410', 'company_id': '345', 'company_name': '浙江安谐智能科技有限公司', 'tax_date': '202110', 'is_deleted': 0, 'declaration_id': 0, 'select_type': 0, 'buyer_name': '徐州市公安局交通警察支队', 'buyer_id': '11320300014051773Q', 'seller_name': None, 'seller_id': None}, {'invoice_amount': '80000', 'network_invoice_number': '', 'goods_name': '*交通管制设备*违法数据处理、上传模块', 'invoice_date': '2021-10-20 19:38:18.0', 'invoice_user': '', 'invoice_number': '29319086', 'tax_amount': '9203.54', 'invoice_code': '033002000711', 'invoice_status': '正常', 'tax_rate': '0.13', 'invoice_type': '增值税电子普通发票', 'tenant_code': 'ZH-383-20191217145410', 'company_id': '345', 'company_name': '浙江安谐智能科技有限公司', 'tax_date': '202110', 'is_deleted': 0, 'declaration_id': 0, 'select_type': 0, 'buyer_name': '徐州市公安局交通警察支队', 'buyer_id': '11320300014051773Q', 'seller_name': None, 'seller_id': None}, {'invoice_amount': '80000', 'network_invoice_number': '', 'goods_name': '*交通管制设备*违法数据处理、上传模块', 'invoice_date': '2021-10-20 19:40:04.0', 'invoice_user': '', 'invoice_number': '29319087', 'tax_amount': '9203.54', 'invoice_code': '033002000711', 'invoice_status': '正常', 'tax_rate': '0.13', 'invoice_type': '增值税电子普通发票', 'tenant_code': 'ZH-383-20191217145410', 'company_id': '345', 'company_name': '浙江安谐智能科技有限公司', 'tax_date': '202110', 'is_deleted': 0, 'declaration_id': 0, 'select_type': 0, 'buyer_name': '徐州市公安局交通警察支队', 'buyer_id': '11320300014051773Q', 'seller_name': None, 'seller_id': None}, {'invoice_amount': '80000', 'network_invoice_number': '', 'goods_name': '*交通管制设备*远光灯持续判别模块', 'invoice_date': '2021-10-20 19:40:04.0', 'invoice_user': '', 'invoice_number': '29319087', 'tax_amount': '9203.54', 'invoice_code': '033002000711', 'invoice_status': '正常', 'tax_rate': '0.13', 'invoice_type': '增值税电子普通发票', 'tenant_code': 'ZH-383-20191217145410', 'company_id': '345', 'company_name': '浙江安谐智能科技有限公司', 'tax_date': '202110', 'is_deleted': 0, 'declaration_id': 0, 'select_type': 0, 'buyer_name': '徐州市公安局交通警察支队', 'buyer_id': '11320300014051773Q', 'seller_name': None, 'seller_id': None}, {'invoice_amount': '80000', 'network_invoice_number': '', 'goods_name': '*交通管制设备*远光灯持续判别模块', 'invoice_date': '2021-10-20 19:40:37.0', 'invoice_user': '', 'invoice_number': '29319088', 'tax_amount': '9203.54', 'invoice_code': '033002000711', 'invoice_status': '正常', 'tax_rate': '0.13', 'invoice_type': '增值税电子普通发票', 'tenant_code': 'ZH-383-20191217145410', 'company_id': '345', 'company_name': '浙江安谐智能科技有限公司', 'tax_date': '202110', 'is_deleted': 0, 'declaration_id': 0, 'select_type': 0, 'buyer_name': '徐州市公安局交通警察支队', 'buyer_id': '11320300014051773Q', 'seller_name': None, 'seller_id': None}, {'invoice_amount': '80000', 'network_invoice_number': '', 'goods_name': '*交通管制设备*软件授权', 'invoice_date': '2021-10-20 19:41:18.0', 'invoice_user': '', 'invoice_number': '29319089', 'tax_amount': '9203.54', 'invoice_code': '033002000711', 'invoice_status': '正常', 'tax_rate': '0.13', 'invoice_type': '增值税电子普通发票', 'tenant_code': 'ZH-383-20191217145410', 'company_id': '345', 'company_name': '浙江安谐智能科技有限公司', 'tax_date': '202110', 'is_deleted': 0, 'declaration_id': 0, 'select_type': 0, 'buyer_name': '徐州市公安局交通警察支队', 'buyer_id': '11320300014051773Q', 'seller_name': None, 'seller_id': None}, {'invoice_amount': '80000', 'network_invoice_number': '', 'goods_name': '*交通管制设备*软件授权', 'invoice_date': '2021-10-20 19:41:38.0', 'invoice_user': '', 'invoice_number': '29319090', 'tax_amount': '9203.54', 'invoice_code': '033002000711', 'invoice_status': '正常', 'tax_rate': '0.13', 'invoice_type': '增值税电子普通发票', 'tenant_code': 'ZH-383-20191217145410', 'company_id': '345', 'company_name': '浙江安谐智能科技有限公司', 'tax_date': '202110', 'is_deleted': 0, 'declaration_id': 0, 'select_type': 0, 'buyer_name': '徐州市公安局交通警察支队', 'buyer_id': '11320300014051773Q', 'seller_name': None, 'seller_id': None}, {'invoice_amount': '80000', 'network_invoice_number': '', 'goods_name': '*交通管制设备*软件授权', 'invoice_date': '2021-10-20 19:42:07.0', 'invoice_user': '', 'invoice_number': '29319091', 'tax_amount': '9203.54', 'invoice_code': '033002000711', 'invoice_status': '正常', 'tax_rate': '0.13', 'invoice_type': '增值税电子普通发票', 'tenant_code': 'ZH-383-20191217145410', 'company_id': '345', 'company_name': '浙江安谐智能科技有限公司', 'tax_date': '202110', 'is_deleted': 0, 'declaration_id': 0, 'select_type': 0, 'buyer_name': '徐州市公安局交通警察支队', 'buyer_id': '11320300014051773Q', 'seller_name': None, 'seller_id': None}]
    # callback_saas(data)
    lock = Lock()
    main()
