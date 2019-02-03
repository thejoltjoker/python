#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
create_dv_stills.py
Description of create_dv_stills.py.
"""
import os


def main():
    path = r"/Volumes/data_a/media/dv/tapes"
    """docstring for main"""
    for folder, root, filenames in os.walk(path):
        for f in [f for f in filenames if f.endswith(('mpeg', 'avi'))]:
            in_file = os.path.join(folder, f)
            out_file = os.path.join(folder, "stills", "{fname}_{number}.{ext}".format(
                fname=os.path.splitext(f)[0], number='%04d', ext='jpg'))
            freq = "1/60"
            if not os.path.exists(os.path.join(folder, 'stills')):
                os.makedirs(os.path.join(folder, 'stills'))
            print("{input} => {output} @ {freq}".format(
                input=in_file, freq=freq, output=out_file))
            os.system(
                'ffmpeg -n -i {input} -vf fps={freq} {output}'.format(input=in_file, freq=freq, output=out_file))


if __name__ == '__main__':
    main()
