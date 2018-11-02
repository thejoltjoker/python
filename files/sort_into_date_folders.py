#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
sort_into_date_folders.py
Description of sort_into_date_folders.py.
"""
import os
import time
import shutil

# options
source_folder = '/Volumes/mcbeast/temp_media/sorted/pictures'

print('Source folder is {}'.format(source_folder))


def move_file(source, destination):
    shutil.move(source, destination)


def create_destination_folder(date):
    year = date.split('-')[0]
    dest_folder = os.path.join(source_folder, year, date)

    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    return dest_folder


def main():
    """docstring for main"""

    for subdir, dirs, files in os.walk(source_folder):
        for file in files:

            file_path = os.path.join(subdir, file)
            file_date = time.strftime(
                '%Y-%m-%d', time.gmtime(os.path.getmtime(file_path)))

            # debug stuff
            # print('File name: {}'.format(file))
            # print('Path: {}'.format(file_path))
            # print('Date: {}'.format(file_date))

            created_dest_folder = create_destination_folder(file_date)
            dest_file_path = os.path.join(created_dest_folder, file)

            move_file(file_path, dest_file_path)
            print("{src} moved to {dest}".format(
                src=file_path, dest=dest_file_path))


if __name__ == '__main__':
    main()
