import requests
import json
import re
import time
import pymysql
from lxml import etree
'''
将镶嵌在网站的数据和带附件的数据分离开
'''
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
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36',
}
db = pymysql.connect(host="localhost", user="root", password='123456', database="spider_gaoxinqiye", port=3306)
cursor = db.cursor()
sql = 'SELECT * FROM spider_filted_data'
cursor.execute(sql)
data = cursor.fetchall()
num = 1
a = []
b = []
c = []
d = []
e = []
f = []
g = []

n = 1
#  3-7 ; 12 13 15 16 18 21 22 23 24 25 28 29 30 31-34 38 39 41 43 51 52 ;53(数据不存在) （28页数据镶嵌在网页里）
new_list = []
lists = [3,4,5,6,7,12,13,15,16,18,21,22,23,24,25,28,29,30,31,32,33,34,38,39,41,43,51]
for i in data:
    # print((n,i[1],i[2]))
    if n not in lists:
        new_list.append((i[2],i[1]))
    n+=1

for j in new_list:
    print(j)
#
# for i in a:
#
#     url = i[1]
#     title = i[2]
#     response = ''
#     for IP in range(10):
#         try:
#             response = requests.request(method='get', url=url, headers=headers, proxies=proxys[-1],timeout=10)
#             if response.status_code == 200:
#                 response = response.content.decode('utf8')
#                 break
#         except Exception:
#             dl()
#     print(response)
#     print(title)
#
#     element = etree.HTML(response)
#     u = element.xpath('//div[@class="article-conter"]/p[5]/a/@href')
#     print(u[0])
#     detail_url = 'http://kjt.zj.gov.cn'+u[0]
#     print(detail_url)
#     response = requests.get(detail_url).content
#     name = detail_url.split('.')[-1]
#
#     with open('./files/{}.{}'.format(title,name),'wb')as fp:
#         fp.write(response)
#     exit()