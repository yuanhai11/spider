import scrapy
import requests
import json
import re
import math
import requests
from ..items import LianJiaItem
# from lxml import etree
class SpiderLianjiaSpider(scrapy.Spider):
    custom_settings = {
        'ITEM_PIPELINES': {'ScrapyProjects.pipelines.LianJiaPipeline': 300},
    }
    name = 'spider_lianjia'
    allowed_domains = ['*']

    def start_requests(self):
        for i in range(1,10):
            url = "https://hz.fang.lianjia.com/loupan/pg{}/".format(i)
            data = 'hello world'
            yield scrapy.Request(url=url, callback=self.parse_lists,meta={'d':data})

    def parse_lists(self,response):
        '''
        不同spider对应不同user_agent
        '''

        items = LianJiaItem()
        ele_lists = response.xpath('//ul[@class="resblock-list-wrapper"]/li')
        for ele in ele_lists:
            title = ele.xpath('./a/@title').extract_first()
            items['title'] = title
            yield items
