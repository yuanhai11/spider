#coding:utf-8
import re
import os
import json
import math
import time
import requests
import pymysql
import docx
import urllib.parse

from lxml import etree
from win32com import client as wc

db = pymysql.connect(host="localhost", user="root", password='123456', database="spider_gaoxinqiye", port=3306)
cursor = db.cursor()

headers = {
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
}
proxys = []
def dl():
    dlurl = 'http://dynamic.goubanjia.com/dynamic/get/d490a5d4debefc8980ae6ee4c4148552.html?sep=3'
    resp = requests.get(dlurl).text
    time.sleep(2)
    resp = re.sub(r'\n', '', resp)
    proxy = {
        'https':resp
    }
    proxys.append(proxy)
    print(proxys[-1])
dl()
url = 'http://www.jianggan.gov.cn/module/xxgk/search.jsp?standardXxgk=0&isAllList=1&texttype=&fbtime=&vc_all=&vc_filenumber=&vc_title=&vc_number=&currpage=1&sortfield=,compaltedate:0'
data = {
        'infotypeId': 'A0100503',
        'jdid': 2143,
        'divid': 'div1256933',
        'compaltedate':0,
        'currpage': 1,
        'standardXxgk': 0,
        'isAllList': 1,
        }
res = requests.post(url=url, headers=headers,data=data,proxies=proxys[-1]).text
print(res)
number = int(re.findall('页/共&nbsp;(.*?)&nbsp;页', res,re.S)[0])
sum = []
for i in range(1,number+1):
    url = 'http://www.jianggan.gov.cn/module/xxgk/search.jsp?standardXxgk=0&isAllList=1&texttype=&fbtime=&vc_all=&vc_filenumber=&vc_title=&vc_number=&currpage=%s&sortfield=,compaltedate:0'%i
    data = {
            'infotypeId': 'A0100503',
            'jdid': 2143,
            'divid': 'div1256933',
            'compaltedate':0,
            'currpage': i,
            'standardXxgk': 0,
            'isAllList': 1,
            }
    aaa = requests.post(url=url, headers=headers,data=data,proxies=proxys[-1]).text
    lists = re.findall(
        '''<a href='(.*?)' target='_blank' title='(.*?)' class='bt_link' style='line-height:35px;' >.*?</a></td><td align='center' width='80'>(.*?)</td><td align='center' width='180'>(.*?)</td>''',
        aaa, re.S)

    for i in lists:
        print(i)
        if '浙江省科技型中小企业' in i[1]:
            db_dict = {}

            db_dict['url'] = i[0]
            db_dict['title'] = i[1]
            db_dict['year'] = i[2]
            db_dict['project_name'] = '省科技型中小'
            db_dict['source'] = '科技局'
            db_dict['area'] = '江干区'
            if db_dict not in sum:
                sum.append(db_dict)
        elif '市级高新技术企业' in i[1]:
            db_dict = {}
            db_dict['url'] = i[0]
            db_dict['title'] = i[1]
            db_dict['gmt_updated'] = i[2]
            db_dict['project_name'] = '市高'
            db_dict['source'] = '科技局'
            db_dict['area'] = '江干区'
            if db_dict not in sum:
                sum.append(db_dict)
    time.sleep(1.4)
print(sum)
def main():
    sum = [{'url': 'http://www.jianggan.gov.cn/art/2018/11/22/art_1257287_25547419.html', 'title': '转发市科委《关于开展2018年第三批杭州市级高新技术企业申报的通知》', 'year': '2018-11-22', 'project_name': '市高', 'source': '科技局', 'area': '江干区'}, {'url': 'http://www.jianggan.gov.cn/art/2018/8/16/art_1257287_20454580.html', 'title': '转发市科委《关于认定2018年杭州市第一批浙江省科技型中小企业的通知》', 'year': '2018-08-16', 'project_name': '省科技型中小', 'source': '科技局', 'area': '江干区'}, {'url': 'http://www.jianggan.gov.cn/art/2017/12/27/art_1257287_14677927.html', 'title': '转发市科委《2017年第二批杭州市级高新技术企业认定公示》', 'year': '2017-12-27', 'project_name': '市高', 'source': '科技局', 'area': '江干区'}, {'url': 'http://www.jianggan.gov.cn/art/2017/12/21/art_1257287_14473193.html', 'title': '转发市科委《关于认定2017年杭州市第三批浙江省科技型中小企业的通知 》', 'year': '2017-12-21', 'project_name': '省科技型中小', 'source': '科技局', 'area': '江干区'}, {'url': 'http://www.jianggan.gov.cn/art/2017/11/27/art_1257287_13331327.html', 'title': '转发市科委《关于开展2017年第二批杭州市级高新技术企业认定工作的通知》', 'year': '2017-11-27', 'project_name': '市高', 'source': '科技局', 'area': '江干区'}, {'url': 'http://www.jianggan.gov.cn/art/2016/12/27/art_1257287_4791419.html', 'title': '转发市科委《关于认定2016年杭州市第三批浙江省科技型中小企业的通知》', 'year': '2016-12-27', 'project_name': '省科技型中小', 'source': '科技局', 'area': '江干区'}, {'url': 'http://www.jianggan.gov.cn/art/2016/5/16/art_1257287_4764284.html', 'title': '转发市科委《关于开展2016年第一批杭州市级高新技术企业认定工作的通知 》', 'year': '2016-05-16', 'project_name': '市高', 'source': '科技局', 'area': '江干区'}, {'url': 'http://www.jianggan.gov.cn/art/2015/5/14/art_1257287_4764317.html', 'title': '转发市科委《关于组织开展2015年杭州市级高新技术企业认定工作的通知》', 'year': '2015-05-14', 'project_name': '市高', 'source': '科技局', 'area': '江干区'}]
    for i in sum:
        url = i.get('url')
        name = i.get('title')
        project_name = i.get('project_name')
        gmt_updated = i.get('year')
        area = "江干区"
        source = "科技局"

        sql = """insert into spider_all_data (id,url,title,project_name,gmt_updated,source,area)values(NULL,'{}','{}','{}','{}','{}','{}')""".format(
            url, name, project_name, gmt_updated, source,area)
        cursor.execute(sql)
        db.commit()
    db.close()
if __name__ == '__main__':
    main()