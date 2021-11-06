#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
script_name.py
Scrapes wikipedia for swedish birds and creates a lightroom keyword list.
"""
import sqlite3
import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
from pathlib import Path
from pprint import pprint
import string
import re
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Sport:
    def __init__(self, name, category=None, sub_category=None):
        self.name = name
        self.category = category
        self.sub_category = sub_category

class BirdScraper:
    def __init__(self):
        self.birdlist = []

    def print(self):
        print(f"{sum(len(y) for x, y in self.birdlist)} fåglar och {len([x for x in self.birdlist])} familjer")
        for family, birds in self.birdlist:
            print(f"Familj: {family.swedish_name} (latin: {family.latin_name}, engelska: {family.english_name})")
            for bird in birds:
                print(f"  - {bird.swedish_name} (latin: {bird.latin_name}, engelska: {bird.english_name})")

    def get_english_name(self, url):
        """Get the english name for the bird"""
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        for i in soup.find_all("li", class_="interwiki-en"):
            english_name = i.a.get('title').replace(" – engelska", "").lower()
            return english_name

    def get_birds(self):
        """docstring for main"""
        response = requests.get("https://sv.wikipedia.org/wiki/Lista_%C3%B6ver_f%C3%A5glar_i_Sverige")
        html = response.text
        # html = Path("/Users/johannes/Desktop/birds.html").open("r")
        soup = BeautifulSoup(html, 'html.parser')

        # Find all families and go through them
        h2 = soup.find_all("h2")

        for n, i in enumerate(h2):
            print("")
            if "Innehåll" in i.text:
                continue
            elif "Se även" in i.text:
                break

            # Sort family
            family = i.next_element.next_element.text
            family_url = i.next_element.next_element.a.get("href")
            family_swedish, family_latin = family.lower().split("(")
            family_latin = family_latin.strip(" ()")
            family_english = self.get_english_name(family_url)
            print(f"Familj: {family_swedish.title()}")
            # Birds
            birds = []
            ul = i.next_sibling.next_sibling

            # Iterate list of birds
            for li in ul.find_all("li"):
                bird_status = li.text.split(" ")[0].strip(" ()")
                bird_swedish = li.a.text.lower()
                bird_latin = li.i.text.lower()
                bird_english = self.get_english_name(li.a.get("href"))
                print(f"  - {bird_swedish.title()} (latin: {bird_latin.title()}, engelska: {bird_english.title()})")
                bird = Bird(bird_latin, bird_swedish, family, bird_status, english_name=bird_english)
                birds.append(bird)

            self.birdlist.append((Family(family_latin, family_swedish, family_english), birds))
        print(self.birdlist)

    def create_keyword_list(self):
        """Create a lightroom formatted keyword list"""
        keywords_file = Path("swedish_birds_lightroom.txt")
        text = []
        text.append("fåglar\n")
        text.append("\t{fågel}\n")
        text.append("\t{birds}\n")
        text.append("\t{bird}\n")
        text.append("\t{animal}\n")
        text.append("\t{dinosaur}\n")
        text.append("\t{theropod}\n")
        text.append("\t{birdwatching}\n")
        text.append("\t{fågelskådning}\n")

        for family, birds in self.birdlist:

            # Create family top-level
            text.append(f"\t{family.swedish_name}\n")

            # Make aliases for english and latin names
            text.append(f"\t\t{{{family.latin_name}}}\n")
            if family.english_name is not None:
                if family.english_name != family.latin_name:
                    text.append(f"\t\t{{{family.english_name}}}\n")

            # Create bird child
            for bird in birds:
                text.append(f"\t\t{bird.swedish_name}\n")

                # Make aliases for english and latin names
                text.append(f"\t\t\t{{{bird.latin_name}}}\n")
                if bird.english_name is not None:
                    text.append(f"\t\t\t{{{bird.english_name}}}\n")

        # Write keywords to file
        with keywords_file.open("w") as f:
            f.writelines(text)


def get_wikipedia_article(url):
    """Get the html content of a wikipedia article"""
    local_html = Path('sports.html')
    if not local_html.is_file():
        response = requests.get(url)
        local_html.write_text(response.text)
    return local_html.read_text()


def process_string(input_string):
    """Remove illegal characters etc"""
    if input_string is not None:
        text = input_string.replace('[edit]', '')

        valid_chars = f' -_.{string.ascii_letters}{string.digits}'
        return ''.join([x for x in text if x in valid_chars]).lower()
    return


def parse_html(html):
    """Parse html and get sports"""
    sports = []

    soup = BeautifulSoup(html, 'lxml')

    # Find all families and go through them
    # h2s = soup.find_all("h2")
    # for h2 in h2s:
    #     h3 = h2.find_next('h3')
    #     while True:
    #         print(h3.text.strip('[edit]'))
    #
    #         if not h3:
    #             break
    #         h3 = h3.find_next('h3')
    container = soup.find("div", {"class": 'mw-parser-output'})
    category = ''
    subcategory = ''
    sport = ''
    for child in container.children:
        if isinstance(child, Tag):
            if child.name == 'h3':
                category = process_string(child.text)
                continue

            if child.name == 'ul':
                logger.info(f'category: {category}')
                for li in child.find_all('li'):
                    # Get sport name
                    if li.a:
                        name = process_string(li.a.text)
                    else:
                        name = process_string(li.text)
                    logger.info(f'name: {name}')


                    ul = li.find('ul')
                    if ul:
                        subcategory = name
                        logger.info(f'\tsubcategory: {subcategory}')
                        for i in ul.find_all('li'):
                            name = i.text
                            sport = Sport(name, category=category, subcategory=subcategory)
                            sports.append(sport)

                    else:
                        sport = Sport(name, category=category)
                        sports.append(sport)
                        # print(f'\tsport: {sport}')

            # print(child.text)
            #     print('-------')
    return sports

def create_sports_dict(sports):
    """Create a dict from sports"""
    sports_dict = {}
    for sport in sports:
        if not sports_dict.get(sport.category):
            sports_dict[sport.category] = []



def create_keyword_list(sports):
    """Create a lightroom formatted keyword list"""
    keywords_file = Path("sports.txt")
    text = []
    text.append("sports\n")
    text.append("\t{sport}\n")

    for sport in sports:

        # Create family top-level
        text.append(f"\t{family.swedish_name}\n")

        # Make aliases for english and latin names
        text.append(f"\t\t{{{family.latin_name}}}\n")
        if family.english_name is not None:
            if family.english_name != family.latin_name:
                text.append(f"\t\t{{{family.english_name}}}\n")

        # Create bird child
        for bird in birds:
            text.append(f"\t\t{bird.swedish_name}\n")

            # Make aliases for english and latin names
            text.append(f"\t\t\t{{{bird.latin_name}}}\n")
            if bird.english_name is not None:
                text.append(f"\t\t\t{{{bird.english_name}}}\n")

    # Write keywords to file
    with keywords_file.open("w") as f:
        f.writelines(text)


def main():
    url = 'https://en.wikipedia.org/wiki/List_of_sports'
    html = get_wikipedia_article(url)
    parse_html(html)


if __name__ == '__main__':
    main()
