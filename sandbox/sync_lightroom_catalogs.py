#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
sync_lightroom_catalogs.py
Description of sync_lightroom_catalogs.py.
"""
import os
import logging
import hashlib
import pprint
import json


class LRSync:
    def __init__(self):
        self.catalogs = []
        self.logger = self.setup_logger()

    def setup_logger(self):
        # Setup logger
        logger = logging.getLogger(__name__)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)-20s %(name)-10s %(levelname)-8s %(message)s', "%Y-%m-%d %H:%M:%S")

        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
        return logger

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

    def get_catalogs(self, volume):
        catalogs_meta = {}
        lr_work_path = os.path.join(
            '/Volumes', volume, 'pictures', 'lightroom', 'catalogs')
        # Check if folder exists
        if os.path.isdir(lr_work_path):
            self.logger.debug(lr_work_path)
            for root, dirs, files in os.walk(lr_work_path, topdown=True):
                catalogs = [c for c in files if c.endswith(
                    'lrcat') and 'backups' not in root.lower()]
                for cat in catalogs:
                    cat_path = os.path.join(root, cat)
                    catalogs_meta[cat] = {
                        "path": cat_path,
                        "rel_path": cat_path.replace(lr_work_path, ''),
                        "last_modified": os.path.getmtime(cat_path),
                        "md5": self.hashfile(cat_path)
                    }
                    self.logger.debug(catalogs_meta[cat])
        self.logger.debug(catalogs_meta)
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
    volumes = lr_sync.get_volumes_list()
    print(volumes)
    catalogs = lr_sync.get_catalogs('mcdrive')
    print(catalogs)

if __name__ == '__main__':
    main()
