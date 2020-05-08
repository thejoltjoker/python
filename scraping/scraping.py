#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
scraping.py
Description of scraping.py.
"""
import logging
import os
import logging
import random
import pathlib
import requests
import time
import json
from bs4 import BeautifulSoup
from itertools import cycle

# Proxy variables
proxies_file_name = "proxies.json"
proxies_path = pathlib.Path.cwd() / proxies_file_name
proxy_limit = 50

# User agent variables
user_agents_file_name = "user_agents.json"
user_agents_path = pathlib.Path.cwd() / user_agents_file_name
user_agent_limit = 50


def scrape_user_agents(limit=user_agent_limit, browser="chrome"):
    """Return a list of common user agents
    :return user_agents"""
    # Set browser
    browsers = {
        "firefox": "https://developers.whatismybrowser.com/useragents/explore/software_name/firefox/",
        "chrome": "https://developers.whatismybrowser.com/useragents/explore/software_name/chrome/"
    }
    url = browsers.get(browser)

    # Make request to whatismybrowser.com
    html = requests.get(url)
    logging.debug(html)

    # Parse html using bs4
    soup = BeautifulSoup(html.text, 'html.parser')
    # Find all table rows with user agents
    rows = soup.find_all("td", "useragent")

    # Create list of user agents
    user_agents = []
    count = 0

    # Iterate through all the table rows
    for row in rows:
        # Get the text from table row
        row_text = row.text
        if count < limit and 'bot' not in row_text:
            user_agents.append(row_text)
            count += 1
        else:
            pass

    logging.debug(len(user_agents))
    logging.debug(user_agents)

    # Output to file
    output_json_to_file(user_agents_path, user_agents)

    return user_agents


def test_user_agents(user_agents):
    """Test user agents against httpbin"""
    url = "https://httpbin.org/user-agent"

    # Loop through user_agents
    for n in range(1, len(user_agents)):
        # Pick a random user agent
        user_agent = random.choice(user_agents)

        # Make the request
        response = requests.get(url, headers={'User-Agent': user_agent})
        response_text = response.json()
        response_ua = response_text["user-agent"]

        logging.info(f"User agent sent: {user_agent}")
        logging.info(f"User agent returned: {response_ua}")


def scrape_proxies(limit=user_agent_limit, ssl=True):
    """Get free proxies for scraping using free-proxy-list.net"""
    url = "https://free-proxy-list.net/"

    if ssl:
        url = "https://www.sslproxies.org/"

    # Make request
    html = requests.get(url)
    logging.debug(html)

    # Parse html using bs4
    soup = BeautifulSoup(html.text, "html.parser")
    table = soup.find(id="proxylisttable")  # Table containing all proxies
    table_body = table.find('tbody')  # Skip to the table content
    rows = table_body.find_all('tr')  # Get all rows with proxies

    proxies = []
    count = 0

    # Loop through html table of proxies and create a dict
    for row in rows:
        cols = row.find_all('td')
        proxy = {
            "ip": cols[0].text,
            "port": cols[1].text,
            "country": cols[3].text,
            "type": cols[4].text
        }

        if count < limit and 'elite' in proxy["type"]:
            proxies.append(proxy)
            count += 1
        else:
            pass

    logging.debug(len(proxies))
    logging.debug(proxies)

    # Save proxies to file
    output_json_to_file(proxies_path, proxies)
    return proxies


def scrape_proxies_list(limit, ssl=True):
    """Return proxies as a list of ip:port"""
    proxies_dict = scrape_proxies(limit, ssl)
    proxies = [":".join((p["ip"], p["port"])) for p in proxies_dict]
    logging.debug(len(proxies))
    logging.debug(proxies)
    return proxies


def test_proxies(proxies_list):
    """Test proxy list agains httpbin.org"""
    url = "https://httpbin.org/ip"
    actual_ip = requests.get(url).json()["origin"]
    logging.debug(f"IP {actual_ip}")

    proxy_pool = cycle(proxies_list)

    for i in range(1, len(proxies_list)):
        # Get a proxy from the pool
        proxy = next(proxy_pool)
        logging.debug(f"Testing proxy {proxy}")
        try:
            response = requests.get(
                url, proxies={"http": proxy, "https": proxy})
            response_ip = response.json()["origin"]
            logging.info(f"My ip: {actual_ip}")
            logging.info(f"Returned ip: {response_ip}")
        except Exception as e:
            logging.warning(e)
            logging.debug("Proxy failed")


def load_proxies(return_list=True):
    """Load proxies from file"""
    with proxies_path.open(mode="r") as json_file:
        proxies = json.load(json_file)
        if return_list:
            return [":".join((p["ip"], p["port"])) for p in proxies]
        else:
            return proxies


def get_proxies(limit=proxy_limit, ssl=True, return_list=True):
    """Load proxies from file or update if it's too old"""
    # Check if proxies exist on file
    if proxies_path.exists():
        # Check when file was modified to see if it needs to be update
        file_modified = os.path.getmtime(proxies_path)
        current_time = time.time()
        time_since_last_scrape = current_time - file_modified
        time_since_last_scrape_str = time.strftime(
            "%H:%M:%S", time.gmtime(time_since_last_scrape))
        logging.info(
            f"Time since last scrape of proxies {time_since_last_scrape_str}")

        # Update local list if older than 5 minutes
        if time_since_last_scrape > 300:
            scrape_proxies(limit, ssl)

        return load_proxies(return_list)

    else:
        scrape_proxies(limit, ssl)

        return load_proxies(return_list)


