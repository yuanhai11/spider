import scrapy
import requests
import time,re

class SpiderSpider(scrapy.Spider):
    name = 'spider'
    allowed_domains = ['51job.com']
    # start_urls = ['http://51job.com/']

    def start_requests(self):
        company_name = "中国人寿保险股份有限公司杭州市分公司"
        page = 1
        url = "https://search.51job.com/list/000000,000000,0000,00,9,99,中国人寿保险股份有限公司杭州市分公司,{},1.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare=".format(
            page)
        dlurl = 'http://dps.kdlapi.com/api/getdps/?orderid=969607686104916&num=1&pt=2&sep=1'
        resp = requests.get(dlurl).text
        time.sleep(4)
        resp = re.sub(r'\n', '', resp)
        yield scrapy.Request(url=url,callback=self.parse_data,meta={'proxy':'http://%s'%resp})

    def parse_data(self, response):
        data = response.text
        print(data)

