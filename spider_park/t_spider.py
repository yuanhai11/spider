import requests,json,re,time
import pymysql
from lxml import etree
'''
数据维度：
    园区ID、园区名称、省份、城市、面积、创建时间、更新时间
问题：
    - 具备身份信息才有详情页url
    - 动态IP可能出现请求成功，但是没有数据的情况，对IP进行处理。
结果：
    - 将新鲜数据更新入库
'''
'''
结果：完成数据更新机制！！！
研究：1、布隆过滤器进行去重；2、考虑到布隆过滤器转换为本地文件；3、考虑更新机制
'''
import math
import requests,json,re,time
from lxml import etree
import pymysql
import decouple
db = pymysql.connect(host='192.168.2.222', user='root', password='123456', database='test', port=3306)
cursor = db.cursor()
dlurl = 'http://dynamic.goubanjia.com/dynamic/get/d490a5d4debefc8980ae6ee4c4148552.html?sep=3'
proxys = []

headers = {
    'cookie':'TYCID=94475540afac11ea98e4d9a990e2b084; undefined=94475540afac11ea98e4d9a990e2b084; ssuid=6200252146; _ga=GA1.2.888189839.1592296638; bad_idb3ebcec0-09a9-11ea-b7e1-aff0bff10886=86d4afb1-afad-11ea-909e-35fcf798de25; tyc-user-phone=%255B%252218837076355%2522%255D; jsid=SEM-BAIDU-PZ0703-VIP-000001; bannerFlag=false; tyc-user-info=%257B%2522claimEditPoint%2522%253A%25220%2522%252C%2522vipToMonth%2522%253A%2522false%2522%252C%2522explainPoint%2522%253A%25220%2522%252C%2522personalClaimType%2522%253A%2522none%2522%252C%2522integrity%2522%253A%252210%2525%2522%252C%2522state%2522%253A0%252C%2522announcementPoint%2522%253A%25220%2522%252C%2522bidSubscribe%2522%253A%2522-1%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522onum%2522%253A%25220%2522%252C%2522monitorUnreadCount%2522%253A%25220%2522%252C%2522discussCommendCount%2522%253A%25220%2522%252C%2522showPost%2522%253Anull%252C%2522claimPoint%2522%253A%25220%2522%252C%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODgzNzA3NjM1NSIsImlhdCI6MTU5MzY1MDgxNywiZXhwIjoxNjA5MjAyODE3fQ.N7ZafL02yvCgmRsD8HEe-ZOobj49OgKoUHWXO3mFPirHMLe4uA6Zfg7Nl1wgjClDN41xobzxeCz6PhpyuXIjcg%2522%252C%2522schoolAuthStatus%2522%253A%25222%2522%252C%2522redPoint%2522%253A%25220%2522%252C%2522myTidings%2522%253A%25220%2522%252C%2522companyAuthStatus%2522%253A%25222%2522%252C%2522myAnswerCount%2522%253A%25220%2522%252C%2522myQuestionCount%2522%253A%25220%2522%252C%2522signUp%2522%253A%25220%2522%252C%2522privateMessagePointWeb%2522%253A%25220%2522%252C%2522nickname%2522%253A%2522%25E5%25B8%258C%25E6%258B%2589%25E7%2591%259E%25C2%25B7%25E8%25BE%25BE%25E8%258A%2599%2522%252C%2522privateMessagePoint%2522%253A%25220%2522%252C%2522bossStatus%2522%253A%25222%2522%252C%2522isClaim%2522%253A%25220%2522%252C%2522yellowDiamondEndTime%2522%253A%25220%2522%252C%2522yellowDiamondStatus%2522%253A%2522-1%2522%252C%2522pleaseAnswerCount%2522%253A%25220%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522bizCardUnread%2522%253A%25220%2522%252C%2522mobile%2522%253A%252218837076355%2522%257D; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODgzNzA3NjM1NSIsImlhdCI6MTU5MzY1MDgxNywiZXhwIjoxNjA5MjAyODE3fQ.N7ZafL02yvCgmRsD8HEe-ZOobj49OgKoUHWXO3mFPirHMLe4uA6Zfg7Nl1wgjClDN41xobzxeCz6PhpyuXIjcg; _gid=GA1.2.2073413964.1596700270; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1596700270; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1596700270; aliyungf_tc=AQAAAKoUE0GjmgMAI7u6PBRMAi1ZlB0S; csrfToken=t8yrH6lIqRt_VSp7XZJ3X2RZ; Hm_lvt_119671739c1e44de485415e23b342d18=1595300724,1596093581,1596108972,1596700286; Hm_lpvt_119671739c1e44de485415e23b342d18=1596702319',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
}
def dl():
    resp = requests.get(dlurl).text
    time.sleep(2)
    resp = re.sub(r'\n', '', resp)
    proxy = {
        'http': resp
    }
    proxys.append(proxy)
    print(proxys[-1])