def load_user_agents():
    """Load user agents from file"""
    if user_agents_path.exists():
        with user_agents_path.open(mode="r") as json_file:
            user_agents = json.load(json_file)

            return user_agents
    else:
        return None


def get_user_agents(limit=user_agent_limit):
    """Load proxies from file or update if it's too old"""
    # Check if proxies exist on file
    if user_agents_path.exists():
        # Check when file was modified to see if it needs to be update
        file_modified = os.path.getmtime(user_agents_path)
        current_time = time.time()
        time_since_last_scrape = current_time - file_modified
        time_since_last_scrape_str = time.strftime(
            "%H:%M:%S", time.gmtime(time_since_last_scrape))
        logging.debug(
            f"Time since last scrape of user agents {time_since_last_scrape_str}")

        # Update local list if older than 12 hours
        if time_since_last_scrape > 43200:
            scrape_user_agents(limit)

        return load_user_agents()

    else:
        scrape_user_agents(limit)

        return load_user_agents()


def get_request(url, headers=None, use_proxy=True, random_user_agent=True):
    """Send a GET request using a proxy and random user agent"""
    if headers is None:
        headers = {}
    proxy = None
    proxy_pool = None

    if use_proxy:
        proxies = get_proxies()
        random.shuffle(proxies)
        proxy_pool = cycle(proxies)  # Cycle proxies

    if random_user_agent:
        user_agents = get_user_agents()
        user_agent = random.choice(user_agents)
        headers['User-Agent'] = user_agent

    # Send request
    response = None
    while response is None:
        # Cycle to next proxy in list
        if use_proxy:
            proxy = next(proxy_pool)

        try:
            response = requests.get(url,
                                    headers=headers,
                                    proxies={"http": proxy,
                                             "https": proxy})
            logging.debug("Connection successful")

        except Exception as e:
            logging.error(e)
            logging.error("Skipping proxy. Connnection error")
            pass

    logging.debug(response)
    return response


def post_request(url, data=None, headers=None, files=None, use_proxy=True, random_user_agent=True):
    """Send a GET request using a proxy and random user agent"""
    if headers is None:
        headers = {}
    proxy = None
    proxy_pool = None

    if use_proxy:
        proxies = get_proxies()
        random.shuffle(proxies)
        proxy_pool = cycle(proxies)  # Cycle proxies

    if random_user_agent:
        user_agents = get_user_agents()
        user_agent = random.choice(user_agents)
        headers['User-Agent'] = user_agent

    # Send request
    response = None
    while response is None:
        # Cycle to next proxy in list
        if use_proxy:
            proxy = next(proxy_pool)

        try:
            if files is not None:
                response = requests.post(url,
                                         data=data,
                                         headers=headers,
                                         files=files,
                                         proxies={"http": proxy,
                                                  "https": proxy})
            else:
                response = requests.post(url,
                                         data=data,
                                         headers=headers,
                                         proxies={"http": proxy,
                                                  "https": proxy})
            logging.debug("Connection successful")

        except Exception as e:
            logging.error(e)
            break

    logging.debug(response)
    return response


def output_json_to_file(filename, content):
    """Output json data to a file"""
    path = pathlib.Path(filename)
    with path.open(mode="w") as file:
        json.dump(content, file)


def main():
    """docstring for main"""
    # Get and test user agents
    scrape_user_agents()
    user_agents = get_user_agents()
    test_user_agents(user_agents)

    # Get and test proxies
    scrape_proxies()
    proxies = get_proxies()
    test_proxies(proxies)


if __name__ == '__main__':

    logging.getLogger(__name__).addHandler(logging.NullHandler())
    main()
