#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
fix_filenames.py
Remove illegal characters from filenames.
"""
import os
import string

source_folder = r"E:\Dropbox\temp\_sort"
valid_chars = " -_.{letters}{digits}".format(
    letters=string.ascii_letters, digits=string.digits)


def convert_filename(file):
    filename = file.replace('å', 'a')
    filename = filename.replace('ä', 'a')
    filename = filename.replace('ö', 'o')
    filename = filename.replace(' ', '_')
    filename = ''.join(c for c in filename if c in valid_chars)

    return filename


def main():
    """docstring for main"""
    for root, folders, files in os.walk(source_folder):
        for file in files:
            new_filename = convert_filename(file)
            full_filename = os.path.join(root, file)
            new_full_filename = os.path.join(root, new_filename)
            os.rename(full_filename, new_full_filename)
            print("{original} -> {new}".format(original=file,  new=new_filename))


if __name__ == '__main__':
    main()
