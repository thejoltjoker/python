#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
script_name.py
Description of script_name.py.
"""
# TODO multiple destinations
# TODO make it easier to customize 7:45 torsdag 24
import os
import hashlib
import xxhash
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
                        'AVIN0001.INT',
                        'mdb.bk',
                        'mdb.db',
                        'Get_started_with_GoPro.url',
                        '.Spotlight-V100',
                        'VolumeConfiguration.plist',
                        'psid.db',
                        'indexState',
                        '0.indexHead',
                        '0.indexGroups',
                        'live.0.indexPostings',
                        'live.0.indexIds',
                        'live.0.indexBigDates',
                        'live.0.indexGroups',
                        'live.0.indexPositions',
                        'live.0.indexDirectory',
                        'live.0.indexCompactDirectory',
                        'live.0.indexArrays',
                        'live.0.shadowIndexHead',
                        'live.0.directoryStoreFile',
                        'live.0.directoryStoreFile.shadow',
                        'store.db',
                        '.store.db',
                        'reverseDirectoryStore',
                        'tmp.spotlight.state',
                        'shutdown_time',
                        'reverseDirectoryStore.shadow',
                        '0.shadowIndexHead',
                        'store.updates',
                        'permStore',
                        'live.1.indexHead',
                        'live.1.indexIds',
                        '0.shadowIndexGroups',
                        'live.1.indexUpdates',
                        'live.2.indexHead',
                        'live.2.indexIds',
                        'live.2.indexBigDates',
                        'live.2.indexGroups',
                        'live.0.shadowIndexGroups',
                        'reverseStore.updates',
                        'live.1.indexBigDates',
                        'tmp.spotlight.loc',
                        'live.1.indexGroups',
                        'live.1.indexPostings',
                        'live.1.indexTermIds',
                        'live.1.indexDirectory',
                        'live.1.indexCompactDirectory',
                        'live.1.indexArrays',
                        'live.2.indexPostings',
                        'live.1.directoryStoreFile',
                        'live.1.shadowIndexHead',
                        'live.1.shadowIndexTermIds',
                        'live.1.shadowIndexArrays',
                        'live.1.shadowIndexCompactDirectory',
                        'live.1.shadowIndexDirectory',
                        'live.1.directoryStoreFile.shadow',
                        'live.1.shadowIndexGroups',
                        'live.2.indexTermIds',
                        'live.2.indexPositions',
                        'live.2.indexPositionTable',
                        'live.2.indexDirectory',
                        'live.2.indexCompactDirectory',
                        'live.2.indexArrays',
                        'live.2.indexUpdates',
                        'live.2.directoryStoreFile',
                        'live.2.shadowIndexHead',
                        'live.2.shadowIndexTermIds',
                        'live.2.shadowIndexPositionTable',
                        'live.2.shadowIndexArrays',
                        'live.2.shadowIndexCompactDirectory',
                        'live.2.shadowIndexDirectory',
                        'live.2.directoryStoreFile.shadow',
                        'live.2.shadowIndexGroups',
                        'live.0.indexHead',
                        'journal.412',
                        'retire.411']

    def setup_logger(self):
        # Setup logger
        logger = logging.getLogger(__name__)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)-20s %(name)-10s %(levelname)-8s %(message)s', "%Y-%m-%d %H:%M:%S")

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
        total_file_size = sum([source_file_list[x]['size']
                               for x in source_file_list])
        total_transferred_size = 0
        self.logger.info("Total file size: %s",
                         self.convert_size(total_file_size))
        self.logger.info("---\n")

        # Get start time to calculate remaining time
        start_time = time.time()

        # Iterate files in list
        for file_id in source_file_list:
            incremental = 0
            current_file = source_file_list[file_id]

            self.logger.info("Processing file %s/%s (~%s%%) | %s", file_id, len(source_file_list),
                             round((total_transferred_size /
                                    total_file_size) * 100, 2),
                             current_file['name'])

            # Skip file if it's in the exclude list
            if current_file['name'] in self.exclude:
                self.logger.warning('Filename in exclude list %s, skipping',
                                    current_file['name'])

                # Check if file already exists at destination
                skipped_files.append(current_file['name'])

            # If file is not in include list move on to copy
            else:
                while True:
                    if self.original_structure:
                        new_filename = current_file['name']
                        dest_file_path = os.path.join(
                            current_file['path'].replace(self.source, self.destination))
                    else:
                        # Create destination path
                        new_filename = self.create_new_filename(
                            current_file, incremental)

                        dest_file_path = os.path.join(self.destination,
                                                      current_file['date'].strftime(
                                                          '%Y'),
                                                      current_file['date'].strftime(
                                                          '%Y-%m-%d'),
                                                      new_filename)

                    # Check if file already exists at destination
                    if os.path.isfile(dest_file_path):

                        self.logger.info(
                            'File with the same name exists in destination, comparing checksums')
                        # Get file info for existing file
                        dest_file_info = self.get_file_info(dest_file_path)

                        # Compare checksums
                        # if current_file['checksum'] == dest_file_info['checksum']:
                        if self.compare_checksums(current_file['path'], dest_file_info['path']):
                            self.logger.warning('File %s (%s) already exists in destination, skipping',
                                                dest_file_info['name'],
                                                current_file['name'])
                            # self.logger.warning('Checksums: %s (source)| %s (destination)',
                            #                     current_file['checksum'],
                            #                     dest_file_info['checksum'])
                            self.logger.debug('Source: %s', current_file)
                            self.logger.debug(
                                'Destination: %s', dest_file_info)

                            # Add file to skipped list
                            skipped_files.append(current_file['name'])

                            break

                        # If file with same name exists but has mismatching checksums
                        else:
                            self.logger.warning(
                                'File with same name %s (%s) already exists in destination, adding incremental',
                                dest_file_info['name'],
                                current_file['name'])
                            # self.logger.warning('Checksums: %s (source)| %s (destination)',
                            #                     current_file['checksum'],
                            #                     dest_file_info['checksum'])
                            self.logger.debug('Source: %s', current_file)
                            self.logger.debug(
                                'Destination: %s', dest_file_info)

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
                                self.logger.info(
                                    "Moving %s", self.convert_size(current_file['size']))
                            else:
                                self.logger.info(
                                    "Copying %s", self.convert_size(current_file['size']))
                            self.logger.info(
                                "Source: %s", current_file['path'])
                            self.logger.info("Destination: %s", dest_file_path)

                            # Get checksum
                            # current_file['checksum'] = self.get_file_checksum_xxhash(
                            #     current_file['path'])

                            if self.dryrun:
                                self.logger.info("DRYRUN ENABLED, NOT COPYING")
                            else:
                                if self.move:
                                    self.move_file(
                                        current_file['path'], dest_file_path)
                                else:
                                    self.copy_file(
                                        current_file['path'], dest_file_path)

                                # Verify transferred file
                                self.logger.info(
                                    'Verifying transferred file')
                                if self.compare_checksums(
                                        current_file['path'], dest_file_path):
                                    self.logger.info(
                                        'File %s transferred successfully', current_file['name'])

                            # Add file to transferred list
                            transferred_files.append(current_file['name'])

                        except Exception as e:
                            self.logger.error(e)
                        break

            # Add file size to total
            total_transferred_size += current_file['size']

            # Calculate remaining time
            elapsed_time = time.time() - start_time
            self.logger.debug("Elapsed time: %s", time.strftime(
                '%-M min %-S sec', time.gmtime(elapsed_time)))

            bytes_per_second = 0.00001 + total_transferred_size / elapsed_time
            self.logger.debug("Avg. transfer speed: %s/s",
                              self.convert_size(bytes_per_second))

            size_remaining = 0.00001 + total_file_size - total_transferred_size
            time_remaining = 0.00001 + size_remaining / bytes_per_second
            self.logger.debug("Size remaining: %s",
                              self.convert_size(size_remaining))
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
                                         os.path.splitext(
                                             file_info['name'])[0],
                                         "{:03d}{}".format(incremental, os.path.splitext(file_info['name'])[1])])

            else:
                new_filename = "_".join([file_info['date'].strftime('%y%m%d'),
                                         file_info['name']])

        return new_filename

    def compare_checksums(self, source, destination, hashtype='xxhash'):
        source_hash = self.get_file_checksum(source)
        dest_hash = self.get_file_checksum(destination)
        if dest_hash == source_hash:
            self.logger.debug(
                'Checksums match: %s (source)| %s (destination)', source_hash, dest_hash)
            return True
        else:
            self.logger.warning(
                'Checksums mismatch: %s (source)| %s (destination)', source_hash, dest_hash)
            return False

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
                file_list[file_id] = self.get_file_info(
                    os.path.join(root, file))

                # Append file size
                total_file_size += file_list[file_id]['size']

                # Increment file id
                file_id += 1

                self.logger.info("%s files collected", file_id - 1)
                self.logger.debug("Total size collected: %s",
                                  self.convert_size(total_file_size))
        return file_list

    def get_file_checksum_md5(self, fname):
        hash_md5 = hashlib.md5()
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def get_file_checksum_xxhash(self, fname):
        hash_xxhash = xxhash.xxh64()
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_xxhash.update(chunk)
        return hash_xxhash.hexdigest()

    def get_file_checksum(self, file):
        return self.get_file_checksum_xxhash(file)

    def get_file_date(self, file_path):
        return os.path.getmtime(file_path)

    def get_file_info(self, file_path):
        file_timestamp = self.get_file_date(file_path)

        file_info = {
            'name': os.path.basename(file_path),
            'path': file_path,
            'timestamp': file_timestamp,
            'date': datetime.datetime.fromtimestamp(file_timestamp),
            'size': os.path.getsize(file_path)
        }
        self.logger.debug("File info: %s", file_info)
        return file_info


def main():
    """docstring for main"""
    # Create the parser
    cmd_parser = argparse.ArgumentParser(
        description='Offload files with checksum verification')

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
    ol = Offloader(args.source, args.destination,
                   args.original_structure, args.move, args.dryrun)
    ol.offload()


if __name__ == '__main__':
    main()
