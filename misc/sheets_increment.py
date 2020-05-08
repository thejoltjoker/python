#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
sheets_increment.py
Increment sheet numbers in formulas
"""


def main():
    for i in range(100):
        i = i+1
        print(f"=IF(ISBLANK(R{i}),,ROUNDUP(W{i}*R{i}*VARIABLER!B3))")


if __name__ == '__main__':
    main()
