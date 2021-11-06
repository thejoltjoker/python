#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
script_name.py
Description of script_name.py.
"""

import argparse


def calculate(follower_count, avg_like_count):
    """Calculate the price of a post based on followers and likes"""
    cpf = 0.0025
    cpl = 0.025
    cost = (follower_count * cpf) + (avg_like_count * cpl)

    return cost


def main():
    """docstring for main"""
    parser = argparse.ArgumentParser(description='Calculate the cost of a post based on followers and likes')
    parser.add_argument('followers',
                        type=int,
                        help='Follower count')
    parser.add_argument('likes',
                        type=int,
                        help='Average likes per post')

    args = parser.parse_args()
    cost =calculate(args.followers, args.likes)
    print(f'{round(cost, 2)}$')


if __name__ == '__main__':
    main()
