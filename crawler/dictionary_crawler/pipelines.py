# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


# class DictionaryCrawlerPipeline(object):
#     def process_item(self, item, spider):
#         return item

import logging
from pymongo import MongoClient


class MongoPipeline(object):
    collection_name = 'cambridge_dict'

    def __init__(self, host, username, password, mongo_db):
        self.host = host
        self.username = username
        self.password = password
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        # pull in information from settings.py
        return cls(
            host=crawler.settings.get('MONGO_HOST'),
            username=crawler.settings.get('MONGO_USERNAME'),
            password=crawler.settings.get('MONGO_PASSWORD'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        # initializing spider
        # opening db connection
        self.client = MongoClient(self.host, username=self.username, password=self.password, authSource=self.mongo_db,
                                  authMechanism='SCRAM-SHA-256')
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        # clean up when spider is closed
        self.client.close()

    def process_item(self, item, spider):
        # how to handle each post
        self.db[self.collection_name].insert(dict(item))
        logging.debug("Post added to MongoDB")
        return item
