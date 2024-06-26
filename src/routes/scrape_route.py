from datetime import datetime
from src.base import LoguruLogger, Config

from fastapi import APIRouter

from src.core.validation import ScrapeRequest

logger = LoguruLogger(__name__).get_logger()
scrape_api_config = Config().get_value('APIRoutes', 'Scrape')

router = APIRouter(prefix=scrape_api_config['prefix'],
                   tags=[scrape_api_config['tag']])


@router.post(scrape_api_config['routes']['Post']['StartScraping'])
async def start_scraping(request: ScrapeRequest):
    raise NotImplementedError


@router.get(scrape_api_config['routes']['Get']['GetAllScrapes'])
async def get_all_scrapes():
    raise NotImplementedError
