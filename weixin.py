# -*- coding: utf-8 -*-
import scrapy


class WeixinSpider(scrapy.Spider):
    name = 'weixin'
    allowed_domains = ['ershicimi.com']
    start_urls = ['http://ershicimi.com/']

    def parse(self, response):
        pass
