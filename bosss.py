import time
from selenium import webdriver
from lxml import etree
import requests
import re
proxys = []

def dl():
    dlurl = 'http://dynamic.goubanjia.com/dynamic/get/d490a5d4debefc8980ae6ee4c4148552.html?sep=3'
    resp = requests.get(dlurl).text
    time.sleep(2)
    resp = re.sub(r'\n', '', resp)
    proxy = {
        'http': resp
    }
    proxys.append(proxy)
    print(proxys[-1])
dl()
url = 'https://www.zhipin.com/c101210100-p100101/?page=10&ka=page-10'
headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
    'cookie':'lastCity=101210100; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1595499486,1595560125,1597304737,1597645006; __g=-; __zp_stoken__=fce8afDIbKyI%2Fd2o%2FaxQjcEUfNwdfdk07NVRjFGMOMg8tDA0KSWE1LXE4OzU7OihHHjt%2BZF1lNyBgX0hVRlooMHtjM1kCDmgNMzgBRww8QAY9XE1ZQ3wRXhxSFhshJwMMXAI7G0dsSFgtbDQ%3D; __c=1597645008; __l=l=%2Fwww.zhipin.com%2Fc101210100-p100101%2F%3Fpage%3D10%26ka%3Dpage-10&r=&g=&friend_source=0&friend_source=0; __a=48297146.1592461039.1597304737.1597645008.235.15.12.32; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1597650523'
}

content = requests.get(url).content.decode('utf-8')
print(content)

