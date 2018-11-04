#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
check_duplicates_md5.py
A script to calculate how much storage space you can save by removing duplicates
"""
# TODO get file size
import os
import sys
import hashlib


def get_file_size(file):
    size = os.path.getsize(file)
    mb_size = float(size) / (1024 * 1024.0)
    return str(round(mb_size, 2))


def hashfile(path, blocksize=65536):
    file = open(path, 'rb')
    hasher = hashlib.md5()
    buf = file.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = file.read(blocksize)
    file.close()
    return hasher.hexdigest()


def find_duplicates(folder):
    dups = {}
    for root, subdirs, files in os.walk(folder):
        for filename in files:
            path = os.path.join(root, filename)
            file_hash = hashfile(path)

            if file_hash in dups:
                dups[file_hash].append(path)
            else:
                dups[file_hash] = [path]
    return dups


def main():
    """docstring for main"""
    result = find_duplicates('/Volumes/data_a/media/photos/2008')
    for i in result.items():
        print(i)


if __name__ == '__main__':
    main()
