#!/usr/bin/python
# -*- coding: utf-8 -*-
import re

from bs4 import BeautifulSoup
import urllib
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s|%(name)-6s|%(threadName)-6s|%(levelname)-8s|%(message)s')
logger = logging.getLogger("spider")
logger.setLevel(logging.INFO)

# 创建handler
handler1 = logging.FileHandler("spider.log",encoding='utf-8')
handler1.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s|%(name)-12s+ %(threadName)-8s +%(levelname)-8s++%(message)s')
handler1.setFormatter(formatter)
logger.addHandler(handler1)

import time, requests


def dl():
    global resp
    proxys = []
    for i in range(1):

        time.sleep(1)
        dlurl = 'http://dps.kdlapi.com/api/getdps/?orderid=922450652890692&num=1&pt=1&sep=1'
        try:
            resp = requests.get(dlurl).text
        except Exception:
            logger.warn("访问快代理出现问题，原因1：断网，原因2：快代理本身问题，休眠60s ")
            time.sleep(60)
        if '今日' not in resp:
            resp = re.sub(r'\n', '', resp)
            proxy = str(resp)
            proxys.append(proxy)
        else:
            # t = datetime.datetime.replace(datetime.datetime.now() + datetime.timedelta(days=1), hour=9, minute=0, second=0)
            # logger.info("休眠中，！！！明天9点运行》")
            # time.sleep((t - datetime.datetime.now()).total_seconds())
            # proxies_queue.put({'https':'117.43.52.160:21604'})
            pass
    return proxys


def get_html(url):
    request = urllib.request.Request(url)
    request.add_header("User-Agent",
                       "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.99 Safari/537.36")
    html = urllib.request.urlopen(request)
    return html.read()


def get_soup(url):
    soup = BeautifulSoup(get_html(url), "lxml")
    return soup


def fetch_kxdaili(page):
    """
    从www.kxdaili.com抓取免费代理
    """
    proxyes = []
    try:
        url = "http://www.kxdaili.com/dailiip/1/%d.html" % page
        soup = get_soup(url)
        table_tag = soup.find("table", attrs={"class": "segment"})
        trs = table_tag.tbody.find_all("tr")
        for tr in trs:
            tds = tr.find_all("td")
            ip = tds[0].text
            port = tds[1].text
            latency = tds[4].text.split(" ")[0]
            if float(latency) < 0.5:  # 输出延迟小于0.5秒的代理
                proxy = "%s:%s" % (ip, port)
                proxyes.append(proxy)
    except:
        logger.warning("fail to fetch from kxdaili")
    return proxyes


def img2port(img_url):
    """
    mimvp.com的端口号用图片来显示, 本函数将图片url转为端口, 目前的临时性方法并不准确
    """
    code = img_url.split("=")[-1]
    if code.find("AO0OO0O") > 0:
        return 80
    else:
        return None


def fetch_mimvp():
    """
    从http://proxy.mimvp.com/free.php抓免费代理
    """
    proxyes = []
    try:
        url = "http://proxy.mimvp.com/free.php?proxy=in_hp"
        soup = get_soup(url)
        table = soup.find("div", attrs={"id": "list"}).table
        tds = table.tbody.find_all("td")
        for i in range(0, len(tds), 10):
            id = tds[i].text
            ip = tds[i + 1].text
            port = img2port(tds[i + 2].img["src"])
            response_time = tds[i + 7]["title"][:-1]
            transport_time = tds[i + 8]["title"][:-1]
            if port is not None and float(response_time) < 1:
                proxy = "%s:%s" % (ip, port)
                proxyes.append(proxy)
    except:
        logger.warning("fail to fetch from mimvp")
    return proxyes


