#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
csv_to_json.py
Description of csv_to_json.py.
"""
import csv
import sys
import json


def convert(filename):
    csv_filename = filename[0]
    f = open(csv_filename, 'r')
    csv_reader = csv.DictReader(f)
    print(json.dumps([r for r in csv_reader]))
    f.close()


if __name__ == "__main__":
    convert(sys.argv[1:])
