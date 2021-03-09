import scrapy
import pymysql
import math,re,time
from ..items import SpiderCompanyItem

class SpiderCompanyInfoSpider(scrapy.Spider):
    name = 'spider_company_info'
    allowed_domains = ['www.qcc.com']
    # start_urls = ['https://www.qcc.com/more_zonesearch.html?p=1']

    def start_requests(self):
        park_url = 'https://www.qcc.com/more_zonesearch.html?p=1'
        # for page in range(1,501):
        #     park_url = 'https://www.qcc.com/more_zonesearch.html?p={}'.format(page)
        yield scrapy.Request(url=park_url,callback=self.parse_data)
    def parse_data(self,response):
        response_content = response.text
        ele_lists = response.xpath('//div[@class="panel n-s m-t-md"]/a')
        for ele in ele_lists:
            item = SpiderCompanyItem()
            park_url = 'https://www.qcc.com' + ele.xpath('./@href').extract_first().strip()
            park_name = ele.xpath('./div[1]/text()').extract_first().strip()
            province = ele.xpath('./div[2]/span[1]/text()').extract_first().strip().split('：')[-1]
            city = ele.xpath('./div[2]/span[2]/text()').extract_first().strip().split('：')[-1]
            area = ele.xpath('./div[3]/span[1]/text()').extract_first().strip().split('：')[-1]
            times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            item['park_url'] =park_url
            item['park_name'] =park_name
            item['province'] =province
            item['city'] =city
            item['area'] =area
            item['gmt_created'] = times
            item['gmt_updated'] = times
            yield item



