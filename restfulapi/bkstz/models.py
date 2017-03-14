#coding=utf-8
from __future__ import unicode_literals

from django.db import models
from restfulapi import settings
import pymongo
from bson import ObjectId
# Create your models here.

class Bkstz:
    db = None
    coll = None
    __inited = False
    @classmethod
    def __init_cls__(cls):
        try:
            cls.db = pymongo.MongoClient(host=settings.MONGO_HOST, port=settings.MONGO_PORT).get_database('zhjw')
            cls.coll = cls.db.get_collection("bkstz")
            cls.__inited = True
        except Exception,e:
            print "".join(("Failed in connecting Mongodb: ", e.message))
            cls.__inited = False
            exit()


    @classmethod
    def get_bkstz_list(cls, page, limit):
        if not cls.__inited:
            cls.__init_cls__()
        shortKeys = ['_id', 'title', 'time', 'url']
        sortedby = [("time", pymongo.DESCENDING), ("index_id", pymongo.DESCENDING), ]
        ret = list()
        for item in cls.coll.find(projection=shortKeys, sort=sortedby, skip=page*10, limit=limit):
            tmpDict = dict(item)
            tmpDict['id'] = str(tmpDict['_id'])
            tmpDict['origin'] = tmpDict['url']
            tmpDict['url'] = "".join((settings.SITE_NAME,"/bkstz/",tmpDict['id']))
            del tmpDict['_id']
            ret.append(tmpDict)
        return ret

    @classmethod
    def get_bkstz(cls, id):
        if not cls.__inited:
            cls.__init_cls__()
        item = cls.coll.find_one({"_id": ObjectId(id)})
        if item is not None:
            item['id'] = str(item['_id'])
            del item['_id']
            return item

