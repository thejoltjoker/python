#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
random_dinosaur.py
Gets a random dinosaur from dinosaurpictures and returns an image, name and some info in json format
"""
import logging
import requests
import json
import random
from pathlib import Path
from bs4 import BeautifulSoup


def logger(level="info"):
    """Create a logger with file and stream handler"""
    # Create logger
    logger = logging.getLogger()
    if logger.hasHandlers():
        logger.handlers.clear()

    if level == 'debug':
        logger.setLevel(logging.DEBUG)
    elif level == 'info':
        logger.setLevel(logging.INFO)

    # Create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # Create file handler and set level to debug
    fh = logging.FileHandler('tjj-bot.log', mode='a')
    fh.setLevel(logging.DEBUG)

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message).1024s')

    # Add formatter
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    # Add handlers to logger
    logger.addHandler(ch)
    logger.addHandler(fh)

    return logger


def random_dinosaur():
    """docstring for main"""
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36"
    ]
    user_agent = random.choice(user_agents)
    headers = {
        "User-Agent": user_agent
    }
    response = requests.get("https://dinosaurpictures.org/random", headers=headers)
    url = response.url
    soup = BeautifulSoup(response.text, "html.parser")

    # Get dinosaur name
    title = soup.title.string
    dino_name = title.split(" ")[0]


    # Get info
    intro = soup.find("div", "intro").find_all("p")
    intro_p = [x for x in intro][:-1]
    dino_info = intro_p[0].text.replace("\n", " ")


    # Get pictures
    images = []
    image_containers = soup.find_all("div", {"class": "img-container"})
    for containers in image_containers:
        for a in containers.findChildren("a"):
            if a.text.strip().lower() == "save":
                images.append(a["href"])



    # Compile data
    dinosaur = {
        "name": dino_name,
        "info": dino_info.strip(),
        "images": images,
        "url": url
    }
    logging.info(f"Dinosaur name is {dinosaur['name']}")
    logging.info(f"Here's some info about {dinosaur['name']}:")
    logging.info(dinosaur["info"])
    logging.info(f"These are the images found for {dino_name}")
    for img in dinosaur["images"]:
        logging.info(img)
    logging.info(f"Read more about {dinosaur['name']} here {dinosaur['url']}")
    logging.debug(dinosaur)

    return dinosaur


if __name__ == '__main__':
    logger("info")
    print(random_dinosaur())
