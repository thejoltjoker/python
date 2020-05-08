#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
sync_lightroom_catalogs.py
Keep lightroom catalogs up to date on different volumes.
"""
import os
import logging
import hashlib
import pprint
import datetime
import json
import time
import argparse
from pathlib import Path


def setup_logger():
    # Setup logger
    # logger = logging.getLogger(__name__)
    # handler = logging.StreamHandler()
    logging.basicConfig(level=logging.INFO, format='%(name)-10s %(levelname)8s %(message)s')
    # formatter = logging.Formatter('%(asctime)-20s %(name)-10s %(levelname)-8s %(message)s', "%Y-%m-%d %H:%M:%S")
    #
    # handler.setFormatter(formatter)
    # logger.addHandler(handler)
    # logger.setLevel(logging.DEBUG)
    # return logger


class LRSync:
    def __init__(self, catalogs_path=None):
        self.catalogs = []
        if catalogs_path is None:
            self.catalogs_path = Path("/Users/johannes/Dropbox/Pictures/lightroom/catalogs/lr_catalogs.json")

    @staticmethod
    def get_volumes_list():
        """returns a list of volumes"""
        return [os.path.join('/Volumes', d) for d in os.listdir('/Volumes')]

    @staticmethod
    def save_json(path, data):
        path = Path(path)
        with open(path, 'w') as outfile:
            json.dump(data, outfile)

    @staticmethod
    def hashfile(path, blocksize=65536):
        file = open(path, 'rb')
        hasher = hashlib.md5()
        buf = file.read(blocksize)
        while len(buf) > 0:
            hasher.update(buf)
            buf = file.read(blocksize)
        file.close()
        return hasher.hexdigest()

    def load_catalogs(self):
        if self.catalogs_path.exists():
            logging.debug(f"Loading paths from {self.catalogs_path}")
            with self.catalogs_path.open(mode="r") as json_file:
                catalogs_meta = json.load(json_file)
                return catalogs_meta
        else:
            logging.info(f"Couldn't load catalogs file from {self.catalogs_path}")
            return {}

    def get_catalogs(self, directory, save_to_file=True):
        catalogs_meta = {}
        directory = Path(directory)

        # Load paths from existing catalogs file if it exists
        catalogs_meta = self.load_catalogs()

        # Check if folder exists
        if directory.exists():
            logging.info(f"Scanning {directory} for Lightroom catalogs")

            # Walk through files and directories
            for root, dirs, files in os.walk(directory, topdown=True):

                # Skip backups folders
                if "Backups" in root:
                    continue

                # Skip lrdata folders
                dirs[:] = [x for x in dirs if not x.endswith(".lrdata")]

                # Get catalog files
                catalogs = [c for c in files if c.endswith('lrcat') and 'backups' not in root.lower()]

                # Save all catalogs and paths
                for cat in catalogs:
                    cat_path = str(Path(os.path.join(root, cat)).resolve())
                    # Add new catalog to data or append if it already exists
                    if cat not in catalogs_meta:
                        logging.debug(f"Adding {cat} to list of catalogs")
                        catalogs_meta[cat] = {
                            "sync": True,
                            "paths": [cat_path]
                        }
                    else:
                        logging.debug(f"{cat} already exists in list of catalogs, adding additional path")
                        if cat_path not in catalogs_meta[cat]["paths"]:
                            catalogs_meta[cat]["paths"].append(cat_path)

            # Save paths to file
            if save_to_file:
                self.save_json(self.catalogs_path, catalogs_meta)

        else:
            logging.warning("Directory doesn't exist")
            return None

        return catalogs_meta

    def get_latest_catalog(self, catalog_name):
        catalog_meta = self.load_catalogs()
        catalog_paths = catalog_meta[catalog_name]['paths']

        paths = {}

        # Iterate through paths
        for cat in catalog_paths:
            # Set some meta variables
            path = Path(cat)
            catalog_change_date = path.lstat().st_mtime

            # Create new key if not existing
            if not paths:
                paths = {
                    path.absolute().resolve(): catalog_change_date
                }
            else:
                paths[path.absolute().resolve()] = catalog_change_date

        # Get most recently modified file
        latest = max(paths, key=paths.get)

        return latest


def main():
    """docstring for main"""

    # Create LRSync object
    lr_sync = LRSync()

    # Get list of volumes
    # volumes = lr_sync.get_volumes_list()
    # print(volumes)

    # Scan for catalogs and save to file
    # path = "/Volumes/mcdaddy/Pictures/lightroom/catalogs"
    # catalogs = lr_sync.get_catalogs(path)
    # pprint.pprint(catalogs)

    # Get latest catalog
    print(lr_sync.get_latest_catalog("lr_classic_2019_002.lrcat"))

    # List catalogs with more than one copy
    cat_meta = lr_sync.load_catalogs()
    inc = 1
    for c in sorted(cat_meta):
        copy_count = len(cat_meta[c]['paths'])
        if copy_count > 1:
            print(f"{inc}: {c} ({copy_count})")
            inc += 1


def cli():
    """Command line interface"""
    # Load LRSync object
    lr_sync = LRSync()
    catalog_meta = lr_sync.load_catalogs()
    syncable_catalogs = {x: y for x, y in catalog_meta.items() if len(y["paths"]) > 1}

    # Create the parser
    parser = argparse.ArgumentParser(description="Sync Lightroom catalogs")

    # Add the arguments
    parser.add_argument("-s", "--sync",
                        type=str,
                        help="Sync catalogs",
                        action="store")

    parser.add_argument("-l", "--list",
                        help="Move files instead of copy",
                        action="store_true")

    # Execute the parse_args() method
    args = parser.parse_args()

    # Print the title
    print("Lightroom Sync")
    print("")

    if args.list:
        print("Here are all the catalogs with multiple paths.")
        print("The most recently modified is marked with a star.")
        for cat in sorted(syncable_catalogs):
            print(cat)
            latest = str(lr_sync.get_latest_catalog(cat))

            for p in catalog_meta[cat]["paths"]:
                path = Path(p)
                formatted_time = datetime.datetime.utcfromtimestamp(path.lstat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                if p == latest:
                    print(f"* \t{p} ({formatted_time})")
                else:
                    print(f"\t{p} ({formatted_time})")
            print("")
    # if args.sync is None:
    #     print(f"Choose a catalog to sync:")
    #     for n, cat in enumerate(sorted(syncable_catalogs), 1):
    #         print(f"{n}: {cat}")
    #
    # while True:
    #     try:
    #         source_input = int(input("> ").strip())
    #         if volumes.get(source_input):
    #             source = volumes[source_input]
    #             break
    #         else:
    #             print("Invalid choice. Try again.")
    #
    #     except:
    #         print("Invalid selection")
    #         exit(1)
    # else:
    #     source = args.source

    print("")


if __name__ == '__main__':
    setup_logger()
    cli()
