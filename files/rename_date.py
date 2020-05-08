#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
script_name.py
Description of script_name.py.
"""
from pathlib import Path


def main(path):
    """docstring for main"""
    for f in path.iterdir():
        if f.name.startswith("2"):
            print(f.name)
            split_name = f.name.split("_")
            split_date = split_name[0].split("-")
            new_date = "".join((split_date[0][2:], split_date[1], split_date[2]))
            print(new_date)
            split_name.pop(0)
            split_name.insert(0, new_date)
            print(split_name)
            new_name = "_".join(split_name)
            print(new_name)
            new_path = Path(f.parent) / new_name
            print(f"{f} -> {new_path}")
            f.rename(new_path)

if __name__ == '__main__':
    path = Path("/Users/johannes/gdrive/caffeineCreations_old/documents/economy/invoices/ut/2019")
    main(path)
