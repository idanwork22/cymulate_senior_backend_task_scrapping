# scraper.py
from fastapi import FastAPI, HTTPException
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import requests
import pymongo
from datetime import datetime

from src.base import LoguruLogger
from src.core.validation import ScrapeResponse
from src.data_access.mongo_class import MongoDBClient

app = FastAPI()

client = pymongo.MongoClient("mongodb://mongodb:27017/")
db = client.scraping_db
collection = db.results


class Scraper:
    def __init__(self):
        self.logger = LoguruLogger(__name__).get_logger()
        self.mongo_class = MongoDBClient(
            connection_string="mongodb://localhost:27017",
            database_name="cymulate_db",
            collection_name="cymulate_collection"
        )

    def scrape_website(self, base_url, scrape_id):
        urls = []
        response = requests.get(base_url)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to retrieve the website")

        soup = BeautifulSoup(response.text, 'html.parser')

        for link in soup.find_all('a', href=True):
            href = link['href']
            parsed_url = urlparse(href)
            if parsed_url.scheme and parsed_url.netloc:
                urls.append(href)
            else:
                urls.append(urlparse(base_url).scheme + "://" + urlparse(base_url).netloc + href)
        self.update_record(scrape_id=scrape_id, urls=urls)

    def save_initial_record(self, base_url):
        doc_id = str(hash(base_url+str(datetime.now())))
        scrape_id = self.mongo_class.insert_document({
            "_id": doc_id,
            "base_url": base_url,
            "execution_time": datetime.utcnow(),
            "list_of_urls": [],
            "status": "in process"
        })
        return doc_id

    def update_record(self, scrape_id, urls):
        self.mongo_class.update_document(query=
                                         {"_id": scrape_id},
                                         new_values=
                                         {"$set": {
                                             "list_of_urls": urls,
                                             "status": "finished"
                                         }})

    def get_all_scrapers_from_db(self):
        result = self.mongo_class.get_all_documents()
        for res in result:
            res['_id'] = str(res['_id'])
        return result