def fetch_xici():
    """
    http://www.xicidaili.com/nn/
    """
    proxyes = []
    try:
        url = "http://www.xicidaili.com/nn/"
        soup = get_soup(url)
        table = soup.find("table", attrs={"id": "ip_list"})
        trs = table.find_all("tr")
        for i in range(1, len(trs)):
            tr = trs[i]
            tds = tr.find_all("td")
            ip = tds[2].text
            port = tds[3].text
            speed = tds[7].div["title"][:-1]
            latency = tds[8].div["title"][:-1]
            if float(speed) < 3 and float(latency) < 1:
                proxyes.append("%s:%s" % (ip, port))
    except:
        logger.warning("fail to fetch from xici")
    return proxyes


def fetch_ip181():
    """
    http://www.ip181.com/
    """
    proxyes = []
    try:
        url = "http://www.ip181.com/"
        soup = get_soup(url)
        table = soup.find("table")
        trs = table.find_all("tr")
        for i in range(1, len(trs)):
            tds = trs[i].find_all("td")
            ip = tds[0].text
            port = tds[1].text
            latency = tds[4].text[:-2]
            if float(latency) < 1:
                proxyes.append("%s:%s" % (ip, port))
    except Exception as e:
        logger.warning("fail to fetch from ip181: %s" % e)
    return proxyes


def fetch_httpdaili():
    """
    http://www.httpdaili.com/mfdl/
    更新比较频繁
    """
    proxyes = []
    try:
        url = "http://www.httpdaili.com/mfdl/"
        soup = get_soup(url)
        table = soup.find("div", attrs={"kb-item-wrap11"}).table
        trs = table.find_all("tr")
        for i in range(1, len(trs)):
            try:
                tds = trs[i].find_all("td")
                ip = tds[0].text
                port = tds[1].text
                type = tds[2].text
                if type == u"匿名":
                    proxyes.append("%s:%s" % (ip, port))
            except:
                pass
    except Exception as e:
        logger.warning("fail to fetch from httpdaili: %s" % e)
    return proxyes


def fetch_66ip():
    """    
    http://www.66ip.cn/
    每次打开此链接都能得到一批代理, 速度不保证
    """
    proxyes = []
    try:
        # 修改getnum大小可以一次获取不同数量的代理
        url = "http://www.66ip.cn/nmtq.php?getnum=10&isp=0&anonymoustype=3&start=&ports=&export=&ipaddress=&area=1&proxytype=0&api=66ip"
        content = get_html(url)
        urls = content.split("</script>")[-1].split("<br />")
        for u in urls:
            if u.strip():
                proxyes.append(u.strip())
    except Exception as e:
        logger.warning("fail to fetch from httpdaili: %s" % e)
    return proxyes


def check(proxy):
    import requests
    # import urllib.request
    proxy = {'https': '{}'.format(proxy)}
    url = "http://www.baidu.com/js/bdsug.js?v=1.0.3.0"
    try:
        response = requests.request(method='get', url=url, proxies=proxy)
        return response.status_code == 200
    except Exception:
        return False
    # proxy_handler = urllib.request.ProxyHandler({'http': "http://" + proxy})
    # opener = urllib.request.build_opener(proxy_handler, urllib.request.HTTPHandler)
    # try:
    #     response = opener.open(url, timeout=3)
    #     return response.code == 200
    # except Exception:
    #     return False


def fetch_all(endpage=2):
    proxyes = []

    # dl()
    proxyes += dl()
    # for i in range(1, endpage):
    #     proxyes += fetch_kxdaili(i)
    # proxyes += fetch_mimvp()
    # proxyes += fetch_xici()
    # proxyes += fetch_ip181()
    # proxyes += fetch_httpdaili()
    # proxyes += fetch_66ip()
    # valid_proxyes = []
    # logger.info("checking proxyes validation")
    # for p in proxyes:
    #     if check(p):
    #         valid_proxyes.append(p)
    # logger.info("wxt ---------- 进来获取IP，执行 dl（）方法")
    return proxyes


if __name__ == '__main__':
    import sys

    proxyes = fetch_all()
    logger.info(proxyes)

    # print check("202.29.238.242:3128")
    # for p in proxyes:
    #     print  p
