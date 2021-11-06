#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
create_contact_sheet.py
Description of create_contact_sheet.py.
"""
import sys
import argparse
from pathlib import Path
import subprocess


def run_montage(input_files, output_path, width):
    """Run exiftool in subprocess and return the output"""
    # montage -geometry 300x300+10+10 -label '%f' -fill "#ffffff" -background "#111111" *.jpg index.jpg
    output_path = Path(output_path)
    files = "\n".join(sorted(input_files))
    temp_list_path = Path().home() / "_cs_temp_file_list.txt"
    temp_list_path.write_text(files)

    print(f"Running montage for {output_path.parent}")
    cmd = ["montage",
           "-geometry", f"{width}x{width}^+10+10",
           "-gravity", "center",
           "-crop", f"1:1",
           "+repage",
           # "-label", "%f",
           # "-fill", "#ffffff",
           "-background", "#ffffff",
           f"@{temp_list_path}", output_path]
    try:
        s = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        s = s.stdout.read()

        return s.strip()

    except subprocess.CalledProcessError as e:
        print(e)
        return None


def create_contact_sheet(photos_folder):
    """docstring for main"""
    directory = Path(photos_folder)
    files = [str(x.resolve()) for x in directory.iterdir() if not str(x).endswith("index.jpg")]
    folders = [str(x.resolve()) for x in directory.iterdir() if x.is_dir()]
    output_file = directory / f"{directory.name}_index.jpg"

    # run_montage(files, output_file)
    if folders:
        for f in folders:
            directory = Path(f)
            files = [str(x.resolve()) for x in directory.iterdir() if not str(x).endswith("index.jpg")]
            output_file = directory / f"{directory.name}_index.jpg"
            run_montage(files, output_file, width=400)
    else:
        run_montage(files, output_file, width=400)
    # if sys.argv[1]:
    #     img = Path(sys.argv[1])
    #     output_file = Path(img.parent)/f"{str(img.name).split('.')[0]}.txt"


#     output_file.write_text(str(img))
def main(path, width=1920, columns=6, names=True, square=False, random_order=False):
    pass
if __name__ == '__main__':
    create_contact_sheet(sys.argv[1])
