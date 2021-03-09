import re
import os
import json
import math
import time
import requests
import pymysql
import docx
from win32com import client as wc
'''
shike 市科技
shengke 省科技
shengkeji zhongxiao 省科技中小
chuying 雏鹰计划
'''
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

def main():
    a = []
    num = 0
    single = 1

    data = {
        "startrecord": 1,
        "endrecord": 120,
        "perpage": 40,
        "col": 1,
        "appid": 1,
        "webid": 3387,
        "path": "/",
        "columnid": 1228971341,
        "sourceContentType": 1,
        "unitid": 5339897,
        "webname": "浙江省科技厅",
        "permissiontype": 0,
    }
    url = "http://kjt.zj.gov.cn/module/jpage/dataproxy.jsp?"
    response_web = ""
    for IP in range(10):
        try:
            response_web = requests.request(method='post', url=url, headers=headers, data=data, proxies=proxys[-1],timeout=10)
            if response_web.status_code == 200:
                response_web = response_web.content.decode('utf8')
                break
        except Exception:
            dl()
    print(response_web)
    pattern = re.compile('<totalrecord>(.*?)</totalrecord>')
    flag = int(pattern.findall(response_web)[0])
    print('--------------第一次请求，总数--------------', flag)
    number = math.ceil(flag/120)

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
            "webid": 3387,
            "path": "/",
            "columnid": 1228971341,
            "sourceContentType": 1,
            "unitid": 5339897,
            "webname": "浙江省科技厅",
            "permissiontype": 0,
        }
        url = "http://kjt.zj.gov.cn/module/jpage/dataproxy.jsp?"
        response = ""
        for IP in range(10):
            try:
                response = requests.post(url=url, headers=headers, data=data, proxies=proxys[-1], timeout=10)
                if response.status_code == 200:
                    response = response.content.decode('utf8')
                    break
            except Exception:
                dl()
        pattern = re.compile('<a href="(.*?)" title="(.*?)" target="_blank".*?<span>(.*?)</span>')
        all_data = pattern.findall(response)
        print(all_data)
        for j in all_data:
            db_dict = {}

            if '浙江省科技型中小' in j[1]:
            # if len(res) != 0 or len(res1) != 0 :
                if j[0].endswith('pdf') or 'http' in j[0]:
                    db_dict['url'] = j[0]
                else:
                    db_dict['url'] = 'http://kjt.zj.gov.cn'+j[0]
                db_dict['name'] = j[1]
                db_dict['gmt_updated'] = j[2]
                db_dict['project_name'] = "浙江省科技型中小企业"
                if db_dict not in a:
                    a.append(db_dict)

            elif '浙江省科技型' in j[1]:
                if j[0].endswith('pdf') or 'http' in j[0]:
                    db_dict['url'] = j[0]
                else:
                    db_dict['url'] = 'http://kjt.zj.gov.cn'+j[0]
                db_dict['name'] = j[1]
                db_dict['gmt_updated'] = j[2]
                db_dict['project_name'] = "浙江省科技型企业"
                if db_dict not in a:
                    a.append(db_dict)
        num += 120
        single += 1
        time.sleep(1.5)
    print(a)
    # exit()
    write_db(a)
    # test_detail(need_data)

def write_db(sum):

    db = pymysql.connect(host="localhost", user="root", password='123456', database="spider_gaoxinqiye", port=3306)
    cursor = db.cursor()
    for i in sum:
        url = i.get('url')
        name = i.get('name')
        project_name = i.get('project_name')
        gmt_updated = i.get('gmt_updated')
        area = "浙江省"
        source = "省科技厅"

        sql = """insert into one (id,url,title,project_name,gmt_updated,source,area)values(NULL,'{}','{}','{}','{}','{}','{}')""".format(url,name,project_name,gmt_updated,source,area)
        cursor.execute(sql)
        db.commit()
    db.close()
    # exit()

if __name__ == '__main__':
    main()
