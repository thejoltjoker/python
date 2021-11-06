#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
script_name.py
Description of script_name.py.
"""
from datetime import datetime
from pathlib import Path
import logging
import csv

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')


def write_csv(filename, data: list):
    """Write dict to csv file"""
    with open(filename, mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = [x for x in data[0].keys()]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def get_projects(root):
    """Get all project folders in a dir"""
    return [x for x in root.iterdir() if x.is_dir()]


def project_date(path: Path):
    """Find the oldest file in the folder and return date"""
    start_date = None
    end_date = None
    for f in path.rglob('*'):
        if not start_date:
            start_date = f.stat().st_ctime
        if not end_date:
            end_date = f.stat().st_mtime

        if f.stat().st_ctime < start_date:
            start_date = f.stat().st_ctime
        if f.stat().st_mtime > end_date:
            end_date = f.stat().st_mtime
    return start_date, end_date


def main():
    """docstring for main"""
    # for path in Path('U:\\projects\\').iterdir():
    path = Path(r'U:\projects\2014')
    projects = []
    for p in get_projects(path):
        split_name = p.name.split('_')
        split_name.pop(0)
        proj = {
            "project_name": f'{" ".join(split_name)}',
            "begin_date": datetime.fromtimestamp(project_date(p)[0]),
            "end_date": datetime.fromtimestamp(project_date(p)[1]),
            "local_dropbox_path": p.relative_to(r'U:\\').as_posix()
        }
        projects.append(proj)
        for k, v in proj.items():
            logging.info(f'{k}: {v}')
    write_csv(f'{path.name}.csv', projects)


if __name__ == '__main__':
    main()
