#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
script_name.py
Description of script_name.py.
"""
import os
import timeit
import hashlib
import xxhash
from pathlib import Path

folder_path_pathlib = Path.home() / "Downloads"
print(folder_path_pathlib)

folder_path_os = os.path.join(os.path.expanduser("~"), "Downloads")
print(folder_path_os)

folder_path_check = folder_path_os

test_file_path = "/Users/johannes/Downloads/projects-20191030T163812Z-001.zip"


def get_filelist_pathlib(folder_path):
    return [x.resolve() for x in Path(folder_path).rglob("*")]


def get_filelist_os(folder_path):
    filelist = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            filelist.append(os.path.join(root, file))
    return filelist


def get_checksum_regular(file):
    hash_md5 = hashlib.md5()
    block_size = 65000
    with open(file, "rb") as f:
        fb = f.read(block_size)
        while len(fb) > 0:
            hash_md5.update(fb)
            fb = f.read(block_size)
    return hash_md5.hexdigest()

block_size = 65536
def get_checksum_xxhash(filename):
    h = xxhash.xxh64()
    # block_size = 16384
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(block_size), b""):
            h.update(chunk)
        return h.hexdigest()


def get_checksum_md5(filename):
    h = hashlib.md5()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(block_size), b""):
            h.update(chunk)
        return h.hexdigest()


def get_checksum_pathlib(file):
    hash_md5 = hashlib.md5()
    file_path = Path(file)
    with file_path.open("rb") as f:
        for chunk in iter(lambda: f.read(), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def check_get_filelist_pathlib():
    return get_filelist_pathlib(folder_path_check)


def check_get_filelist_os():
    return get_filelist_os(folder_path_check)


def check_checksums_pathlib():
    return get_checksum_pathlib(test_file_path)


def check_checksums_regular():
    return get_checksum_regular(test_file_path)


def check_checksum_xxhash():
    return get_checksum_xxhash(test_file_path)


def check_checksum_md5():
    return get_checksum_md5(test_file_path)


def main():
    """docstring for main"""

    # Filelist
    # print("Checking filelist creation time for pathlib")
    # filelist_pathlib = get_filelist_pathlib(folder_path_pathlib)
    # print("Took {} to finish".format(timeit.timeit(check_get_filelist_pathlib, number=1)))
    #
    # print("")
    #
    # print("Checking filelist creation time for os")
    # filelist_os = get_filelist_os(folder_path_os)
    # print("Took {} to finish".format(timeit.timeit(check_get_filelist_os, number=1)))

    # Checksums
    # print("Checking checksum creation time for pathlib")
    # print("Pathlib took {} to finish".format(timeit.timeit(check_checksums_pathlib, number=3)))
    #
    # print("")
    #
    # print("Checking filelist creation time for regular")
    # print("Regular took {} to finish".format(timeit.timeit(check_checksums_regular, number=3)))

    print("Checking checksum creation time for xxhash (os)")
    print("xxhash took {} to finish".format(timeit.timeit(check_checksum_xxhash, number=1)))

    print("Checking checksum creation time for md5 (os)")
    print("md5 took {} to finish".format(timeit.timeit(check_checksum_md5, number=1)))


if __name__ == '__main__':
    main()
