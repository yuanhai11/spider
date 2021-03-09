import re
import os
import json
import math
import time
import requests
import pymysql
import docx
from lxml import etree
from win32com import client as wc

db = pymysql.connect(host="localhost", user="root", password='123456', database="spider_gaoxinqiye", port=3306)
cursor = db.cursor()
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
}
proxys = []
def dl():
    dlurl = 'http://dynamic.goubanjia.com/dynamic/get/d490a5d4debefc8980ae6ee4c4148552.html?sep=3'
    resp = requests.get(dlurl).text
    time.sleep(2)
    resp = re.sub(r'\n', '', resp)
    proxy = {
        'https': resp
    }
    proxys.append(proxy)
    print(proxys[-1])
dl()

def one():
    a = []
    num = 0
    single = 1
    data = {
        "startrecord": 1,
        "endrecord": 120,
        "perpage": 40,
        "col": 1,
        "appid": 1,
        "webid": 3255,
        "path": "/",
        "columnid": 1693962,
        "sourceContentType": 1,
        "unitid": 5099936,
        "webname": "杭州市科学技术局",
        "permissiontype": 0,
    }
    url = "http://kj.hangzhou.gov.cn/module/jpage/dataproxy.jsp?"
    response_web = ""
    for IP in range(10):
        try:
            response_web = requests.request(method='post', url=url, headers=headers, data=data, proxies=proxys[-1],
                                            timeout=10)
            if response_web.status_code == 200:
                response_web = response_web.content.decode('utf8')
                break
        except Exception:
            dl()
    pattern = re.compile('<totalrecord>(.*?)</totalrecord>')
    flag = int(pattern.findall(response_web)[0])
    print('--------------第一次请求，总数--------------', flag)
    number = math.ceil(flag / 120)

    for i in range(number):
        startrecord = num + 1
        endrecord = 120 * single
        if endrecord > flag:
            endrecord = flag
        data = {
            "startrecord": startrecord,
            "endrecord": endrecord,
            "perpage": 40,
            "col": 1,
            "appid": 1,
            "webid": 3255,
            "path": "/",
            "columnid": 1693962,
            "sourceContentType": 1,
            "unitid": 5099936,
            "webname": "杭州市科学技术局",
            "permissiontype": 0,
        }
        url = "http://kj.hangzhou.gov.cn/module/jpage/dataproxy.jsp?"
        response = ""
        for IP in range(10):
            try:
                response = requests.request(method='post', url=url,data=data, headers=headers, proxies=proxys[-1],timeout=10)
                if response.status_code == 200:
                    response = response.content.decode('utf8')
                    break
            except Exception:
                dl()
        pa = re.compile('<a href="(.*?)" target="_blank" title="(.*?)".*?<span.*?>(.*?)</span>')
        all_data = pa.findall(response)
        print(all_data)
        for j in all_data:
            db_dict = {}
            if "浙江省科技型中小企业" in j[1]:
                if 'http' in j[0] or j[0].endswith('pdf'):
                    db_dict['url'] = j[0]
                else:
                    db_dict['url'] = 'http://kj.hangzhou.gov.cn' + j[0]
                db_dict['title'] = j[1]
                db_dict['gmt_updated'] = j[2].strip()
                db_dict['project_name'] = "浙江省科技型中小企业"
                db_dict['area'] = "杭州市"
                db_dict['source'] = "科技局"
                a.append(db_dict)
            elif '浙江省科技型' in j[1]:
                if 'http' in j[0] or j[0].endswith('pdf'):
                    db_dict['url'] = j[0]
                else:
                    db_dict['url'] = 'http://kj.hangzhou.gov.cn' + j[0]
                db_dict['title'] = j[1]
                db_dict['gmt_updated'] = j[2].strip()
                db_dict['project_name'] = "浙江省科技型企业"
                db_dict['area'] = "杭州市"
                db_dict['source'] = "科技局"
                a.append(db_dict)
            elif "雏鹰计划" in j[1]:
                if 'http' in j[0] or j[0].endswith('pdf'):
                    db_dict['url'] = j[0]
                else:
                    db_dict['url'] = 'http://kj.hangzhou.gov.cn' + j[0]
                db_dict['title'] = j[1]
                db_dict['gmt_updated'] = j[2].strip()
                db_dict['project_name'] = "雏鹰计划"
                db_dict['area'] = "杭州市"
                db_dict['source'] = "科技局"
                a.append(db_dict)
            elif "杭州市级高新技术企业的通知" in j[1]:
                if 'http' in j[0] or j[0].endswith('pdf'):
                    db_dict['url'] = j[0]
                else:
                    db_dict['url'] = 'http://kj.hangzhou.gov.cn' + j[0]
                db_dict['title'] = j[1]
                db_dict['gmt_updated'] = j[2].strip()
                db_dict['project_name'] = "杭州市级高新技术企业"
                db_dict['area'] = "杭州市"
                db_dict['source'] = "科技局"
                a.append(db_dict)
        num += 120
        single += 1
        time.sleep(2.5)
    print(a)
    # exit()

    for i in a:
        url = i.get('url')
        name = i.get('name')
        project_name = i.get('project_name')
        gmt_updated = i.get('gmt_updated')
        area = "杭州市"
        source = "科技局"

        sql = """insert into spider_all_data (id,url,title,project_name,gmt_updated,source,area)values(NULL,'{}','{}','{}','{}','{}','{}')""".format(
            url, name, project_name, gmt_updated, source,area )
        cursor.execute(sql)
        db.commit()
    db.close()
