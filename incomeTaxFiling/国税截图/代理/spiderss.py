import base64
import json
import logging.config
import os
import re
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

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select


MAP_KEYS = windll.user32.MapVirtualKeyA

logger = logging.getLogger('loggerManager')
logger.setLevel(logging.DEBUG)
USER_PATH = 'E:\\Users\\20945'

from queue import Queue

q = Queue()
def dl(proxys):
    time.sleep(1)
    try:
        dlurl = 'http://api.ip.data5u.com/dynamic/get.html?order=fba1729fce7d27397dc2db1dc5db9977&random=2&sep=3'
        resp = requests.get(dlurl).text
        resp = re.sub(r'\n', '', resp)
        proxy = {
            'https': resp
        }
        proxys[0] = resp
        print(proxys)
    except Exception as e:
        dl(proxys)



def handle_message():
    proxys = ["1"]
    dl(proxys)
    options = Options()
    # 下面代码为设置端口、忽略证书错误以及指定文件夹
    #  开启无头模式，浏览器窗口不太好看。默认不开启
    # options.add_argument('--headless')  # 无头
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-javascript')
    # options.add_argument('--disable-software-rasterizer')
    # options.add_argument("--blink-settings=imagesEnabled=false")
    # 全屏启动
    # options.add_argument('start-fullscreen')
    options.add_argument("--disable-extensions")
    options.add_argument(
        "–user-agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'")
    options.add_argument("-incognito")  # 无痕
    # options.add_argument("–window-size=1200,768")
    options.add_argument(('--proxy-server=http://{}'.format(proxys[-1])))
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
    driver.get("https://etax.zhejiang.chinatax.gov.cn/zjgfdzswj/main/home/wybs/index.html?ticket=ST-2758348-Xfasz6tv0dUbYjfU44U4-com.hz.zkxx.ydzhz")
    time.sleep(100)
    exit()


if __name__ == '__main__':
    """
    获取当前月的数据
    """
    handle_message()
