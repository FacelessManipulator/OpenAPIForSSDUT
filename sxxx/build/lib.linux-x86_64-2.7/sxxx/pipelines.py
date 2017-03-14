# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import redis
import settings
import json, logging

logger = logging.getLogger("zhjwLog")
FileHandler = logging.FileHandler(settings.LOG_INFO_FILE , 'a')
FileHandler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
FileHandler.setFormatter(formatter)
logger.addHandler(FileHandler)

#INFO: 访问太频繁，不如直接把数据存成json字符串，有需要时直接返回
class SxxxPipeline(object):
    def __init__(self):
        self.bulk = []
        self.trunk_account = set()
        self.db = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
        self.pipeline = self.db.pipeline()
        account_list = self.db.hgetall('account')
        self.fetch_list = [{'account':i, 'password':j} for i,j in zip(account_list.keys(), account_list.values())]


    def trunck(self):
        for item in self.bulk:
            if item['type'] == 'list':
                self.pipeline.rpush(item['field']+'_'+item['master'], item['data'])
            elif item['type'] == 'hash':
                self.pipeline.hset(item['field'], {item['master']: item['data']})
            elif item['type'] == 'string':
                self.pipeline.append(item['field']+'_'+item['master'], item['data'])
        self.bulk = []
        self.pipeline.execute()

    def clear_key(self, type, name, hfiled = None):
        if type == 'string':
            self.pipeline.set(name, "")
        elif type == 'list':
            self.pipeline.delete(name)
        elif type == 'hash':
            if hfiled is not None:
                self.pipeline.hdel(name, hfiled)
            else:
                self.pipeline.delete(name)

    def open_spider(self, spider):
        spider.fetch_list = self.fetch_list

    def process_item(self, item, spider):
        if item['account'] is None:
            logger.info("incomplete data was dropped.")
            return item
        elif item['account'] not in self.trunk_account:
            self.trunk_account.add(item['account'])
            self.clear_key('list', 'kb_'+item['account'])
            self.clear_key('list', 'grade_'+item['account'])

        if item.item_type == 'SxxxItem':
            self.bulk.append({'master': item['account'], 'field': 'grade',
                              'data': json.dumps(dict(item)), 'type': 'list'})
        elif item.item_type == 'KbItem':
            self.bulk.append({'master': item['account'], 'field': 'kb',
                              'data': json.dumps(dict(item)), 'type': 'list'})
        elif item.item_type == 'SignalItem':
            if item['signal'] == 'ERROR_PASSWORD':
                self.clear_key('hash', 'account', item['account'])
        if len(self.bulk) > settings.MAX_REDIS_REQUEST:
            self.trunck()
        return item

    def close_spider(self, spider):
        self.trunck()