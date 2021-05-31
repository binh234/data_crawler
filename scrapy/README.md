# scrapy

## Clone project
```bash
git clone https://github.com/binh234/scrapy.git

cd  scrapy
```

## Install reuired library
```bash
python -m pip install -r requirements.txt
```

## Usage Example
After having installed required library, you can use this project in 2 ways:

### Using CLI
```bash
python main.py [-h] [-t [TEXT [TEXT ...]]] [-i [IMG [IMG ...]]] [-d DEPTH]
               [-o OUTPUT]
               urls [urls ...]
```

Example:
```bash
python main.py https://www.coolfreecv.com/ -t .docx -d 1 -o result/
```
#### Parameters

<ul>
<li><b>urls</b> - start urls to crawl</li>
<li><b>text</b> - text file extensions (.pdf, .doc, .docx, .txt, .csv, ...). Default is .pdf</li>
<li><b>img</b> - image file extensions (.jpg, .png, .jpeg, .gif, .svg, ...). Default is empty</li>
<li><b>depth</b> - max crawling depth. Default is 1</li>
<li><b>output</b> - the directory where the files should be saved. Default is the <italic>result</italic> directory of the current directory  </li>
</ul>

### Using class
You can import the Scraper class in the following way:
```python
from scraper import Scraper

scraper = Scraper(depth=1)					# Max crawling depth
scraper.crawl(
	url_list=["https://www.coolfreecv.com/", 	        # Start urls to crawl
	"https://www.resumeviking.com/templates/word/"], 
	txt_extensions=[".docx", ".doc"],	                # Text file extensions (.pdf, .docx, ...)
	img_extensions=[".jpg"],				# Image file extensions (.jpg, .png, ...)
	output_dir="D:/scala/"					# Output directory
	)
```
