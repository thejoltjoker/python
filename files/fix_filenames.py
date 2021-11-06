#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
fix_filenames.py
Remove illegal characters from filenames.
"""
import argparse
import os
import string

# from pathlib import Path
VALID_CHARACTERS = " -_.+{letters}{digits}".format(
    letters=string.ascii_letters, digits=string.digits)
INVALID_CHARACTERS = r'~\/:*?"<>|'
CHARACTER_TABLE = {
    # ' ': '_',
    '¡': '!',
    '¿': '?',
    'ä': 'a', 'à': 'a', 'á': 'a', 'â': 'a', 'ã': 'a', 'å': 'a', 'ǎ': 'a', 'ą': 'a', 'ă': 'a', 'æ': 'a', 'ā': 'a',
    'ç': 'c', 'ć': 'c', 'ĉ': 'c', 'č': 'c', 'ď': 'c', 'đ': 'c', 'ð': 'c',
    'è': 'e', 'é': 'e', 'ê': 'e', 'ë': 'e', 'ě': 'e', 'ę': 'e', 'ė': 'e', 'ē': 'e',
    'ĝ': 'g', 'ģ': 'g', 'ğ': 'g',
    'ĥ': 'h',
    'ì': 'i', 'í': 'i', 'î': 'i', 'ï': 'i', 'ı': 'i', 'ī': 'i', 'į': 'i',
    'ĵ': 'j',
    'ķ': 'k',
    'ĺ': 'l', 'ļ': 'l', 'ł': 'l', 'ľ': 'l', 'ŀ': 'l',
    'ñ': 'n', 'ń': 'n', 'ň': 'n', 'ņ': 'n',
    'ö': 'o', 'ò': 'o', 'ó': 'o', 'ô': 'o', 'õ': 'o', 'ő': 'o', 'ø': 'o', 'œ': 'o',
    'ŕ': 'r', 'ř': 'r',
    # 'ẞ': 's',
    # 'ß': 'ss',
    'ś': 's', 'ŝ': 's', 'ş': 's', 'š': 's', 'ș': 's',
    'ť': 't', 'ţ': 't', 'þ': 't', 'ț': 't',
    'ü': 'u', 'ù': 'u', 'ú': 'u', 'û': 'u', 'ű': 'u', 'ũ': 'u', 'ų': 'u', 'ů': 'u', 'ū': 'u',
    'ŵ': 'w',
    'ý': 'y', 'ÿ': 'y', 'ŷ': 'y',
    'ź': 'z', 'ž': 'z', 'ż': 'z'
}


def replace_characters(input_string: str):
    """Replace characters based on table"""
    output_string = input_string
    for k, v in CHARACTER_TABLE.items():
        output_string = output_string.replace(k, v)
        output_string = output_string.replace(k.upper(), v.upper())
    return output_string


def remove_characters(input_string: str):
    """Remove illegal characters"""
    return ''.join(c for c in input_string if c not in INVALID_CHARACTERS)
    # return ''.join(c for c in input_string if c in VALID_CHARACTERS)


def convert_filename(filename):
    """Fix a filename"""
    # Try and replace illegal characters
    filename = replace_characters(filename)

    # Remove remaining illegal characters
    filename = remove_characters(filename)

    return filename


def rename(root, name):
    """Rename a file or a folder with correct characters"""
    inc = 1
    converted_name = convert_filename(name)
    old_path = os.path.join(root, name)
    new_path = os.path.join(root, converted_name)

    while True:
        if old_path != new_path and os.path.exists(new_path):
            print(f'{os.path.basename(new_path)} exists, incrementing')
            new_name = f'{os.path.splitext(converted_name)[0]}_{inc:03d}{os.path.splitext(converted_name)[-1]}'
            new_path = os.path.join(root, new_name)
            inc += 1
        else:
            # os.rename(old_path, new_path)
            break

    return old_path, new_path


def fix_filenames(path, include_subfoldes=False, folder_names=False):
    """docstring for fix_filenames"""

    for root, folders, files in os.walk(path):
        # Rename folders
        # if folder_names:
        #     for folder in folders:
        #         old, new = rename(root, folder)
        #         if old != new:
        #             print(f"{os.path.relpath(old, path)} -> {os.path.relpath(new, path)}")
        #         # Replace old folder name with new for os.walk
        #         folders = [os.path.basename(new) if x == os.path.basename(old) else x for x in folders]
        #         print(folders)

        for file in files:
            old, new = rename(root, file)
            if old != new:
                print(f"{os.path.relpath(old, path)} -> {os.path.relpath(new, path)}")

        # Stop if include subfolders is false
        if not include_subfoldes:
            return


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fix all filenames in given folder')
    parser.add_argument('path',
                        help='The path to search for files')
    parser.add_argument('-s', '--include-subfolders', action='store_true',
                        help='Search for files in subfolders (default: False)')
    parser.add_argument('-f', '--include-foldernames', action='store_true',
                        help='Rename folders as well (default: False)')

    args = parser.parse_args()
    print(args)
    if os.path.isdir(args.path):
        fix_filenames(args.path, args.include_subfolders, args.include_foldernames)
    else:
        print(f'{args.path} is not a directory')