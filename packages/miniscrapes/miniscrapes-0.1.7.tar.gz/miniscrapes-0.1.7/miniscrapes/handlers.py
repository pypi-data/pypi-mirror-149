import dpath.util
import logging
import os
import requests

from typing import Callable
from typing import Dict
from typing import List
from typing import Tuple


logger = logging.getLogger(__name__)
MAILGUN_KEY = os.getenv('MAILGUN_KEY')
MAILGUN_OUTGOING_DOMAIN = os.getenv('MAILGUN_OUTGOING_DOMAIN')


def format_temperature(temp: dict):
    return f"{round(temp['temp'])} (Feels like {round(temp['feels_like'])})"


def format_air_quality(quality: dict):
    return f"{quality['index']} ({quality['category']})"


EXTRACTORS: Dict[str, Tuple[Tuple[str, str, Callable], ...]] = {
    'weather': (
        ('Morning', 'today/morning', format_temperature),
        ('Daytime', 'today/day', format_temperature),
        ('Evening', 'today/evening', format_temperature),
        ('Night', 'today/night', format_temperature),
        ('UV index', 'today/uvi', lambda x: round(x)),
        ('Weather', 'today/description', lambda x: x)),
    'nyt_covid': (
        ('Cases per 100K',
         'cases_avg_per_100k', lambda x: round(x)),
        # Helps identify whether the data source is stale.
        ('Latest date', 'date', lambda x: x)),
    'airnow_air_quality': (
        ('PM2.5', 'pm25', format_air_quality),
        ('Ozone', 'ozone', format_air_quality))
}


def send_simple_message(to: str, subject: str, text: str):
    requests.post(
        f'https://api.mailgun.net/v3/{MAILGUN_OUTGOING_DOMAIN}/messages',
        auth=('api', MAILGUN_KEY),
        data={
            'from': 'Miniscrapes daily email <marcua@marcua.net>',
            'to': [to],
            'subject': subject,
            'text': text}).raise_for_status()


def _extract_result(scrape: str, results: dict,
                    extractors: Tuple[Tuple[str, str, Callable], ...]) -> str:
    extracted_list: List[str] = []
    for description, path, formatter in extractors:
        try:
            formatted = formatter(dpath.util.get(results, path))
        except Exception:
            formatted = '***Error formatting result***'
            logger.exception('Error formatting result')
        extracted_list.append(f'  * {description}: {formatted}')
    extracted = '\n'.join(extracted_list)
    formatted_results = f'{scrape}\n{extracted}'
    return formatted_results


def email_results(to: str, subject: str,
                  scrapers: Dict[str, dict], results: dict):
    extracted = '\n\n'.join(
        _extract_result(
            scraper_config['name'],
            results[scraper_slug],
            EXTRACTORS[scraper_config['extractor']])
        for scraper_slug, scraper_config
        in scrapers.items())
    text = f'Good morning! Here are your miniscrapes!\n\n{extracted}'
    send_simple_message(to, subject, text)
