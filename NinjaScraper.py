import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

class NinjaScraper(scrapy.Spider):
    name = "doj-website"

    def start_requests(self):
        urls = [
            "https://doj.gov.in/",
        ]
        for url in urls:
            yield scrapy.Request(url = url, callback = self.parse_request)

    def parse_request(self, response):
        filename = "output.txt"
        with open(filename, 'w') as file:
            file.write(response.text)
        print(response)
        self.logger.info(f"Saved file {filename}")

def init_crawler():
    crawler = CrawlerProcess(get_project_settings())
    crawler.crawl(NinjaScraper)
    crawler.start()
