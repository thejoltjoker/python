#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
remove_duplicates.py
Remove duplicate files
"""
import os
import xxhash
from pathlib import Path


def file_checksum(file_path, block_size=65536):
    """Get the checksum for a file"""
    path = Path(file_path)
    h = xxhash.xxh64()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(block_size), b""):
            h.update(chunk)
        return h.hexdigest()


def file_list(directory):
    """Returns a list of files"""
    all_files = []
    for root, subdirs, files in os.walk(directory):
        for f in files:
            path = Path(root) / f
            all_files.append(path)
    return all_files


def remove_duplicates(rm_dir, check_dir):
    # Get hashes for existing files
    check_files = {file_checksum(x): str(x) for x in file_list(check_dir)}
    rm_files = {file_checksum(x): str(x) for x in file_list(rm_dir)}
    print(rm_files)
    print(check_files)
    # Check for duplicates in rm_dir
    for k, v in rm_files.items():
        if check_files.get(k):
            print(f"Removing {v} because it already exists in {check_files[k]}")
            os.remove(v)


def main():
    """docstring for main"""
    dir1 = "/Users/johannes/gdrive/caffeineCreations_old"
    dir2 = "/Users/johannes/gdrive/caffeineCreations"
    remove_duplicates(dir1, dir2)


if __name__ == '__main__':
    main()
