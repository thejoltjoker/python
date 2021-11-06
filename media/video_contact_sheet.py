#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
create_dv_stills.py
Description of create_dv_stills.py.
"""
import os
import sys
import subprocess
from pathlib import Path


class IndexCreator:
    def __init__(self, input_file):
        self.input_path = Path(input_file)
        self.temp_dir = self.input_path.parent / "_cs_temp_dir"
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        self.output_path = self.input_path.parent / f"{self.input_path.name}_index.jpg"
        self.thumbnails = None

        # Run
        self.generate_thumbnails()
        self.create_contact_sheet()
        self.cleanup()

    def cleanup(self):
        for f in self.temp_dir.rglob("*"):
            f.unlink()
        self.temp_dir.rmdir()

    def generate_thumbnails(self, frequency="1/4"):
        out_file = self.temp_dir / f"{self.input_path.name}_%04d.jpg"

        print("{input} => {output} @ {freq}".format(
            input=self.input_path, freq=frequency, output=out_file))
        os.system('ffmpeg -n -i {input} -vf fps={freq} {output}'.format(input=self.input_path, freq=frequency, output=out_file))
        self.thumbnails = [str(x) for x in self.temp_dir.rglob("*.jpg")]
        return self.thumbnails

    def create_contact_sheet(self):
        temp_list_path = self.temp_dir / "_cs_temp_file_list.txt"
        temp_list_path.write_text("\n".join(self.thumbnails))

        print(f"Running montage for {self.output_path.parent}")
        cmd = ["montage",
               "-geometry", "300x300",
               "-fill", "#ffffff",
               "-background", "#111111",
               f"@{temp_list_path}", self.output_path]
        try:
            s = subprocess.Popen(cmd, stdout=subprocess.PIPE)
            s = s.stdout.read()

            return s.strip()

        except subprocess.CalledProcessError as e:
            print(e)
            return None


def main(path):
    path = Path(path)
    ext = ("m2t", "avi", "mp4", "mpeg")
    files = [x for x in path.rglob("*") if str(x).endswith(ext)]
    for f in files:
        IndexCreator(f)


if __name__ == '__main__':
    main(sys.argv[1])
