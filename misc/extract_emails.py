#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
extract_emails.py
Description of extract_emails.py.
"""
import re
import sys

def extract_emails(input_string):
    """docstring for main"""
    emails = []
    str = input_string
    match = re.findall(r'[\w.-]+@[\w.-]+', str)
    if match:
        for i in match:
            if i not in emails:
                emails.append(i)
    for i in emails:
        name = i.split("@")[0]
        print(name.strip()+", "+i)


if __name__ == '__main__':
    extract_emails(sys.argv[1])
