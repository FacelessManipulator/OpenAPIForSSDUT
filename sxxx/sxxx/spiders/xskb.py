# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from ..items import SxxxItem, KbItem, SignalItem
import re

class XskbSpider(scrapy.Spider):
    name = "xskb"
    allowed_domains = ["http://zhjw.dlut.edu.cn/"]
    start_urls = (
        'http://zhjw.dlut.edu.cn/',
    )
    login_url = 'http://zhjw.dlut.edu.cn/loginAction.do'
    grade_url = 'http://zhjw.dlut.edu.cn/gradeLnAllAction.do?type=ln&oper=sxinfo&lnsxdm=001'
    class_url = 'http://zhjw.dlut.edu.cn/xkAction.do?actionType=6'
    header = {'Host': 'zhjw.dlut.edu.cn',
            'Origin': 'http://zhjw.dlut.edu.cn',
            'Referer': 'http://zhjw.dlut.edu.cn/loginAction.do',
              }

    # def start_requests(self):
    #     while self.fetch_list is not None and len(self.fetch_list) > 0:
    #         yield Request(url=self.login_url, callback=self.parse_login)

    def start_requests(self):
        while self.fetch_list is not None and len(self.fetch_list) > 0:
            try:
                student = self.fetch_list.pop()
            except IndexError, e:
                self.close(self, "list is empty")
            # yield scrapy.FormRequest.from_response(
            #     response,
            #     formdata={'zjh': student['account'], 'mm': student['password']},
            #     callback=self.after_login
            # )
            yield scrapy.FormRequest(url=self.login_url,
                                     callback=self.after_login,
                                     formdata={'zjh': student['account'], 'mm': student['password']},
                                     encoding='gb2312',
                                     meta={'account': student['account']},
                                     )

    def after_login(self, response):
        if response.xpath("//title/text()").extract()[0].startswith("URP"):
            item = SignalItem()
            item['account'] = response.meta['account']
            item['signal'] = "ERROR_PASSWORD"
            yield item
        else:
            yield Request(url=self.grade_url, callback=self.parse_grade, meta={'account': response.meta['account']})
            yield Request(url=self.class_url, callback=self.parse_class, meta={'account': response.meta['account']})

    def parse_grade(self, response):
        trs = response.xpath("//tr[@class='odd']")
        for tr in trs:
            item = SxxxItem()
            try:
                tds = tr.xpath("td//text()").extract()
                item['class_number'] = tds[0].strip()
                item['course_number'] = tds[1].strip()
                item['class_name'] = tds[2].strip()
                item['credit'] = tds[4].strip()
                item['required'] = tds[5].strip()
                item['grade'] = tds[7].strip()
                item['reason'] = tds[9].strip()
                item['account'] = response.meta['account']
            except IndexError, e:
                self.logger.info(e.message)
            yield item

    def parse_class(self, response):
        trs = response.xpath("//table[@class='displayTag']")[1].xpath("tr")
        item = None  #这行只是为了防止warning
        for tr in trs:
            tds = tr.xpath("td/text()").extract()
            if len(tds) > 17:
                if item is not None:
                    yield item
                item = KbItem()
                item['account'] = response.meta['account']
                item['class_number'] = tds[1].strip()
                item['class_name'] = tds[2].strip()
                item['course_number'] = tds[3].strip()
                item['credit'] = tds[4].strip()
                item['required'] = tds[5].strip()
                item['teacher'] = tds[7].strip()
                item['time'] = []
                time_index_base = 11
            else:
                time_index_base = 0
            #将格式为"1-8,10-17周上"转化为"1,2,3,4,5,6,7,8,10,11,12,13,14,15,16,17"
            week = re.sub("(\d*)-(\d*)",
                   lambda obj:','.join([str(i) for i in range(int(obj.groups()[0]),int(obj.groups()[1])+1,1)]),
                   re.sub('[^\d\-\,]','',tds[0+time_index_base].strip()))
            time = {'week':  week,
                    'weekday': tds[1+time_index_base].strip(),
                    'section': tds[2+time_index_base].strip(),
                    'section_count': tds[3+time_index_base].strip(),
                    'campus': tds[4+time_index_base].strip(),
                    'building': tds[5+time_index_base].strip(),
                    'classroom': tds[6+time_index_base].strip(),
                    }
            item['time'].append(time)
        yield item
