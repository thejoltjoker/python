#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
script_name.py
Description of script_name.py.
"""
import argparse
import xxhash
from pathlib import Path


def file_checksum(file_path, block_size=65536):
    """Get the checksum for a file"""
    path = Path(file_path)
    h = xxhash.xxh64()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(block_size), b""):
            h.update(chunk)
        return h.hexdigest()


def main():
    """docstring for main"""
    parser = argparse.ArgumentParser(description="Get the xxhash checksum for a file")
    parser.add_argument("file",
                        help="The file to get checksum for",
                        type=str)
    args = parser.parse_args()

    if args:
        print(file_checksum(args.file))


if __name__ == '__main__':
    main()
