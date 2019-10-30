#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
setup_logger.py
Description of setup_logger.py.
"""
import logging


class App:
    def __init__(self):
        self.logger = self.setup_logger()

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


def main():
    """docstring for main"""
    pass


if __name__ == '__main__':
    main()
