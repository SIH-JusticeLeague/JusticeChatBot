import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.item import Item, Field
from urllib.parse import urlparse
from llama_index.core.schema import Document

class NinjaScraper(scrapy.Spider):
    name = 'ninja-scraper'
    start_urls = ['https://doj.gov.in/']
    doc_list = list()

    def __init__(self, *args, **kwargs):
        super(NinjaScraper, self).__init__(*args, **kwargs)
        self.file = open('output.txt', 'w', encoding='utf-8')
        self.allowed_domain = urlparse(self.start_urls[0]).netloc
    
    def parse(self, response):
        # HTML tag parsing
        title = response.xpath('//title/text()').get()
        text = response.xpath('//main//p/text()').getall()

        # Write to file
        doc = Document()
        doc.text = " ".join(text) 
        doc.metadata = { 
            "url" : "site name",
            "title": title,
        }
        doc.id_ = "site name"
        self.file.writelines(str(doc) + '\n') 
        # self.doc_list.append(doc)

        # Follow links within domain
        # self.file.write('Links: \n' + str(response.css('a::attr(href)').getall())) # Debug links
        for href in response.css('a::attr(href)').getall():
            next_page = response.urljoin(href)
            if self.is_internal_link(next_page):
                yield scrapy.Request(next_page, callback=self.parse)
        
        # Logger
        self.logger.info('Successfully Scraped!')

    def is_internal_link(self, url):
        parsed_url = urlparse(url)
        return parsed_url.netloc == self.allowed_domain

    def close(self, reason):
        print(f'File Closed: {reason}')
        self.file.close()

# class StructureData(Item):
#     metadata = Field()
#     content = Field()
        
def start_crawler():
    crawler = CrawlerProcess(get_project_settings())
    crawler.crawl(NinjaScraper)
    crawler.start()
