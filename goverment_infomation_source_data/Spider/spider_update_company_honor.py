#encoding:utf-8
import re
import math
import time
import requests
import pymysql
import hashlib
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
}
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

db = pymysql.connect(host="localhost", user="root", password='123456', database="spider_gaoxinqiye", port=3306)
cursor = db.cursor()

def write_db(sum):
    for i in sum:
        url = i.get('url')
        name = i.get('title')
        project_name = i.get('project_name')
        gmt_updated = i.get('gmt_updated')
        source = i.get('source')
        area = i.get('area')
        finger_print = i.get('finger')
        spider_update = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        sql = """insert into spider_all_data (id,url,title,project_name,gmt_updated,source,area,finger_print,spider_updated)values(NULL,'{}','{}','{}','{}','{}','{}','{}','{}')""".format(
            url, name, project_name, gmt_updated,source, area,finger_print,spider_update)
        cursor.execute(sql)
        db.commit()
    db.close()

'''
# 浙江省 
# POST请求
# url = "http://kjt.zj.gov.cn/module/jpage/dataproxy.jsp?"
'''
def zjs():
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
                if j[0].endswith('pdf') or 'http' in j[0]:
                    db_dict['url'] = j[0]
                else:
                    db_dict['url'] = 'http://kjt.zj.gov.cn' + j[0]
                db_dict['title'] = j[1]
                db_dict['gmt_updated'] = j[2]
                db_dict['project_name'] = "浙江省科技型中小企业"
                db_dict['source'] = "省科技厅"
                db_dict['area'] = "浙江省"
                if db_dict not in sum:
                    sum.append(db_dict)
            elif '浙江省科技型' in j[1]:
                if j[0].endswith('pdf') or 'http' in j[0]:
                    db_dict['url'] = j[0]
                else:
                    db_dict['url'] = 'http://kjt.zj.gov.cn' + j[0]
                db_dict['title'] = j[1]
                db_dict['gmt_updated'] = j[2]
                db_dict['project_name'] = "浙江省科技型企业"
                db_dict['source'] = "省科技厅"
                db_dict['area'] = "浙江省"
                if db_dict not in sum:
                    sum.append(db_dict)
        num += 120
        single += 1
        time.sleep(1.5)
'''
# 杭州市
# POST
# http://kj.hangzhou.gov.cn/module/jpage/dataproxy.jsp?
'''
def hzs():
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
                sum.append(db_dict)
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
                sum.append(db_dict)
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
                sum.append(db_dict)
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
                sum.append(db_dict)
        num += 120
        single += 1
        time.sleep(2.5)

'''
# 上城区
# 'http://www.hzsc.gov.cn/col/col1267801/index.html'，'http://www.hzsc.gov.cn/col/col1268021/index.html
#  GET
'''
def scq():
    u = ['http://www.hzsc.gov.cn/col/col1267801/index.html', 'http://www.hzsc.gov.cn/col/col1268021/index.html']
    for i in u:
        url = i
        response_web = ""
        for IP in range(10):
            try:
                response_web = requests.request(method='get', url=url, headers=headers, proxies=proxys[-1], timeout=10)
                if response_web.status_code == 200:
                    response_web = response_web.content.decode('utf8')
                    break
            except Exception:
                dl()
        print(response_web)
        pattern = re.compile(
            "urls.*?='(.*?)';.*?headers.*?=(.*?);.*?year.*?='(.*?)';.*?month.*?='(.*?)';.*?day.*?='(.*?)';", re.S)
        all_data = pattern.findall(response_web)
        print(all_data)
        for j in all_data:
            db_dict = {}
            if '雏' in j[1]:
                if j[0].endswith('pdf') or 'http' in j[0]:
                    db_dict['url'] = j[0]
                else:
                    db_dict['url'] = 'http://www.hzsc.gov.cn' + j[0]
                db_dict['title'] = eval(j[1])
                db_dict['gmt_updated'] = j[2] + '-' + j[3] + '-' + j[4]
                db_dict['project_name'] = "雏鹰计划"
                db_dict['area'] = "上城区"
                db_dict['source'] = "科技局"
                sum.append(db_dict)
            elif '浙江省科技型中小企业' in j[1]:
                if j[0].endswith('pdf') or 'http' in j[0]:
                    db_dict['url'] = j[0]
                else:
                    db_dict['url'] = 'http://www.hzsc.gov.cn' + j[0]
                db_dict['title'] = eval(j[1])
                db_dict['gmt_updated'] = j[2] + '-' + j[3] + '-' + j[4]
                db_dict['project_name'] = "浙江省科技型中小企业"
                db_dict['area'] = "上城区"
                db_dict['source'] = "科技局"
                sum.append(db_dict)
        time.sleep(1.5)

