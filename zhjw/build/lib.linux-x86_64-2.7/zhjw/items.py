# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhjwItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class XszzListItem(scrapy.Item):
    item_type = 'XszzListItem'
    index_id = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    time = scrapy.Field()
    detail_url = scrapy.Field()
    crawl_time = scrapy.Field()

class XszzContentItem(scrapy.Item):
    item_type = 'XszzContentItem'
    index_id = scrapy.Field()
    html_content = scrapy.Field()
    downloads = scrapy.Field()
