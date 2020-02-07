#!/usr/bin/env python3
# Create a 'data' dir, which contains today's date dir
# Inside that dir are further two dirs (today, yesterday), which contain market
# data (OHLC) for these tickers
#
# Run as:  ./analyse.py DATADIR PERC1 PERC2
# Example: ./analyse.py ./2020-02-06 4 3

import argparse
import os
from datetime import datetime

# Helpers
def is_dir(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)



# Parse args
parser = argparse.ArgumentParser(
    description='Display last day data for ticker')
parser.add_argument('dir_path', metavar='DIR_PATH', type=is_dir,
    help='Path to dir')
parser.add_argument('perc1', metavar='PERC1', type=int,
    help='Percentage day 1')
parser.add_argument('perc2', metavar='PERC2', type=int,
    help='Percentage day 2')
args = parser.parse_args()

# Main
dates = os.listdir(args.dir_path)
# TODO: Check there are only two subdirs
for date in dates:
    datedir = args.dir_path + '/' + date
    if is_dir(datedir):
        # Symbols
        symbols = os.listdir(datedir)
        print(symbols)
        # TODO: Read file, get average, get percentages
        # TODO: Categorise
        # TODO: Output count
        # TODO: Output table