def reload(page):
    time.sleep(1)
    dl()
    response = ""
    for g in range(10):
        try:
            response = requests.get(url='https://s.tianyancha.com/parks/p{}'.format(page),
                                    proxies=proxys[-1], headers=headers, timeout=10)
            time.sleep(1)
            print(response)
            if response.status_code == 200:
                response = response.content.decode('utf8')
                break
        except Exception:
            dl()
    print(response)
    # exit()
    tree = etree.HTML(response)
    element = tree.xpath('//div[@class="search-item"]')
    return element

def main():
    parks_response = ""
    for nn in range(20):
        try:
            parks_response = requests.get(url='https://s.tianyancha.com/parks', headers=headers,
                                    proxies=proxys[-1],timeout=12)
            if parks_response.status_code == 200:
                parks_response = parks_response.content.decode('utf8')
                print('break')
                break
        except Exception:
            dl()
    t = etree.HTML(parks_response)
    # 查询到所有园区数据
    all_num = int(t.xpath('//div[@class="num-title"]/span/text()')[0])
    num = 1
    parks_page = math.ceil(all_num/20)
    print(parks_page)
    sum = []
    for page in range(num,parks_page+1):
        response = ""
        for g in range(10):
            try:
                response = requests.get(url='https://s.tianyancha.com/parks/p{}'.format(page), proxies=proxys[-1],headers=headers,timeout=10)
                print(response)
                if response.status_code == 200:
                    response = response.content.decode('utf8')
                    print('break')
                    break
            except Exception:
                dl()

        tree = etree.HTML(response)
        element = tree.xpath('//div[@class="search-item"]')
        while True:
            if len(element)==0:
                element = reload(page)
                print('触发了reload函数！！！！')
            else:
                break
        for el in element:
            single = {}
            detail_url = el.xpath('.//div[@class="header clearfix"]/a/@href')[0].strip()
            yq_name = el.xpath('.//div[@class="header clearfix"]/a/text()')[0].strip()
            privice = el.xpath('.//div[@class="park-row"]//div[@class="title text-ellipsis"][1]/span/text()')[0].strip()
            city = el.xpath('.//div[@class="park-row"]//div[@class="title text-ellipsis"][2]/span/text()')[0].strip()
            area = el.xpath('.//div[@class="park-row"]/div[@class="col-4"][2]//span/text()')[0].strip()
            single['园区id'] = detail_url
            single['园区名称'] = yq_name
            single['所属省份'] = privice
            single['所属城市'] = city
            single['占地面积'] = area

            times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            single['gmt_created'] = times
            single['gmt_updated'] = times

            sum.append(single)
            print(single)
        time.sleep(2.4)
    print(sum)
    sum = get_updated(sum)
    if len(sum)==0:
        print('---------------------暂时没有数据更新！！！--------------------')
    else:
        print('--------------------------有数据更新{}个----------------------'.format(len(sum)))
        insert_db(sum)

def get_updated(sum):
    sql = "select * from tyc_source_data"
    cursor.execute(sql)
    data = cursor.fetchall()
    if len(data)==0:
        return sum
    data = [i[2] for i in data]
    from pybloom_live import ScalableBloomFilter
    bloom = ScalableBloomFilter(initial_capacity=100,error_rate=0.001)
    for bl in data:
        bloom.add(bl)
    sum = [i for i in sum if i['园区id'] not in bloom]
    return sum

def insert_db(data):
    for i in data:
        id = i.get('园区id').strip()
        yq = i.get('园区名称').strip()
        province = i.get('所属省份')
        city = i.get('所属城市')
        area = i.get('占地面积')
        gmt_created = i.get('gmt_created')
        gmt_updated = i.get('gmt_updated')

        sql = """insert into tyc_source_data (id,park_name,park_id,province,city,area,gmt_created,gmt_updated)values(NULL,'{}','{}','{}','{}','{}','{}','{}')""".format(yq,id,province,city,area,gmt_created,gmt_updated)
        cursor.execute(sql)
    db.commit()
    db.close()

if __name__ =='__main__':
    dl()
    main()