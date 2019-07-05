#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
mullvad.py
Check if you're connected to Mullvad VPN
"""
import sys
import requests
import json


def main():
    """docstring for main"""
    try:
        r = requests.get('https://am.i.mullvad.net/json')
        json_data = r.json()

        if json_data['mullvad_exit_ip']:
            print("You are connected to Mullvad!")
        else:
            print("You are NOT connected to Mullvad!")
        if 'json' in sys.argv:
            # for k, v in json_data.items():
            #     print("{key}: {value}".format(key=k, value=v))
            print(json.dumps(json_data, indent=2))
        else:
            print("IP: {}".format(json_data['ip']))
            print("Country: {}".format(json_data['country']))
            if json_data['city'] is not None:
                print("City: {}".format(json_data['city']))
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
