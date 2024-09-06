import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from urllib.parse import urlparse
from llama_index.core.schema import Document
from llama_index.readers.pdf_marker import PDFMarkerReader
import os
import pickle
from pathlib import Path

FILE = os.path.join(os.getcwd(), "scrapped-data", "doc-bin")
print(FILE)

class NinjaScraper(scrapy.Spider):
    name = 'ninja-scraper'
    start_urls = [
            'https://doj.gov.in/',
            'https://cdnbbsr.s3waas.gov.in/'
                  ]

    def __init__(self, *args, **kwargs):
        super(NinjaScraper, self).__init__(*args, **kwargs)

        os.system(f"mkdir -p {FILE}")

        # making temp folder to save pdf
        self.tempPath = os.path.join(FILE,"tempPath")
        os.system(f"mkdir -p {self.tempPath}")

        # for out of domain check
        self.allowed_domain = [urlparse(site).netloc for site in self.start_urls]

        # PDF reader init
        self.pdf_reader = PDFMarkerReader()


    # pickle to directory
    def save_doc (self, doc : Document, suffix : str) -> None:
        with open(os.path.join(FILE, f"{doc.id_}{suffix}"), "wb") as file : 
            pickle.dump(doc,file)
        return None
    

    # to download pdf
    def save_pdf (self, url : str) -> str | None: 
        name = url.split('/')[-1]
        if (name.split(".")[-1] == "pdf") : os.system(f"wget {url} -P {self.tempPath}")
        else:
            return None
        return name


    # parse pdf pages
    def parse_pdf (self, response) -> None:
        site_url = str(response).split()[1][:-1]

        name = self.save_pdf(site_url)
        if name is not None : 
            path = Path(os.path.join(self.tempPath, name))
            doc = self.pdf_reader.load_data(path)[0]
            doc.metadata = { 
                "url" : site_url,
                "title": name,
            }
            doc.id_ = name
            self.save_doc(doc,"_md")

        return None


    # parse html pages 
    def parse_url (self, response) -> None:
        site_url = str(response).split()[1][:-1]

        title = response.xpath('//title/text()').get() 
        title = " ".join(str(title).split("|")[:-2]) 

        text = response.xpath("//main//div[@class='container' and @id='row-content']//p//text() | //main//div[@class='container' and @id='row-content']//li//text()").getall()

        doc = Document()
        doc.text = " ".join(text) 
        doc.metadata = { 
            "url" : site_url,
            "title": title,
        }
        doc.id_ = title
        self.save_doc(doc,"_html")
        return None
    

    # call back to in-domain url's  
    def parse(self, response, *args, **kwargs):
        site_url = str(response).split()[1][:-1]
        
        if urlparse(site_url).netloc == self.allowed_domain[0] : # url 
            self.parse_url(response)
        else : # pdf 
            self.parse_pdf(response)


        # Follow links within domain
        # self.file.write('Links: \n' + str(response.css('a::attr(href)').getall())) # Debug links
        for href in response.css('a::attr(href)').getall():
            next_page = response.urljoin(href)
            if self.is_internal_link(next_page):
                yield scrapy.Request(next_page, callback=self.parse)
        
        # Logger
        self.logger.info('Successfully Scraped!')


    # in domain checker 
    def is_internal_link(self, url):
        parsed_url = urlparse(url)
        return parsed_url.netloc in self.allowed_domain


    # terminating 
    def close(self, *arg, **kwargs):
        print(f'File Closed: {arg}\n{kwargs}')
        os.system(f"rm -rf {self.tempPath}")


        
def start_crawler():
    crawler = CrawlerProcess(get_project_settings())
    crawler.crawl(NinjaScraper)
    crawler.start()


if __name__ == "__main__":
    start_crawler()
