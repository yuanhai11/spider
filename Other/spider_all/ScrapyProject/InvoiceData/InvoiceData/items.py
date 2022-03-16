# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InvoicedataItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # 表的结构:
    id = scrapy.Field()
    company_name = scrapy.Field()
    company_num = scrapy.Field()
    tax_num = scrapy.Field()
    reg_addr = scrapy.Field()
    phone = scrapy.Field()
    bank = scrapy.Field()
    bank_card = scrapy.Field()

    gmt_created = scrapy.Field()
    gmt_updated = scrapy.Field()
