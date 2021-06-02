#coding:utf-8
import json
import os
import pathlib
import re
import time
import requests
import pymysql
from lxml import etree
from sqlalchemy import Column, String, create_engine,Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,ForeignKey,String
from sqlalchemy.orm import relationship


# db_connect_string='mysql://liu:liu@'+IP+':3306/bishe?charset=utf8'
# engine = create_engine(db_connect_string)
# Base = declarative_base(engine)

# 初始化数据库连接:
engine = create_engine('mysql+pymysql://root:BOOT-xwork1024@192.168.2.96:3306/spider_leilei?charset=utf8')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
# 创建session对象:
session = DBSession()
# 创建对象的基类:
Base = declarative_base(engine)
# 定义User对象:
class Medicine(Base):
    # 表的名字:
    __tablename__ = 'spider_social_insurance'

    # 表的结构:
    id = Column(Integer(), primary_key=True,autoincrement=True)
    city_name = Column(String(256))
    # social_insurance_minimum_base = Column(String(256))
    # pension_personal = Column(String(256))
    # medical_personal = Column(String(256))
    # unemployment_personal = Column(String(256))
    # pension_company = Column(String(256))
    # medical_company = Column(String(256))
    # unemployment_company = Column(String(256))
    # injury_job_company = Column(String(256))
    # accumulation_fund_minimum_base = Column(String(256))
    # accumulation_fund_personal = Column(String(256))
    # accumulation_fund_company = Column(String(256))
    # gmt_created = Column(String(256))
    # gmt_updated = Column(String(256))

Base.metadata.create_all()
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
}
# proxys = []

# def dl():
#     dlurl = 'http://api.goubanjia.com/dynamic/get/d490a5d4debefc8980ae6ee4c4148552.html?sep=3'
#     resp = requests.get(dlurl).text
#     time.sleep(2)
#     resp = re.sub(r'\n', '', resp)
#     proxy = {
#         'https': resp
#     }
#     proxys.append(proxy)
#     print(proxys[-1])
# dl()
import chardet
def main():
    # bloom = get_updated()
    sum = []
    for i in range(1,2):
        url = "http://www.ch12333.com/Public/js/area.js"
        response = requests.request(method='get', url=url, headers=headers,timeout=10,verify=False)
        text = response.content
        new_content = text.decode('utf-8')
        new_content = new_content.strip('var ChineseDistricts = ')[:-1]
        new_content = new_content.replace(' ','')
        new_content=new_content.replace("""\r\n//710000:'台湾省',\r\n//810000:'香港特别行政区',\r\n//820000:'澳门特别行政区'""","")
        new_content = new_content.replace('\r\n','\r\n"')
        new_content = new_content.replace('"}','}')
        new_content = new_content.replace(',\r\n}','\r\n}')
        new_content = new_content.replace(':','":')
        new_content = new_content.replace("'",'"')
        new_content = json.loads(new_content)

        obtained = {}
        no_obtain = {}
        provinces = new_content['86']
        # 遍历所有省份
        for province_id in provinces:
            # if province_id == '110000' or province_id =='120000'or province_id =='130000':
            #     continue
            citys = new_content[province_id]
            obtained[province_id] ={}
            no_obtain[province_id] ={}
            # 遍历本省份下的所有城市
            for city_id in citys:
                url = "http://www.ch12333.com/index.php/Home/index/shebao.html"
                data ={
                    "news_province": province_id,
                    "news_city": city_id,
                    'provincecn':provinces[province_id],
                    "citycn":citys[city_id],
                    "sousuo" : 1
                }
                response = requests.request(method='post', url=url,data=data, headers=headers,timeout=10,verify=False)
                content = response.content
                content = content.decode('utf-8')
                tree = etree.HTML(content)

                city_urls = tree.xpath('//span[@class="bold_title_topic"]/a/@href')
                #当获取城市社保文档后，没有文档，添加到无获取列表，跳出此次循环
                if city_urls == []:
                    no_obtain[province_id][city_id] = citys[city_id]
                    continue

                # 遍历本城市下的所有文档，防止有的文档没有图片
                for city_url in city_urls:
                    # 当图片已经获取后跳出循环
                    if city_id in obtained[province_id]:
                        break
                    page_security(city_url,provinces,province_id,citys,city_id,no_obtain,obtained)

            # 查询遗漏城市数据

            # 获取本省第一页数据，为获取本省一共有几页数据
            url = 'http://www.ch12333.com/shebao/m/Home/news_province/'+province_id+'/news_city/0/citycn/请选择市/sousuo/1/page/1.html'
            response = requests.request(method='get', url=url, headers=headers,timeout=10,verify=False)
            content = response.content
            content = content.decode('utf-8')
            tree = etree.HTML(content)
            page = tree.xpath('//div/ul/li/span/text()')[-1]
            page = re.findall("/(.*?)页", page)[0].replace(' ','')
            for i in range (1,int(page)+1):
                url = 'http://www.ch12333.com/shebao/m/Home/news_province/'+province_id+'/news_city/0/citycn/请选择市/sousuo/1/page/'+str(i)+'.html'
                response = requests.request(method='get', url=url, headers=headers,timeout=10,verify=False)
                content = response.content
                content = content.decode('utf-8')
                tree = etree.HTML(content)
                city_urls = tree.xpath('//span[@class="bold_title_topic"]/a/@href')
                city_titles = tree.xpath('//span[@class="bold_title_topic"]/a/text()')
                for city_url,city_title in zip(city_urls,city_titles):
                    no_city = no_obtain[province_id].copy()
                    for city_id in no_city:
                        city_name = no_city[city_id].split('市')[0]
                        if city_name in city_title:
                            page_security(city_url,provinces,province_id,citys,city_id,no_obtain,obtained,sum)

                            print()

                            if len(sum) == 0:
                                print('本次无更新数据！！！')
                            else:
                                print('本地数据更新了{}条！！！'.format(len(sum)))
                                write_db(sum)



