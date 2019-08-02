#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
script_name.py
Description of script_name.py.
"""
import os
import hashlib
import logging
from datetime import datetime
import shutil
import math
import argparse


class Offloader:
    def __init__(self, source, dest):
        self.logger = self.setup_logger()
        self.source = source
        self.destination = dest
        self.exclude = ['MEDIAPRO.XML',
                        'STATUS.BIN',
                        'SONYCARD.IND',
                        'AVIN0001.INP',
                        'AVIN0001.BNP',
                        'MOVIEOBJ.BDM',
                        'PRV00001.BIN',
                        'INDEX.BDM',
                        'fseventsd-uuid',
                        '.dropbox.device',
                        'AVIN0001.INT']

    def setup_logger(self):
        # Setup logger
        logger = logging.getLogger(__name__)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)-20s %(name)-10s %(levelname)-8s %(message)s', "%Y-%m-%d %H:%M:%S")

        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
        return logger

    def offload(self):
        skipped_files = []
        transferred_files = []

        # Get list of files to transfer
        source_file_list = self.get_file_list(self.source)

        # Get total file size to calculate percentage
        total_file_size = sum([source_file_list[x]['size'] for x in source_file_list])
        total_transferred_size = 0
        self.logger.info("Total file size: %s", self.convert_size(total_file_size))

        self.logger.info("---\n")

        # Iterate files in list
        for file_id in source_file_list:
            incremental = 0
            current_file = source_file_list[file_id]

            self.logger.info("Processing file %s/%s (~%s%%) | %s", file_id, len(source_file_list),
                             round((total_transferred_size / total_file_size) * 100, 2),
                             current_file['name'])

            if current_file['name'] in self.exclude:
                self.logger.warning('Filename in exclude list %s, skipping',
                                    current_file['name'])

                # Check if file already exists at destination
                skipped_files.append(current_file['name'])

            else:
                while True:
                    # Create destination path
                    new_filename = self.create_new_filename(current_file, incremental)
                    dest_file_path = os.path.join(self.destination,
                                                  current_file['date'].strftime('%Y'),
                                                  current_file['date'].strftime('%Y-%m-%d'),
                                                  new_filename)

                    # Check if file already exists at destination
                    if os.path.isfile(dest_file_path):

                        # Get file info for existing file
                        dest_file_info = self.get_file_info(dest_file_path)

                        # Compare checksums
                        if current_file['checksum'] == dest_file_info['checksum']:
                            self.logger.warning('File %s (%s) already exists in destination, skipping',
                                                dest_file_info['name'],
                                                current_file['name'])
                            self.logger.warning('Checksums: %s (source)| %s (destination)',
                                                current_file['checksum'],
                                                dest_file_info['checksum'])
                            self.logger.debug('Source: %s', current_file)
                            self.logger.debug('Destination: %s', dest_file_info)

                            # Add file to skipped list
                            skipped_files.append(current_file['name'])

                            break

                        else:
                            self.logger.warning(
                                'File with same name %s (%s) already exists in destination, adding incremental',
                                dest_file_info['name'],
                                current_file['name'])
                            self.logger.warning('Checksums: %s (source)| %s (destination)',
                                                current_file['checksum'],
                                                dest_file_info['checksum'])
                            self.logger.debug('Source: %s', current_file)
                            self.logger.debug('Destination: %s', dest_file_info)

                            # Increment number
                            incremental += 1
                            self.logger.debug("Incremental: %s", incremental)

                    else:

                        # Create destination folder
                        self.create_folder(os.path.dirname(dest_file_path))

                        # Copy file
                        try:
                            self.logger.info("Copying %s", self.convert_size(current_file['size']))
                            self.logger.info("Source: %s", current_file['path'])
                            self.logger.info("Destination: %s", dest_file_path)
                            self.copy_file(current_file['path'], dest_file_path)

                            # Add file to transferred list
                            transferred_files.append(current_file['name'])

                        except Exception as e:
                            self.logger.error(e)
                        break

            # Add file size to total
            total_transferred_size += current_file['size']

            self.logger.info("---\n")

        self.logger.info("%s files transferred", len(transferred_files))
        self.logger.debug("Transferred files: %s", transferred_files)

        self.logger.info("%s files skipped", len(skipped_files))
        self.logger.debug("Skipped files: %s", skipped_files)

    def create_new_filename(self, file_info, incremental=0):
        if incremental >= 1:
            new_filename = "_".join([file_info['date'].strftime('%y%m%d'),
                                     os.path.splitext(file_info['name'])[0],
                                     "{:03d}{}".format(incremental, os.path.splitext(file_info['name'])[1])])

        else:
            new_filename = "_".join([file_info['date'].strftime('%y%m%d'),
                                     file_info['name']])
        return new_filename

    def offload_old(self):
        # Get list of files to transfer
        file_list = self.get_file_list(self.source)
        transferred_file_list = {}

        # Get total file size to calculate percentage
        total_file_size = sum([file_list[x]['size'] for x in file_list])
        total_transferred_size = 0

        # Transfer files
        for file_id in file_list:
            current_file = file_list[file_id]

            # Create destination path
            date_formatted = self.convert_date(current_file['date']).strftime('%Y-%m-%d')
            new_filename = "_".join([self.convert_date(current_file['date']).strftime('%y%m%d'),
                                     current_file['name']])
            dest_path = os.path.join(self.destination, date_formatted[:4], date_formatted, new_filename)

            # Add file size to total
            total_transferred_size += current_file['size']

            # Copy files if they don't already exist
            if os.path.isfile(dest_path):
                dest_file_info = self.get_file_info(dest_path)
                self.logger.warning("file exists", dest_file_info)
                pass
            else:
                self.create_folder(os.path.dirname(dest_path))
                try:
                    self.copy_file(current_file['path'], dest_path)
                    # Add transferred file info to list
                    transferred_file_list[file_id] = self.get_file_info(dest_path)
                except Exception as e:
                    self.logger.error(e)
                    pass

                print("Copying file {id}/{total}\n"
                      "{trans_size} of {total_size} transferred ({percentage}%)\n"
                      "Source: {source}\n"
                      "Destination: {dest}\n"
                      "Size: {size}\n".format(name=current_file['name'],
                                              id=file_id,
                                              total=len(file_list),
                                              source=current_file['path'],
                                              dest=dest_path,
                                              size=self.convert_size(current_file['size']),
                                              trans_size=self.convert_size(total_transferred_size),
                                              total_size=self.convert_size(total_file_size),
                                              percentage=round((total_transferred_size / total_file_size) * 100, 2)))

    def copy_file(self, source, destination):
        shutil.copyfile(source, destination)

    def convert_size(self, size_bytes):
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return "%s %s" % (s, size_name[i])

    def create_folder(self, folder):
        if not os.path.exists(folder):
            os.makedirs(folder)

    def convert_date(self, timestamp):
        year = datetime.fromtimestamp(timestamp).strftime('%Y')
        month = datetime.fromtimestamp(timestamp).strftime('%m')
        day = datetime.fromtimestamp(timestamp).strftime('%d')
        # return (year, month, day)
        return datetime.fromtimestamp(timestamp)

    def get_file_list(self, path):
        file_list = {}
        file_id = 1
        for root, dirs, files in os.walk(path):
            for file in files:
                file_list[file_id] = self.get_file_info(os.path.join(root, file))
                file_id += 1
                self.logger.info("%s files collected", file_id - 1)
        return file_list

    def get_file_checksum(self, fname):
        hash_md5 = hashlib.md5()
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def get_file_date(self, file_path):
        return os.path.getctime(file_path)

    def get_file_info(self, file_path):
        file_timestamp = self.get_file_date(file_path)

        file_info = {
            'name': os.path.basename(file_path),
            'path': file_path,
            'timestamp': file_timestamp,
            'date': datetime.fromtimestamp(file_timestamp),
            'checksum': self.get_file_checksum(file_path),
            'size': os.path.getsize(file_path)
        }
        self.logger.debug("File info: %s", file_info)
        return file_info


def main():
    """docstring for main"""
    # Create the parser
    cmd_parser = argparse.ArgumentParser(description='Offload files with checksum verification')

    # Add the arguments
    cmd_parser.add_argument('source',
                            metavar='source',
                            type=str,
                            help='The source folder')

    cmd_parser.add_argument('destination',
                            metavar='destination',
                            type=str,
                            help='The destination folder')

    # Execute the parse_args() method
    args = cmd_parser.parse_args()

    ol = Offloader(args.source, args.destination)
    ol.offload()


if __name__ == '__main__':
    main()
