from scrapy_demo.scraper import Scraper
import os
import argparse

BASE_DIR = os.path.join(os.getcwd(), "result")
LOG_PATH = "log.csv"

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('urls', nargs='+',
                    help='start urls to crawl')
	parser.add_argument('-e', '--ext', nargs='*', default=[".pdf"],
                    help='file extensions (.pdf, .doc, .docx, .txt, .csv, .jpg, ...)')
	parser.add_argument("-d", "--depth", default=1, type=int, help='crawling depth')
	parser.add_argument("-s", "--save", default=True, action="store_true", help='saving files to output directory')
	parser.add_argument("-o", "--output", default=BASE_DIR, help='output directory')
	parser.add_argument("-l", "--log", default=LOG_PATH, help='log file path (csv or json file)')
	args = parser.parse_args()
	# print(vars(args))

	scraper = Scraper(log_path=args.log, depth=args.depth)						# Max crawling depth
	scraper.crawl(	
		url_list=args.urls, 
		extensions=args.ext,								# Text file extensions (.pdf, .docx, ...)
		save=args.save,
		output_dir=args.output								# Output directory
	)

