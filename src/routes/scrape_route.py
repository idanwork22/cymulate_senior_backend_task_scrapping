import threading
from datetime import datetime

from src.base import LoguruLogger, Config

from fastapi import APIRouter, HTTPException

from src.classes import Scraper
from src.core.validation import ScrapeRequest

logger = LoguruLogger(__name__).get_logger()
scrape_api_config = Config().get_value('APIRoutes', 'Scrape')

router = APIRouter(prefix=scrape_api_config['prefix'],
                   tags=[scrape_api_config['tag']])


@router.post(scrape_api_config['routes']['Post']['StartScraping'], status_code=200)
async def start_scraping(request: ScrapeRequest):
    scraper = Scraper(request.url)
    scraper.save_initial_record()
    threading.Thread(target=start_scraping, args=(scraper,)).start()

    return {"scrape_id": str(scraper.scrape_id), "status": "in process"}


@router.get(scrape_api_config['routes']['Get']['GetAllScrapes'])
async def get_all_scrapes():
    raise NotImplementedError
