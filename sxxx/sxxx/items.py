# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SxxxItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    item_type = 'SxxxItem'
    account = scrapy.Field()
    class_number = scrapy.Field()
    course_number = scrapy.Field()
    class_name = scrapy.Field()
    credit = scrapy.Field()
    required = scrapy.Field()
    grade = scrapy.Field()
    reason = scrapy.Field()

class KbItem(scrapy.Item):
    item_type = 'KbItem'
    account = scrapy.Field()
    class_number = scrapy.Field()
    course_number = scrapy.Field()
    class_name = scrapy.Field()
    credit = scrapy.Field()
    required = scrapy.Field()
    teacher = scrapy.Field()
    time = scrapy.Field()

class SignalItem(scrapy.Item):
    item_type = 'SignalItem'
    account = scrapy.Field()
    signal = scrapy.Field()