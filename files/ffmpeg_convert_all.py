#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ffmpeg_convert_all.py
Description of ffmpeg_convert_all.py.
"""
import os
import time
import shutil

# options
source_folder = '/Volumes/mcbeast/temp_media/sorted/videos'
new_file_ext = 'mp4'

print('Source folder is {}'.format(source_folder))


def convert_file(source, destination):
    os.system(
        # 'ffmpeg -i {input} -c:v prores_ks {output}'.format(input=source, output=destination))
        'ffmpeg -i {input} {output}'.format(input=source, output=destination))
    pass


def main():
    """docstring for main"""

    for subdir, dirs, files in os.walk(source_folder):
        for file in files:

            if not file.endswith(new_file_ext):
                file_path = os.path.join(subdir, file)

                # debug stuff
                print('File name: {}'.format(file))
                print('Path: {}'.format(file_path))

                converted_file_path = '{path}.{ext}'.format(
                    path=os.path.splitext(file_path)[0], ext=new_file_ext)
                convert_file(file_path, converted_file_path)
                print("{src} converted to {dest}".format(
                    src=file_path, dest=converted_file_path))


if __name__ == '__main__':
    main()
