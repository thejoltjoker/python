#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
script_name.py
Description of script_name.py.
"""
import csv
from pathlib import Path


def create_keyword_list(tatorter):
    """Create a lightroom formatted keyword list"""
    keywords_file = Path("svenska_tatorter_lightroom.txt")
    text = []
    text.append("sverige\n")
    text.append("\t{sweden}\n")
    text.append("\t{svea rike}\n")

    for lan, kommun in tatorter.items():
        print(lan)

        # Create family top-level
        text.append(f"\t{lan}\n")

        for kommun, tatorter in kommun.items():
            print(kommun)
            # Create kommun
            text.append(f"\t\t{kommun}\n")

            # Create tatort
            for tatort in tatorter:
                text.append(f"\t\t\t{tatort}\n")

    # Write keywords to file
    with keywords_file.open("w") as f:
        f.writelines(text)
def tatorter_to_keywords(data):
    keywords = {}
    path = Path(data)
    with path.open("r") as raw_data:
        csv_data = list(csv.reader(raw_data))
        for i in csv_data[1:]:
            lan = i[1].lower()
            print(lan)
            kommun = f"{i[3]} kommun".lower()
            print(kommun)
            tatort = i[5].lower()
            print(tatort)
            if keywords.get(lan):
                if keywords[lan].get(kommun):
                    keywords[lan][kommun].append(tatort)
                else:
                    keywords[lan][kommun] = [tatort]
            else:
                keywords[lan] = {
                    kommun: [tatort]
                }

    create_keyword_list(keywords)

def main():
    """docstring for main"""
    pass


if __name__ == '__main__':
    print(tatorter_to_keywords("/Users/johannes/Dropbox/temp/data.csv"))
    main()
