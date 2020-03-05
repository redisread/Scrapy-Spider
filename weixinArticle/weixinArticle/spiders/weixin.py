# -*- coding: utf-8 -*-
import scrapy
from scrapy import Spider,Request
from urllib.parse import urljoin
from weixinArticle.items import WeixinarticleItem

class WeixinSpider(scrapy.Spider):
    name = 'weixin'
    allowed_domains = ['ershicimi.com','weixin.qq.com']
    #start_urls = ['https://www.ershicimi.com/a/10589?page=32']

    def start_requests(self):
        base_url = 'https://www.ershicimi.com/a/10589?page='
        for i in range(32,0,-1):
            yield Request(base_url+str(i),self.first_parse)
    
    def first_parse(self,response):
        domain_url = 'https://www.ershicimi.com'
        article_elems = response.xpath('//div[@class="weui_media_bd"]/h4/a/@href')
        for elem in article_elems:
            yield Request(urljoin(domain_url,elem.get()),self.parse)

    def parse(self, response):
        title = response.xpath('//div[@id="img-content"]//h2//text()').extract_first()
        content = response.xpath('//div[@id="img-content"]').extract_first()
        item = WeixinarticleItem()
        item['title'] = title
        item['article'] = content
        yield item
