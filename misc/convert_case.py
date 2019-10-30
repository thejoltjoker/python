#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
convert_case.py
Description of convert_case.py.
"""
import argparse


def convert_string_case(input_string):
    if input_string.upper:
        return input_string.input.upper()
    elif input_string.lower:
        return input_string.input.lower()
    elif input_string.title:
        return input_string.input.title()
    elif input_string.sentence:
        return input_string.input.capitalize()
    else:
        return input_string.input


def main():
    """convert input to different cases"""
    # Create the parser
    cmd_parser = argparse.ArgumentParser(
        description='Convert input to different cases')

    # Add the arguments
    cmd_parser.add_argument('input',
                            metavar='input',
                            type=str,
                            help='The input string')

    cmd_parser.add_argument('-l', '--lower',
                            action='store_true',
                            help='Convert string to lowercase')

    cmd_parser.add_argument('-u', '--upper',
                            action='store_true',
                            help='Convert string to UPPERCASE')

    cmd_parser.add_argument('-t', '--title',
                            action='store_true',
                            help='Convert string to Title Case')

    cmd_parser.add_argument('-s', '--sentence',
                            action='store_true',
                            help='Convert string to Sentence case')

    # Execute the parse_args() method
    args = cmd_parser.parse_args()

    # Convert string
    output = convert_string_case(args)

    print(output)


if __name__ == '__main__':
    main()
