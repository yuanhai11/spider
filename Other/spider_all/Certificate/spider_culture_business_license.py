# coding:utf-8
import re
import os
import json
import math
import time
import requests
import pymysql
from lxml import etree
import re
import os
import json
import math
import time
import requests
import pymysql
import json
from lxml import etree
from sqlalchemy import Column, String, create_engine, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from getCompanyId.get_company_id import get_company_id

# 创建对象的基类:
Base = declarative_base()


# 定义User对象:

class Medicine(Base):
    # 表的名字:
    __tablename__ = 'spider_culture_business_license'

    # 表的结构:
    id = Column(Integer(), primary_key=True, autoincrement=True)
    file_url = Column(String(256))
    file_name = Column(String(256))
    company_name = Column(String(256))
    matter_name = Column(String(256))
    approval_date = Column(String(256))
    release_date = Column(String(256))
    business_water_number = Column(String(256))
    project_name = Column(String(256))
    business_type = Column(String(256))
    accept_manager_people = Column(String(256))
    current_type = Column(String(256))
    data_source = Column(String(256))
    administrative_license_matter = Column(String(256))
    province = Column(String(256))
    area = Column(String(256))
    business_position = Column(String(256))
    business_license_number = Column(String(256))
    company_id = Column(String(256))

    gmt_created = Column(String(256))
    gmt_updated = Column(String(256))


# 初始化数据库连接:
engine = create_engine('mysql+pymysql://root:BOOT-xwork1024@192.168.2.99:3306/spider')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
# 创建session对象:
session = DBSession()
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
}

'''
更新：直接获取前三页数据     
注意：个别公司信息显示 page not found
'''
proxys = []


def dl():
    dlurl = 'http://api.goubanjia.com/dynamic/get/d490a5d4debefc8980ae6ee4c4148552.html?sep=3'

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
    bloom = get_updated()
    last_page_complete = False
    num = 0
    page = 1
    data = {
        "startrecord": 1,
        "endrecord": 120,
        "perpage": 40,
        "col": 1,
        "appid": 1,
        "webid": 3214,
        "path": "/",
        "columnid": 1653000,
        "sourceContentType": 1,
        "unitid": 5019490,
        "webname": "浙江省文化和旅游厅",
        "permissiontype": 0
    }
    url = "http://ct.zj.gov.cn/module/jpage/dataproxy.jsp?"
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
    print('数据共{}页！！！'.format(number))
    sum = []

    for i in range(number):
        startrecord = num + 1
        endrecord = 120 * page
        if endrecord > flag:
            endrecord = flag
            last_page_complete = True
        data = {
            "startrecord": startrecord,
            "endrecord": endrecord,
            "perpage": 40,
            "col": 1,
            "appid": 1,
            "webid": 3214,
            "path": "/",
            "columnid": 1653000,
            "sourceContentType": 1,
            "unitid": 5019490,
            "webname": "浙江省文化和旅游厅",
            "permissiontype": 0
        }
        url = "http://ct.zj.gov.cn/module/jpage/dataproxy.jsp?"
        response = ""
        for IP in range(10):
            try:
                response = requests.post(url=url, headers=headers, data=data, proxies=proxys[-1], timeout=10)
                print(response)
                if response.status_code == 200:
                    response = response.content.decode('utf8')
                    print('break')
                    break
            except Exception:
                dl()
        pattern = re.compile('<a href="(.*?)".*?>(.*?)</a><span .*?>(.*?)</span>', re.S)
        data = pattern.findall(response)
        if not last_page_complete:
            data = data[:-1]

        for i in data:
            single = {}
            file_url = 'http://ct.zj.gov.cn' + i[0]
            file_name = i[1]

            single['file_name'] = file_name
            single['file_url'] = file_url

            if file_url not in bloom:
                sum.append(single)

        num += 120
        page += 1
        time.sleep(1.5)
        break  # 用来更新数据 获取一页就满足条件了

    if len(sum) == 0:
        print('本次无更新数据！！！')
    else:
        print('本地数据更新了{}条！！！'.format(len(data)))
        parse(sum)


