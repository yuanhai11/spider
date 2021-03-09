# *_*coding:utf-8 *_*
import requests
import re
import time
import pymysql
from lxml import etree
# 智联招聘数据ETL
# 前程无忧
# 百度招聘
# La_Gou
# boss 直聘
# 大学生创业
class Spider():
    def __init__(self):

        self.headers  = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36',}
        self.proxys = []
        self.conn = pymysql.connect(host='192.168.2.99', user='root', password='BOOT-xwork1024', database='spider', port=3306)
        self.cursor = self.conn.cursor()
        self.get_ip()
        self.bloom = self.get_db_data()
    def get_db_data(self):
        sql = "select * from 58zl"
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        data = [i[4] for i in data]
        from pybloom_live import ScalableBloomFilter
        bloom = ScalableBloomFilter(initial_capacity=100, error_rate=0.001)
        for bl in data:
            bloom.add(bl)
        return bloom

    def get_ip(self):
        time.sleep(3)

        dlurl = 'http://dynamic.goubanjia.com/dynamic/get/d490a5d4debefc8980ae6ee4c4148552.html?sep=3'
        resp = requests.get(dlurl).text
        resp = re.sub(r'\n', '', resp)
        proxy = {
            'http': resp
        }
        self.proxys.append(proxy)
        print(self.proxys[-1])

    def proxy_requested_response(self,url):
        time.sleep(2)
        response = ""
        for g in range(50):
            try:
                response = requests.request(method='get', url=url, headers=self.headers,
                                            proxies=self.proxys[-1], timeout=10)
                print(response)
                if response.status_code == 200:
                    response = response.content.decode('utf-8')
                    time.sleep(1)
                    break
            except Exception:
                self.get_ip()
        if response == "":
            raise ValueError('使用代理请求的数据为 --- 空 ---')
        return response
    def parse_data(self):
        for i in range(1, 71):
            urllist = []
            url1 = 'https://hz.58.com/jianggan/zhaozu/pn{}/pve_1092_0/m1/?PGTID=0d30000d-0005-4753-23ab-b172ca89cd69&ClickID=1'.format(str(i))
            url2 = 'https://hz.58.com/hzshangcheng/zhaozu/pn{}/pve_1092_0/m1/?PGTID=0d30000d-0005-26f0-5024-8da66580056a&ClickID=1'.format(str(i))
            url3 = 'https://hz.58.com/xiaoshan/zhaozu/pn{}/pve_1092_0/m1/?PGTID=0d30000d-0005-777a-628a-f3536b52c4e7&ClickID=1'.format(str(i))
            url4 = 'https://hz.58.com/binjiang/zhaozu/pn{}/pve_1092_0/m1/?PGTID=0d30000d-0005-5290-d5aa-5e582417c8e8&ClickID=1'.format(str(i))
            urllist.append(url1)
            urllist.append(url2)
            urllist.append(url3)
            urllist.append(url4)
            # print(urllist)
            for url in urllist:
                response = self.proxy_requested_response(url=url)
                ele = etree.HTML(response)
                ele_list = ele.xpath('//ul[@id="house-list-wrap"]/li')

                for ele in ele_list:
                    detail_url = ele.xpath('./div[1]/a/@href')[0]
                    contents = self.proxy_requested_response(detail_url)

                    name_list = re.findall('<span class="name-text">(.*?)</span>', contents, re.S)
                    if len(name_list) == 0 :
                        xsname = ""
                    else:
                        xsname = name_list[0]
                    phone_list = re.findall('''<p class='phone-num phone-after-click.*?>(.*?)</p>''', contents, re.S)
                    if len(phone_list) == 0:
                        phone = ""
                    else:
                        phone = phone_list[0]
                    company_name_list = re.findall('<p class="poster-company-.*?">(.*?)</p>', contents, re.S)
                    if len(company_name_list) == 0:
                        company_name = ""
                    else:
                        company_name = company_name_list[0]
                    # detail_url = 'https://hz.58.com/zhaozu/1851975272977x.shtml?legourl=//legoclick.58.com/jump?target=szqCXB3draOWUvYfXh66ULGds1EQrjNQrH0dnW0zrH0LXaO1pZwVUT7bsyEYrjF-nAN3sy7hnjcVPjTOPBdBmvNQsHK-nWDLuhRbPjK6PTD1P1mLPWcYnWckPW01PEDKnHE1PHTQnHDdnj9YrHTzPkDzPHbknTDzPHbknTDQsjDYTH0Osj9YTHDdrj01Pj0dnW9znWNKP97AEzdEEzL--mUb8Fo-Msjb8Jxb8sf-BFxCCpWGCUg-6GM-ouxhGUkKnEDdTEDVnEDKnHcdnjEvnWb3n1DLPWn1nHcvPTDvTgK60h7V01DzP1CkTHDKuhDOPAPhPWnVrH6-PBYYPHNksyFBmHNVnhFWnvEQmHuWnjnvTHDzPHTYPWcOrjndn1c3PHb1rHcKnHcdnjEvnWb3n1EvnHNYn1b1P9DKTEDKTiYKTE7CIZwk01Cfsv6lsWN3shPfUiqJpy78uvI6UBqlpA7fXMNf0A3dsLKvuRtQnjbzg1TfUHDfTEDQnHn8nHTksW9YsWDQnkDVnEDkTEDQsjDYTgVqTHDknjnYTHDknjDdnHNKuWTOujbdujEVPjNdniYYmHNLsy7buWNVujTYmHPBPAw6mHEYTEDkTEDKnTDLrik3Pak1nWD3nkDQTHRBnjcLmynLmWcYm19YnHT&referinfo=true&utm_source=&spm=&product=jingxuan'
                    print(xsname, company_name, phone, detail_url)
                    if detail_url not in self.bloom:
                        self.cursor.execute("""insert into 58zl(id,xsname,company_name,phone,details_url)values(NULL,%s,%s,%s,%s)""", (xsname, company_name, phone, detail_url))
                        self.conn.commit()
                    else:
                        print('该数据数据库已经存在')
                    # break
                    exit()
    def close_db(self):
        self.conn.close()

if __name__ == '__main__':
    spider = Spider()
    spider.parse_data()
    spider.close_db()
