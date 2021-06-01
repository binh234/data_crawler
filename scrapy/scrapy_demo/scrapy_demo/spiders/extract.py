import re
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
import scrapy
from scrapy.http import Request
from scrapy_selenium import SeleniumRequest
import os
from urllib.parse import urlparse, urljoin
from lxml.html import iterlinks, resolve_base_href
import validators
import datetime


from .helper import get_extension
from ..items import CrawlItem

URL_REGEX = re.compile(
	r'\b((?:(ht|f)tps?:\/\/)'
	r'(?:(?:www\.)?(?:[\da-z\.-]+)\.(?:[a-z]{2,6})|'
	r'(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|'
	r'(?:(?:[0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:(?:(?::[0-9a-fA-F]{1,4}){1,6})|:(?:(?::[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(?::[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(?:ffff(?::0{1,4}){0,1}:){0,1}(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])|(?:[0-9a-fA-F]{1,4}:){1,4}:(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])))(?::[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])?'
	r'(?:\/[\w \.-]*)*\/?)\b'
	, re.IGNORECASE)
BASE_DIR = os.path.join(os.getcwd(), "result/")


def extract_list(value):
    if isinstance(value, list):
        return value
    return value.replace(" ", "").split(",")

class ExtractSpider(scrapy.Spider):
    name = "extractor"
    start_urls = [
        # 'https://truyentranhaudio.online/manga-slug/dua-mami-ve-nha/',
        # 'https://truyentranhaudio.online/manga-slug/toi-tu-dong-san-mot-minh/chap-86/',
        # 'https://www.daimler.com/investors/reports-news/annual-reports/',
        # 'http://truyenqq.com',
        # 'http://truyenqq.com/truyen-tranh/vua-choi-da-co-tai-khoan-vuong-gia-10552',
        # 'https://vingroup.net/quan-he-co-dong/bao-cao-tai-chinh/2020',
        # 'https://www.coolfreecv.com/',
        # 'https://www.resumeviking.com/templates/word/',
        # "https://zingmp3.vn",
        # "https://tailieu.vn/",
        # "https://www.tailieu123.org/",
        "https://www.tailieu123.org/giai-bai-tap-hoa-lop-9-protein.html"
    ]

    custom_settings = {
        'FEED_EXPORT_FIELDS': ['name', 'url', 'extension', 'time'],
    }

    def __init__(self, *args, **kwargs):
        super(ExtractSpider, self).__init__(*args, **kwargs)
        self.start_urls = extract_list(kwargs.get("urls", []))
        self.extensions = extract_list(kwargs.get("ext", [".pdf"]))
        self.save_enable = kwargs.get("save", False)

        self.output_dir = kwargs.get("output", BASE_DIR)
        # print(kwargs)

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        # driver = response.request.meta['driver']
        # self.logger.info("Crawl " + response.url)

        ext = get_extension(response)
        url = response.url if response.url[-1] != '/' else response.url[:-1]
        name = url.split("?")[0].split("/")[-1]
        name = name.replace(ext, '') + ext
        crawl_time = datetime.datetime.now()
        check_ext = ext in self.extensions
        prev_url = kwargs.get("prev_url", None)

        if check_ext and self.save_enable:
            self.save_item(name, response, prev_url)
        
        loader = ItemLoader(item=CrawlItem())
        loader.add_value('name', name)
        loader.add_value('url', url)
        loader.add_value('extension', ext[1:])
        loader.add_value('time', crawl_time.strftime("%d-%m-%Y %H:%M:%S"))

        yield loader.load_item()

        
        if hasattr(response, "text"):  # HTML page
            links = []
            # Extract links
            for link in re.findall(URL_REGEX, response.text):
                links.append(response.urljoin(link[0]))

            links.extend([response.urljoin(link) for element, attribute, link, pos in iterlinks(resolve_base_href(response.text))])
            links = set(links)
            links = list(filter(lambda link: validators.url(link), links))
            self.logger.info("Found {} links on {}".format(len(links), url))
            for link in links:
                # print(link)
                yield Request(
                    url=link,
                    callback=self.parse,
                    cb_kwargs=dict(prev_url=response.url)
                )

    def save_item(self, name, response, prev_url):
        if prev_url:
            result = urlparse(prev_url)
            directory = result.path[1:].split(".")[0]
            output_dir = os.path.join(self.output_dir, directory)
        else:
            output_dir = self.output_dir

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        path = os.path.join(output_dir, name)

        self.logger.info("Saving file to %s" % path)
        with open(path, "wb") as f:
            f.write(response.body)