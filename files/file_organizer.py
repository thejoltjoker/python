#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
organize_files_year.py
Description of organize_files_year.py.
"""
# TODO check for duplicates
# TODO fix filenames
# TODO exclude
# TODO move
# TODO delete empty
import os
import time
import string
import shutil
import hashlib
import pprint


class FileOrganizer:
    def __init__(self, source, dest=None, exclude=None, group=True):

        # Set variables

        # Get source folder
        self.source_folder = source

        # Get destination folder
        if dest is None:
            self.dest_folder = '{}_sorted'.format(source)
        else:
            self.dest_folder = dest

        if exclude is None:
            self.exclude = []

        self.grouped = group

        self.groups = {'books': ['epub', 'mobi'],
                       'web': ['html', 'htm', 'php'],
                       'videos': ['mp4', 'avi', 'mpg', 'mov', 'mpeg', 'flv', 'mkv', 'mod'],
                       'images': ['jpg', 'arw', 'gif', 'psd', 'jpeg', 'dng', 'cr2', 'arw', 'tif', 'tiff', 'png', 'gpr',
                                  'bmp', 'exr'],
                       'photoshop': ['psd', 'psb'],
                       'illustrator': ['ai'],
                       'disc': ['iso', 'bin', 'dmg', 'toast', 'vcd'],
                       'luts': ['cube', 'mga'],
                       '3d': ['abc', 'obj', 'ma', 'mb', '3ds', 'fbx'],
                       'archives': ['zip', 'tar', 'gz', 'rar', '7z', '7zip', 'arj', 'z'],
                       'documents': ['doc', 'gdoc', 'xls', 'docx', 'xlsx', 'pdf', 'txt', 'md'],
                       'audio': ['mp3', 'wav', 'flac', 'opus', 'wma', 'aif', 'mpa', 'ogg', 'aiff', 'midaac'],
                       'apps': ['exe', 'app'],
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
        valid_chars = " -_.{letters}{digits}".format(letters=string.ascii_letters, digits=string.digits)
        valid_file_name = file_name.replace('å', 'a')
        valid_file_name = valid_file_name.replace('ä', 'a')
        valid_file_name = valid_file_name.replace('ö', 'o')
        valid_file_name = ''.join(c for c in valid_file_name if c in valid_chars)
        valid_file_name = valid_file_name.replace(' ', '_')
        return valid_file_name

    def if_folder_empty(self, folder):
        if len(os.listdir(folder)) == 0:
            return True
        else:
            return False

    def create_destination_folder(self, ftype, year):
        type_folder = os.path.join(self.dest_folder, "_{}".format(ftype))
        year_folder = os.path.join(type_folder, year)

        if not os.path.exists(type_folder):
            os.makedirs(type_folder)

        if not os.path.exists(year_folder):
            os.makedirs(year_folder)

        return year_folder

    def get_file_date(self, file_path):
        file_date = time.strftime('%Y-%m-%d', time.gmtime(os.path.getmtime(file_path)))
        return file_date.split('-')

    def get_file_checksum(self, fname):
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
        for path in base_folders:
            for subdir, dirs, files in os.walk(path):
                for n, file in enumerate(files):
                    file_path = os.path.join(subdir, file)
                    file_info = self.get_file_info(file_path)
                    file_checksum = file_info['checksum']
                    file_list[file_id] = file_info

                    print("\r{} files found".format(file_id), end='')
                    # Increase id counter
                    file_id += 1
        print('')

        return file_list

    def dryrun(self, verify=True, validate_name=True):
        self.organize(operation='dryrun', verify=verify, validate_name=validate_name)

    def copy(self, verify=True, validate_name=True):
        self.organize(operation='copy', verify=verify, validate_name=validate_name)

    def move(self, verify=True, validate_name=True, delete_empty=False):
        self.organize(operation='move', verify=verify, validate_name=validate_name)
        self.delete_empty_folders(self.source_folder)

    def organize(self, operation=None, verify=True, validate_name=True):
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
                dest_file_path = os.path.join(self.dest_folder, file_type, file_year, self.validate_filename(file_name))
            else:
                dest_file_path = os.path.join(self.dest_folder, file_type, file_year, file_name)

            if operation in ['copy', 'move']:
                # Create destination folder
                self.create_folder(os.path.dirname(dest_file_path))

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
                        "{op} {cur_count}/{tot_count}: {src}\t->\t{dest}".format(op=operation.title(), cur_count=n + 1,
                                                                                 tot_count=file_count, src=file_path,
                                                                                 dest=dest_file_path))
                else:
                    print("Operation cancelled. Checksum mismatch\n{src}\t->\t{dest}".format(src=file_path,
                                                                                             dest=dest_file_path))
            else:
                print("{op}: {src}\t->\t{dest}".format(op=operation.title(), src=file_path, dest=dest_file_path))

    def pretty_print(self, input):
        # Pretty print output
        pp = pprint.PrettyPrinter(indent=2)
        pp.pprint(input)

    def find_duplicates(self):
        # Get source files
        all_files = self.get_file_list([self.source_folder, self.dest_folder])

        # Get destination files
        # dest_files = self.get_file_list(self.dest_folder)

        # print(source_files)
        # self.pretty_print(source_files)
        # self.pretty_print(dest_files)
        duplicate_files = {}

        # Go through all files to check for duplicates
        for n, file_id in enumerate(all_files):
            # Get file checksum
            file_checksum = all_files[file_id]['checksum']
            file_path = all_files[file_id]['path']

            if not duplicate_files.get(file_checksum):
                duplicate_files[file_checksum] = []

            # Add file path to dictionary
            duplicate_files[file_checksum].append(file_path)

        return duplicate_files


def main():
    # organizer = FileOrganizer(r'C:\Users\thejoltjoker\Desktop\test\source', r'C:\Users\thejoltjoker\Desktop\test\dest')
    organizer = FileOrganizer(r'E:\Dropbox\temp')
    # organizer.dryrun()
    # organizer.copy()
    # organizer.move(verify=False, delete_empty=True)
    organizer.delete_empty_folders()
    # organizer.pretty_print(organizer.find_duplicates())


if __name__ == '__main__':
    main()
    # print(get_file_type('jens.JPG'))
