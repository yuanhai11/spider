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
from selenium.webdriver.chrome.webdriver import WebDriver
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

        if len(result_list) >= 2:
            for index, i in enumerate(result_list):
                if i.done():
                    result_list.remove(result_list[index])
            time.sleep(1)
            continue
        try:
            # message = consumer.poll()
            message = next(consumer)
            consumer.commit()
            message_str = message.value.decode("utf-8").replace(" ", "").replace("\t", "")
            logger.info("receive message: {}".format(message_str))
            # print(message)
            # continue
            message_dict = json.loads(message_str)
            l = [message_dict["taskId"], message_dict["companyName"], message_dict["Url"], message_dict["taxDate"]]
            result = executor.submit(handle_message, l)
            result_list.append(result)

        except StopIteration as se:
            time.sleep(2)
        except Exception as e:
            logger.error(e)


def image_to_url(dz):
    headers1 = {
        'Content-Type': 'application/json;charset=UTF-8',
        'Host': OSS_HOST
    }
    with open(dz, "rb") as f:
        base64_data = base64.b64encode(f.read())
        base64_data = str(base64_data).split("'")[1]
        url = OSS_URL
        data = {"imgContent": base64_data}
        data = json.dumps(data)
        for k in range(5):
            try:
                gaga = requests.post(url=url, data=data, headers=headers1)
                gaga1 = json.loads(gaga.text)
                gaga.close()
                break
            except Exception:
                continue

        zzz = gaga1['data']['imageUrl']
    return zzz


def callback_saas(task_id, status, image, tax_qualification, shebao_data, type_res=None):
    """
    status:
    0 有数据，1 密码错误 2，国税URL超时 3，所在税期无数据 4，国税无数据 5，国税改版
    identity_code: 1一般纳税人 2小规模
    type_res 本次截图税种是否完整；0 完整 1 不完整 2 无数据
    """
    try:
        if not shebao_data:
            shebao_data = {}
        if type_res == None or type_res == []:
            resType = 2
        else:
            try:
                dd = [False for i in type_res if len(image[i]) == 0]
                if False in dd:
                    resType = 1
                else:
                    resType = 0
            except Exception:
                resType = 1

        headers2 = {
            'Content-Type': 'application/json;charset=UTF-8',
            'Host': CALL_BACK_HOST,
            'Connection': 'close',
        }
        data = {
            "status": status, "images": image, "taxTaskId": task_id,
            "taxType": 1, "cnt": 1, "taxpayerQualification": tax_qualification,
            "taxCompleted": resType,
            "sheBaoData": shebao_data
        }
        purl = CALL_BACK_URL
        if status == 0:
            data = data
        elif status == 1:
            data['exceptionCause'] = "国税账号或密码错误"
        elif status == 2:
            data['exceptionCause'] = "国税URL超时"
        elif status == 3:
            data['exceptionCause'] = "所在税期无数据"
        elif status == 4:
            data['exceptionCause'] = "国税无数据"
        elif status == 5:
            data['exceptionCause'] = "国税登录问题，验证码超时"
        elif status == 6:
            data['exceptionCause'] = "没有税务账号"
        elif status == 7:
            data['exceptionCause'] = "该办税人员未进行自然人用户注册，无法使用密码登录"

        try:
            response = requests.post(url=purl, json=data, headers=headers2, timeout=10)
            aaa = response.text
            response.close()
        except Exception as  e:
            logger.info("回调第{}次异常，taskId:{},cause:{}".format(1, task_id, e))
            aaa = "error"
    except Exception:
        aaa = "error"
    return aaa


