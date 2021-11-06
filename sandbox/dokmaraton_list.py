#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
script_name.py
Description of script_name.py.
"""
import requests
from bs4 import BeautifulSoup
import string
import math
import csv
import pandas


def main():
    """docstring for main"""
    list_url = "https://www.imdb.com/list/ls054856346/"
    response = requests.get(list_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    films = []

    for n, item in enumerate(soup.find_all("div", "lister-item")):
        # Set rating
        rating = ""
        if item.find("span", "ipl-rating-star__rating"):
            rating = item.find("span", "ipl-rating-star__rating").text

        # Genre
        genre = ""
        if item.find("span", "genre"):
            genre = item.find("span", "genre").text.strip()

        # Runtime
        runtime = 0
        if item.find("span", "runtime"):
            runtime = int("".join([x for x in item.find("span", "runtime").text if x in string.digits]))

        hours = math.floor(runtime / 60)
        minutes = int((runtime / 60 - hours) * 60)

        # Poster
        # TODO
        poster_url = item.find("div", "lister-item-image").img["loadlate"]
        print(poster_url)
        film_poster = f'=IMAGE("{poster_url}")'
        # Put it all together
        film = {
            "Title": item.h3.a.text,
            "Rating": rating,
            "Genre": genre,
            "Hours": hours,
            "Minutes": minutes,
            "Runtime": runtime,
            "IMDB": f"https://www.imdb.com/{item.h3.a['href']}",
            "Poster": film_poster
        }
        print(n, film["Title"])
        films.append(film)
    with open("dokmaraton.csv", mode="w") as dok_file:
        fieldnames = ["Title", "Rating", "Genre", "Hours", "Minutes", "Runtime", "IMDB", "Poster"]
        dok_writer = csv.DictWriter(dok_file, delimiter=",", fieldnames=fieldnames)
        for film in films:
            dok_writer.writerow(film)


if __name__ == '__main__':
    main()
