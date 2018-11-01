#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
extract_hashtags.py
Description of extract_hashtags.py.
"""


def main():
    """docstring for main"""
    jens = {tag.strip("#") for tag in caption.split() if tag.startswith("#")}
    print jens


if __name__ == '__main__':
    main()
