#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
load_settings.py
Load settings from a json file.
"""
import json
import os


@staticmethod
def load_settings():
    """Load settings from file"""
    settings_file = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), 'settings.json')

    with open(settings_file, 'r') as read_file:
        settings = json.load(read_file)

    return settings

def main():
    """docstring for main"""
    load_settings()


if __name__ == '__main__':
    main()
