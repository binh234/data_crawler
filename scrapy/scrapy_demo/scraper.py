from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy_demo.scrapy_demo.spiders.extract import ExtractSpider
import os
import pathlib

class Scraper:
    def __init__(self, log_path, depth=1):
        settings_file_path = 'scrapy_demo.settings' # The path seen from root, ie. from main.py
        os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
        self.settings = get_project_settings()

        log_format = log_path.split('.')[-1]
        self.settings.update({
			'DEPTH_LIMIT': depth,
			'ROBOTSTXT_OBEY': True,
            'DOWNLOAD_DELAY': 0.5,
            'FEEDS': {
                log_path: {
                    'format': log_format,
                    'fields': ['name','url', 'extension', 'time'],
                    'overwrite': True
                }
            }
        })
        self.process = CrawlerProcess(self.settings)
        self.spider = ExtractSpider # The spider you want to crawl

    def crawl(self, url_list, extensions=[".pdf"], output_dir=None):
        self.process.crawl(self.spider, urls=url_list, ext=extensions, 
        	output=output_dir)
        self.process.start()  # the script will block here until the crawling is finished