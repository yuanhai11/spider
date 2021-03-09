# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderCompanyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    park_url = scrapy.Field()
    park_name = scrapy.Field()
    province = scrapy.Field()
    city = scrapy.Field()
    area = scrapy.Field()
    gmt_created = scrapy.Field()
    gmt_updated = scrapy.Field()
