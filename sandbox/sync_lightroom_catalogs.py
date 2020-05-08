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
import json
from pathlib import Path


def setup_logger():
    # Setup logger
    # logger = logging.getLogger(__name__)
    # handler = logging.StreamHandler()
    logging.basicConfig(level=logging.DEBUG, format='%(name)-10s %(levelname)8s %(message)s')
    # formatter = logging.Formatter('%(asctime)-20s %(name)-10s %(levelname)-8s %(message)s', "%Y-%m-%d %H:%M:%S")
    #
    # handler.setFormatter(formatter)
    # logger.addHandler(handler)
    # logger.setLevel(logging.DEBUG)
    # return logger


class LRSync:
    def __init__(self):
        self.catalogs = []

    @staticmethod
    def get_volumes_list():
        """returns a list of volumes"""
        return [os.path.join('/Volumes', d) for d in os.listdir('/Volumes')]

    @staticmethod
    def save_json(path, data):
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

    def update_catalogs_list(self, volumes):
        catalogs = {}
        for vol in volumes:
            catalogs[vol] = self.get_catalogs(vol)

    def get_catalogs(self, directory, save_to_file=True):
        catalogs_meta = {}
        directory = Path(directory)

        # Check if folder exists
        if directory.exists():
            logging.debug(directory)
            for root, dirs, files in os.walk(directory, topdown=True):
                if "Backups" in root:
                    continue
                # Skip lrdata folders
                dirs[:] = [x for x in dirs if not x.endswith(".lrdata")]

                # Get catalog files
                catalogs = [c for c in files if c.endswith('lrcat') and 'backups' not in root.lower()]

                for cat in catalogs:
                    cat_path = Path(os.path.join(root, cat))
                    catalogs_meta[cat] = {
                        "path": cat_path,
                        "last_modified": cat_path.stat().st_mtime,
                        "md5": self.hashfile(cat_path)
                    }
                    logging.debug(catalogs_meta[cat])
        logging.debug(catalogs_meta)
        return catalogs_meta


def main():
    """docstring for main"""
    # volumes = get_volumes_list()
    # volumes = ['mcdaddy', 'mcdrive']
    # catalogs_meta = {}
    # for vol in volumes:
    #     vol = os.path.basename(vol)
    #     catalogs_meta[vol] = get_catalogs(vol)
    #
    # pprint.pprint(catalogs_meta)
    lr_sync = LRSync()
    # volumes = lr_sync.get_volumes_list()
    # print(volumes)
    catalogs = lr_sync.get_catalogs("/Volumes/mcdaddy/pictures/lightroom/catalogs")
    pprint.pprint(catalogs)


if __name__ == '__main__':
    setup_logger()
    main()
