#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
file_organizer.py
Organize files based on type etc.
"""

import os
import time
import string
import shutil
import hashlib
import xxhash
import pprint
import argparse
from pathlib import Path


class FileOrganizer:
    def __init__(self, source, dest=None, exclude=None, group=True):
        # Get source folder
        self.source_folder = source

        # Get destination folder
        if dest is None:
            self.dest_folder = '{}_sorted'.format(source)
        else:
            self.dest_folder = dest

        # Create list for exclusion
        self.exclude_filter = []
        if exclude is None:
            self.exclude = []
        elif type(exclude) == list:
            self.exclude_filter.extend(exclude)
        else:
            self.exclude_filter.append(exclude)

        self.grouped = group

        self.groups = {'books': ['epub', 'mobi'],
                       'web': ['html', 'htm', 'php'],
                       'videos': ['mp4', 'avi', 'mpg', 'mov', 'mpeg', 'flv', 'mkv', 'mod', 'm2ts', '3gp'],
                       'images': ['jpg', 'arw', 'gif', 'psd', 'jpeg', 'dng', 'cr2', 'arw', 'tif', 'tiff', 'png', 'gpr',
                                  'bmp', 'exr', 'sr2', 'arw'],
                       'photoshop': ['psd', 'psb'],
                       'illustrator': ['ai'],
                       'disc': ['iso', 'bin', 'dmg', 'toast', 'vcd'],
                       'luts': ['cube', 'mga'],
                       '3d': ['abc', 'obj', 'ma', 'mb', '3ds', 'fbx'],
                       'archives': ['zip', 'tar', 'gz', 'rar', '7z', '7zip', 'arj', 'z'],
                       'documents': ['doc', 'gdoc', 'xls', 'docx', 'xlsx', 'pdf', 'txt', 'md', 'pptx', 'ppt', 'odt'],
                       'audio': ['mp3', 'wav', 'flac', 'opus', 'wma', 'aif', 'mpa', 'ogg', 'aiff', 'mid', 'aac'],
                       'apps': ['exe', 'app', 'apk', 'msi'],
                       'fonts': ['ttf', 'otf']
                       }

        print('Source folder is {}'.format(self.source_folder))
        print('Destination folder is {}'.format(self.dest_folder))

    def create_folder(self, folder):
        if not os.path.exists(folder):
            os.makedirs(folder)

    def get_file_type(self, file_path):
        ext = os.path.splitext(file_path)[-1].lower()[1:]
        if self.grouped:
            new_ext = "other"
            for group in self.groups:
                if ext in self.groups[group]:
                    new_ext = group
            return new_ext
        else:
            return ext

    def move_file(self, source, destination):
        shutil.move(source, destination)

    def copy_file(self, source, destination):
        shutil.copy2(source, destination)

    def delete_empty_folders(self, base_path=None):
        if base_path is None:
            base_path = self.source_folder
        for subdir, dirs, files in os.walk(base_path, topdown=False):
            if self.if_folder_empty(subdir):
                print("Deleting empty folder {}".format(subdir))
                os.rmdir(subdir)

    def validate_filename(self, file_name):
        valid_chars = " -_.{letters}{digits}".format(
            letters=string.ascii_letters, digits=string.digits)
        valid_file_name = file_name.replace('å', 'a')
        valid_file_name = valid_file_name.replace('ä', 'a')
        valid_file_name = valid_file_name.replace('ö', 'o')
        valid_file_name = ''.join(
            c for c in valid_file_name if c in valid_chars)
        valid_file_name = valid_file_name.replace(' ', '_')
        return valid_file_name

    def if_folder_empty(self, folder):
        if len(os.listdir(folder)) == 0:
            return True
        else:
            return False

    def get_file_date(self, file_path):
        file_date = time.strftime(
            '%Y-%m-%d', time.gmtime(os.path.getmtime(file_path)))
        return file_date.split('-')

    def get_file_checksum(self, fname):
        hash_xxhash = xxhash.xxh64()
        hash_md5 = hashlib.md5()
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def get_file_info(self, file_path):
        file_info = {}
        file_info['name'] = os.path.basename(file_path)
        file_info['path'] = file_path
        file_info['type'] = self.get_file_type(file_path)
        file_info['date'] = {'year': self.get_file_date(file_path)[0],
                             'month': self.get_file_date(file_path)[1],
                             'day': self.get_file_date(file_path)[2]}
        file_info['checksum'] = self.get_file_checksum(file_path)
        file_info['size'] = os.path.getsize(file_path)

        return file_info

    def get_file_list(self, input_folders):
        base_folders = []
        if type(input_folders) == list:
            base_folders.extend(input_folders)
        else:
            base_folders.append(input_folders)
        file_list = {}
        file_id = 1

        # Go through all folders
        for path in base_folders:
            for subdir, dirs, files in os.walk(path):
                for n, file in enumerate(files):
                    file_path = os.path.join(subdir, file)

                    # Check if file path contains exclusion filter
                    if any(exclusion in file_path for exclusion in self.exclude_filter):
                        print(
                            "\nFile matched exclusion pattern. Skipping {}".format(file_path))
                    else:
                        try:
                            file_info = self.get_file_info(file_path)
                            file_list[file_id] = file_info
                        except Exception as e:
                            print("Error: {}".format(e))
                            pass

                    print("\r{} files found".format(file_id), end='')

                    # Increase id counter
                    file_id += 1
        print('\n')

        return file_list

    def dryrun(self, verify=True, validate_name=True):
        self.organize(operation='dryrun', verify=verify,
                      validate_name=validate_name)

    def copy(self, verify=True, validate_name=True):
        self.organize(operation='copy', verify=verify,
                      validate_name=validate_name)

    def move(self, verify=True, validate_name=True, delete_empty=False):
        self.organize(operation='move', verify=verify,
                      validate_name=validate_name)
        self.delete_empty_folders(self.source_folder)

    def organize(self, operation=None, verify=True, validate_name=True, overwrite=False):
        """docstring for main"""
        source_files = self.get_file_list(self.source_folder)
        file_count = len(source_files)
        for n, file_id in enumerate(source_files):
            file_name = source_files[file_id]['name']
            file_path = source_files[file_id]['path']
            file_type = source_files[file_id]['type']
            file_year = source_files[file_id]['date']['year']
            file_checksum = source_files[file_id]['checksum']

            if validate_name:
                dest_file_path = os.path.join(
                    self.dest_folder, file_type, file_year, self.validate_filename(file_name))
            else:
                dest_file_path = os.path.join(
                    self.dest_folder, file_type, file_year, file_name)

            if operation in ['copy', 'move']:
                # Create destination folder
                self.create_folder(os.path.dirname(dest_file_path))

            if os.path.exists(dest_file_path) and not overwrite:
                print("{op}: File with same name already exists in destination. Skipping {src}".format(
                    op=operation.title(),
                    src=file_path))

            else:
                if operation == 'copy':
                    # Copy file
                    self.copy_file(file_path, dest_file_path)

                elif operation == 'move':
                    # Copy file
                    self.move_file(file_path, dest_file_path)

                # Verify
                if verify and operation in ['copy', 'move']:
                    if self.get_file_checksum(dest_file_path) == file_checksum:
                        print(
                            "{op} {cur_count}/{tot_count}: {src}\t->\t{dest}".format(op=operation.title(),
                                                                                     cur_count=n + 1,
                                                                                     tot_count=file_count,
                                                                                     src=file_path,
                                                                                     dest=dest_file_path))
                    else:
                        print("Operation cancelled. Checksum mismatch\n{src}\t->\t{dest}".format(src=file_path,
                                                                                                 dest=dest_file_path))
                else:
                    print("{op}: {src}\t->\t{dest}".format(op=operation.title(),
                                                           src=file_path, dest=dest_file_path))

    def pretty_print(self, input):
        # Pretty print output
        pp = pprint.PrettyPrinter(indent=2)
        pp.pprint(input)

    def find_duplicates(self):
        # Get source files
        all_files = self.get_file_list([self.source_folder, self.dest_folder])

        all_files_list = {}
        duplicate_files = {}

        # Go through all files and add to dictionary
        for n, file_id in enumerate(all_files):
            # Get file checksum
            file_checksum = all_files[file_id]['checksum']
            file_path = all_files[file_id]['path']

            # Create new dictionary key if it doesn't exist
            if not all_files_list.get(file_checksum):
                all_files_list[file_checksum] = []

            # Add file path to dictionary
            all_files_list[file_checksum].append(file_path)

        # Remove keys for files that aren't duplicates
        for key, value in all_files_list.items():
            if len(value) > 1:
                duplicate_files[key] = value

        print("{} duplicates found".format(len(duplicate_files)))

        return duplicate_files


def main():
    # organizer = FileOrganizer(r'C:\Users\thejoltjoker\Desktop\test\source', r'C:\Users\thejoltjoker\Desktop\test\dest')
    # organizer = FileOrganizer(r'E:\Dropbox\Pictures', exclude=['lightroom'])
    # Create organizer object
    # organizer = FileOrganizer('/Volumes/data_a/temp/foto_01/Bilder/72 ppi', dest="/Users/johannes/Dropbox/temp/server")
    source_path = r"/Volumes/data_a/temp/temp_macbook/videos"
    organizer = FileOrganizer(source_path, dest="/Users/johannes/Dropbox/temp/server")

    # Make a dryrun
    # organizer.dryrun(verify=False)

    # Copy files
    # organizer.copy()

    # Move files
    organizer.move(delete_empty=True)

    # Delete empty folders
    # organizer.delete_empty_folders()

    # Find and move duplicates
    # dupes = organizer.find_duplicates()
    # organizer.pretty_print(dupes)
    # Move duplicates
    # for key, values in dupes.items():
    #     # print(values[1])
    #     os.remove(values[1])
    #     for file_path in values:
    #         if '0301' in file_path:
    #             print(file_path)
    #             os.remove(file_path)
    # print(os.path.join('/Volumes/mcbeast/temp_media/_duplicates', os.path.basename(file_path)))
    # organizer.move_file(file_path, os.path.join(
    #     '/Volumes/mcbeast/temp_media/_duplicates', os.path.basename(file_path)))


def cli():
    """Command line interface"""
    # Create the parser
    parser = argparse.ArgumentParser(
        description="Organize files")

    # Add the arguments
    parser.add_argument("source",
                        type=str,
                        help="The source folder")

    parser.add_argument("-d", "--destination",
                        type=str,
                        help="The destination folder",
                        action="store")

    parser.add_argument("-m", "--move",
                        help="Move files instead of copy",
                        action="store_true")

    parser.add_argument("-e", "--exclude",
                        help="Move files instead of copy",
                        action="store_true")

    parser.add_argument("--dryrun",
                        help="Run the script without actually changing any files",
                        action="store_true")

    # Execute the parse_args() method
    args = parser.parse_args()

    # Print the title
    print("================")
    print("File organizer")
    print("================")
    print("")

    confirmation = False

    source = args.source

    print("")

    # Set the folder structure
    folder_structure = args.structure

    # Set the transfer mode
    if args.move:
        mode = "move"
    else:
        mode = "copy"

    # Run offloader
    organizer = FileOrganizer(source=source,
                              dest=destination,
                              exclude=None,
                              group=True)


if __name__ == '__main__':
    main()
    # print(get_file_type('jens.JPG'))
