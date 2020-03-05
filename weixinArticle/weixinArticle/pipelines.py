# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from html2text import HTML2Text
import pypandoc
from os.path import join
import os

class HTMLPipeline(object):
    def __init__(self):
        self.f = open('每日学英语-公众号.html','a',encoding='utf-8')
    
    def process_item(self, item, spider):
        if self.f:
            self.f.write(item['article'])
            self.f.write('<br>')
        return item

    def close_spider(self,spider):
        self.f.close()
        output = pypandoc.convert_file('每日学英语-公众号.html','epub',format='html',outputfile='每日学英语.epub')
        # print(output)

class MarkdownPipeline(object):
    def __init__(self):
        self.path = 'markdown'
        if os.path.exists(self.path):
            os.mkdir(self.path)
    
    def process_item(self, item, spider):
        fp = join(self.path,item['title']+".md")
        print('*'*40)
        print(fp)
        print('*'*40)
        text = item['article']
        h = HTML2Text()
        text = h.handle(text)
        with open(fp,'w',encoding='utf-8') as f:
            f.write(text)
        return item
