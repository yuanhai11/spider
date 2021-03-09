# coding:utf-8
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

问题：
    企查查不封iP，封账号。
'''
import math
import requests,json,re,time
from lxml import etree
import pymysql
import decouple
import random
dlurl = 'http://dynamic.goubanjia.com/dynamic/get/d490a5d4debefc8980ae6ee4c4148552.html?sep=3'
proxys = []

def dl():
    resp = requests.get(dlurl).text
    time.sleep(2)
    resp = re.sub(r'\n', '', resp)
    proxy = {
        'http': resp
    }
    proxys.append(proxy)
    print(proxys[-1])
def get_ua():
    user_agents = [
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60',
        'Opera/8.0 (Windows NT 5.1; U; en)',
        'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
        'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2 ',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0) ',
    ]
    user_agent = random.choice(user_agents)  # random.choice(),从列表中随机抽取一个对象
    headers = {
        'cookie':'UM_distinctid=172bbaccc62603-0050d30577940c-4353761-1fa400-172bbaccc647d; zg_did=%7B%22did%22%3A%20%22172bbaccd883ee-0647a7453ea16a-4353761-1fa400-172bbaccd8949e%22%7D; _uab_collina=159228656386499679453544; QCCSESSID=hfalkfri2e4pvkb97m91e3dfs4; Hm_lvt_78f134d5a9ac3f92524914d0247e70cb=1598348563,1598348951,1598403196,1598494727; zg_88a2b557a17244ae873029004837f331=%7B%22sid%22%3A%201598504311954%2C%22updated%22%3A%201598504313192%2C%22info%22%3A%201598504311957%2C%22superProperty%22%3A%20%22%7B%5C%22%E5%BA%94%E7%94%A8%E5%90%8D%E7%A7%B0%5C%22%3A%20%5C%22%E6%89%BE%E5%AE%A2%E6%88%B7WEB%E7%AB%AF%5C%22%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.qcc.com%22%2C%22cuid%22%3A%20%2231831%22%7D; zg_faa71dba513e47e2b1742e346e8fdf66=%7B%22sid%22%3A%201598576211914%2C%22updated%22%3A%201598576211981%2C%22info%22%3A%201598536003039%2C%22superProperty%22%3A%20%22%7B%5C%22%E5%BA%94%E7%94%A8%E5%90%8D%E7%A7%B0%5C%22%3A%20%5C%22%E9%A3%8E%E6%8E%A7%E7%AE%A1%E5%AE%B6WEB%E7%AB%AF%5C%22%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.qcc.com%22%2C%22zs%22%3A%200%2C%22sc%22%3A%200%7D; acw_tc=65e21c1c15985762302013937e6ea898cac8849fb4287a784be0f14302; CNZZDATA1254842228=1553687765-1592281864-https%253A%252F%252Fsp0.baidu.com%252F%7C1598574362; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201598576228920%2C%22updated%22%3A%201598576489627%2C%22info%22%3A%201598344658396%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%2C%22zs%22%3A%200%2C%22sc%22%3A%200%2C%22cuid%22%3A%20%228b60bc5b630af5b0d5d4eea7102cf528%22%7D; Hm_lpvt_78f134d5a9ac3f92524914d0247e70cb=1598576490',
        'user-agent': user_agent
}
    return headers
def main():
    db = pymysql.connect(host='192.168.2.99', user='root', password='BOOT-xwork1024', database='spider', port=3306)
    cursor = db.cursor()
    sql = "select park_name,park_id from spider_park_data"
    cursor.execute(sql)
    data = cursor.fetchall()
    print(data)
    sum = []
    n = 1
    for num,i in enumerate(data):
        park_name = i[0]
        park_url = i[1]
        # 从第 * 页开始爬取
        if num < 2790:     #  261 页开始
            continue
        if num ==2852:
            if len(sum)!=0:
                insert_db(sum)
            break
        # exit()
        parks_response = ""
        for i in range(20):
            try:
                parks_response = requests.get(url=park_url, headers=get_ua(),
                                              proxies=proxys[-1], timeout=12)
                time.sleep(1)
                if parks_response.status_code == 200:
                    parks_response = parks_response.content.decode('utf8')
                    print('break')
                    break
            except Exception:
                dl()
        time.sleep(1)
        t = etree.HTML(parks_response)
        try:
            all_num = int(t.xpath('//span[@class="font-15 text-dark-dk"]/span/text()')[0].strip())
            print(all_num)
        except Exception as e:
            print('园区：{} 没有企业数据'.format(park_name))
            continue
        num = 1
        parks_page = math.ceil(all_num/10)
        print(parks_page)
        if parks_page>500:
            parks_page = 500
        for page in range(num,parks_page+1):
            response = ""
            for g in range(10):
                try:
                    response = requests.get(url=park_url + '&p={}'.format(page), proxies=proxys[-1],headers=get_ua(),timeout=10)
                    print(response)
                    if response.status_code == 200:
                        response = response.content.decode('utf8')
                        print('break')
                        break
                except Exception:
                    dl()
            tree = etree.HTML(response)
            element_lists = tree.xpath('//table[@class="m_srchList"]/tbody/tr')
            for el in element_lists:
                single = {}
                url = el.xpath('./td[2]/a/@href')[0].strip()
                name = el.xpath('./td[2]/a/text()')[0].strip()
                single['url'] = 'https://www.qcc.com'+url
                single['name'] = name
                single['park_name'] = park_name
                sum.append(single)
                print(single)
                # exit()
            time.sleep(1.5)
        print(sum)
        # 每10页插入数据库一次
        if n==10:
            insert_db(sum)
            sum = []
            n = 1
            dl()
        n+=1

def insert_db(data):
    db = pymysql.connect(host='192.168.2.99', user='root', password='BOOT-xwork1024', database='spider', port=3306)
    cursor = db.cursor()
    for i in data:
        url = i.get('url').strip()
        name = i.get('name').strip()
        park_name = i.get('park_name')
        times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql = """insert into spider_park_company_connect (id,company_url,company_name,company_connect_park,gmt_created,gmt_updated)values(NULL,'{}','{}','{}','{}','{}')""".format(url,name,park_name,times,times)

        cursor.execute(sql)
    db.commit()
    db.close()



if __name__ =='__main__':
    dl()
    main()


