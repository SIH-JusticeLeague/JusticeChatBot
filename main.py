
# Logging
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# Setup environment
from dotenv import load_dotenv
load_dotenv()

# Scraper
from NinjaScraper import start_crawler

if __name__ == "__main__":
    start_crawler()