'''
#  下城区
#  http://www.hzxc.gov.cn/module/jpage/dataproxy.jsp
#  POST
'''
def xcq():
    num = 0
    single = 1
    data = {
        "startrecord": 1,
        "endrecord": 30,
        "perpage": 10,
        "col": 1,
        "appid": 1,
        "webid": 2973,
        "path": "/",
        "columnid": 1509909,
        "sourceContentType": 1,
        "unitid": 4667837,
    }
    url = "http://www.hzxc.gov.cn/module/jpage/dataproxy.jsp?"
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
            "webid": 2973,
            "path": "/",
            "columnid": 1509909,
            "sourceContentType": 1,
            "unitid": 4667837,
        }
        url = "http://www.hzxc.gov.cn/module/jpage/dataproxy.jsp?"
        response = ""
        for IP in range(10):
            try:
                response = requests.post(url=url, headers=headers, data=data, proxies=proxys[-1], timeout=10)
                if response.status_code == 200:
                    response = response.content.decode('utf8')
                    break
            except Exception:
                dl()
        pattern = re.compile('<a href="(.*?)".*?<span>(.*?)</span><i>(.*?)</i>')
        all_data = pattern.findall(response)
        print(all_data)
        for j in all_data:
            db_dict = {}

            if '杭州市“雏鹰计划”企业和杭州市级高新技术企业认定' in j[1]:
                if j[0].endswith('pdf') or 'http' in j[0]:
                    db_dict['url'] = j[0]
                else:
                    db_dict['url'] = 'http://www.hzxc.gov.cn' + j[0]
                db_dict['title'] = j[1]
                db_dict['gmt_updated'] = j[2]
                db_dict['project_name'] = "雏鹰计划"
                db_dict['area'] = "下城区"
                db_dict['source'] = "科技局"
                sum.append(db_dict)
        num += 120
        single += 1
        time.sleep(1.5)

'''
#  余杭区
#  http://www.yuhang.gov.cn/col/col1601762/index.html
#  GET
'''
def yhq():
    url = "http://www.yuhang.gov.cn/col/col1601762/index.html"
    response_web = ""
    for IP in range(10):
        try:
            response_web = requests.request(method='get', url=url, headers=headers, proxies=proxys[-1], timeout=10)
            if response_web.status_code == 200:
                response_web = response_web.content.decode('utf8')
                break
        except Exception:
            dl()
    print(response_web)
    pattern = re.compile(
        "urls.*?='(.*?)';.*?headers.*?=(.*?);.*?year.*?='(.*?)';.*?month.*?='(.*?)';.*?day.*?='(.*?)';", re.S)
    all_data = pattern.findall(response_web)
    print(all_data)
    for j in all_data:
        db_dict = {}
        if '雏鹰计划' in j[1]:
            if j[0].endswith('pdf') or 'http' in j[0]:
                db_dict['url'] = j[0]
            else:
                db_dict['url'] = 'http://www.yuhang.gov.cn' + j[0]
            db_dict['title'] = eval(j[1])
            db_dict['gmt_updated'] = j[2] + j[3] + j[4]
            db_dict['project_name'] = "雏鹰计划"
            db_dict['area'] = "余杭区"
            db_dict['source'] = "科技局"
            sum.append(db_dict)

