#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
files_to_database.py
Create a database with all files in selected directory
"""
import os
import sys
import sqlite3
from pathlib import Path
import hashlib


class Database:
    def __init__(self, name):
        self.conn = sqlite3.connect(name)
        self.cur = self.conn.cursor()
        self.create_table()

    def create_table(self):
        query = """CREATE TABLE IF NOT EXISTS files (
                    id INTEGER PRIMARY KEY,
                    path TEXT NOT NULL UNIQUE,
                    md5 TEXT,
                    mtime TEXT,
                    ctime TEXT,
                    size TEXT
                );"""
        self.cur.execute(query)
        self.conn.commit()

    def insert(self, path, md5, mtime, ctime, size):
        """Insert a path to database"""
        query = f"INSERT OR REPLACE INTO files (path, md5, mtime, ctime, size) " \
                f"VALUES ('{path}', '{md5}', '{mtime}', '{ctime}','{size}');"
        self.cur.execute(query)
        self.conn.commit()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cur.close()


def main(path):
    """docstring for main"""
    path = Path(path)
    db = Database(f'{path.stem}_files.db')
    for f in path.rglob('*'):
        if f.is_file():
            db.insert(str(f.resolve()),  # path
                      hashlib.md5(f.read_bytes()).hexdigest(),  # md5 checksum
                      f.stat().st_mtime,  # modification time
                      f.stat().st_ctime,  # creation time
                      f.stat().st_size)  # size
            print(f)
    # for root, dirs, files in os.walk(path):
    #     for f in files:
    #         f_path = os.path.join(root, f)
    #         print(f_path)
    #         db.insert(f_path)


if __name__ == '__main__':
    main(sys.argv[1])
