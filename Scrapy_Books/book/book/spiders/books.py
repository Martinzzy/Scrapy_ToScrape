# -*- coding: utf-8 -*-
import scrapy
from book.items import BookItem
from scrapy.linkextractors import LinkExtractor


class BooksSpider(scrapy.Spider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    #书籍列表页面的解析函数
    def parse(self, response):
        #提取书籍列表页面中每本书的url
        items = LinkExtractor(restrict_css='article.product_pod h3')
        for book_url in items.extract_links(response):
            yield scrapy.Request(url = book_url.url,callback=self.parse_book)
        #提取‘下一页’的链接
        next_url = response.css('ul.pager li.next a::attr(href)').extract_first()
        if next_url:
            next_url = response.urljoin(next_url)
            yield scrapy.Request(url=next_url,callback=self.parse)

    #书籍页面的解析函数
    def parse_book(self,response):
        book = BookItem()

        item = response.css('div.product_main')
        book['name'] = item.css('div.product_main h1::text').extract_first()
        book['price'] = item.css('p.price_color::text').extract_first()
        book['review_rating'] = item.css('p.star-rating::attr(class)').re_first('star-rating ([A-Za-z]+)')
        book['upc'] = response.css('table.table-striped tr:nth-child(1) td::text').extract_first()
        book['stock'] = response.css('table.table-striped tr:nth-child(6) td::text').re_first('In stock \((\d+) available\)')
        book['review_num'] = response.css('table.table-striped tr:nth-child(7) td::text').extract_first()

        yield book