# coding:utf-8
import math
import requests,json,re,time
from lxml import etree
import pymysql
import decouple
import random

dlurl = 'http://dps.kdlapi.com/api/getdps/?orderid=969607686104916&num=1&pt=2&sep=1'
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
        'cookie':'QCCSESSID=dtnvhk3k2clrofdm4l2huajnt6; zg_did=%7B%22did%22%3A%20%22174c36455ce45f-01eae4887719c1-333376b-1fa400-174c36455cf8e1%22%7D; UM_distinctid=174c364578018e-08bbf1ec92b5c1-333376b-1fa400-174c36457814b7; Hm_lvt_78f134d5a9ac3f92524914d0247e70cb=1601005968,1601006714,1601006965,1601011018; hasShow=1; _uab_collina=160101109077994162435362; acw_tc=7d4dab2316010212855285175e2149981a5bf0003d92e2522a6c75fd84; CNZZDATA1254842228=1795050360-1601009095-%7C1601019895; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201601021285671%2C%22updated%22%3A%201601022672858%2C%22info%22%3A%201601005966807%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.qcc.com%22%2C%22cuid%22%3A%20%228b60bc5b630af5b0d5d4eea7102cf528%22%2C%22zs%22%3A%200%2C%22sc%22%3A%200%7D; Hm_lpvt_78f134d5a9ac3f92524914d0247e70cb=1601022673',
        'user-agent': user_agent
}
    return headers
def main():
    sum = []
    all_parks = ['恒大国际家居建材城']
    for title in all_parks:
        url = "https://www.qcc.com/more_zonesearch?searchKey={}".format(title)
        parks_response = ""
        for i in range(10):
            if i==9:
                raise TypeError('代理出现问题！！！')
            try:
                parks_response = requests.get(url=url, headers=get_ua(),
                                              proxies=proxys[-1],
                                              timeout=12)
                if parks_response.status_code == 200:
                    parks_response = parks_response.content.decode('utf8')
                    print('break')
                    # print(parks_response)
                    # exit()
                    break
            except Exception:
                time.sleep(2)
                dl()

        parks_response = etree.HTML(parks_response)
        ele_lists1 = parks_response.xpath('//div[@class="panel n-s m-t-md"]/a')
        ele_lists2 = parks_response.xpath('//div[@class="panel n-s m-t-md"]/div[2]/a')

        if len(ele_lists1)!=0:
            ele_lists = ele_lists1
        elif len(ele_lists2)!=0:
            ele_lists = ele_lists2
        else:
            print('该园区：{}没有企业数据！！！不入库'.format(title))
            continue

        for ele in ele_lists:
            park_url = 'https://www.qcc.com' + ele.xpath('./@href')[0].strip()
            park_name = "".join(ele.xpath('./div[1]//text()')).strip()
            province = ele.xpath('./div[2]/span[1]//text()')[0].strip().split('：')[-1]
            city = ele.xpath('./div[2]/span[2]//text()')[0].strip().split('：')[-1]
            area = ele.xpath('./div[3]/span[1]//text()')[0].strip().split('：')[-1]

            if park_name == title:
                parks_response = ""
                for i in range(10):
                    if i == 9:
                        raise TypeError('代理出现问题！！！')
                    try:
                        parks_response = requests.get(url=park_url, headers=get_ua(),
                                                      proxies=proxys[-1],
                                                      timeout=12)
                        if parks_response.status_code == 200:
                            parks_response = parks_response.content.decode('utf8')
                            print('break')
                            break
                    except Exception:
                        time.sleep(2)
                        dl()
                t = etree.HTML(parks_response)
                try:
                    all_num = int(t.xpath('//span[@class="font-15 text-dark-dk"]/span/text()')[0].strip())
                    print(all_num)
                except Exception as e:
                    print('园区：{} 没有企业数据'.format(park_name))
                    continue

                parks_page = math.ceil(all_num / 10)
                print(parks_page)
                if parks_page > 500:
                    parks_page = 500

                id = park_url.split('_')[-1]
                for page in range(1, parks_page + 1):
                    park_url = 'https://www.qcc.com/more_zonecompany.html?id={}&p={}'.format(id,page)
                    response = ""
                    for g in range(10):
                        if g==9:
                            raise TypeError('代理出现问题！！！')
                        try:
                            response = requests.get(url=park_url,
                                                    headers=get_ua(),
                                                    proxies=proxys[-1],
                                                    timeout=10)
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
                        company_url = el.xpath('./td[2]/a/@href')[0].strip()
                        company_name = el.xpath('./td[2]/a/text()')[0].strip()

                        single['company_url'] = 'https://www.qcc.com' + company_url
                        single['company_name'] = company_name

                        single['park_url'] = park_url
                        single['park_name'] = park_name
                        single['park_province'] = province
                        single['park_city'] = city
                        single['park_area'] = area

                        sum.append(single)
                        print(single)
                    time.sleep(1.5)
            time.sleep(1.6)
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


