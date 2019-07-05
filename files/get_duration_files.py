#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
get_duration_files.py
Description of get_duration_files.py.
"""
import os
import subprocess
import logging
import json
import datetime
import sys


class ClipsDuration:
    def __init__(self, path):
        self.total_duration = 0
        duration_clip_count = 0
        self.logger = self.setup_logger()
        file_list = self.scan_files(path)
        self.logger.debug(file_list)

        # Add durations to create total duration
        for n, i in file_list.items():
            self.logger.debug(i)
            if i.get('duration'):
                self.total_duration += i['duration']
                duration_clip_count += 1
                self.logger.debug("Adding %s to total_duration. New total duration is %s", i['duration'],
                                  self.total_duration)
            else:
                self.logger.debug("%s doesn't have a duration, skipping", i.get('path'))
        # Print total duration
        formatted_time = datetime.timedelta(seconds=self.total_duration)
        self.logger.info("Total duration of %s clips is %s", duration_clip_count, formatted_time)

    @staticmethod
    def setup_logger():
        """Creates a logger"""
        logger = logging.getLogger()
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s %(name)-12s %(levelname)-8s %(message)s', "%Y-%m-%d %H:%M:%S")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

        return logger

    def get_ffprobe_data(self, file_path):
        try:
            exif_data = subprocess.check_output(
                'ffprobe -loglevel quiet -print_format json -show_format {}'.format(file_path), shell=True)
        except Exception as e:
            self.logger.warning(e)
            return {}

        try:
            metadata = json.loads(exif_data.decode('ascii'))
        except Exception as e:
            self.logger.error(e)
            metadata = json.loads(exif_data)[0]

        return metadata

    def scan_files(self, path):
        file_list = {}
        file_id = 0
        for subdir, dirs, files in os.walk(path):
            for n, file in enumerate(files):
                file_id += 1
                file_path = os.path.join(subdir, file)
                self.logger.debug(file_path)

                # Add file to dictionary
                file_list[file_id] = {
                    'path': file_path
                }

                # Get ffprobe data
                file_info = self.get_ffprobe_data(file_path)
                self.logger.debug(file_info)

                # Get duration if ffprobe was successful
                if file_info.get('format'):
                    file_duration = file_info['format'].get('duration')
                    file_list[file_id]['duration'] = float(file_duration)
                    self.logger.debug(file_list[file_id])

        self.logger.info("%s files found", len(file_list))

        return file_list


def main():
    """docstring for main"""
    app = ClipsDuration(sys.argv[1])


if __name__ == '__main__':
    main()
