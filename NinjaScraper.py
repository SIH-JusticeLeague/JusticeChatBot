import scrapy
from scrapy.crawler import CrawlerProcess

class NinjaScraper(scrapy.Spider):
    name = "doj-website"

    def startRequest(self):
        urls = [
            "doj.gov.in",
        ]
        for url in urls:
            yield scrapy.Request(url = url, callback = self.parseRequest)

    def parseRequest(self, response):
        filename = "output.txt"
        with open(filename, 'wb') as file:
            file.write(response.body)
        print(response)
        self.log(f"Saved file {filename}")

def initCrawler():
    crawler = CrawlerProcess()
    crawler.crawl(NinjaScraper)
    crawler.start()
