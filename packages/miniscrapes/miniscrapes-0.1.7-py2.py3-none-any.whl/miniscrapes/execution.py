from typing import Callable
from typing import Dict

from miniscrapes.scrapers import airnow_air_quality
from miniscrapes.scrapers import nyt_covid
from miniscrapes.scrapers import weather


SCRAPERS: Dict[str, Callable] = {
    'nyt_covid': nyt_covid,
    'weather': weather,
    'airnow_air_quality': airnow_air_quality
}


def run_scrapers(scrapers: Dict[str, dict]):
    results = {}
    for slug, scraper in scrapers.items():
        scraper_slug: str = scraper['scraper']
        kwargs: dict = scraper['args']
        results[slug] = SCRAPERS[scraper_slug](**kwargs)

    return results
