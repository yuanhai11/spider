# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import json

class LianJiaPipeline:
    sum = []
    def process_item(self, item, spider):
        LianJiaPipeline.sum.append(dict(item))
        return item

    def close_spider(self,spider):
        with open('./data/lianjia.json','w',encoding='utf-8')as fp:
            fp.write(json.dumps({'data':LianJiaPipeline.sum},ensure_ascii=False))

class BookPipeline:
    sum = []
    def process_item(self, item, spider):
        BookPipeline.sum.append(dict(item))
        return item

    def close_spider(self, spider):
        with open('./data/book.json', 'w', encoding='utf-8')as fp:
            fp.write(json.dumps({'data': BookPipeline.sum}, ensure_ascii=False))
