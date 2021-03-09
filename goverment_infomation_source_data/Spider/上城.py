import re
import os
import json
import math
import time
import requests
import pymysql
import docx
from win32com import client as wc
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
    u = ['http://www.hzsc.gov.cn/col/col1267801/index.html','http://www.hzsc.gov.cn/col/col1268021/index.html']
    for i in u:
        url = i
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
            if '雏' in j[1] :
                if j[0].endswith('pdf') or 'http' in j[0]:
                    db_dict['url'] = j[0]
                else:
                    db_dict['url'] = 'http://www.hzsc.gov.cn'+j[0]
                db_dict['name'] = eval(j[1])
                db_dict['gmt_updated'] = j[2]+'-' + j[3] +'-'+ j[4]
                db_dict['project_name'] = "雏鹰计划"
                if db_dict not in a:
                    a.append(db_dict)
            elif '浙江省科技型中小企业' in j[1]:
                if j[0].endswith('pdf') or 'http' in j[0]:
                    db_dict['url'] = j[0]
                else:
                    db_dict['url'] = 'http://www.hzsc.gov.cn' + j[0]
                db_dict['name'] = eval(j[1])
                db_dict['gmt_updated'] = j[2]+'-' + j[3] +'-'+ j[4]
                db_dict['project_name'] = "浙江省科技型中小企业"
                if db_dict not in a:
                    a.append(db_dict)
        time.sleep(1.5)
    print(a)
    print([i['url'] for i in a])

    # write_db(a)

def write_db(sum):

    db = pymysql.connect(host="localhost", user="root", password='123456', database="spider_gaoxinqiye", port=3306)
    cursor = db.cursor()
    for i in sum:
        url = i.get('url')
        name = i.get('name')
        project_name = i.get('project_name')
        gmt_updated = i.get('gmt_updated')
        area = "上城区"
        source = "科技局"

        sql = """insert into spider_all_data (id,url,title,project_name,gmt_updated,source,area)values(NULL,'{}','{}','{}','{}','{}','{}')""".format(url,name,project_name,gmt_updated,area,source)
        cursor.execute(sql)
        db.commit()
    db.close()
    # exit()

if __name__ == '__main__':
    main()
