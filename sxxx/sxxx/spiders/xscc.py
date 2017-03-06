# -*- coding: utf-8 -*-
import scrapy


class XsccSpider(scrapy.Spider):
    name = "xscc"
    allowed_domains = ["http://zhjw.dlut.edu.cn/"]
    start_urls = (
        'http://www.http://zhjw.dlut.edu.cn//',
    )

    def parse(self, response):
        pass
