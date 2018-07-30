# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo

class MongoPipeline(object):
    def __init__(self, uri, db):
        self.uri = uri
        self.db = db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            uri = crawler.settings.get('MONGO_URI'),
            db = crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.uri)
        self.db = self.client[self.db]

    def process_item(self, item, spider):
        self.db['transcripts'].insert(dict(item))
        return item

    def close_spider(self, spider):
        self.client.close()
