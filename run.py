#coding=utf-8
from scrapy import cmdline
import os

if __name__ == '__main__':
    os.chdir('sxxx')
    cmdline.execute("scrapy crawl xskb".split())