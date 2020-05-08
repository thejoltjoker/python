#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
fix_foldernames.py
Remove illegal characters from filenames.
"""
import os
import string
import sys
from pathlib import Path

source_folder = r"R:\media\photos\2011"


def validate(input_string):
    valid_chars = "-_.{letters}{digits}".format(letters=string.ascii_letters, digits=string.digits)
    valid_string = input_string.replace('å', 'a')
    valid_string = valid_string.replace('ä', 'a')
    valid_string = valid_string.replace('ö', 'o')
    valid_string = valid_string.replace(' ', '_')
    valid_string = ''.join(c for c in valid_string if c in valid_chars)

    return valid_string


def main(source):
    """docstring for main"""
    for s in source:
        source_path = Path(s)
        folders = [x for x in source_path.glob("*") if x.is_dir()]
        for path in folders:
            new_path = path.parent / validate(path.name)
            if not new_path.is_dir():
                path.rename(new_path)
                print(f"{path.resolve()} > {new_path.resolve()}")


if __name__ == '__main__':
    main(sys.argv)
