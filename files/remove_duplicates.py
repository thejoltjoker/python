#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
remove_duplicates.py
Remove duplicate files
"""
import os
import argparse
import logging
from pathlib import Path

try:
    import xxhash

    HASHER = xxhash.xxh3_64
except ImportError as e:
    import hashlib

    HASHER = hashlib.md5
    logging.warning(f'xxhash not found, using md5')


def setup_logging(level=logging.INFO):
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(level)
    return logger


def file_checksum(path, block_size=65536):
    """Get the checksum for a file"""
    h = HASHER
    return h(path.read_bytes()).hexdigest()


def filelist(path, include_subfolders=False):
    """Returns a list of files"""
    if include_subfolders:
        return sorted([x for x in path.rglob('*.*') if x.is_file()])
    else:
        return sorted([x for x in path.iterdir() if x.is_file()])


def remove_duplicates(path, include_subfolders=False, move=False, dryrun=False):
    # Get hashes for existing files
    path = Path(path)
    move_path = path / '..' / f'{path.stem}_duplicates'
    if include_subfolders:
        logging.info(f'Looking for duplicates in {path}, including its subfolders')
    else:
        logging.info(f'Looking for duplicates in {path}')
    files = filelist(path, include_subfolders=include_subfolders)

    # Check for duplicates in path
    checksums = {}
    duplicates = 0
    for n, file in enumerate(files, 1):
        checksum = file_checksum(file)
        logging.info(f'Checking file {n}/{len(files)}: {file.name}\t|\t{checksum}')
        if checksums.get(checksum):
            duplicates += 1
            if dryrun:
                logging.info(f'Duplicate found')
                checksums[checksum].append(file)
            else:
                if move:
                    logging.info(f'Duplicate found, moving file')
                    move_path.mkdir(parents=True, exist_ok=True)
                    new_path = move_path / file.name
                    new_path.write_bytes(file.read_bytes())
                else:
                    logging.info(f'Duplicate found, deleting file')
                file.unlink()
        else:
            checksums[checksum] = [file]
    logging.info(f'{duplicates} duplicates found')
    if dryrun:
        for k, v in checksums.items():
            if len(v) > 1:
                logging.info(f'{len(v)} {k}:')
                logging.info("\n".join([str(x) for x in v]))


def main():
    """docstring for main"""
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='The path to look for duplicates')
    parser.add_argument('-s', '--include-subfolders', dest='subfolders', action='store_true',
                        help='Whether or not to scan in subfolders')
    parser.add_argument('-m', '--move', dest='move', action='store_true',
                        help='Move duplicate files instead of deleting')
    parser.add_argument('--dryrun', dest='dryrun', action='store_true',
                        help='Just test')
    args = parser.parse_args()
    remove_duplicates(args.path, args.subfolders, args.move, args.dryrun)


if __name__ == '__main__':
    setup_logging()
    main()
