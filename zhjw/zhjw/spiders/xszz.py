# -*- coding: utf-8 -*-
import scrapy
from ..pipelines import TestPrintPipeline
from scrapy import Request
from ..items import XszzListItem, XszzContentItem
import re


class XszzSpider(scrapy.Spider):
    name = "xszz"
    allowed_domains = ["ssdut.dlut.edu.cn"]
    start_urls = (
        'http://ssdut.dlut.edu.cn/index/bkstz.htm',
    )

    def start_requests(self):
        yield Request('http://ssdut.dlut.edu.cn/index/bkstz.htm', self.parse)

    def parse(self, response):
        for sel in response.xpath("//a[contains(@href,'../info/')]"):
            item = XszzListItem()
            temp = sel.xpath("@href").extract()[0]
            item['url'] = 'http://ssdut.dlut.edu.cn/' + temp.replace('../', '')
            # item['index_id'] = item['url'][30:34] + item['url'][35:39]
            item['index_id'] = re.sub("\D", "", item['url'])
            item['title'] = sel.xpath("@title").extract()[0].strip()
            temp = sel.xpath("following-sibling::*[1]/text()").extract()[0]
            item['time'] = temp.strip()
            yield item
            yield Request(item['url'],  self.parse_content)
        next_link = response.xpath("//a[@class='Next']/@href | //a[@class='Prev']/@href").extract()
        for link in next_link:
            link = link.replace('bkstz/', '')
            yield Request('http://ssdut.dlut.edu.cn/index/bkstz/'+link,  self.parse)

    def parse_content(self, response):
        item = XszzContentItem()
        item['index_id'] = re.sub("\D", "", response.url)
        item['html_content'] = response.xpath("//div[contains(@id,'vsb_content')]").extract()[0]
        item['downloads'] = []
        for li in response.xpath("//div[contains(@id,'vsb_content')]/following-sibling::ul/li"):
            item['downloads'].append({'doc_name':li.xpath("a/text()").extract()[0],
                                      'doc_url':'http://ssdut.dlut.edu.cn/'+li.xpath("a/@href").extract()[0]})
        #info['downloads'] = json.dumps(temp)
        yield item

