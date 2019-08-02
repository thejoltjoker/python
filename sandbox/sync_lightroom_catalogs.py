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


def get_volumes_list():
    """returns a list of volumes"""
    return [os.path.join('/Volumes', d) for d in os.listdir('/Volumes')]


def hashfile(path, blocksize=65536):
    file = open(path, 'rb')
    hasher = hashlib.md5()
    buf = file.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = file.read(blocksize)
    file.close()
    return hasher.hexdigest()


def get_catalogs(volume):
    catalogs_meta = {}
    lr_work_path = os.path.join('/Volumes', volume, 'pictures', 'lightroom', 'catalogs')
    # Check if folder exists
    if os.path.isdir(lr_work_path):
        logger.debug(lr_work_path)
        for root, dirs, files in os.walk(lr_work_path, topdown=True):
            catalogs = [c for c in files if c.endswith('lrcat') and 'backups' not in root.lower()]
            for cat in catalogs:
                cat_path = os.path.join(root, cat)
                catalogs_meta[cat] = {
                    "path": cat_path,
                    "rel_path": cat_path.replace(lr_work_path, ''),
                    "last_modified": os.path.getmtime(cat_path),
                    "md5": hashfile(cat_path)
                }
                logger.debug(catalogs_meta[cat])
    logger.debug(catalogs_meta)
    return catalogs_meta


def main():
    """docstring for main"""
    volumes = get_volumes_list()
    catalogs_meta = {}
    for vol in volumes:
        vol = os.path.basename(vol)
        catalogs_meta[vol] = get_catalogs(vol)
    logger.info(catalogs_meta)
    pprint.pprint(catalogs_meta)


if __name__ == '__main__':
    # Setup logger
    logger = logging.getLogger(__name__)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    main()