'''
#  拱墅区
#  http://www.yuhang.gov.cn/col/col1601762/index.html
#  GET
'''
def gsq():
    data = {
        "startrecord": 1,
        "endrecord": 100,
        "perpage": 40,
        "col": 1,
        "appid": 1,
        "webid": 2096,
        "path": "/",
        "columnid": 1230548,
        "sourceContentType": 1,
        "unitid": 4535233,
        "webname": "杭州市拱墅区人民政府",
        "permissiontype": 0,
    }
    url = "http://www.gongshu.gov.cn/module/jpage/dataproxy.jsp?"
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
    pattern = re.compile('<a href="(.*?)" target="_blank">(.*?)<span.*?>(.*?)</span>')
    all_data = pattern.findall(response_web)
    print(all_data)
    for j in all_data:
        db_dict = {}
        if '市级高新技术企业' in j[1]:
            if j[0].endswith('pdf') or 'http' in j[0]:
                db_dict['url'] = j[0]
            else:
                db_dict['url'] = 'http://www.gongshu.gov.cn' + j[0]
            db_dict['title'] = j[1]
            db_dict['gmt_updated'] = j[2]
            db_dict['project_name'] = "市级高新技术企业"
            db_dict['area'] = "拱墅区"
            db_dict['source'] = "科技局"
            sum.append(db_dict)

'''
#  江干区
#  http://www.jianggan.gov.cn/module/xxgk/search.jsp?standardXxgk=0&isAllList=1&texttype=&fbtime=&vc_all=&vc_filenumber=&vc_title=&vc_number=&currpage=1&sortfield=,compaltedate:0
#  POST
'''
def jgq():
    url = 'http://www.jianggan.gov.cn/module/xxgk/search.jsp?standardXxgk=0&isAllList=1&texttype=&fbtime=&vc_all=&vc_filenumber=&vc_title=&vc_number=&currpage=1&sortfield=,compaltedate:0'
    data = {
        'infotypeId': 'A0100503',
        'jdid': 2143,
        'divid': 'div1256933',
        'compaltedate': 0,
        'currpage': 1,
        'standardXxgk': 0,
        'isAllList': 1,
    }
    res = requests.post(url=url, headers=headers, data=data, proxies=proxys[-1]).text
    number = int(re.findall('页/共&nbsp;(.*?)&nbsp;页', res, re.S)[0])
    sum = []
    for i in range(1, number + 1):
        url = 'http://www.jianggan.gov.cn/module/xxgk/search.jsp?standardXxgk=0&isAllList=1&texttype=&fbtime=&vc_all=&vc_filenumber=&vc_title=&vc_number=&currpage=%s&sortfield=,compaltedate:0' % i
        data = {
            'infotypeId': 'A0100503',
            'jdid': 2143,
            'divid': 'div1256933',
            'compaltedate': 0,
            'currpage': i,
            'standardXxgk': 0,
            'isAllList': 1,
        }
        aaa = requests.post(url=url, headers=headers, data=data, proxies=proxys[-1]).text
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
                sum.append(db_dict)
            elif '市级高新技术企业' in i[1]:
                db_dict = {}
                db_dict['url'] = i[0]
                db_dict['title'] = i[1]
                db_dict['gmt_updated'] = i[2]
                db_dict['project_name'] = '市高'
                db_dict['source'] = '科技局'
                db_dict['area'] = '江干区'
                sum.append(db_dict)
        time.sleep(1.4)

