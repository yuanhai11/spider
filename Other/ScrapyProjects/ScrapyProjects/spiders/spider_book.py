import scrapy
from ..items import BookItem

class SpiderBookSpider(scrapy.Spider):
    name = 'spider_book'
    allowed_domains = ['yoususu.com']

    custom_settings = {
        'ITEM_PIPELINES': {'ScrapyProjects.pipelines.BookPipeline': 300},
    }
    def start_requests(self):
        for i in range(1,11):
            url = 'https://www.yousuu.com/bookstore/?channel&classId&tag&countWord&status&update&sort&page={}'.format(i)
            yield scrapy.Request(url=url,callback=self.parse_data)

    def parse_data(self, response):
        items = BookItem()
        ele_lists = response.xpath('//div[@class="common-card-layout StoreBooks"]/div/div')
        for ele in ele_lists:
            book_name = ele.xpath('.//a[@class="book-name"]/text()').extract_first()
            print(book_name)
            items['book_name'] = book_name
            yield items