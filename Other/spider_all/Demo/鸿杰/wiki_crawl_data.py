'''
Author：dhj
Date:2022-1-4
'''
import re
import time

from lxml import etree
import urllib.request
import urllib.parse
import requests
proxys = []
def dl():
    time.sleep(2)
    try:
        dlurl = 'http://api.ip.data5u.com/dynamic/get.html?order=fba1729fce7d27397dc2db1dc5db9977&random=2&sep=3'
        resp = requests.get(dlurl).text
        resp = re.sub(r'\n', '', resp)
        proxy = {
            'https': resp
        }
        proxys.append(proxy)
        print(proxys[-1])
    except:
        dl()

def query():
    dl()
    # 航空母舰 候选词
    Aircraft_carrier_list = ['尼米兹号航空母舰', '德怀特·D·艾森豪号航空母舰', '卡尔·文森号航空母舰', '西奥多·罗斯福号航空母舰', '亚伯拉罕·林肯号航空母舰', '乔治·华盛顿号航空母舰',
                             '约翰·C·史坦尼斯号航空母舰', '哈瑞·S·杜鲁门号航空母舰', '隆纳·雷根号航空母舰', '乔治·H·W·布希号航空母舰', '福特号航空母舰']
    # 请求地址
    # url = 'https://en.wikipedia.org/wiki/' + content
    url1 = 'https://baike.baidu.com/item/%E5%B0%BC%E7%B1%B3%E5%85%B9%E5%8F%B7%E8%88%AA%E7%A9%BA%E6%AF%8D%E8%88%B0/3501097'
    url2 = 'https://zh.wikipedia.org/wiki/%E5%B0%BC%E7%B1%B3%E8%8C%B2%E8%99%9F%E8%88%AA%E7%A9%BA%E6%AF%8D%E8%89%A6'
    # 请求头部
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'no-cache',
        'cookie': 'WMF-Last-Access=05-Jan-2022; WMF-Last-Access-Global=05-Jan-2022; GeoIP=US:CA:Los_Angeles:34.05:-118.27:v4; zhwikimwuser-sessionId=24fa46b40025df2992ac; zhwikiel-sessionId=3ef0317eec8b36881d52; zhwikiwmE-sessionTickLastTickTime=1641352652034; zhwikiwmE-sessionTickTickCount=6',
        'pragma': 'no-cache',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
    }
    # 利用请求地址和请求头部构造请求对象
    while 1:
        try:
            req = requests.request(url=url2, headers=headers, method='GET',timeout=10,verify=False,proxies=proxys[-1]).text
            print(req)
            exit()
        except Exception:
            dl()
            continue

if __name__ == '__main__':
    query()
    # while (True):
    #     content = input('Word: ')
    #     result = query(content)
    #     print("Result: %s" % result)
