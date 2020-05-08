#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
practice.py
Description of practice.py.
"""
import random
import csv


class Practice:
    # TODO stats
    # TODO which questions wrong
    def __init__(self):
        self.questions = {
            "1": "räven",
            "2": "haren",
            "3": "teknikbacken",
            "4": "äventyrsspåret",
            "5": "vintergatan",
            "6": "urspårningen",
            "7": "rallarsvängen",
            "8": "himlabacken",
            "9": "rälsbrottet",
            "10": "lilla björn",
            "11": "solkurvan",
            "12": "växeln",
            "13": "karven",
            "14": "raka spåret",
            "15": "hemvändaren",
            "16": "ängarna",
            "17": "svarta björn",
            "18": "grytspåret",
            "19": "grytan",
            "20": "banvallen",
            "21": "stora drivan",
            "22": "isfallet",
            "23": "tunneln"
        }

    def practice(self):
        correct = 0
        incorrect = 0
        questions = [x.strip() for x in self.questions.keys()]
        random.shuffle(questions)
        for n, q in enumerate(questions):
            while True:
                response = input(f"Vad heter {q.title()}?\n")
                if response.lower() == self.questions[q]:
                    print("Korrekt!")
                    correct += 1
                    break
                else:
                    print(f"Fel svar! Rätt svar är \"{self.questions[q].title()}\"")
                    incorrect += 1
                    break
            print(f"--- {n + 1}/{len(questions)} ---")

        print(f"{correct} rätta svar och {incorrect} fel")


def main():
    """docstring for main"""

    names = [n for n in reader]
    names.pop(0)
    random.shuffle(names)
    # read file row by row
    for n, row in enumerate(names):
        name = row[0].strip()
        job_title = row[1]

        while True:
            response = input("Who is {}? ".format(
                job_title.upper())).strip()
            if len(response) > 1 and response.lower() in name.lower():
                print("Correct! {} is {}".format(
                    name.title(), job_title.upper()))
                break
            else:
                print("Incorrect! {} is {}".format(
                    name.title(), job_title.upper()))

        print("--- {}/{} ---".format(n + 1, len(names)))


if __name__ == '__main__':
    # main()
    p = Practice()
    p.practice()
