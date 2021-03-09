import requests
import os
import pymysql
from lxml import etree
# 周五：把自己爬下的网站数据入库
    # 省科技、
    # 包括市科技中小企业
    # 省科技型中小、 包括（省高科技型中小）
    # 雏鹰
'''
解析 网页中数据 类型1
'''
url = "http://www.hhtz.gov.cn/art/2017/3/13/art_1485818_20324421.html"
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36',
}
# def main():
#     response = requests.request(method='get',headers=headers,url=url).content.decode('utf-8')
#     element = etree.HTML(response)
#     ele = element.xpath('//div[@class="article-conter"]//tbody/tr[position()>1]')
#     print(len(ele))
#     # exit()
#     sum = []
#     flag = True
#     xixi = ""
#     for i in ele:
#         single = {}
#
#         company_name = "".join(i.xpath('./td[3]/p//text()'))
#         area = i.xpath('./td[2]/p//text()')
#         if len(area)==0:
#             xixi = '浙江'
#             flag = False
#             continue
#         if flag:
#             if area[0] not in "\xa0":
#                 xixi = "".join(area).split('（')[0]
#             else:
#                 area = xixi
#
#         area = xixi
#         # print(company_name)
#         # print(area)
#         # exit()
#         # area = '高新区（滨江）'
#
#         honor_year = '2007'
#         type = '省科技型'
#         batch = '第一批'
#         single['company_name'] = company_name
#         single['company_place'] = area
#         single['get_honor_year'] = honor_year
#         single['type_of_honor'] = type
#         single['batch'] = batch
#
#         print(single)
#         sum.append(single)
#     # exit()
#     insert_db(sum)

def main():
    sum = []
    response = requests.request(method='get', headers=headers, url=url).content.decode('utf-8')
    element = etree.HTML(response)
    ele = element.xpath('//tbody/tr[position()>1]')
    print(len(ele))
    # exit()
    for i in ele:
        single = {}
        company_name = i.xpath('./td[2]/p/text()')[0]
        # area = i.xpath('./td[3]/div/text()')[0]

        honor_year = '2016'
        type = '国高'
        batch = ''
        single['company_name'] = company_name
        single['company_place'] = '高新区'
        single['get_honor_year'] = honor_year
        single['type_of_honor'] = type
        single['batch'] = batch
        sum.append(single)
        print(single)
    # exit()
    insert_db(sum)

def insert_db(sum):
    db = pymysql.connect(host="localhost", user="root", password='123456', database="spider_gaoxinqiye", port=3306)
    cursor = db.cursor()
    for i in sum:
        company_name = i.get('company_name')
        company_place = i.get('company_place')
        get_honor_year = i.get('get_honor_year')
        type_of_honor = i.get('type_of_honor')
        batch = i.get('batch')

        sql = """insert into company_honor (id,company_name,company_place,get_honor_year,types_of_honor,batch)
                values(NULL,'{}','{}','{}','{}','{}')""".format(company_name,company_place,get_honor_year,type_of_honor,batch)
        cursor.execute(sql)
        db.commit()
    db.close()

if __name__ == '__main__':
    main()