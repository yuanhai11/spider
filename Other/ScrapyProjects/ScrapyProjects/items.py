# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LianJiaItem(scrapy.Item):
    title = scrapy.Field()

class BookItem(scrapy.Item):
    book_name = scrapy.Field()