#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
script_name.py
Description of script_name.py.
"""
import os


def main():
    """docstring for main"""

    for subdir, dirs, files in os.walk('E:\Dropbox\entertainment\music\_unsorted'):
        for file in files:
            if file.startswith('._'):
                print(file)
                os.remove(os.path.join(subdir, file))


if __name__ == '__main__':
    main()
