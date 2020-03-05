# -*- coding: utf-8 -*-
import scrapy


class TestSpider(scrapy.Spider):
    name = 'test'
    allowed_domains = ['wxapp-union.com']
    start_urls = ['http://www.wxapp-union.com/article-8-1.html']

    def parse(self, response):
        # tbody = response.xpath('//table').extract_first()
        print('*'*40)
        print(response.text)
        print('*'*40)
