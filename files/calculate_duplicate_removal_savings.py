#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
check_duplicates_xxhash.py
Check for duplicates using xxhash.
"""

import os
import sys
import xxhash
import hashlib
from pathlib import Path
from pprint import pprint

def human_file_size(num):
    """Readable file size"""
    for unit in ["", "KB", "MB", "GB", "TB", "PB", "EB", "ZB"]:
        if abs(num) < 1024.0:
            return "%3.1f %s" % (num, unit)
        num /= 1024.0
    return "%.1f%s" % (num, "YB")

def file_checksum(file_path, block_size=65536):
    """Get the checksum for a file"""
    path = Path(file_path)
    h = xxhash.xxh64()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(block_size), b""):
            h.update(chunk)
        return h.hexdigest()


def scan_directory(directory):
    filelist = {}

    # Create filelist
    for root, subdirs, files in os.walk(directory):
        for f in files:
            path = Path(root) / f
            file_hash = file_checksum(path)

            if filelist.get(file_hash):
                filelist[file_hash]["paths"].append(str(path))
            else:
                filelist[file_hash] = {
                    "paths": [str(path)],
                    "size": path.stat().st_size,
                    "checksum": file_hash
                }

    return filelist


class SpaceSavings:
    def __init__(self, directory, method="hash"):
        self.filelist = scan_directory(directory)
        self.duplicates = self.get_duplicates(method=method)
        self.savings = self.calculate_savings()

    def get_duplicates(self, directory=None, method="hash"):
        if directory is None:
            filelist = self.filelist
        else:
            filelist = scan_directory(directory)

        duplicates = {}
        for f in filelist:
            if len(filelist[f].get("paths")) > 1:
                duplicates[f] = filelist[f]
        print(f"Found {len(duplicates)} duplicates in {len(filelist)} files")

        return duplicates

    def calculate_savings(self):
        savings = 0
        for f in self.duplicates:
            # Calculate based on how many duplicates
            amount = len(self.duplicates[f].get("paths"))
            savings += ((amount - 1) * self.duplicates[f].get("size"))

        return savings


def main():
    """docstring for main"""
    dir = "/Users/johannes/Desktop/1909_kulturrundan"

    ss = SpaceSavings(dir)
    print(human_file_size(ss.savings))


if __name__ == '__main__':
    main()
