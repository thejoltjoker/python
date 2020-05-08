#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
read_write_json.py
Read, write and update json files
"""
import json
from pathlib import Path


def read_json_file(path):
    """Read json from a file"""
    path = Path(path)
    try:
        with path.open("r") as file:
            json_file = json.load(file)
            return json_file
    except FileNotFoundError as e:
        print("File not found.")


def write_json_file(path, json_data):
    """Write json to a file"""
    path = Path(path)

    with path.open("w") as file:
        json_file = json.dump(json_data, file)
        return json_file


def update_json_file(path, json_data):
    """Read json from a file and update it with new data"""
    path = Path(path)
    data = {}
    try:
        with path.open("r") as file:
            data = json.load(file)
    except FileNotFoundError as e:
        print("File not found.")

    # Update data
    if isinstance(data, list):
        if isinstance(json_data, list):
            data.extend(json_data)
        else:
            data.append(json_data)
    elif isinstance(data, dict):
        data.update(json_data)

    # Write data
    with path.open("w") as file:
        json_file = json.dump(data, file)
        return json_file


def main():
    """docstring for main"""
    path = Path(__file__).parent / "test.json"

    data = ["tjosdf"]
    # data = {"test": "fest"}
    # # Read json file
    # print(read_json_file(path))

    # # Write json file
    # print(write_json_file(path, data))

    # Update json file
    print(update_json_file(path, data))


if __name__ == '__main__':
    main()
