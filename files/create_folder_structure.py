#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
create_folder_structure.py
Description of create_folder_structure.py.
"""
import os

folder_structure_json = [
    {
        "name": "film",
        "root": True,
        "children": [
            {
                "name": "assets",
                "children": [
                    {
                        "name": "audio",
                        "children": [
                            {
                                "name": "music"
                            },
                            {
                                "name": "sfx"
                            },
                            {
                                "name": "recorded"
                            }
                        ]
                    },
                    {
                        "name": "graphics"
                    },
                    {
                        "name": "luts"
                    },
                    {
                        "name": "thumbnail",
                        "children": [
                            {
                                "name": "exports"
                            },
                            {
                                "name": "work"
                            }
                        ]
                    },
                    {
                        "name": "video"
                    }
                ]
            },
            {
                "name": "client",
                "children": [
                    {
                        "name": "fromClient"
                    },
                    {
                        "name": "toClient"
                    },
                    {
                        "name": "delivery"
                    }
                ]
            },
            {
                "name": "dailies"
            },
            {
                "name": "editorial",
                "children": [
                    {
                        "name": "work"
                    },
                    {
                        "name": "exports"
                    }
                ]
            },
            {
                "name": "sandbox"
            }
        ]
    }
]


def process_folder_structure(path, node):
    path = os.path.join(path, node["name"])

    if not os.path.exists(path):
        os.mkdir(path)
        print(path)

    for child in node.get("children", []):
        process_folder_structure(path, child)


def main():
    """docstring for main"""
    proj_type = "film"
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    for f in folder_structure_json:
        if f.get('name') is proj_type:
            folder_structure = f
    process_folder_structure(path, folder_structure)


if __name__ == '__main__':
    main()
