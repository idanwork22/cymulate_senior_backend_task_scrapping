# scraper.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import requests
import pymongo
from datetime import datetime
from bson.objectid import ObjectId

from src.base import LoguruLogger
from src.data_access.mongo_class import MongoDBClient

app = FastAPI()

client = pymongo.MongoClient("mongodb://mongodb:27017/")
db = client.scraping_db
collection = db.results


class Scraper:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.urls = []
        self.scrape_id = None
        self.logger = LoguruLogger(__name__).get_logger()
        self.mongo_class = MongoDBClient(
            connection_string="mongodb://localhost:27017",
            database_name="cymulate_db",
            collection_name="cymulate_collection"
        )

    def scrape_website(self):
        response = requests.get(self.base_url)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to retrieve the website")

        soup = BeautifulSoup(response.text, 'html.parser')

        for link in soup.find_all('a', href=True):
            href = link['href']
            parsed_url = urlparse(href)
            if parsed_url.scheme and parsed_url.netloc:
                self.urls.append(href)
            else:
                self.urls.append(urlparse(self.base_url).scheme + "://" + urlparse(self.base_url).netloc + href)

    def save_initial_record(self):
        self.scrape_id = self.mongo_class.insert_document({
            "base_url": self.base_url,
            "execution_time": datetime.utcnow(),
            "list_of_urls": [],
            "status": "in process"
        }).inserted_id

    def update_record(self):
        self.mongo_class.update_document(query=
                                         {"_id": self.scrape_id},
                                         new_values=
                                         {"$set": {
                                             "list_of_urls": self.urls,
                                             "status": "finished"
                                         }})
