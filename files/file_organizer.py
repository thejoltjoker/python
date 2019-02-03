#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
organize_files_year.py
Description of organize_files_year.py.
"""
# TODO check for duplicates
# TODO fix filenames
import os
import time
import shutil


# class FileOrganizer:
#     def __init__(self, *args, **kwargs):
#         # options
#         self.source_folder = r'E:\Dropbox\temp\Folder'
#         # dest_folder = '{}_sorted'.format(source_folder)
#         self.dest_folder = r'E:\Dropbox\temp\_sorted'
#         self.file_operation = 'move'  # copy, move, print
#         self.grouped = True
#         self.exclude = ['wqwerwtqew90t']


# options
source_folder = r'E:\Dropbox\temp\_sort'
# dest_folder = '{}_sorted'.format(source_folder)
dest_folder = r'E:\Dropbox\temp'
file_operation = 'move'  # copy, move, print
delete_empty = True
grouped = True
exclude = ['wqwerwtqew90t']

print('Source folder is {}'.format(source_folder))
print('Destination folder is {}'.format(dest_folder))
print('File operation is {}'.format(source_folder))
print('File grouping is {}'.format(grouped))

# grouping
groups = {
    'books': ['epub', 'mobi'],
    'web': ['html', 'htm', 'php'],
    'videos': ['mp4',
               'avi',
               'mpg',
               'mov',
               'mpeg',
               'flv',
               'mkv',
               'mod'
               ],

    'images': ['jpg',
               'arw',
               'gif',
               'psd',
               'jpeg',
               'dng',
               'cr2',
               'arw',
               'tif',
               'tiff',
               'png',
               'gpr',
               'psd',
               'exr'
               ],
    'disc': [
        'iso',
        'bin',
        'dmg',
        'toast',
        'vcd'
    ],
    'luts': [
        'cube',
        'mga'
    ],
    '3d': [
        'abc',
        'obj',
        'ma',
        'mb',
        '3ds',
        'fbx'
    ],
    'archives': ['zip',
                 'tar',
                 'gz',
                 'rar',
                 '7z',
                 '7zip',
                 'arj',
                 'z'
                 ],

    'documents': ['doc',
                  'gdoc',
                  'xls',
                  'docx',
                  'xlsx',
                  'pdf',
                  'txt',
                  'md'
                  ],
    'audio': ['mp3',
              'wav',
              'flac',
              'opus',
              'wma',
              'aif',
              'mpa',
              'ogg',
              'aiff',
              'mid'
              'aac'
              ],
    'apps': ['exe',
             'app'
             ],
    'fonts': ['ttf',
              'otf'
              ]

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
    type_folder = os.path.join(dest_folder, "_{}".format(ftype))
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
    if delete_empty:
        for subdir, dirs, files in os.walk(source_folder, topdown=False):
            for exclusion in exclude:
                if exclusion not in subdir.lower():
                    if len(os.listdir(subdir)) == 0:
                        print("Deleting empty folder {}".format(subdir))
                        os.rmdir(subdir)


if __name__ == '__main__':
    main()
    # print(get_file_type('jens.JPG'))
