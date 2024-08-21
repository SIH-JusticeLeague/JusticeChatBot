import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

class NinjaScraper(scrapy.Spider):
    name = 'ninja-scraper'
    start_urls = ['https://doj.gov.in/']

    def __init__(self, *args, **kwargs):
        super(NinjaScraper, self).__init__(*args, **kwargs)
        self.file = open('output.txt', 'w', encoding='utf-8')
    
    def parse(self, response):
        # HTML tag parsing
        title = response.xpath('//title/text()').get()
        paragraphs = response.css('p::text').getall()

        # Write to file
        self.file.write(f'Title: {title}\n')
        self.file.write('Paragraphs:\n')
        self.file.write('\n'.join(paragraphs))
        self.file.write('\n\n')

        # Follow links
        self.file.write('Links: \n' + str(response.css('a::attr(href)').getall()))
        for href in response.css('a::attr(href)').getall():
            next_page = response.urljoin(href)
            if next_page.startswith('http'):
                yield scrapy.Request(next_page, callback=self.parse)
        
        # Logger
        self.logger.info('Successfully Scraped!')

    def close(self, reason):
        print(f'File Closed: {reason}')
        self.file.close()

def start_crawler():
    crawler = CrawlerProcess(get_project_settings())
    crawler.crawl(NinjaScraper)
    crawler.start()