def parse(sum):
    all_data = []
    for i in sum:
        file_url = i['file_url']
        file_name = i['file_name']
        response = ""
        for IP in range(10):
            try:
                response = requests.get(url=file_url, headers=headers, proxies=proxys[-1], timeout=10)
                if response.status_code == 200:
                    response = response.content.decode('utf-8')
                    print('break')
                    break
            except Exception:
                dl()
        try:
            key1 = re.findall(r'申请单位/申请人：</span>(.*?)<br/>', response, re.S)
            key2 = re.findall(r'申请单位/申请人：(.*?)<br/>', response, re.S)
            key3 = re.findall(r'申请单位/申请人：</span>&nbsp;(.*?)</p>', response, re.S)

        except Exception as e:
            print('数据获取失败！！！可能出现404！！！跳过！')
            continue

        if len(key1) != 0 or len(key2) != 0:
            release_date = re.findall(r'发布日期：(.*?)</span>', response, re.S)[0]

            business_water_number = re.findall(r'业务流水号：</span>(.*?)<br/>', response, re.S)
            if len(business_water_number) != 0:
                business_water_number = business_water_number[0]
            else:
                lis = re.findall(r'业务流水号：(.*?)<br/>', response, re.S)
                business_water_number = lis[0]

            company_name = re.findall(r'申请单位/申请人：</span>(.*?)<br/>', response, re.S)
            if len(company_name) != 0:
                company_name = company_name[0]
            else:
                lis = re.findall(r'申请单位/申请人：(.*?)<br/>', response, re.S)
                company_name = lis[0]

            matter_name = re.findall(r'事项名称：</span>(.*?)<br/>', response, re.S)
            if len(matter_name) != 0:
                matter_name = matter_name[0]
            else:
                lis = re.findall(r'事项名称：(.*?)<br/>', response, re.S)
                matter_name = lis[0]

            project_name = re.findall(r'项目名称：</span>(.*?)<br/>', response, re.S)
            if len(project_name) != 0:
                project_name = project_name[0]
            else:
                lis = re.findall(r'项目名称：(.*?)<br/>', response, re.S)
                project_name = lis[0]

            business_type = re.findall(r'业务类型：</span>(.*?)<br/>', response, re.S)
            if len(business_type) != 0:
                business_type = business_type[0]
            else:
                lis = re.findall(r'业务类型：(.*?)<br/>', response, re.S)
                business_type = lis[0]

            accept_manager_people1 = re.findall(r'受理经办人：</span>(.*?)<br/>', response, re.S)
            accept_manager_people2 = re.findall(r'受理经办人：(.*?)<br/>', response, re.S)
            if len(accept_manager_people1) != 0:
                accept_manager_people = accept_manager_people1[0]
            elif len(accept_manager_people2) != 0:
                accept_manager_people = accept_manager_people2[0]
            else:
                accept_manager_people = 'null'

            current_type = re.findall(r'当前状态：</span>.*?<span .*?">(.*?)</span>', response, re.S)
            if len(current_type) != 0:
                current_type = current_type[0]
            else:
                lis = re.findall(r'当前状态：.*?<span .*?">(.*?)</span>', response, re.S)
                current_type = lis[0]

            approval_date = re.findall(r'<span style="font-size: 18px;">(.*?)</span>', response, re.S)
            if len(approval_date) != 0:
                approval_date = approval_date[-1]
            else:
                approval_date = re.findall(r'<span style=\\"font-size: 18px;\\">(.*?)</span>', response, re.S)[-1]

            data_source = '浙江省文化和旅游厅'

            file_url = file_url.strip()
            file_name = file_name.strip()
            company_name = company_name.strip()
            matter_name = matter_name.strip()
            approval_date = approval_date.strip()
            release_date = release_date.strip()
            business_water_number = business_water_number.strip()
            project_name = project_name.strip()
            business_type = business_type.strip()
            accept_manager_people = accept_manager_people.strip()
            current_type = current_type.strip()
            data_source = data_source.strip()

            administrative_license_matter = 'null'
            province = 'null'
            area = 'null'
            business_position = 'null'
            business_license_number = 'null'
            times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            company_id = get_company_id(company_name)
            if company_id:
                print((file_url, file_name, company_name, matter_name, approval_date, release_date,
                       business_water_number, project_name,
                       business_type, accept_manager_people, current_type, data_source, administrative_license_matter,
                       province, area, business_position,
                       business_license_number, company_id))
                zhilian = Medicine(file_url=file_url, company_name=company_name, matter_name=matter_name,
                                   approval_date=approval_date, release_date=release_date,
                                   business_water_number=business_water_number, project_name=project_name,
                                   business_type=business_type,
                                   accept_manager_people=accept_manager_people, current_type=current_type,
                                   data_source=data_source,
                                   administrative_license_matter=administrative_license_matter,
                                   province=province, area=area, business_position=business_position,
                                   business_license_number=business_license_number,
                                   gmt_created=times, gmt_updated=times, company_id=company_id)
                all_data.append(zhilian)
            else:
                print((file_url, file_name, company_name, matter_name, approval_date, release_date,
                       business_water_number, project_name,
                       business_type, accept_manager_people, current_type, data_source, administrative_license_matter,
                       province, area, business_position,
                       business_license_number))
                zhilian = Medicine(file_url=file_url, company_name=company_name, matter_name=matter_name,
                                   approval_date=approval_date, release_date=release_date,
                                   business_water_number=business_water_number, project_name=project_name,
                                   business_type=business_type,
                                   accept_manager_people=accept_manager_people, current_type=current_type,
                                   data_source=data_source,
                                   administrative_license_matter=administrative_license_matter,
                                   province=province, area=area, business_position=business_position,
                                   business_license_number=business_license_number,
                                   gmt_created=times, gmt_updated=times)
                all_data.append(zhilian)

        elif len(key3) != 0:
            release_date = re.findall(r'发布日期：(.*?)</span>', response, re.S)[0]

            business_water_number = re.findall(r'业务流水号：</span>(.*?)</span>', response, re.S)
            if len(business_water_number) != 0:
                business_water_number = business_water_number[0]
            else:
                lis = re.findall(r'业务流水号：(.*?)<br/>', response, re.S)
                business_water_number = lis[0]

            company_name = re.findall(r'申请单位/申请人：</span>(.*?)</p>', response, re.S)
            if len(company_name) != 0:
                company_name = company_name[0]
            else:
                lis = re.findall(r'申请单位/申请人：(.*?)<br/>', response, re.S)
                company_name = lis[0]

            matter_name = re.findall(r'事项名称：</span>(.*?)</p>', response, re.S)
            if len(matter_name) != 0:
                matter_name = matter_name[0]
            else:
                lis = re.findall(r'事项名称：(.*?)<br/>', response, re.S)
                matter_name = lis[0]

            project_name = re.findall(r'项目名称：</span>(.*?)</p>', response, re.S)
            if len(project_name) != 0:
                project_name = project_name[0]
            else:
                lis = re.findall(r'项目名称：(.*?)<br/>', response, re.S)
                project_name = lis[0]

            business_type = re.findall(r'业务类型：</span>(.*?)</p>', response, re.S)
            if len(business_type) != 0:
                business_type = business_type[0]
            else:
                lis = re.findall(r'业务类型：(.*?)<br/>', response, re.S)
                business_type = lis[0]

            accept_manager_people1 = re.findall(r'受理经办人：</span>(.*?)</p>', response, re.S)
            accept_manager_people2 = re.findall(r'受理经办人：(.*?)</p>', response, re.S)
            if len(accept_manager_people1) != 0:
                accept_manager_people = accept_manager_people1[0]
            elif len(accept_manager_people2) != 0:
                accept_manager_people = accept_manager_people2[0]
            else:
                accept_manager_people = 'null'

            current_type = re.findall(r'当前状态：</span>.*?<span .*?">(.*?)</span>', response, re.S)
            if len(current_type) != 0:
                current_type = current_type[0]
            else:
                lis = re.findall(r'当前状态：.*?<span .*?">(.*?)</span>', response, re.S)
                current_type = lis[0]

            approval_date = re.findall(r'浙江省文化厅</p><p .*?">(.*?)</p>', response, re.S)
            if len(approval_date) != 0:
                approval_date = approval_date[0]
            else:
                approval_date = re.findall(r'<span style=\\"font-size: 18px;\\">(.*?)</span>', response, re.S)[-1]

            data_source = '浙江省文化和旅游厅'

            file_url = file_url.strip()
            file_name = file_name.strip()
            company_name = company_name.strip().replace('&nbsp;', '')
            matter_name = matter_name.strip().replace('&nbsp;', '')
            approval_date = approval_date.strip()
            release_date = release_date.strip()
            business_water_number = business_water_number.strip().replace('&nbsp;', '')
            project_name = project_name.strip()
            business_type = business_type.strip()
            accept_manager_people = accept_manager_people.strip()
            current_type = current_type.strip()
            data_source = data_source.strip()

            administrative_license_matter = 'null'
            province = 'null'
            area = 'null'
            business_position = 'null'
            business_license_number = 'null'

            times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            company_id = get_company_id(company_name)
            if company_id:
                print((file_url, file_name, company_name, matter_name, approval_date, release_date,
                       business_water_number, project_name,
                       business_type, accept_manager_people, current_type, data_source, administrative_license_matter,
                       province, area, business_position,
                       business_license_number, company_id))
                zhilian = Medicine(file_url=file_url, company_name=company_name, matter_name=matter_name,
                                   approval_date=approval_date, release_date=release_date,
                                   business_water_number=business_water_number, project_name=project_name,
                                   business_type=business_type,
                                   accept_manager_people=accept_manager_people, current_type=current_type,
                                   data_source=data_source,
                                   administrative_license_matter=administrative_license_matter,
                                   province=province, area=area, business_position=business_position,
                                   business_license_number=business_license_number,
                                   gmt_created=times, gmt_updated=times, company_id=company_id)
                all_data.append(zhilian)
            else:
                print((file_url, file_name, company_name, matter_name, approval_date, release_date,
                       business_water_number, project_name,
                       business_type, accept_manager_people, current_type, data_source, administrative_license_matter,
                       province, area, business_position,
                       business_license_number))
                zhilian = Medicine(file_url=file_url, company_name=company_name, matter_name=matter_name,
                                   approval_date=approval_date, release_date=release_date,
                                   business_water_number=business_water_number, project_name=project_name,
                                   business_type=business_type,
                                   accept_manager_people=accept_manager_people, current_type=current_type,
                                   data_source=data_source,
                                   administrative_license_matter=administrative_license_matter,
                                   province=province, area=area, business_position=business_position,
                                   business_license_number=business_license_number,
                                   gmt_created=times, gmt_updated=times)
                all_data.append(zhilian)

        else:
            release_date = re.findall(r'发布日期：(.*?)</span>', response, re.S)[0]
            administrative_license_matter = re.findall(r'行政许可事项：(.*?)<br/>', response, re.S)
            if len(administrative_license_matter) != 0:
                administrative_license_matter = administrative_license_matter[0]
            else:
                lis = re.findall(r'行政许可事项：(.*?)<br />', response, re.S)
                administrative_license_matter = lis[0]

            company_name = re.findall(r'单位名称：(.*?)<br/>', response, re.S)
            if len(company_name) != 0:
                company_name = company_name[0]
            else:
                lis = re.findall(r'单位名称：(.*?)<br />', response, re.S)
                company_name = lis[0]
            province = re.findall(r'省份：(.*?)<br/>', response, re.S)
            if len(province) != 0:
                province = province[0]
            else:
                lis = re.findall(r'省份：(.*?)<br />', response, re.S)
                province = lis[0]
            area = re.findall(r'地市：(.*?)<br/>', response, re.S)
            if len(area) != 0:
                area = area[0]
            else:
                lis = re.findall(r'地市：(.*?)<br />', response, re.S)
                area = lis[0]
            business_position = re.findall(r'营业场所：(.*?)<br/>', response, re.S)
            if len(business_position) != 0:
                business_position = business_position[0]
            else:
                lis = re.findall(r'营业场所：(.*?)<br />', response, re.S)
                business_position = lis[0]
            business_license_number = re.findall(r'营业许可证号：(.*?)<br/>', response, re.S)
            if len(business_license_number) != 0:
                business_license_number = business_license_number[0]
            else:
                lis = re.findall(r'营业许可证号：(.*?)<br />', response, re.S)
                business_license_number = lis[0]
            current_type = re.findall(r'当前状态：<span .*?">(.*?)</span>', response, re.S)[0]
            approval_date = re.findall(r'<span style="font-size: 18px;">(.*?)</span>', response, re.S)
            if len(approval_date) != 0:
                approval_date = approval_date[-1]
            else:
                approval_date = re.findall(r'<span style=\\"font-size: 18px;\\">(.*?)</span>', response, re.S)[-1]
            data_source = '浙江省文化和旅游厅'

            file_url = file_url.strip()
            file_name = file_name.strip()
            company_name = company_name.strip()
            matter_name = 'null'
            approval_date = approval_date.strip()
            release_date = release_date.strip()
            business_water_number = 'null'
            project_name = 'null'
            business_type = 'null'
            accept_manager_people = 'null'
            current_type = current_type.strip()
            data_source = data_source.strip()

            administrative_license_matter = administrative_license_matter.strip()
            province = province.strip()
            area = area.strip()
            business_position = business_position.strip()
            business_license_number = business_license_number.strip()
            times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            company_id = get_company_id(company_name)
            if company_id:
                print(
                    (file_url, file_name, company_name, matter_name, approval_date, release_date, business_water_number,
                     project_name,
                     business_type, accept_manager_people, current_type, data_source, administrative_license_matter,
                     province,
                     area, business_position,
                     business_license_number, company_id))
                zhilian = Medicine(file_url=file_url, company_name=company_name, matter_name=matter_name,
                                   approval_date=approval_date, release_date=release_date,
                                   business_water_number=business_water_number, project_name=project_name,
                                   business_type=business_type,
                                   accept_manager_people=accept_manager_people, current_type=current_type,
                                   data_source=data_source,
                                   administrative_license_matter=administrative_license_matter,
                                   province=province, area=area, business_position=business_position,
                                   business_license_number=business_license_number,
                                   gmt_created=times, gmt_updated=times, company_id=company_id)
                all_data.append(zhilian)
            else:
                print(
                    (file_url, file_name, company_name, matter_name, approval_date, release_date, business_water_number,
                     project_name,
                     business_type, accept_manager_people, current_type, data_source, administrative_license_matter,
                     province,
                     area, business_position,
                     business_license_number))
                zhilian = Medicine(file_url=file_url, company_name=company_name, matter_name=matter_name,
                                   approval_date=approval_date, release_date=release_date,
                                   business_water_number=business_water_number, project_name=project_name,
                                   business_type=business_type,
                                   accept_manager_people=accept_manager_people, current_type=current_type,
                                   data_source=data_source,
                                   administrative_license_matter=administrative_license_matter,
                                   province=province, area=area, business_position=business_position,
                                   business_license_number=business_license_number,
                                   gmt_created=times, gmt_updated=times)
                all_data.append(zhilian)
        time.sleep(0.8)

    write_db(all_data)


def get_updated():
    db = pymysql.connect(host="192.168.2.99", user="root", password='BOOT-xwork1024', database="spider", port=3306)
    cursor = db.cursor()
    sql = "select file_url from spider_culture_business_license"
    cursor.execute(sql)
    db_data = cursor.fetchall()
    # print(db_data)
    # exit()
    data = [i[0] for i in db_data]
    from pybloom_live import ScalableBloomFilter
    bloom = ScalableBloomFilter(initial_capacity=10000, error_rate=0.001)
    for bl in data:
        bloom.add(bl)
    return bloom


def write_db(sum):
    for i in sum:
        session.add(i)
    session.commit()
    session.close()


if __name__ == '__main__':
    main()
