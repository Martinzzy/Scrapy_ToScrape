# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field


class BookItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = Field()
    price = Field()
    review_rating = Field()
    upc = Field()
    stock = Field()
    review_num = Field()


#测试BookItem的一些代码
# book1 = BookItem(name='Needful Things',price=45.0)
# book2 = {}
# book2['name'] = 'Life of Pi'
# book2['price'] = 50
# print(book2)
