# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from MyTest.items import ArticleItem

class WxSpider(CrawlSpider):
    name = 'wx'
    allowed_domains = ['wxapp-union.com']
    start_urls = ['http://www.wxapp-union.com/portal.php?mod=list&catid=2&page=255']

    rules = (
        Rule(LinkExtractor(allow=r'.+mod=list&catid=2&page=\d'), follow=True),
        Rule(LinkExtractor(allow=r'.+article-.+\.html'),callback="parse_item",follow=False)
    )

    def parse_item(self, response):
        title = response.xpath('//h1[@class="ph"]/text()').get()
        author = response.xpath('//p[@class="authors"]//a').get()
        _time = response.xpath('//span[@class="time"]/text()').get()
        visitors = response.xpath('//div[contains(@class,"focus_num")]//a/text()').get()
        pre_talk = response.xpath('//div[@class="blockquote"]//p/text()').get()
        article_content = response.xpath('//td[@id="article_content"]').get()
        item = ArticleItem(title=title,author=author,_time=_time,visitors=visitors,pre_talk=pre_talk,article_content=article_content)
        print('*'*40)
        print(title)
        print('*'*40)
        return  item
