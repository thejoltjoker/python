#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
script_run_timer.py
Description of script_run_timer.py.
"""
import time


def main():
    """docstring for main"""
    start_time = time.time()
    print(start_time)

    time.sleep(1)
    print(time.time() - start_time)

if __name__ == '__main__':
    main()
