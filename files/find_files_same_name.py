#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
script_name.py
Description of script_name.py.
"""
import os
from pathlib import Path
from pprint import pprint

def main(path):
    """docstring for main"""
    filelist = {}
    for root, subdirs, files in os.walk(path):
        for file in files:
            file_path = Path(root) / file
            if "venv" not in str(file_path):
                if filelist.get(file_path.name):
                    filelist[file_path.name].append(file_path)
                else:
                    filelist[file_path.name] = [file_path]

    for f in filelist:
        if len(filelist[f]) > 1:
            pprint(filelist[f])

    # print(duplicates)


if __name__ == '__main__':
    main("/Users/johannes/Dropbox/code/repos/maya")
