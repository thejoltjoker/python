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
from unittest import TestCase

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


def filelist(path, exclude=None, include_subfolders=False):
    """Returns a list of files"""
    path = Path(path)

    if include_subfolders:
        files = [x for x in path.rglob('*.*') if x.is_file()]
    else:
        files = [x for x in path.iterdir() if x.is_file()]

    if exclude:
        if isinstance(exclude, str):
            exclude = [exclude]

        files = [x for x in files if not any(ex in str(x.resolve()) for ex in exclude)]
    # print(f'{len(files)} | {exclude} | {include_subfolders}')
    return sorted(files)


def remove_duplicates(path, include_subfolders=False, move=False, exclude=None, dryrun=False):
    # Get hashes for existing files
    path = Path(path)
    move_path = path / '..' / f'{path.stem}_duplicates'
    if include_subfolders:
        logging.info(f'Looking for duplicates in {path}, including its subfolders')
    else:
        logging.info(f'Looking for duplicates in {path}')
    if exclude:
        if isinstance(exclude, str):
            logging.info(f'Skipping any paths containing {exclude}')
        else:
            logging.info(f'Skipping any paths containing {", ".join([x for x in exclude])}')
    files = filelist(path, exclude=exclude, include_subfolders=include_subfolders)

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

    if dryrun:
        for k, v in checksums.items():
            if len(v) > 1:
                logging.info(f'{k}:')
                logging.info("\n".join([f'\t{y}: {x}' for y, x in enumerate(v, 1)]))

    logging.info('')
    logging.info(f'{duplicates} duplicates found')
    logging.info('')

def main():
    """docstring for main"""
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='The path to look for duplicates')
    parser.add_argument('-s', '--include-subfolders', dest='subfolders', action='store_true',
                        help='Whether or not to scan in subfolders')
    parser.add_argument('-m', '--move', dest='move', action='store_true',
                        help='Move duplicate files instead of deleting')
    parser.add_argument('-e', '--exclude', nargs='+', dest='exclude',
                        help='A string or list of strings to exclude if in full path')
    parser.add_argument('--dryrun', dest='dryrun', action='store_true',
                        help='Just test')

    args = parser.parse_args()
    remove_duplicates(args.path, args.subfolders, args.move, exclude=args.exclude, dryrun=args.dryrun)


if __name__ == '__main__':
    setup_logging()
    main()
