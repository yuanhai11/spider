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
    'cookie':'UM_distinctid=172bbaccc62603-0050d30577940c-4353761-1fa400-172bbaccc647d; zg_did=%7B%22did%22%3A%20%22172bbaccd883ee-0647a7453ea16a-4353761-1fa400-172bbaccd8949e%22%7D; _uab_collina=159228656386499679453544; QCCSESSID=hfalkfri2e4pvkb97m91e3dfs4; zg_88a2b557a17244ae873029004837f331=%7B%22sid%22%3A%201598504311954%2C%22updated%22%3A%201598504313192%2C%22info%22%3A%201598504311957%2C%22superProperty%22%3A%20%22%7B%5C%22%E5%BA%94%E7%94%A8%E5%90%8D%E7%A7%B0%5C%22%3A%20%5C%22%E6%89%BE%E5%AE%A2%E6%88%B7WEB%E7%AB%AF%5C%22%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.qcc.com%22%2C%22cuid%22%3A%20%2231831%22%7D; zg_faa71dba513e47e2b1742e346e8fdf66=%7B%22sid%22%3A%201598576211914%2C%22updated%22%3A%201598576211981%2C%22info%22%3A%201598536003039%2C%22superProperty%22%3A%20%22%7B%5C%22%E5%BA%94%E7%94%A8%E5%90%8D%E7%A7%B0%5C%22%3A%20%5C%22%E9%A3%8E%E6%8E%A7%E7%AE%A1%E5%AE%B6WEB%E7%AB%AF%5C%22%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.qcc.com%22%2C%22zs%22%3A%200%2C%22sc%22%3A%200%7D; acw_tc=73dc081515989239590361012ec83528c79b7bbbe482194d07932d8203; CNZZDATA1254842228=1553687765-1592281864-https%253A%252F%252Fsp0.baidu.com%252F%7C1598920277; Hm_lvt_78f134d5a9ac3f92524914d0247e70cb=1598494727,1598604787,1598845804,1598923962; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201598923960413%2C%22updated%22%3A%201598925662283%2C%22info%22%3A%201598344658396%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.baidu.com%22%2C%22zs%22%3A%200%2C%22sc%22%3A%200%2C%22cuid%22%3A%20%228b60bc5b630af5b0d5d4eea7102cf528%22%7D; Hm_lpvt_78f134d5a9ac3f92524914d0247e70cb=1598925662',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
}
def dl():
    resp = requests.get(dlurl).text
    time.sleep(3)
    resp = re.sub(r'\n', '', resp)
    proxy = {
        'http': resp
    }
    proxys.append(proxy)
    print(proxys[-1])
def reload(page):
    dl()
    response = ""
    for g in range(10):
        try:
            response = requests.get(method='get',url='https://www.qcc.com/more_zonesearch.html?p={}'.format(page),
                                    proxies=proxys[-1], headers=headers, timeout=10)
            print(response)
            if response.status_code == 200:
                response = response.content.decode('utf8')
                time.sleep(1)
                break
        except Exception:
            dl()
    tree = etree.HTML(response)
    element = tree.xpath('//div[@class="panel n-s m-t-md"]/a')
    return element

def main():
    parks_response = ""
    for nn in range(20):
        try:
            parks_response = requests.get(method='get',url='https://www.qcc.com/more_zonesearch', headers=headers,
                                    proxies=proxys[-1],timeout=12)
            if parks_response.status_code == 200:
                parks_response = parks_response.content.decode('utf8')
                print('break')
                break
        except Exception:
            dl()
    t = etree.HTML(parks_response)
    # 查询到所有园区数据
    all_num = int(t.xpath('//h2[@class="e_zone-h2"]/span/text()')[0])
    num = 1
    parks_page = math.ceil(all_num/10)
    print(parks_page)
    sum = []
    for page in range(num,parks_page+1):
        response = ""
        for g in range(10):
            try:
                response = requests.get(url='https://www.qcc.com/more_zonesearch.html?p={}'.format(page), proxies=proxys[-1],headers=headers,timeout=10)
                print(response)
                if response.status_code == 200:
                    response = response.content.decode('utf8')
                    print('break')
                    break
            except Exception:
                dl()

        tree = etree.HTML(response)
        element = tree.xpath('//div[@class="panel n-s m-t-md"]/a')
        while True:
            if len(element)==0:
                element = reload(page)
                print('触发了reload函数！！！！')
            else:
                break
        for el in element:
            single = {}
            detail_url = el.xpath('./@href')[0].strip()
            yq_name = el.xpath('./div[1]/text()')[0].strip()
            privice = el.xpath('./div[2]/span[1]/text()')[0].strip()
            city = el.xpath('./div[2]/span[2]/text()')[0].strip()
            area = el.xpath('./div[3]/span[1]/text()')[0].strip()
            single['园区id'] = 'https://www.qcc.com'+detail_url
            # 园区名称
            single['园区名称'] = yq_name
            # 所属省份
            privice = privice.split('：')[-1]
            single['所属省份'] = privice
            # 所属城市
            city = city.split('：')[-1]
            single['所属城市'] = city
            # 占地面积
            area = area.split('：')[-1]
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
    sql = "select * from qcc_source_data"
    cursor.execute(sql)
    data = cursor.fetchall()
    if len(data)==0:
        return sum
    data = [i[2] for i in data]
    from pybloom_live import ScalableBloomFilter
    bloom = ScalableBloomFilter(initial_capacity=10000,error_rate=0.001)
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

        sql = """insert into qcc_source_data (id,park_name,park_id,province,city,area,gmt_created,gmt_updated)values(NULL,'{}','{}','{}','{}','{}','{}','{}')""".format(yq,id,province,city,area,gmt_created,gmt_updated)
        cursor.execute(sql)
    db.commit()
    db.close()

def blood_filter_pickle(sum):

    sql = "select * from qcc_source_data"
    cursor.execute(sql)
    data = cursor.fetchall()
    if len(data) == 0:
        return sum
    data = [i[2] for i in data]
    from pybloom_live import ScalableBloomFilter
    bloom = ScalableBloomFilter(initial_capacity=10000, error_rate=0.001)
    for bl in data:
        bloom.add(bl)
    sum = [i for i in sum if i['园区id'] not in bloom]
    return sum
if __name__ =='__main__':
    dl()
    main()