'''
# 滨江区
# http://www.hhtz.gov.cn/module/jpage/dataproxy.jsp?
# POST
'''
def bjq():
    num = 0
    single = 1
    data = {
        "startrecord": 1,
        "endrecord": 120,
        "perpage": 40,
        "col": 1,
        "appid": 1,
        "webid": 2945,
        "path": "/",
        "columnid": 1485818,
        "sourceContentType": 1,
        "unitid": 4678776,
        "webname": "杭州高新区（滨江）门户网站",
        "permissiontype": 0,
    }
    url = "http://www.hhtz.gov.cn/module/jpage/dataproxy.jsp?"
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
            "webid": 2945,
            "path": "/",
            "columnid": 1485818,
            "sourceContentType": 1,
            "unitid": 4678776,
            "webname": "杭州高新区（滨江）门户网站",
            "permissiontype": 0,
        }
        url = "http://www.hhtz.gov.cn/module/jpage/dataproxy.jsp?"
        response = ""
        for IP in range(10):
            try:
                response = requests.post(url=url, headers=headers, data=data, proxies=proxys[-1], timeout=10)
                if response.status_code == 200:
                    response = response.content.decode('utf8')
                    break
            except Exception:
                dl()
        pattern = re.compile('<a href="(.*?)" .*?>(.*?)</a>.*?<span.*?>(.*?)</span>', re.S)
        all_data = pattern.findall(response)
        print(all_data)
        for j in all_data:
            db_dict = {}

            if '浙江省科技型中小企业' in j[1]:
                pattern = re.compile(r'.*关于下达.*?浙江省科技型中小企业资助经费的通知')
                res = pattern.findall(j[1])
                if len(res) !=0:
                    if j[0].endswith('pdf') or 'http' in j[0]:
                        db_dict['url'] = j[0]
                    else:
                        db_dict['url'] = 'http://www.hhtz.gov.cn' + j[0]
                    db_dict['title'] = j[1]
                    db_dict['gmt_updated'] = j[2]
                    db_dict['project_name'] = "浙江省科技型中小企业"
                    db_dict['source'] = '科技局'
                    db_dict['area'] = '滨江区'

                    sum.append(db_dict)
            elif '雏鹰' in j[1]:
                if j[0].endswith('pdf') or 'http' in j[0]:
                    db_dict['url'] = j[0]
                else:
                    db_dict['url'] = 'http://www.hhtz.gov.cn' + j[0]
                db_dict['title'] = j[1]
                db_dict['gmt_updated'] = j[2]
                db_dict['project_name'] = "雏鹰计划"
                db_dict['source'] = '科技局'
                db_dict['area'] = '滨江区'
                sum.append(db_dict)
            elif '国家高新技术企业' in j[1]:
                pattern = re.compile(r'国家高新技术企业.*奖励名单公示')
                res = pattern.findall(j[1])
                pattern1 = re.compile(r'关于办理杭州高新区（滨江）.*年认定或新引进国家高新技术企业奖励的通知')
                res1 = pattern1.findall(j[1])
                if len(res) != 0 or len(res1) != 0:
                    if j[0].endswith('pdf') or 'http' in j[0]:
                        db_dict['url'] = j[0]
                    else:
                        db_dict['url'] = 'http://www.hhtz.gov.cn' + j[0]
                    db_dict['title'] = j[1]
                    db_dict['gmt_updated'] = j[2]
                    db_dict['project_name'] = "国家高新技术企业"
                    db_dict['source'] = '科技局'
                    db_dict['area'] = '滨江区'
                    sum.append(db_dict)
        num += 120
        single += 1
        time.sleep(1.5)
'''
# 萧山区
# http://www.xiaoshan.gov.cn/module/jpage/dataproxy.jsp?
# POST
'''
def xsq():
    num = 0
    single = 1

    data = {
        "startrecord": 1,
        "endrecord": 120,
        "perpage": 40,
        "col": 1,
        "appid": 1,
        "webid": 2243,
        "path": "/",
        "columnid": 1684591,
        "sourceContentType": 1,
        "unitid": 5066478,
    }
    url = "http://www.xiaoshan.gov.cn/module/jpage/dataproxy.jsp?"
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
            "webid": 2243,
            "path": "/",
            "columnid": 1684591,
            "sourceContentType": 1,
            "unitid": 5066478,
        }
        url = "http://www.xiaoshan.gov.cn/module/jpage/dataproxy.jsp?"
        response = ""
        for IP in range(10):
            try:
                response = requests.post(url=url, headers=headers, data=data, proxies=proxys[-1], timeout=10)
                if response.status_code == 200:
                    response = response.content.decode('utf8')
                    break
            except Exception:
                dl()
        pattern = re.compile('<a href="(.*?)">(.*?)</a><span.*?>(.*?)</span>')
        all_data = pattern.findall(response)
        print(all_data)

        for j in all_data:
            db_dict = {}

            if '雏鹰计划' in j[1]:
                if j[0].endswith('pdf') or 'http' in j[0]:
                    db_dict['url'] = j[0]
                else:
                    db_dict['url'] = 'http://www.xiaoshan.gov.cn' + j[0]
                db_dict['title'] = j[1]
                db_dict['gmt_updated'] = j[2]
                db_dict['project_name'] = "雏鹰计划"
                db_dict['source'] = '科技局'
                db_dict['area'] = '萧山区'
                sum.append(db_dict)
        num += 120
        single += 1
        time.sleep(1.5)