# 获取直接显示社保页面
def page_security(city_url,provinces,province_id,citys,city_id,no_obtain,obtained,sum):
    url = "http://www.ch12333.com" + city_url
    response = requests.request(method='get', url=url, headers=headers, timeout=10, verify=False)
    content = response.content
    tree = etree.HTML(content)
    try:
        img_url = tree.xpath('//div[@class="article_content_text"]/p/img/@src')[0]
    except:
        print(citys[city_id] + '没有图片！')
        no_obtain[province_id][city_id] = citys[city_id]
        return
    url = img_url
    response = requests.request(method='get', url=url, headers=headers, timeout=10, verify=False)
    # 存储为图片形式，后期需要改为上传图片，存储到数据库
    process_img(provinces,province_id,citys,city_id,response,sum)

    # 查询一个城市时，访问前面文件没有图片，后面文件有图片后删除对应键值对
    if city_id in no_obtain[province_id]:
        del no_obtain[province_id][city_id]
    obtained[province_id][city_id] = citys[city_id]
    time.sleep(1)

#对获取的数据进行处理
def process_img(provinces,province_id,citys,city_id,response,sum):
    # 存储为图片形式，后期需要改为上传图片，存储到数据库
    folder_path = os.getcwd() + '\\img\\' + provinces[province_id]
    if not os.path.exists(folder_path):  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(folder_path)
    print(os.getcwd() + '\\img\\' + provinces[province_id] + '\\' + citys[city_id] + '.png')
    with open(os.getcwd() + '\\img\\' + provinces[province_id] + '\\' + citys[city_id] + '.png', 'wb+') as f:
        f.write(response.content)

    city_name = '北京市'
    # social_insurance_minimum_base = ''
    # pension_personal = ''
    # medical_personal = ''
    # unemployment_personal = ''
    # pension_company = ''
    # medical_company = ''
    # unemployment_company = ''
    # injury_job_company = ''
    # accumulation_fund_minimum_base = ''
    # accumulation_fund_personal = ''
    # accumulation_fund_company = ''

    times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    social_insurance = Medicine(city_name=city_name,)
                                # social_insurance_minimum_base=social_insurance_minimum_base,
                                # pension_personal=pension_personal,medical_personal = medical_personal,unemployment_personal=unemployment_personal,
                                # pension_company=pension_company,medical_company=medical_company,unemployment_company = unemployment_company,
                                # injury_job_company=injury_job_company,accumulation_fund_minimum_base=accumulation_fund_minimum_base,
                                # accumulation_fund_personal=accumulation_fund_personal,accumulation_fund_company=accumulation_fund_company,
                                # gmt_created=times, gmt_updated=times)
    sum.append(social_insurance)


def write_db(sum):
    for i in sum:
        session.add(i)
    session.commit()
    session.close()

if __name__ == '__main__':
    main()

