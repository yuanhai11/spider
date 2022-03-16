import json
import time

import scrapy
from InvoiceData.fetch_free_proxyes import logger
from InvoiceData.items import InvoicedataItem

class InvoiceSpider(scrapy.Spider):
    name = 'invoice'
    allowed_domains = ['tax.tianyancha.com']

    website_possible_httpstatus_list = [403]
    handle_httpstatus_list = [403]

    # data = None
    def bloom_filter(self):
        pass

    def load_data(self):
        import json
        with open(r'D:\projects\S_Git_proj\spider\Other\spider_all\税号-浙江省\data-second.txt', encoding='utf-8')as fp:
            content = json.loads(fp.read())
            print(len(content))
        index = 0
        for index, d in enumerate(content):
            if d[0] == '2886939523':  # 下波数据 2340422782
                print("当前数据的索引位置:{} ".format(index))
                break
        data = content[index + 1:index + 100]
        data = ['https://tax.tianyancha.com/cloud-wechat/qrcode.json?gid={}&_=1634088420699'.format(i[0]) for i in data]
        return data

    def start_requests(self):
        data = self.load_data()
        le = len(data)
        logger.info("剩余公司数量：{}".format(le))
        # print(data)
        urls = data

        for url in (urls):
            yield scrapy.Request(url=url, callback=self.parse)


    def parse_json(self,data):
        c = json.loads(data)
        gid = c.get('gid')
        name = c.get('name')
        taxnum = c.get('taxnum')
        address = c.get('address').strip()
        phone = c.get('phone')
        bank = c.get('bank')
        bankAccount = c.get('bankAccount')
        item = InvoicedataItem()
        item['gid'] = gid
        item['name'] = name
        item['taxnum'] = taxnum
        item['address'] = address
        item['phone'] = phone
        item['bank'] = bank
        item['bankAccount'] = bankAccount
        yield item

    def parse(self, response):
        # if response.body == "banned":
        #     req = response.request
        #     req.meta["change_proxy"] = True
        #     yield req
        # else:
        logger.info("get data from web: %s" % response.text)
        self.parse_json(response.text)
