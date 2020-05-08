#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
script_name.py
Description of script_name.py.
"""
import subprocess

def convert_videos(file_path, preset=None):
    """Run ffmpeg in subprocess and return the output"""
    input = ""
    youtube = ["ffmpeg", "-i", input, "-c:v", "libx264", "-movflags", "faststart", "-crf", "0", "-pix_fmt", "yuv420p", "-r", "24", "-g", "12", "-bf", "2", "-c:a", "libfdk_aac", "-b:a", "384k", "-ar", "48000"]
    cmd = youtube

    try:
        s = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        s = s.stdout.read()

        return s.strip()

    except Exception as e:
        print(e)

def main():
    """docstring for main"""
    pass

if __name__ == '__main__':
    main()