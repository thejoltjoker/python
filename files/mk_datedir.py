#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
mk_datedir.py
Create a folder with a date prefix
"""
import sys
import os
from datetime import datetime
from pathlib import Path


def mkdatedir(dirname):
    """Creates a folder with a date prefix in the working dir"""
    # Set variables
    prefix = datetime.today().strftime('%y%m%d')
    path = Path(os.getcwd()) / "_".join([prefix, dirname])

    # Create dir
    path.mkdir(parents=True)

    print(f"Created new folder {path.resolve()}")
    return path


if __name__ == '__main__':
    if len(sys.argv) == 2:
        mkdatedir(sys.argv[1])
    else:
        dirname = input("Enter a folder name: ")
        mkdatedir(dirname)
