#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
check_duplicates_md5.py
Description of check_duplicates_md5.py.
"""

import os
import sys
import hashlib


def hashfile(path, blocksize=65536):
    afile = open(path, 'rb')
    hasher = hashlib.md5()
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    afile.close()
    return hasher.hexdigest()


def findDup(parentFolder):
    dups = {}
    for dirName, subdirs, fileList in os.walk(parentFolder):
        for filename in fileList:
            path = os.path.join(dirName, filename)
            file_hash = hashfile(path)

            if file_hash in dups:
                dups[file_hash].append(path)
            else:
                dups[file_hash] = [path]
    return dups


def main():
    """docstring for main"""
    result = findDup('/Volumes/mcbeast/media/photos/2008')
    for i in result.items():
        print(i)


if __name__ == '__main__':
    main()
