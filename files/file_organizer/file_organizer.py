#!/usr/bin/env python
# -*- coding: utf-8 -*-
# TODO exclude directories
"""
organize_files_year.py
Description of organize_files_year.py.
"""
import os
import time
import shutil

# options
source_folder = '/Volumes/mcbeast/temp_media/toSort/'
# dest_folder = '{}_sorted'.format(source_folder)
dest_folder = '/Volumes/mcbeast/temp_media/sorted'
file_operation = 'move'  # copy, move, print
grouped = True
exclude = ['wqwerwtqew90t']

print('Source folder is {}'.format(source_folder))
print('Destination folder is {}'.format(dest_folder))
print('File operation is {}'.format(source_folder))
print('File grouping is {}'.format(grouped))

# grouping
groups = {
    "videos": ['mp4',
               'avi',
               'mpg',
               'mov',
               'mpeg',
               'flv',
               'mkv',
               'mod'],

    "pictures": ['jpg',
                 'arw',
                 'psd',
                 'jpeg',
                 'dng',
                 'cr2',
                 'arw',
                 'tif',
                 'tiff',
                 'png',
                 'gpr'],


    "archives": ['zip',
                 'tar',
                 'gz',
                 'rar',
                 '7z',
                 '7zip'],

    "documents": ['doc',
                  'gdoc',
                  'xls',
                  'docx',
                  'xlsx',
                  'pdf',
                  'txt',
                  'md'],
    "audio": ['mp3',
              'wav',
              'flac',
              'opus',
              'wma',
              'aif',
              'aiff']

}


# create destination root
if not os.path.exists(dest_folder) and file_operation is not 'print':
    os.makedirs(dest_folder)


def get_file_type(file):
    ext = file.split('.')[-1].lower()
    if grouped:
        new_ext = "other"
        for group in groups:
            if ext in groups[group]:
                new_ext = group
        return new_ext
    else:
        return ext


def move_file(source, destination):
    shutil.move(source, destination)


def copy_file(source, destination):
    shutil.copy2(source, destination)


def create_destination_folder(ftype, year):
    type_folder = os.path.join(dest_folder, ftype)
    year_folder = os.path.join(type_folder, year)

    if not os.path.exists(type_folder):
        os.makedirs(type_folder)

    if not os.path.exists(year_folder):
        os.makedirs(year_folder)

    return year_folder


def main():
    """docstring for main"""

    for subdir, dirs, files in os.walk(source_folder):
        for exclusion in exclude:
            if exclusion not in subdir.lower():

                for file in files:
                    file_type = get_file_type(file)
                    file_path = os.path.join(subdir, file)
                    file_year = time.strftime(
                        '%Y', time.gmtime(os.path.getmtime(file_path)))

                    # debug stuff
                    # print('File name: {}'.format(file))
                    # print('Path: {}'.format(file_path))
                    # print('Type: {}'.format(file_type))
                    # print('Year: {}'.format(file_year))

                    if file_operation is not 'print':
                        created_dest_folder = create_destination_folder(
                            file_type, file_year)
                        dest_file_path = os.path.join(
                            created_dest_folder, file)

                    if file_operation == 'move':
                        move_file(file_path, dest_file_path)
                        print("{src} moved to {dest}".format(
                            src=file_path, dest=dest_file_path))
                    elif file_operation == 'copy':
                        copy_file(file_path, dest_file_path)
                        print("{src} copied to {dest}".format(
                            src=file_path, dest=dest_file_path))

                    elif file_operation == 'print':
                        dest_file_path = os.path.join(
                            dest_folder, file_type, file_year, file)
                        print("{src} -> {dest}".format(
                            src=file_path, dest=dest_file_path))
                    else:
                        print('Invalid file operation')


if __name__ == '__main__':
    main()
    # print(get_file_type('jens.JPG'))
