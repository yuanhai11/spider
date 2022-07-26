#!/usr/bin/python3
# -*- coding: utf-8 -*-
import base64
import json
import logging.config
import os
import time
import traceback
from ctypes import windll
from threading import Lock

import requests
import arrow
# 加入pywintypes，打包成功
import pywintypes
import pythoncom
from Crypto.Cipher import AES
# 导入config里的变量信息
from decouple import config
from kafka import KafkaConsumer
from selenium.webdriver.common.by import By
from lxml import etree

from logger_manager import LoggerManager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select

# kafka server conf
KAFKA_SERVER = config("KAFKA_SERVER").split(",")
KAFKA_TOPIC = config("KAFKA_TOPIC")

OSS_HOST = config('OSS_HOST')
OSS_URL = config('OSS_URL')

CALL_BACK_HOST = config('CALL_BACK_HOST')
CALL_BACK_URL = config('CALL_BACK_URL')

MAP_KEYS = windll.user32.MapVirtualKeyA

LoggerManager.init_logging("logs/work_manager.log", need_mail=False, need_console=True)
logger = logging.getLogger('loggerManager')
logger.setLevel(logging.DEBUG)
USER_PATH = 'E:\\Users\\20945'

from queue import Queue

q = Queue()

'''
新增数据获取
'''
import time, re, json, uuid
import requests, pymysql
from lxml import etree
from sqlalchemy import Column, String, create_engine, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy import or_
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()


# 定义User对象:
class CompanyPayTax(Base):
    # 表的名字:
    __tablename__ = 'company_pay_tax'

    # 表的结构:
    id = Column(Integer(), primary_key=True, autoincrement=True)

    company_name = Column(String(256))
    company_id = Column(String(256))
    tax_type = Column(String(256))
    tax_date = Column(String(256))
    pay_base = Column(String(256))
    pay_person_num = Column(String(256))
    pay_current_tax = Column(String(256))
    gmt_created = Column(String(256))
    gmt_updated = Column(String(256))


class AccountSetting(Base):
    # 表的名字:
    __tablename__ = 'account_setting'

    # 表的结构:
    id = Column(Integer(), primary_key=True, autoincrement=True)

    accout_name = Column(String(256))
    company_id = Column(String(256))


# 初始化数据库连接:
engine = create_engine('mysql+pymysql://root:BOOT-xwork1024@192.168.2.96:3306/zl_saas')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
# 创建session对象:
session = DBSession()


def main():
    """
    接受消息，进行国税截图动作
    """
    result_list = []
    # consumer
    logger.info("kafka server is {},topic is [{}]".format(KAFKA_SERVER, KAFKA_TOPIC))
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_SERVER,
        group_id='screen_group_1',
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
            # print(message)
            # continue
            message_str = message.value.decode("utf-8").replace(" ", "").replace("\t", "")
            logger.info("receive message: {}".format(message_str))
            message_dict = json.loads(message_str)
            l = [message_dict["taskId"], message_dict["companyName"], message_dict["Url"], message_dict["taxDate"]]

            s = session.query(CompanyPayTax).filter(CompanyPayTax.company_name==message_dict["companyName"]).first()
            if s:
                continue

            result = executor.submit(handle_message, l)
            result_list.append(result)

        except StopIteration as se:
            time.sleep(2)
        except Exception as e:
            logger.error(e)


def get_shebao_data(ss):
    a = []
    b = []
    try:
        for i in range(6, 12):
            res = ss.xpath('//div[@class="table-view sy-ui"]/div[{}]//text()'.format(i))
            a.append(res[3])
            b.append(res[10])
        sums = ''.join(ss.xpath('//div[@data-reactid=".1.1.0.2.6.9"]/text()')).replace(",", "")
        print(max(a).replace(",", ""), max(b).replace(",", ""), sums)
        ss = {"pay_base": max(a).replace(",", ""), "pay_person_num": max(b).replace(",", ""), "pay_current_tax": sums}
    except Exception:
        return ""
    return ss


def insertIntoDb(haha, company_name):

    try:
        data = session.query(AccountSetting).filter(AccountSetting.accout_name == company_name).first()
        if not data:
            return
        company_id = data.company_id
        s = session.query(CompanyPayTax).filter(CompanyPayTax.company_name == company_name).first()
        if s:
            return
        if haha == {}:
            return
        for i in haha:
            try:
                times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                tax = CompanyPayTax(company_id=company_id, company_name=company_name,
                                    tax_type=0, tax_date=i, pay_base=haha[i]['pay_base'],
                                    pay_person_num=haha[i]['pay_person_num'],
                                    pay_current_tax=haha[i]['pay_current_tax'],
                                    gmt_created=times, gmt_updated=times
                                    )
            except Exception:
                continue
            session.add(tax)
            session.commit()
    except Exception  as e:
        print("error:{}".format(e))
        session.rollback()
        return

