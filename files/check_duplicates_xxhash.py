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
import argparse


def file_checksum(file_path, hashtype="xxhash", block_size=65536):
    """Get the checksum for a file"""
    path = Path(file_path)
    h = xxhash.xxh64()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(block_size), b""):
            h.update(chunk)
        return h.hexdigest()


def find_duplicates(directory):
    hashlist = {}
    duplicates = {}
    for root, subdirs, files in os.walk(directory):
        for f in files:
            path = Path(root) / f
            file_hash = file_checksum(path)

            if file_hash in hashlist:
                hashlist[file_hash].append(str(path))
                duplicates[file_hash] = hashlist[file_hash]
            else:
                hashlist[file_hash] = [str(path)]
    return hashlist, duplicates


def main():
    """docstring for main"""

    parser = argparse.ArgumentParser(description='Remove duplicate files')
    parser.add_argument('path',
                        type=str,
                        help='the path to check for duplicates in')

    parser.add_argument('--delete',
                        action='store_true',
                        help='delete all duplicates but the first copy of the file')

    args = parser.parse_args()

    result = find_duplicates(args.path)

    print(f"Found {len(result[1])} files with duplicates")

    if args.delete:
        print("Deleting duplicate files")


if __name__ == '__main__':
    main()
