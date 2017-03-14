# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json, os
import settings
import pymongo
import logging
from pymongo.errors import InvalidOperation

logger = logging.getLogger("bkstzLog")
FileHandler = logging.FileHandler(settings.LOG_INFO_FILE , 'a')
FileHandler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
FileHandler.setFormatter(formatter)
logger.addHandler(FileHandler)

class ZhjwPipeline(object):
    def __init__(self):
        self.collected_id_path = os.path.join(settings.WORK_PATH, 'collectedItems.json')
        self.database_request = []
        self.collected_index = set()
        self.db = pymongo.MongoClient(host=settings.MONGO_HOST, port=settings.MONGO_PORT).get_database('zhjw')
    def open_spider(self, spider):
        if os.path.exists(self.collected_id_path):
            with open(self.collected_id_path, 'r') as f:
                try:
                    self.collected_index = set(json.loads(f.read()))
                except ValueError, e:
                    logger.exception(e.message)
                    self.collected_index = set()
        else:
            for item in self.db.bkstz.find():
                self.collected_index.add(item.get('index_id'))

    def process_item(self, item, spider):
        if item.item_type == 'XszzContentItem':
            if item['index_id'] not in self.collected_index:
                self.database_request.append(pymongo.UpdateOne({"index_id": item['index_id']},
                                                                {'$set': {'detail': dict(item)}}))
        elif item.item_type == 'XszzListItem':
            if item['index_id'] not in self.collected_index:
                self.database_request.append(pymongo.InsertOne(dict(item)))
                self.collected_index.add(item['index_id'])

        if len(self.database_request) >= settings.MONGO_REQUEST_MAX_SIZE:
            self.db.bkstz.bulk_write(self.database_request)
            logger.info(str(len(self.database_request)) + " new bkstz collected")
            self.database_request = []
        return item
    def close_spider(self, spider):
        try:
            self.db.bkstz.bulk_write(self.database_request)
            logger.info(str(len(self.database_request)) + " new bkstz collected")
        except InvalidOperation, e:
            logger.info("0 new bkstz collected")
        with open(self.collected_id_path, 'w') as f:
            f.write(json.dumps(list(self.collected_index)))


class TestPrintPipeline(object):
    def __init__(self):
        self.buf = []
    def close_spider(self, spider):
        with open('/home/miller/workspace/python/zhjw/test.txt', 'w') as f:
            for item in self.buf:
                f.write(item.encode('utf-8'))
    def process_item(self, item, spider):
        self.buf.append(item['index_id'] + item['title'])
        return item