#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
script_name.py
Description of script_name.py.
"""
import os
from pathlib import Path


def main(search_string, replace_string, path, rename=False):
    """docstring for main"""
    path = Path(path)
    for f in path.iterdir():
        old_name = str(f)
        new_name = old_name.replace(search_string, replace_string)
        if new_name != old_name:
            print(f"{old_name} > {new_name}")
        if rename:
            os.rename(old_name, new_name)


if __name__ == '__main__':
    # search_for = "lightroom_classic"
    # replace_with = "lr_classic"
    search_for = "1-2"
    replace_with = "2"
    path = "/Volumes/mcdaddy/pictures/lightroom/catalogs/2018"
    main(search_for, replace_with, path, rename=False)