def handle_message(l):
    task_id = l[0]
    company_name = l[1]
    url = l[2]
    if url == 'None':
        pass
        return
    if url == "change":
        pass
        return
    if url == "NoRegister":
        pass
        return
    # 获取用户目录
    otherStyleTime = time.strftime("%Y%m%d", time.localtime(time.time()))
    cur_task_dir = os.path.join(USER_PATH, "Desktop", "rpa_data", company_name, "{}".format(otherStyleTime))
    if not os.path.exists(cur_task_dir):
        os.makedirs(cur_task_dir)

    options = Options()
    # 下面代码为设置端口、忽略证书错误以及指定文件夹
    #  开启无头模式，浏览器窗口不太好看。默认不开启
    options.add_argument('--headless')  # 无头
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-javascript')
    # options.add_argument('--disable-software-rasterizer')
    # options.add_argument("--blink-settings=imagesEnabled=false")
    options.add_argument("--disable-extensions")
    options.add_argument(
        "–user-agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'")
    options.add_argument("-incognito")  # 无痕
    # options.add_argument("–window-size=1200,768")
    # options.add_argument(('--proxy-server=http://{}'.format(proxys[-1])))
    # options.add_argument("--ignore-certificate-errors")
    # options.add_argument('--user-data-dir=C:\\Users\\20945\\Desktop\\data')
    # 下面代码为避免网站对selenium的屏蔽
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    # 以设定好的方式打开谷歌浏览器
    driver = webdriver.Chrome(
        executable_path=r'C:\Users\20945\Downloads\Compressed\chromedriver_win32\chromedriver.exe',
        options=options)

    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
           Object.defineProperty(navigator, 'webdriver', {
             get: () => undefined
           })
     """
    })
    driver.get(url)
    driver.maximize_window()
    time.sleep(1)

    tree = etree.HTML(driver.page_source)
    h = tree.xpath('//div[@id="alertContainer"]')
    h1 = tree.xpath('//div[@id="back-bg"]')
    if len(h) != 0 or len(h1) != 0:
        logger.info("status=5,{}".format(company_name))
        pass
        driver.close()
        return
    time.sleep(1.2)
    save_image = {}
    status = 0
    base_url = 'https://etax.zhejiang.chinatax.gov.cn/sbbcx/wssb/sjcx/'
    haha = {}
    try:
        tree = etree.HTML(driver.page_source)
        fa = tree.xpath('//div[@class="zj-mask"]')
        if len(fa) != 0:
            element = driver.find_element_by_xpath('//input[@type="checkbox"]')
            webdriver.ActionChains(driver).move_to_element(element).click(element).perform()
            element = driver.find_element_by_xpath('//button[@id="agreegrxx"]')
            webdriver.ActionChains(driver).move_to_element(element).click(element).perform()
            driver.get(url)

        for i in range(3):
            try:
                driver.find_element(By.XPATH, '//div[@id="menuwrapper"]//a[@funcmenu="swsbjjn"]').click()
                break
            except Exception:
                if i == 2:
                    status = 4
                    return
                time.sleep(0.5)
        for type1, num in [['社保', '31']]:
            if type1 == "社保":
                for hh in range(3):
                    try:
                        driver = shebao(driver)
                        break
                    except Exception:
                        time.sleep(1)

                tree_detail = etree.HTML(driver.page_source)
                rr = tree_detail.xpath('//div[@class="ant-modal-body"]')
                rr1 = tree_detail.xpath('//div[@class="login-fail"]')

                if len(rr) == 1 or len(rr1) == 1:
                    return

                for ii in range(3):
                    try:
                        driver = clickk(driver)
                        break
                    except Exception:
                        if ii == 2:
                            status = 5
                            logger.info("status=5,{}".format(company_name))
                            return
                        else:
                            try:
                                time.sleep(1)
                                driver = shebao(driver)
                            except Exception:
                                pass
                time.sleep(1.5)
                tree_detail = etree.HTML(driver.page_source)

                li2 = tree_detail.xpath('//tbody/tr//text()')
                li = tree_detail.xpath('//tbody/tr')
                if ''.join(li2).strip() == '没有数据':
                    return

                for suoyin, s in enumerate(li):

                    detail_image = {}
                    time.sleep(1)
                    for ii in range(3):
                        try:
                            driver = clickk(driver)
                            break
                        except Exception:
                            if ii == 2:
                                return
                            else:
                                try:
                                    time.sleep(2)
                                    driver = shebao(driver)
                                except Exception:
                                    pass

                    time.sleep(1)
                    ti0 = ''.join(s.xpath('./td[1]/text()'))
                    ti1 = ''.join(s.xpath('./td[2]/text()'))
                    ti2 = ''.join(s.xpath('./td[4]/text()'))
                    ti3 = ''.join(s.xpath('./td[9]//text()'))
                    detail_image['belong_date'] = ti1
                    detail_image['apply_date'] = ti2
                    detail_image['apply_status'] = ti3
                    # if ti == tax_date:
                    yin = suoyin + 1
                    time.sleep(1)

                    if ti3 != "已申报已缴款" and ti3 != "已申报未缴款" and ti3 != "已申报缴款失败":
                        continue

                    if "补缴" in ti0:
                        continue

                    # if ti0 != "正常申报":
                    #     continue

                    # 查看申报明细位置不一样所做的兼容
                    for ii in range(10):
                        op = 0
                        try:
                            shenbaomingxi = etree.HTML(driver.page_source)
                            operate_list = shenbaomingxi.xpath(
                                '//tbody/tr[{}]/td[last()]//div[@class="operate"]'.format(yin))
                            for operate_index, op in enumerate(operate_list):
                                name = ''.join(op.xpath('./text()')).strip()
                                if name == "查看申报明细":
                                    op = operate_index + 1
                                    break

                            driver.find_element_by_xpath(
                                '//tbody/tr[{}]/td[last()]//div[@class="operate"][{}]'.format(yin, op)).click()
                            break
                        except Exception:
                            if ii == 8:
                                status = 5
                                logger.info("status=5,{}".format(company_name))

                                return
                            else:
                                time.sleep(2)
                    time.sleep(1.5)
                    ss = etree.HTML(driver.page_source)
                    sss = ss.xpath(
                        "//button[@class='ant-btn ant-btn-primary ant-btn-lg back']".format(yin))
                    if len(sss) == 0:
                        continue

                    shebao_data = get_shebao_data(ss)
                    haha[ti1] = shebao_data
                    for ii in range(5):
                        try:
                            driver.find_element_by_xpath(
                                "//button[@class='ant-btn ant-btn-primary ant-btn-lg back']").click()
                            break
                        except Exception:
                            if ii == 4:
                                status = 5
                                logger.info("status=5,{}".format(company_name))
                                return
                            else:
                                time.sleep(1)
    finally:
        # 回调saas。
        logger.info(haha)
        lock.acquire()
        insertIntoDb(haha, company_name)
        lock.release()
        driver.close()


def shebao(driver):
    driver.get("https://etax.zhejiang.chinatax.gov.cn/zjgfdzswj/main/func/sbfgl/index.html")
    time.sleep(0.5)
    tree_detail = etree.HTML(driver.page_source)
    detail_url = ''
    tr_lists = tree_detail.xpath('//a[@menuid="sbjfcxzj"]/@href')
    for tr in tr_lists:
        if 'sbjfcxzj' in tr:
            detail_url = tr.strip()
            break
    driver.get(detail_url)
    time.sleep(1.5)
    return driver


def clickk(driver):
    time.sleep(0.5)
    driver.find_element(By.XPATH, '//input[@value="02"]').click()
    driver.find_element(By.XPATH,
                        '/html/body/div[1]/div/div/div/div/div[2]/div[1]/div[2]/form/div[1]/div/div/div[1]/label[2]/div/div/div/span[1]/span/input').click()
    driver.find_element(By.XPATH,
                        '//tbody[@class="ant-calendar-month-panel-tbody"]//tr[1]//td[1]').click()
    driver.find_element(By.XPATH,
                        '//form[@class="ant-form-inline"]//button[@type="button"][1]').click()
    return driver


if __name__ == '__main__':
    """
    获取当前月的数据
    """
    from concurrent.futures import ThreadPoolExecutor
    import threading
    lock = threading.Lock()
    executor = ThreadPoolExecutor(max_workers=5)
    main()
    # handle_message(
    # [16865, "杭州花觉文化创意有限公司",
    #  "https://etax.zhejiang.chinatax.gov.cn/zjgfdzswj/main/home/wybs/index.html?ticket=ST-713062-spRjlP0rUq1Kk4Nj4mzg-com.hz.zkxx.ydzhz"
    #  ,"2022-06"]
    # )
    # insertIntoDb({'2022-05': {'pay_base': '5000.00', 'pay_person_num': '1', 'pay_current_tax': '1805.00'}, '2022-04': {'pay_base': '5000.00', 'pay_person_num': '1', 'pay_current_tax': '1805.00'}, '2022-03': {'pay_base': '5000.00', 'pay_person_num': '1', 'pay_current_tax': '1805.00'}, '2022-02': {'pay_base': '5000.00', 'pay_person_num': '1', 'pay_current_tax': '1805.00'}, '2022-01': {'pay_base': '5000.00', 'pay_person_num': '1', 'pay_current_tax': '1805.00'}}
# ,"杭州兴禾美进出口有限公司")
