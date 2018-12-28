#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
rename_dv_tapes_files.py
Description of rename_dv_tapes_files.py.
"""
import os
import re
import shutil


def main():
    path = r"/Volumes/data_a/media/dv/tapes"
    """docstring for main"""
    for folder, root, filenames in os.walk(path):
        for f in [f for f in filenames if not '.jpg' in f]:
            # print(folder)
            # print("old filename: {}".format(f))
            split_filename = re.split('_|\.', f)
            new_filename = "{name}.{ext}".format(
                name=split_filename[0], ext=split_filename[-1])

            if split_filename[0] not in folder:
                # print(folder)
                if not os.path.exists(os.path.join(folder, split_filename[0])):
                    print(os.path.join(folder, split_filename[0]))
                    os.makedirs(os.path.join(folder, split_filename[0]))

                print("{old} => {new}".format(old=os.path.join(folder, f),
                                              new=os.path.join(folder, split_filename[0], new_filename)))
                shutil.move(os.path.join(folder, f),
                            os.path.join(folder, split_filename[0], new_filename))
            elif f != new_filename:
                print("{old} => {new}".format(
                    old=os.path.join(folder, f), new=os.path.join(folder, new_filename)))

                shutil.move(os.path.join(folder, f),
                            os.path.join(folder, new_filename))


if __name__ == '__main__':
    main()