def screen(list):
    time.sleep(1)
    driver = list[0]
    cur_task_dir = list[1]
    detail_title = list[2]
    company_name = list[3]
    # lock.acquire()
    # 接下来是全屏的关键，用js获取页面的宽高，如果有其他需要用js的部分也可以用这个方法
    width = driver.execute_script("return document.documentElement.scrollWidth")
    height = driver.execute_script("return document.documentElement.scrollHeight")
    # 将浏览器的宽高设置成刚刚获取的宽高
    driver.set_window_size(width, height + 50)
    time.sleep(0.5)
    driver.get_screenshot_as_file("{}\\{}.png".format(cur_task_dir, detail_title))
    oss_url = image_to_url("{}\\{}.png".format(cur_task_dir, detail_title))
    # logger.info("{}:{}".format(company_name, oss_url))
    # lock.release()

    return oss_url


def need_screen_type(driver):
    time.sleep(0.5)
    need_screen_tree = etree.HTML(driver.page_source)
    dd = ''.join(need_screen_tree.xpath('//span[@id="h-nsrlx"]//text()'))
    if "增值税一般纳税人" in dd:
        identity_code = 1
    else:
        identity_code = 2
    need_screen_res = ''.join(need_screen_tree.xpath('//div[@id="sbxm_zcsb_menu"]//tr/td[1]//text()'))
    all = {'单位社会保险费': "社保", '印花税税源采集': "印花税",
           '财务报表（小企业会计准则）': "财务报表", '增值税及附加税': "增值税", '企业所得税、财产和行为税合并纳税申报表': "企业所得税"}
    res = [all[a] for a in all.keys() if a in need_screen_res]
    return identity_code, res


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


