# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field

# 定义文章数据结构
class ArticleItem(Item):
    title = Field()
    author = Field()
    _time = Field()
    visitors = Field()
    pre_talk = Field()
    article_content = Field()