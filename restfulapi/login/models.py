#coding=utf-8
from __future__ import unicode_literals
from django.utils.crypto import get_random_string
from django.db import models
from urllib2 import Request, urlopen
from urllib import urlencode
import redis
import datetime
# Create your models here.

def crawl_request(account, password):
    #这边暂时先hardcode了
    req = Request(url="http://localhost:6800/schedule.json")
    data = urlencode({"account": account, "password": password, "project": "sxxx", "spider": "xskb"})
    response = urlopen(req, data=data)
    if response.getcode() == 200:
        return True
    else:
        return False

class Login:
    db = None
    __inited = False
    @classmethod
    def __init_cls__(cls):
        cls.db = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
        __inited = True
    @classmethod
    def verify_user(cls, account, password):
        if not cls.__inited:
            cls.__init_cls__()
        #account 与 password的有效性应在上一层验证
        #TODO: 尝试在这个层面防一下暴力破解?
        ori_pass = cls.db.hget("account", account)
        state = cls.db.hgetall("info_" + account)
        if ori_pass is None:
            cls.db.hset("account", account, password)
            cls.db.hmset(account, {"state": "pending", "wrong": 0})
            crawl_request(account, password)
            return "PENDING"
        elif ori_pass != password:
            verified_key = get_random_string(64)
            cls.db.hset("verified_account", account, verified_key)
        elif ori_pass == password:
            return state[2]

    #懒得写了
    @classmethod
    def get_kb(cls, account, verified_key):
        pass

    @classmethod
    def get_grade(cls, account, verified_key):
        pass




