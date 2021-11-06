#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
script_name.py
Description of script_name.py.
"""

import sys
import subprocess
from pathlib import Path


def crop_video(input_video, lut=None):
    """Run ffmpeg in subprocess and return the output"""
    output_video = input_video.parent / f'{input_video.stem}_vertical.mov'

    vf = 'crop=ih/16*9:ih'
    if lut == 'slog3':
        lut = '/Users/johannes/Desktop/slog3_bright_002_1.201215_C0030.cube'

    if lut:
        vf = f'{vf},lut3d={Path(lut).resolve()}'
    print(vf)

    cmd = ['ffmpeg',
           '-i', input_video,
           '-c:v', 'prores_ks',
           '-profile:v', '3',
           '-qscale:v', '10',
           '-vendor', 'apl0',
           '-pix_fmt', 'yuv422p10le',
           '-vf', vf,
           output_video]

    s = subprocess.check_output(cmd)
    return s


if __name__ == '__main__':
    crop_video(Path(sys.argv[1]), lut=sys.argv[2])
