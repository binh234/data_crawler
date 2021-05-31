from scrapy_demo import Scraper

scraper = Scraper(log_path='log.csv', depth=1)								# Max crawling depth
scraper.crawl(	
	url_list=["https://www.coolfreecv.com/", 			# Start urls to crawl
	"https://www.resumeviking.com/templates/word/"], 
	extensions=[".docx", ".doc"],					# Text file extensions (.pdf, .docx, ...)
	output_dir="D:/scala/"								# Output directory
	)