def handle_message(l):
    task_id = l[0]
    company_name = l[1]
    url = l[2]
    tax_date = l[3]
    tax_t = ""
    shebao_data = ""
    type_res = None
    tax_qualification = ""
    if url == 'None':
        res = callback_saas(task_id, 1, {}, tax_qualification, shebao_data)
        logger.info("taskCallback is success,taskID:{},result:{}".format(task_id, res))
        return
    if url == "change":
        res = callback_saas(task_id, 5, {}, tax_qualification, shebao_data)
        logger.info("taskCallback is success,taskID:{},result:{}".format(task_id, res))
        return
    if url == "NoRegister":
        res = callback_saas(task_id, 7, {}, tax_qualification, shebao_data)
        logger.info("taskCallback is success,taskID:{},result:{}".format(task_id, res))
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
    # 全屏启动
    options.add_argument('start-fullscreen')
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
        executable_path=r'C:\Users\20945\Downloads\Compressed\chromedriver_win32_2\chromedriver.exe',
        options=options)

    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
           Object.defineProperty(navigator, 'webdriver', {
             get: () => undefined
           })
     """
    })
    driver.get(url)
    time.sleep(1)

    tree = etree.HTML(driver.page_source)
    h = tree.xpath('//div[@id="alertContainer"]')
    h1 = tree.xpath('//div[@id="back-bg"]')
    if len(h) != 0 or len(h1) != 0:
        res = callback_saas(task_id, 2, {}, tax_qualification, shebao_data)
        logger.info("taskCallback is success,taskID:{},result:{}".format(task_id, res))
        driver.close()
        return
    time.sleep(1.2)
    save_image = {}

    status = 0
    base_url = 'https://etax.zhejiang.chinatax.gov.cn/sbbcx/wssb/sjcx/'
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
        time.sleep(0.5)
        tree = etree.HTML(driver.page_source)
        yinhuashui = tree.xpath('//iframe[@id="if_gy_ts_1"]')
        if len(yinhuashui) != 0:
            driver.find_element_by_xpath("/html/body/div[3]/div/div/div[3]/button").click()

        tax_qualification, type_res = need_screen_type(driver)

        list1 = [driver, cur_task_dir, "常规申报列表", company_name]
        oss_url = screen(list1)
        save_image['常规申报列表'] = {"常规申报列表": oss_url}

        for type1, num in [['社保', '31'], ['印花税', '11'], ['财务报表', '90'],
                           ['增值税', '01'], ['企业所得税', '04']]:
            if type1 == "社保":
                lis = []
                try:
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
                                    status = 5
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
                                    return
                                else:
                                    time.sleep(2)

                        detail_title = "{}-{}".format(yin, type1)
                        # detail_title="{}".format(type1)
                        time.sleep(1)
                        ss = etree.HTML(driver.page_source)
                        sss = ss.xpath(
                            "//button[@class='ant-btn ant-btn-primary ant-btn-lg back']".format(yin))
                        if len(sss) == 0:
                            continue
                        if "补缴" not in ti0:
                            shebao_data = get_shebao_data(ss)

                        list1 = [driver, cur_task_dir, detail_title, company_name]
                        url = screen(list1)
                        detail_image[detail_title] = url
                        lis.append(detail_image)
                        for ii in range(5):
                            try:
                                driver.find_element_by_xpath(
                                    "//button[@class='ant-btn ant-btn-primary ant-btn-lg back']").click()
                                break
                            except Exception:
                                if ii == 4:
                                    status = 5
                                    return
                                else:
                                    time.sleep(1)

                except Exception as e:
                    status = 5
                    logger.info('社保这块有问题。staus 5 {}'.format(traceback.print_exc()))
                    pass

                finally:
                    save_image[type1] = lis
                    continue

            driver.get(
                "https://etax.zhejiang.chinatax.gov.cn/sbbcx/wssb/sjcx/sb_ysbcx.jsp?xmzslx=24&xmfwly=&sbxmdm=lsbbcx1")
            # driver.find_element_by_name("sssq_q").clear()
            # driver.find_element_by_name("sssq_q").send_keys("20220101")

            S = Select(driver.find_element_by_name('zsxm_dm')).select_by_value(num)
            time.sleep(1.3)
            driver.find_element(By.XPATH, '//div[@class="bottom_btn_div"]/a').click()
            # driver.implicitly_wait()
            time.sleep(1)
            tree = etree.HTML(driver.page_source)
            f = 0

            # 防火墙阻断
            h_inter = tree.xpath('//div[@id="alertContainer"]')
            if len(h_inter) != 0:
                status = 10  # IP被封
                save_image = {}
                print("防火墙阻断" + company_name)
                return

            info = tree.xpath('//table[@class="unnamed1"]/tbody/tr')[1:-1]
            if len(info) == 0:
                save_image[type1] = []
                continue

            listsss = []
            for index, ele in enumerate(info):
                ll = {}
                apply_date = "".join(ele.xpath('./td[3]//text()')).strip()
                start_date = "".join(ele.xpath('./td[4]//text()')).strip()
                end_date = "".join(ele.xpath('./td[5]//text()')).strip()
                # stick 判别程序是否往下继续，用于筛选
                stick = choice_date(start_date, end_date)
                if not stick:
                    continue

                ll['apply_date'] = apply_date
                ll['start_date'] = start_date
                ll['end_date'] = end_date

                fuck = "".join(ele.xpath('./td[last()]//a/@href'))
                fuck_url = base_url + fuck
                driver.get(fuck_url)
                time.sleep(0.5)

                if type1 == "印花税":
                    tree_detail = etree.HTML(driver.page_source)
                    detail_title = ''.join(tree_detail.xpath('//ul[@class="list-head-bg"]/li[1]//text()')).strip()
                    if detail_title == '':
                        continue

                    detail_url = "https://etax.zhejiang.chinatax.gov.cn" + ''.join(
                        tree_detail.xpath('//ul[@class="list-head-bg"]/li[2]/a/@href'))
                    driver.execute_script("window.print = function(){};")
                    driver.get(detail_url)
                    time.sleep(0.5)

                    hh = etree.HTML(driver.page_source)
                    ff = hh.xpath('//div[@class="bootbox modal fade bootbox-alert in"]')
                    if len(ff) == 1:
                        ll[detail_title] = 'None'
                        continue
                    try:
                        driver.find_element(By.XPATH, '//tbody/tr[1]/td/input[last()]').click()
                    except Exception:
                        pass
                    try:
                        driver.find_element(By.XPATH, '//div[@id="printbtn"]/input[last()]').click()
                    except Exception:
                        pass

                    time.sleep(0.2)
                    list1 = [driver, cur_task_dir, detail_title, company_name]
                    url = screen(list1)
                    ll[detail_title] = url
                    listsss.append(ll)

                elif type1 == "企业所得税":

                    tree_detail = etree.HTML(driver.page_source)
                    tr_lists = tree_detail.xpath('//div[@id="dyList"]/ul')
                    for tr in tr_lists:
                        href = tr.xpath('./li[2]/a/@href')
                        if len(href) == 0:
                            continue
                        href = "".join(href)
                        detail_title = ''.join(tr.xpath('./li[1]/text()')).strip()
                        if 'sbbcxcs' in href:
                            detail_url = "https://etax.zhejiang.chinatax.gov.cn" + href
                        else:
                            detail_url = base_url + href
                        driver.get(detail_url)
                        time.sleep(0.5)
                        hh = etree.HTML(driver.page_source)
                        ff = hh.xpath('//div[@class="bootbox modal fade bootbox-alert in"]')
                        if len(ff) == 1:
                            ll[detail_title] = 'None'
                            continue
                        try:
                            driver.find_element(By.XPATH, '//tbody/tr[1]/td/input[last()]').click()
                        except Exception:
                            pass
                        try:
                            driver.find_element(By.XPATH, '//div[@id="printbtn"]/input[last()]').click()
                        except Exception:
                            pass

                        list1 = [driver, cur_task_dir, detail_title, company_name]
                        url = screen(list1)
                        ll[detail_title] = url
                    listsss.append(ll)

                elif type1 == "增值税":

                    tree_detail = etree.HTML(driver.page_source)
                    tr_lists = tree_detail.xpath('//div[@id="dyList"]/ul')
                    if len(tr_lists) != 0:
                        for tr in tr_lists:
                            href = tr.xpath('./li[2]/a/@href')
                            if len(href) == 0:
                                continue
                            href = "".join(href)
                            detail_title = ''.join(tr.xpath('./li[1]/text()')).strip()
                            if 'sbbcxcs' in href:
                                detail_url = "https://etax.zhejiang.chinatax.gov.cn" + href
                            else:
                                detail_url = base_url + href
                            driver.get(detail_url)
                            if "抵扣联明细" in detail_title or "存根联明细" in detail_title:
                                time.sleep(1.5)
                            else:
                                time.sleep(0.5)

                            hh = etree.HTML(driver.page_source)
                            ff = hh.xpath('//div[@class="bootbox modal fade bootbox-alert in"]')
                            if len(ff) == 1:
                                ll[detail_title] = 'None'
                                continue
                            try:
                                driver.find_element(By.XPATH, '//tbody/tr[1]/td/input[last()]').click()
                            except Exception:
                                pass
                            try:
                                driver.find_element(By.XPATH, '//div[@id="printbtn"]/input[last()]').click()
                            except Exception:
                                pass

                            list1 = [driver, cur_task_dir, detail_title, company_name]
                            url = screen(list1)
                            ll[detail_title] = url
                    else:
                        tr_lists = tree_detail.xpath('//tbody/tr')
                        for tr in tr_lists:
                            flag = tr.xpath('./td[2]/div')
                            if len(flag) == 0:
                                continue
                            detail_title = ''.join(tr.xpath('./td[2]/div//text()')).strip()
                            href = ''.join(tr.xpath('./td[3]/div/a/@href'))
                            if 'sbbcxcs' in href:
                                detail_url = "https://etax.zhejiang.chinatax.gov.cn" + href
                            else:
                                detail_url = base_url + href
                            driver.get(detail_url)
                            if "抵扣联明细" in detail_title or "存根联明细" in detail_title:
                                time.sleep(1.5)
                            else:
                                time.sleep(0.5)

                            hh = etree.HTML(driver.page_source)
                            ff = hh.xpath('//div[@class="bootbox modal fade bootbox-alert in"]')
                            if len(ff) == 1:
                                ll[detail_title] = 'None'
                                continue
                            try:
                                driver.find_element(By.XPATH, '//tbody/tr[1]/td/input[last()]').click()
                            except Exception:
                                pass
                            try:
                                driver.find_element(By.XPATH, '//div[@id="printbtn"]/input[last()]').click()
                            except Exception:
                                pass

                            list1 = [driver, cur_task_dir, detail_title, company_name]
                            url = screen(list1)
                            ll[detail_title] = url
                    listsss.append(ll)

                elif type1 == "财务报表":
                    tree_detail = etree.HTML(driver.page_source)
                    tr_lists = tree_detail.xpath('//tbody/tr')
                    if len(tr_lists) != 0:
                        for tr in tr_lists:
                            flag = tr.xpath('./td[2]/div')
                            if len(flag) == 0:
                                continue
                            detail_title = ''.join(tr.xpath('./td[2]/div//text()')).strip()
                            href = ''.join(tr.xpath('./td[3]/div/a/@href'))
                            if 'sbbcxcs' in href:
                                detail_url = "https://etax.zhejiang.chinatax.gov.cn" + href
                            else:
                                detail_url = base_url + href
                            driver.get(detail_url)
                            time.sleep(0.5)
                            hh = etree.HTML(driver.page_source)
                            ff = hh.xpath('//div[@class="bootbox modal fade bootbox-alert in"]')
                            if len(ff) == 1:
                                ll[detail_title] = 'None'
                                continue

                            try:
                                driver.find_element(By.XPATH, '//tbody/tr[1]/td/input[last()]').click()
                            except Exception:
                                pass
                            try:
                                driver.find_element(By.XPATH, '//div[@id="printbtn"]/input[last()]').click()
                            except Exception:
                                pass

                            list1 = [driver, cur_task_dir, detail_title, company_name]
                            url = screen(list1)
                            ll[detail_title] = url

                    else:
                        tr_lists = tree_detail.xpath('//div[@id="dyList"]/ul')
                        for tr in tr_lists:
                            href = tr.xpath('./li[2]/a/@href')
                            if len(href) == 0:
                                continue
                            href = "".join(href)
                            detail_title = ''.join(tr.xpath('./li[1]/text()')).strip()
                            if 'sbbcxcs' in href:
                                detail_url = "https://etax.zhejiang.chinatax.gov.cn" + href
                            else:
                                detail_url = base_url + href
                            driver.get(detail_url)
                            time.sleep(0.5)
                            hh = etree.HTML(driver.page_source)
                            ff = hh.xpath('//div[@class="bootbox modal fade bootbox-alert in"]')
                            if len(ff) == 1:
                                ll[detail_title] = 'None'
                                continue

                            try:
                                driver.find_element(By.XPATH, '//tbody/tr[1]/td/input[last()]').click()
                            except Exception:
                                pass
                            try:
                                driver.find_element(By.XPATH, '//div[@id="printbtn"]/input[last()]').click()
                            except Exception:
                                pass

                            list1 = [driver, cur_task_dir, detail_title, company_name]
                            url = screen(list1)
                            ll[detail_title] = url

                    listsss.append(ll)

            save_image[type1] = listsss


    except Exception as e:
        logger.info("{}截图未知错误，请重试！{}".format(company_name, e))
        status = 5
        save_image = {}

    finally:
        # 回调saas。
        logger.info(
            "screenTask is over!taskId:{},companyName:{},save_image:{}".format(task_id, company_name, save_image))
        res = callback_saas(task_id, status, save_image, tax_qualification, shebao_data, type_res)
        if res == "error":
            pass
        else:
            logger.info("taskCallback is success,taskID:{},result:{}".format(task_id, res))
        driver.close()


def choice_date(start, end):
    # 季报不一定就是季报，可能存在月报
    stick = False
    a = arrow.now()
    big_account = ['01', '04', '07', '10']
    now_date = str(a.shift(months=0))[5:7]
    if now_date in big_account:
        if start[:7] == str(a.shift(months=-3))[:7] and end[:7] == str(a.shift(months=-1))[:7]:
            stick = True
            return stick

    pre_date = str(a.shift(months=-1))[:7]
    if pre_date == start[:7] and pre_date == end[:7]:
        stick = True

    return stick


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
    # driver.find_element(By.XPATH,
    #                     '//div[@class="ant-radio-group"]/label[2]//span[1]//span[1]/input[@class="ant-calendar-picker-input ant-input"]').click()
    # driver.find_element(By.XPATH,
    #                     '//tbody[@class="ant-calendar-month-panel-tbody"]//tr[1]//td[1]').click()
    driver.find_element(By.XPATH,
                        '//form[@class="ant-form-inline"]//button[@type="button"][1]').click()
    return driver


if __name__ == '__main__':
    """
    获取当前月的数据
    """
    from concurrent.futures import ThreadPoolExecutor

    executor = ThreadPoolExecutor(max_workers=2)
    main()
    # handle_message(
    # [16865, "杭州锦慧企业管理咨询有限公司",
    #  "https://etax.zhejiang.chinatax.gov.cn/zjgfdzswj/main/home/wybs/index.html?ticket=ST-1843647-paevcqcsuD2DvVrgSfxB-com.hz.zkxx.ydzhz"
    #  ,"2022-06"]
    # )
    #      'https://etax.zhejiang.chinatax.gov.cn/zjgfdzswj/main/home/wybs/index.html?ticket=ST-2855244-CATMvQN7lw3XOoKHyvUm-com.hz.zkxx.ydzhz'
    #         , "2022-06"
    #      ])
    # ss = {"pay_base": 1245.02, "pay_person_num": 2, "pay_current_tax":1245.00}
    # callback_saas(12710,0,        {'常规申报列表': {'常规申报列表': 'http://oss-xwork.oss-cn-hangzhou.aliyuncs.com/71564208-0f56-4c0f-bd50-0198f63dbd69.jpg'}, '社保': [], '印花税': [], '财务报表': [], '增值税': [], '企业所得税': []},
    # '',ss,''
# )

# print(callback_saas(74052, 0,
#                     {'常规申报列表':
#                          {'常规申报列表': 'http://oss-xwork.oss-cn-hangzhou.aliyuncs.com/a62808a2-8b97-434c-b7c5-237090f40e6a.jpg'},
#                      '社保': [{'belong_date': '2022-05', 'apply_date': '2022-06-07 10:52:27', 'apply_status': '已申报未缴款', '1-社保': 'http://oss-xwork.oss-cn-hangzhou.aliyuncs.com/655bb574-bec2-4dc0-8d8a-1e4d693462c5.jpg'}],
#                      '印花税': [{'apply_date': '2022-06-02', 'start_date': '2022-05-01', 'end_date': '2022-05-31', '申报表:印花税纳税申报（报告）表': 'http://oss-xwork.oss-cn-hangzhou.aliyuncs.com/affa605b-c40d-4b64-bd4e-4841baca9ce8.jpg'}], '财务报表': [], '增值税': [{'apply_date': '2022-06-07', 'start_date': '2022-05-01', 'end_date': '2022-05-31', '增值税一般纳税人-- 增值税申报表': 'http://oss-xwork.oss-cn-hangzhou.aliyuncs.com/b42a8431-0f34-49d3-ab0c-b7225a7de78e.jpg', '增值税一般纳税人-- 附列资料(表一)': 'http://oss-xwork.oss-cn-hangzhou.aliyuncs.com/c56b662b-64a0-4dbd-b3b7-aee6acb97cef.jpg', '增值税一般纳税人-- 附列资料(表四)': 'http://oss-xwork.oss-cn-hangzhou.aliyuncs.com/7c5f008c-03b1-45c5-a72c-c6f90647dc69.jpg', '增值税一般纳税人--增值税及附加税费申报表附列资料《五〉': 'http://oss-xwork.oss-cn-hangzhou.aliyuncs.com/1ba88e56-c328-434d-b8f4-c946eef92577.jpg'}],
#                      '企业所得税': []
#                      },
#                     "",["社保"]))
