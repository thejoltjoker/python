#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
script_name.py
Description of script_name.py.
"""
# TODO verify files after copy
# TODO multiple destinations
# TODO make it easier to customize
import os
import hashlib
import logging
import datetime
import shutil
import math
import argparse
import time


class Offloader:
    def __init__(self, source, dest, original_structure, move, dryrun):
        self.logger = self.setup_logger()
        self.source = source
        self.destination = dest
        self.original_structure = original_structure
        self.move = move
        self.dryrun = dryrun
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
        created_folders = []

        # Get list of files to transfer
        source_file_list = self.get_file_list(self.source)

        # Get total file size to calculate percentage
        total_file_size = sum([source_file_list[x]['size'] for x in source_file_list])
        total_transferred_size = 0
        self.logger.info("Total file size: %s", self.convert_size(total_file_size))
        self.logger.info("---\n")

        # Get start time to calculate remaining time
        start_time = time.time()

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
                    if self.original_structure:
                        new_filename = current_file['name']
                        dest_file_path = os.path.join(current_file['path'].replace(self.source, self.destination))
                    else:
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
                        new_folder = os.path.dirname(dest_file_path)
                        if not self.dryrun:
                            self.create_folder(new_folder)

                        if new_folder not in created_folders:
                            created_folders.append(new_folder)

                        # Copy file
                        try:
                            if self.move:
                                self.logger.info("Moving %s", self.convert_size(current_file['size']))
                            else:
                                self.logger.info("Copying %s", self.convert_size(current_file['size']))
                            self.logger.info("Source: %s", current_file['path'])
                            self.logger.info("Destination: %s", dest_file_path)

                            if self.dryrun:
                                self.logger.info("DRYRUN ENABLED, NOT COPYING")
                            else:
                                if self.move:
                                    self.move_file(current_file['path'], dest_file_path)
                                else:
                                    self.copy_file(current_file['path'], dest_file_path)

                            # Add file to transferred list
                            transferred_files.append(current_file['name'])

                        except Exception as e:
                            self.logger.error(e)
                        break

            # Add file size to total
            total_transferred_size += current_file['size']

            # Calculate remaining time
            elapsed_time = time.time() - start_time
            self.logger.debug("Elapsed time: %s", time.strftime('%-M min %-S sec', time.gmtime(elapsed_time)))

            bytes_per_second = total_transferred_size / elapsed_time
            self.logger.debug("Avg. transfer speed: %s/s", self.convert_size(bytes_per_second))

            size_remaining = total_file_size - total_transferred_size
            time_remaining = size_remaining / bytes_per_second
            self.logger.debug("Size remaining: %s", self.convert_size(size_remaining))
            self.logger.debug("Approx. time remaining: %s",
                              time.strftime('%-M min %-S sec', time.gmtime(time_remaining)))

            self.logger.info("---\n")

        self.logger.info("%s files transferred", len(transferred_files))
        self.logger.debug("Transferred files: %s", transferred_files)

        self.logger.info("%s folders created", len(created_folders))
        self.logger.debug("Created folders: %s", created_folders)

        self.logger.info("%s files skipped", len(skipped_files))
        self.logger.debug("Skipped files: %s", skipped_files)

    def create_new_filename(self, file_info, incremental=0):
        if self.original_structure:
            if incremental >= 1:
                new_filename = "_".join([os.path.splitext(file_info['name'])[0],
                                         "{:03d}{}".format(incremental, os.path.splitext(file_info['name'])[1])])
            else:
                new_filename = file_info['name']
        else:
            if incremental >= 1:
                new_filename = "_".join([file_info['date'].strftime('%y%m%d'),
                                         os.path.splitext(file_info['name'])[0],
                                         "{:03d}{}".format(incremental, os.path.splitext(file_info['name'])[1])])

            else:
                new_filename = "_".join([file_info['date'].strftime('%y%m%d'),
                                         file_info['name']])

        return new_filename

    def copy_file(self, source, destination):
        shutil.copyfile(source, destination)

    def move_file(self, source, destination):
        shutil.move(source, destination)

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
        return datetime.datetime.fromtimestamp(timestamp)

    def get_file_list(self, path):
        file_list = {}
        file_id = 1
        total_file_size = 0
        for root, dirs, files in os.walk(path):
            for file in files:
                self.logger.debug("Getting file info for %s", file)
                file_list[file_id] = self.get_file_info(os.path.join(root, file))

                # Append file size
                total_file_size += file_list[file_id]['size']

                # Increment file id
                file_id += 1

                self.logger.info("%s files collected", file_id - 1)
                self.logger.debug("Total size collected: %s", self.convert_size(total_file_size))
        return file_list

    def get_file_checksum(self, fname):
        hash_md5 = hashlib.md5()
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def get_file_date(self, file_path):
        return os.path.getmtime(file_path)

    def get_file_info(self, file_path):
        file_timestamp = self.get_file_date(file_path)

        file_info = {
            'name': os.path.basename(file_path),
            'path': file_path,
            'timestamp': file_timestamp,
            'date': datetime.datetime.fromtimestamp(file_timestamp),
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

    cmd_parser.add_argument('--original-structure',
                            help='Copies with original filenames and structure',
                            action='store_true')

    cmd_parser.add_argument('--move',
                            help='Move files instead of copy',
                            action='store_true')

    cmd_parser.add_argument('--dryrun',
                            help='Run the script without actually copying anything',
                            action='store_true')

    # Execute the parse_args() method
    args = cmd_parser.parse_args()

    # Run offloader
    ol = Offloader(args.source, args.destination, args.original_structure, args.move,args.dryrun)
    ol.offload()


if __name__ == '__main__':
    main()
