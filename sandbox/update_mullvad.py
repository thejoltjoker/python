#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
update_mullvad.py
Description of update_mullvad.py.
"""
import requests
import platform
from bs4 import BeautifulSoup
from pprint import pprint
from urllib.parse import urlparse
from urllib.parse import urljoin

def main():
    """docstring for main"""
    url = "https://mullvad.net/en/download/"
    base_url = "https://mullvad.net"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    os_string = platform.system()
    downloads = soup.findAll("a", {"class": "download-button"})
    download_links = {}
    for link in downloads:
        if link["href"].endswith(".exe"):
            download_links["windows"] = urljoin(base_url, link["href"])
        elif link["href"].endswith(".pkg"):
            download_links["osx"] = urljoin(base_url, link["href"])
        elif link["href"].endswith(".deb"):
            download_links["debian"] = urljoin(base_url, link["href"])
        elif link["href"].endswith(".rpm"):
            download_links["fedora"] = urljoin(base_url, link["href"])
        elif link["href"].endswith(".apk"):
            download_links["android"] = urljoin(base_url, link["href"])
    pprint(download_links)


if __name__ == '__main__':
    main()