'''
# 西湖区
# http://www.hzxh.gov.cn/module/jpage/dataproxy.jsp?
# POST
'''
def xhq():
    num = 0
    single = 1
    data = {
        "startrecord": 1,
        "endrecord": 60,
        "perpage": 20,
        "col": 1,
        "appid": 1,
        "webid": 1838,
        "path": "/",
        "columnid": 1177988,
        "sourceContentType": 1,
        "unitid": 3970333,
        "webname": "杭州市西湖区政府",
        "permissiontype": 0,
    }
    url = "http://www.hzxh.gov.cn/module/jpage/dataproxy.jsp?"
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
    number = math.ceil(flag / 60)
    for i in range(number):
        startrecord = num + 1
        endrecord = 60 * single
        if endrecord > flag:
            endrecord = flag
        data = {
            "startrecord": startrecord,
            "endrecord": endrecord,
            "perpage": 20,
            "col": 1,
            "appid": 1,
            "webid": 1838,
            "path": "/",
            "columnid": 1177988,
            "sourceContentType": 1,
            "unitid": 3970333,
            "webname": "杭州市西湖区政府",
            "permissiontype": 0,
        }
        url = "http://www.hzxh.gov.cn/module/jpage/dataproxy.jsp?"
        response = ""
        for IP in range(10):
            try:
                response = requests.post(url=url, headers=headers, data=data, proxies=proxys[-1], timeout=10)
                if response.status_code == 200:
                    response = response.content.decode('utf8')
                    break
            except Exception:
                dl()
        pattern = re.compile("<a .*?href='(.*?)' .*?title='(.*?)'>.*?<span.*?>(.*?)</span>", re.S)
        all_data = pattern.findall(response)
        print(all_data)
        for j in all_data:
            db_dict = {}
            if '浙江省科技型中小企业' in j[1]:
                if j[0].endswith('pdf') or 'http' in j[0]:
                    db_dict['url'] = j[0]
                else:
                    db_dict['url'] = 'http://www.hzxh.gov.cn' + j[0]
                db_dict['title'] = j[1]
                db_dict['gmt_updated'] = j[2]
                db_dict['project_name'] = "浙江省科技型中小企业"
                db_dict['source'] = '科技局'
                db_dict['area'] = '西湖区'

                sum.append(db_dict)
            elif '雏鹰计划' in j[1]:
                pattern = re.compile(r'关于西湖区.*?雏鹰计划')
                res = pattern.findall(j[1])
                if len(res) != 0:
                    if j[0].endswith('pdf') or 'http' in j[0]:
                        db_dict['url'] = j[0]
                    else:
                        db_dict['url'] = 'http://www.hzxh.gov.cn' + j[0]
                    db_dict['title'] = j[1]
                    db_dict['gmt_updated'] = j[2]
                    db_dict['project_name'] = "雏鹰计划"
                    db_dict['source'] = '科技局'
                    db_dict['area'] = '西湖区'

                    sum.append(db_dict)
            elif '高新技术企业' in j[1]:
                pattern = re.compile(r'国家.*高新技术企业')
                res = pattern.findall(j[1])
                if len(res) != 0:
                    if j[0].endswith('pdf') or 'http' in j[0]:
                        db_dict['url'] = j[0]
                    else:
                        db_dict['url'] = 'http://www.hzxh.gov.cn' + j[0]
                    db_dict['title'] = j[1]
                    db_dict['gmt_updated'] = j[2]
                    db_dict['project_name'] = "国家高新技术企业"
                    db_dict['source'] = '科技局'
                    db_dict['area'] = '西湖区'

                    sum.append(db_dict)

        num += 60
        single += 1
        time.sleep(1.5)


def get_finger_db():
    sql = 'select * from spider_all_data'
    cursor.execute(sql)
    data = cursor.fetchall()
    print(data)
    finger_data = [i[8] for i in data]
    return finger_data

def update():
    new_sum = []
    for i in sum:
        finger = hashlib.md5(i['url'].encode(encoding='utf-8')).hexdigest()
        i['finger'] = finger
        new_sum.append(i)
    db_finger = get_finger_db()
    data = [i for i in new_sum if i['finger'] not in db_finger]

    print(data)
    exit()
    write_db(data)
if __name__ == '__main__':
    proxys = []
    dl()
    sum = []
    zjs()
    hzs()
    scq()
    xcq()
    gsq()
    jgq()
    bjq()
    xsq()
    xhq()

    update()
