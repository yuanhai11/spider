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

    url = "http://www.yuhang.gov.cn/col/col1601762/index.html"
    response_web = ""
    for IP in range(10):
        try:
            response_web = requests.request(method='get', url=url, headers=headers, proxies=proxys[-1],timeout=10)
            if response_web.status_code == 200:
                response_web = response_web.content.decode('utf8')
                break
        except Exception:
            dl()
    print(response_web)
    pattern = re.compile("urls.*?='(.*?)';.*?headers.*?=(.*?);.*?year.*?='(.*?)';.*?month.*?='(.*?)';.*?day.*?='(.*?)';",re.S)
    all_data = pattern.findall(response_web)
    print(all_data)
    for j in all_data:
        db_dict = {}

        # pattern = re.compile(r'浙江省科学技术厅关于.*?年度浙江省科技型中小企业')
        # res = pattern.findall(j[1])
        # pattern1 = re.compile(r'.*?年第.*?批浙江省科技型中小企业认定公示')
        # res1 = pattern1.findall(j[1])
        if '雏鹰计划' in j[1] :
            if j[0].endswith('pdf') or 'http' in j[0]:
                db_dict['url'] = j[0]
            else:
                db_dict['url'] = 'http://www.yuhang.gov.cn'+j[0]
            db_dict['name'] = eval(j[1])
            db_dict['gmt_updated'] = j[2] + j[3] +  j[4]
            db_dict['project_name'] = "雏鹰计划"
            if db_dict not in a:
                a.append(db_dict)
    time.sleep(1.5)
    write_db(a)

def write_db(sum):

    db = pymysql.connect(host="localhost", user="root", password='123456', database="spider_gaoxinqiye", port=3306)
    cursor = db.cursor()
    for i in sum:
        url = i.get('url')
        name = i.get('name')
        project_name = i.get('project_name')
        gmt_updated = i.get('gmt_updated')
        area = "萧山区"
        source = "科技局"

        sql = """insert into eight (id,url,title,project_name,gmt_updated,source,area)values(NULL,'{}','{}','{}','{}','{}','{}')""".format(url,name,project_name,gmt_updated,area,source)
        cursor.execute(sql)
        db.commit()
    db.close()
    # exit()

if __name__ == '__main__':
    main()
