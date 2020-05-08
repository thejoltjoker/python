#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
scrape_hashtags.py
Description of scrape_hashtags.py.
"""
import logging
from bs4 import BeautifulSoup
import scraping


def main():
    """docstring for main"""
    url = "https://venthstudios.co.uk/101-instagram-photography-feature-accounts-street-travel-urban/"
    html = scraping.get_request(url)
    # Parse html using bs4
    soup = BeautifulSoup(html.text, 'html.parser')
    # Find all table rows with user agents
    article_content = soup.find_all("span", "cb-itemprop")
    # print(article_content)
    hashtags = []
    for i in article_content:
        text = i.text
        text_split = text.split(" ")

        hashtags.extend([x for x in text_split if "#" in x])

    for h in hashtags:
        print(h[1:])


if __name__ == '__main__':
    main()