def two():
    a = []
    num = 0
    single = 1
    data = {
        "startrecord": 1,
        "endrecord": 120,
        "perpage": 40,
        "col": 1,
        "appid": 1,
        "webid": 3255,
        "path": "/",
        "columnid": 1693961,
        "sourceContentType": 1,
        "unitid": 5099936,
        "webname": "杭州市科学技术局",
        "permissiontype": 0,
    }
    url = "http://kj.hangzhou.gov.cn/module/jpage/dataproxy.jsp?"
    response_web = ""
    for IP in range(10):
        try:
            response_web = requests.request(method='post', url=url, headers=headers, data=data, proxies=proxys[-1],
                                            timeout=10)
            if response_web.status_code == 200:
                response_web = response_web.content.decode('utf8')
                break
        except Exception:
            dl()
    pattern = re.compile('<totalrecord>(.*?)</totalrecord>')
    flag = int(pattern.findall(response_web)[0])
    print('--------------第一次请求，总数--------------', flag)
    number = math.ceil(flag / 120)

    for i in range(number):
        startrecord = num + 1
        endrecord = 120 * single
        if endrecord > flag:
            endrecord = flag
        data = {
            "startrecord": startrecord,
            "endrecord": endrecord,
            "perpage": 40,
            "col": 1,
            "appid": 1,
            "webid": 3255,
            "path": "/",
            "columnid": 1693961,
            "sourceContentType": 1,
            "unitid": 5099936,
            "webname": "杭州市科学技术局",
            "permissiontype": 0,
        }
        url = "http://kj.hangzhou.gov.cn/module/jpage/dataproxy.jsp?"
        response = ""
        for IP in range(10):
            try:
                response = requests.request(method='post', url=url, data=data, headers=headers, proxies=proxys[-1],
                                            timeout=10)
                if response.status_code == 200:
                    response = response.content.decode('utf8')
                    break
            except Exception:
                dl()
        pa = re.compile('<a href="(.*?)" target="_blank" title="(.*?)".*?<span.*?>(.*?)</span>')
        all_data = pa.findall(response)
        print(all_data)
        for j in all_data:
            db_dict = {}
            if "杭州市“雏鹰计划”企业的通知" in j[1]:
                if 'http' in j[0] or j[0].endswith('pdf'):
                    db_dict['url'] = j[0]
                else:
                    db_dict['url'] = 'http://kj.hangzhou.gov.cn' + j[0]
                db_dict['name'] = j[1]
                db_dict['gmt_updated'] = j[2].strip()
                db_dict['project_name'] = "雏鹰计划"
                if db_dict not in a:
                    a.append(db_dict)
        num += 120
        single += 1
        time.sleep(2.5)
    for i in a:
        url = i.get('url')
        name = i.get('name')
        project_name = i.get('project_name')
        gmt_updated = i.get('gmt_updated')
        area = "杭州市"
        source = "科技局"

        sql = """insert into two_2 (id,url,title,project_name,gmt_updated,source,area)values(NULL,'{}','{}','{}','{}','{}','{}')""".format(
            url, name, project_name, gmt_updated, area, source)
        cursor.execute(sql)
        db.commit()
    db.close()
