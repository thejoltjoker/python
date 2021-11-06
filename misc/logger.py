#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
script_name.py
Description of script_name.py.
"""

import logging
from pathlib import Path

def setup_logger(level=logging.DEBUG, file_handler=False):
    """Create a logger with file and stream handler
    Args:
        level: The level of verbosity for the logger
        file_handler: Whether or not to save log to file

    Returns:
        logger object
    """
    fh = None
    # Create logger
    logger = logging.getLogger(__name__)
    if logger.hasHandlers():
        logger.handlers.clear()

    # Set level
    logger.setLevel(level)

    # Create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    if file_handler:
        # Create file handler and set level to debug
        fh = logging.FileHandler(f'{__name__}.log', mode='a')
        fh.setLevel(logging.DEBUG)

    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Add formatter
    ch.setFormatter(formatter)
    if file_handler:
        fh.setFormatter(formatter)

    # Add handlers to logger
    logger.addHandler(ch)
    if file_handler:
        logger.addHandler(fh)

    return logger


def main():
    """docstring for main"""
    setup_logger()
    logging.debug('Logger setup')
    logging.info('Logger setup')


if __name__ == '__main__':
    main()
