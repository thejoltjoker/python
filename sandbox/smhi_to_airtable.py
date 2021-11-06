#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
script_name.py
Description of script_name.py.
"""
import os
import requests
import random
import lxml
from bs4 import BeautifulSoup
from airtable import Airtable
from scraping import USER_AGENTS
import logging


def insert(weathers):
    table = Airtable(table_name='weather2', base_key=os.getenv('SMHI_A_BASE'), api_key=os.getenv('SMHI_A_KEY'))
    for w in weathers:
        record = table.insert(w, typecast=True)
        logging.debug(record)
        # table.update('weather',record)


def scrape():
    """Download all items from urls"""
    url = 'https://www.smhi.se/kunskapsbanken/meteorologi/vad-betyder-smhis-vadersymboler-1.12109'
    headers = {
        'User-Agent': random.choice(USER_AGENTS)
    }
    # Get site
    response = requests.get(url, headers=headers)

    # Parse html
    logging.info(response)
    soup = BeautifulSoup(response.text, 'lxml')

    parent = soup.find("div", class_="paragraphs")
    logging.debug(parent)

    headings = parent.find_all('h2')
    pictures = parent.find_all('img')
    descriptions = parent.find_all('p')
    descriptions.pop(0)

    logging.info(f'{len(headings)} headings')
    logging.info(f'{len(pictures)} pictures')
    logging.info(f'{len(descriptions)} descriptions')

    weathers = []
    for n, h in enumerate(headings):
        w = {
            'name': h.text,
            'symbol': f'https://www.smhi.se{pictures[n]["src"]}',
            'description': descriptions[n].text
        }
        weathers.append(w)
    logging.info(weathers)
    return weathers


def main():
    """docstring for main"""
    w = scrape()
    insert(w)


if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    main()