def three():
    a = []
    num = 0
    single = 1
    data = {
        "startrecord": 1,
        "endrecord": 120,
        "perpage": 40,
        "col": 1,
        "appid": 1,
        "webid": 3255,
        "path": "/",
        "columnid": 1693961,
        "sourceContentType": 1,
        "unitid": 5099936,
        "webname": "杭州市科学技术局",
        "permissiontype": 0,
    }
    url = "http://kj.hangzhou.gov.cn/module/jpage/dataproxy.jsp?"
    response_web = ""
    for IP in range(10):
        try:
            response_web = requests.request(method='post', url=url, headers=headers, data=data, proxies=proxys[-1],
                                            timeout=10)
            if response_web.status_code == 200:
                response_web = response_web.content.decode('utf8')
                break
        except Exception:
            dl()
    pattern = re.compile('<totalrecord>(.*?)</totalrecord>')
    flag = int(pattern.findall(response_web)[0])
    print('--------------第一次请求，总数--------------', flag)
    number = math.ceil(flag / 120)

    for i in range(number):
        startrecord = num + 1
        endrecord = 120 * single
        if endrecord > flag:
            endrecord = flag
        data = {
            "startrecord": startrecord,
            "endrecord": endrecord,
            "perpage": 40,
            "col": 1,
            "appid": 1,
            "webid": 3255,
            "path": "/",
            "columnid": 1693961,
            "sourceContentType": 1,
            "unitid": 5099936,
            "webname": "杭州市科学技术局",
            "permissiontype": 0,
        }
        url = "http://kj.hangzhou.gov.cn/module/jpage/dataproxy.jsp?"
        response = ""
        for IP in range(10):
            try:
                response = requests.request(method='post', url=url, data=data, headers=headers, proxies=proxys[-1],
                                            timeout=10)
                if response.status_code == 200:
                    response = response.content.decode('utf8')
                    break
            except Exception:
                dl()
        pa = re.compile('<a href="(.*?)" target="_blank" title="(.*?)".*?<span.*?>(.*?)</span>')
        all_data = pa.findall(response)
        print(all_data)
        for j in all_data:
            db_dict = {}
            if "杭州市级高新技术企业的通知" in j[1]:
                if 'http' in j[0] or j[0].endswith('pdf'):
                    db_dict['url'] = j[0]
                else:
                    db_dict['url'] = 'http://kj.hangzhou.gov.cn' + j[0]
                db_dict['name'] = j[1]
                db_dict['gmt_updated'] = j[2].strip()
                db_dict['project_name'] = "杭州市级高新技术企业"
                if db_dict not in a:
                    a.append(db_dict)
        num += 120
        single += 1
        time.sleep(2.5)

    for i in a:
        url = i.get('url')
        name = i.get('name')
        project_name = i.get('project_name')
        gmt_updated = i.get('gmt_updated')
        area = "杭州市"
        source = "科技局"

        sql = """insert into two_3 (id,url,title,project_name,gmt_updated,source,area)values(NULL,'{}','{}','{}','{}','{}','{}')""".format(
            url, name, project_name, gmt_updated, area, source)
        cursor.execute(sql)
        db.commit()
    db.close()


if __name__ == '__main__':
    one()
