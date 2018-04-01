# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
import pymongo

class BookPipeline(object):
    review_rating_map = {
        'One':1,
        'Two':2,
        'Three':3,
        'Four':4,
        'Five':5
    }
    def process_item(self,item,spider):
        rating = item.get('review_rating')
        if rating:
            item['review_rating'] = self.review_rating_map[rating]
        return item

#把英镑转化为人民币
class PriceConverterPipeline(object):
    exchange_rate = 8.5309
    def process_item(self, item, spider):
        price = float(item['price'][1:])*self.exchange_rate
        item['price'] = '%.2f'%price
        return item

#去重
class DuplicatesPipeline(object):
    def __init__(self):
        self.book_set = set()

    def process_item(self,item,spider):
        name = item['name']
        if name in self.book_set:
            raise DropItem('Duplicate book found:%s'%item)
        self.book_set.add(name)
        return item

#存储到MongoDB数据库
class MongoPipeline(object):

    collection_name = 'book'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(dict(item))
        return item