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

LoggerManager.init_logging("logs/taxpayer_type_title.log", need_mail=False, need_console=True)
logger = logging.getLogger('loggerManager')
logger.setLevel(logging.DEBUG)

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
    # consumer
    logger.info("kafka server is {},topic is [{}]".format(KAFKA_SERVER, KAFKA_TOPIC))
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_SERVER,
        group_id='taxpayer_type_title_group-1',
        auto_offset_reset='earliest',
        enable_auto_commit=False,
        consumer_timeout_ms=3 * 1000,
        max_poll_interval_ms=3000000
    )

    logger.info("rpa worker started!")
    while 1:
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
                 message_dict["companyId"], message_dict.get("companyName"),
                 message_dict["tenant_code"],message_dict['localDate']
                 ]

            # if int(message_dict["companyId"]) not in [243343,469309,470360,475793,472932,482565,483102,450215,462739,66771,466755,464126,457242]:
            #     continue
            handle_message(l)
        except StopIteration as se:
            time.sleep(2)
        except Exception as e:
            logger.error(e)


def handle_message(l):

    data = {
        "handleTaxName": l[2],
        "handleTaxPwd": l[3],
        "taxAccount": l[0],
        "taxPwd": l[1]
    }

    cookie = None
    for i in range(4):
        response = get_login_cookie(data)
        if not response or response['data']['name'] != '0':
            logger.info("{}获取cookie中失败,retry{}次".format(l[5],i))
            time.sleep(2)
            continue
        else:
            cookie = response['data']['value'][7:]
            break

    if cookie:
        get_headers(cookie, l)


def get_login_cookie(data):
    url = LOGIN_API
    headers2 = {
        'Content-Type': 'application/json;charset=UTF-8',
        'Host': CALL_BACK_HOST,
        'Connection': 'close',
    }
    try:
        time.sleep(2)
        response = requests.post(url=url, json=data, headers=headers2, timeout=20)
    except Exception:
        return None

    aaa = response.text
    response.close()
    return json.loads(aaa)

def callback_saas(data):
    headers2 = {
        'Content-Type': 'application/json;charset=UTF-8',
        'Host': CALL_BACK_HOST,
        'Connection': 'close',
    }
    data = {

        "companyId":data[0],
        "companyName":data[2],
        "socialCode":data[1],
        "station":data[3],
        "phone":data[4],
        "bankAccount":data[5],
        "bankStation":data[6],
        "identityCode":data[7],

    }

    purl = CALL_BACK_URL

    try:
        response = requests.post(url=purl, json=data, headers=headers2, timeout=10)
        aaa = response.text
        response.close()
    except Exception as  e:
        aaa = "error"

    return aaa




def get_headers(cookie, l):
    '''
     获取纳税人类型
     '''
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
        'cookie': cookie
    }
    init_url = "https://etax.zhejiang.chinatax.gov.cn/zjgfdzswj/lxrpublic/init.do"
    dd = requests.get(init_url
                        ,
                        headers=headers, timeout=10
                        ).json()['resultObj']
    station, phone = None,None
    if len(dd)>0:
        for jj in dd:
            if jj.get('LXRLX') == "法定代表人":
                station = jj.get('DZ')
                phone = jj.get('LXDH')
                break
            station,phone = dd[0].get('DZ'),dd[0].get('LXDH')

    time.sleep(0.5)
    company_name = None
    a = "https://etax.zhejiang.chinatax.gov.cn/zjgfdzswj/UserController/getUser.do"
    try:
        DJXH1 = requests.get(a
                            ,
                            headers=headers, timeout=10
                            ).json()['resultObj']
        DJXH = DJXH1['dsInfo']['DJXH']
        code = DJXH1['nsrInfo']['nsrlx']['QYLXDM']
        company_name = DJXH1['dsInfo']['NSRMC']

        if code =='10' or code=='12':
            jj = "一般纳税人"
            identity_code = 1
        else:
            jj = "小规模纳税人"
            identity_code = 2
    except Exception:
        identity_code = None

    time.sleep(0.5)
    bank_info = "https://etax.zhejiang.chinatax.gov.cn/zjgfdzswjdjrd/ckzhzhbg/queryinit/{}.do".format(DJXH)
    dd = requests.get(bank_info
                        ,
                        headers=headers, timeout=10
                        ).json()['resultObj']
    if len(dd)>0:
        YHZH = dd[-1].get('YHZH')
        YHYYWD_DM = dd[-1].get('YHYYWD_DM')
        XZQHSZ_DM = dd[-1].get('XZQHSZ_DM')
        YHHB_DM = dd[-1].get('YHHB_DM')
        ZHMC = dd[-1].get("ZHMC")
        time.sleep(0.5)
        code = "https://etax.zhejiang.chinatax.gov.cn/zjgfdzswjdjrd/ckzhzhbg/queryOptjl/JCXXZX016/{}/{}.do".format(YHHB_DM,XZQHSZ_DM)
        dd = requests.get(code
                            ,
                            headers=headers, timeout=10
                            ).json()['resultObj']['JCXXZX016']
        YHYYWD = [i['MC'] for i in dd if i['DM']==YHYYWD_DM]
        if len(YHYYWD) ==0:
            YHYYWD = None
        else:
            YHYYWD = "".join(YHYYWD)
        print(l[0],company_name,station,phone,YHZH,YHYYWD,identity_code)
        res = callback_saas([l[4],l[0],company_name,station,phone,YHZH,YHYYWD,identity_code])
        logger.info(res)
    else:
        YHZH = None
        YHYYWD = None
        ZHMC = None
        print(l[0],company_name,station,phone,YHZH,YHYYWD,identity_code)
        res = callback_saas([l[4],l[0],company_name,station,phone,YHZH,YHYYWD,identity_code])
        logger.info(res)


if __name__ == '__main__':
    # get_headers()
    main()