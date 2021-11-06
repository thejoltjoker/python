#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
script_name.py
Scrapes wikipedia for swedish birds and creates a lightroom keyword list.
"""
import sqlite3
import requests
from bs4 import BeautifulSoup
from pathlib import Path
from pprint import pprint


class Bird:
    def __init__(self, latin_name, swedish_name, family, status, english_name=None):
        self.latin_name = latin_name
        self.swedish_name = swedish_name
        self.english_name = english_name
        self.family = family
        self.status = status


class Family:
    def __init__(self, latin_name, swedish_name, english_name=None):
        self.latin_name = latin_name
        self.swedish_name = swedish_name
        self.english_name = english_name


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


def main():
    birds = BirdScraper()
    birds.get_birds()
    birds.create_keyword_list()
    birds.print()


if __name__ == '__main__':
    main()
