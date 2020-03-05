# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import re
from html2text import HTML2Text
from scrapy.exporters import JsonLinesItemExporter
from urllib.parse import urljoin
import pymongo

## 规范URL
def parse_url(matched):
    return 'src="{}"'.format(urljoin('http://www.wxapp-union.com/',str(matched.group(1))))

# 转化为Markdown
def convert_md(article_content):
    # 规范HTML图片链接
    pattern = 'src="(.*?)"'
    html = re.sub(pattern,parse_url,article_content)
    ## 转化
    h = HTML2Text()
    text = h.handle(html)
    text = re.sub('-\n','-',text)
    return text

# 存储到Json文件中
class JsonPipeline(object):
    def __init__(self):
        self.f = open('wxjc.json','wb')
        self.exporter = JsonLinesItemExporter(self.f,
        ensure_ascii=False,encoding="utf-8")

    def process_item(self, item, spider):
        # 将内容转化为MarkDown格式
        item['article_content'] = convert_md(item['article_content'])
        self.exporter.export_item(item)
        return item
    
    def close_spider(self,spider):
        self.f.close()

# 写入Markdown
class MDPipeline(object):
    def __init__(self):
        self.f = open('wx_teaches.md','a',encoding='utf-8')

    def process_item(self,item,spider):
        if self.f:
            self.f.write('\n')
            self.f.write("# " + item['title'] + '\n')
            header_info = "作者:{}      发布时间:{}      Visitors:{}\n".format(item['author'],item['_time'],item['visitors'])
            self.f.write(header_info)
            self.f.write('> ' + item['pre_talk'] + '\n')
            self.f.write(item['article_content'])
        return item
    
    def close_spider(self,spider):
        self.f.close()

# 存储到MongoDB数据库
class MongoPipeline(object):
    def __init__(self,mongo_uri,mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
    
    @classmethod
    def from_crawler(cls,crawler):
        return cls(mongo_uri = crawler.settings.get('MONGO_URI'),
                    mongo_db = crawler.settings.get('MONGO_DB'))
    
    def open_spider(self,spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db =self.client[self.mongo_db]
    
    def process_item(self,item,spider):
        name = item.__class__.__name__
        # <a href=\"space-uid-17761.html\">Rolan</a> 
        item['author'] = re.search('<a.*?>(.*?)</a>',item['author']).group(1)
        self.db[name].insert(dict(item))
        return item
    
    def close_spider(self,spider):
        self.client.close()