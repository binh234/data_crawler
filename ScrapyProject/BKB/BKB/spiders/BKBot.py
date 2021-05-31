import scrapy
from BKB.items import BkbItem
import os
from scrapy import Request
from scrapy.linkextractors import LinkExtractor
import re
import urllib
import requests
from pathlib import Path

ext = 'htm'
count = 0
class BkbotSpider(scrapy.Spider):
    name = 'BKBot'
    allowed_domains = ['dantri.com.vn']
    # allowed_domains = list(map(get_host_name,allowed_domains))
    start_urls = ['https://dantri.com.vn/']

    def parse(self, response):
        try:
            for target in response.xpath('//body').re(r'http[s]?://[a-zA-Z0-9-\._~/?#@&=]*\.'+ext):
                yield Request(target,callback=self.download)


            for href in response.xpath('//a/@href').extract():
                if not (href.startswith('http') or href.startswith('/')): continue
                yield response.follow(href,callback=self.parse)
        except Exception as e:
            print(e)
            input()
            pass

    def download(self,response):
        global count
        try:
            title = '{}_{}.{}'.format(response.css('title::text').get(),ext)
        except:
            # title = 'Noname_{}.{}'.format(count,ext)
            title = '{}.{}'.format(response.url.split('/')[-1],ext)
            count += 1
        filename = Path(os.path.join('Crawled',title))
        print('Saving to {}...'.format(filename))
        filename.write_bytes(response.body)
        

