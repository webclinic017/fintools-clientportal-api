#!/usr/bin/env python3
# Create a 'data' dir, which contains today's date dir
# Inside that dir are further two dirs (today, yesterday), which contain market
# data (OHLC) for these tickers
#
# Run as:  ./analyse.py DATADIR PERC1 PERC2
# Example: ./analyse.py ./2020-02-06 4 3

import argparse
import json
import os
import pprint
from datetime import datetime

# Helpers
def is_dir(string):
  if os.path.isdir(string):
    return string
  else:
    raise NotADirectoryError(string)

def get_range_prices(average, percentage):
  # input:
  # - average: number, e.g. 102
  # - percentage: number, e.g. 4/100
  # output:
  # - a pair of numbers:
  #   - low price
  #   - high price
  x = average
  p = percentage
  return ( 2*x/(2+p), 2*x*(1+p)/(2+p) )


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
i = 0
out_table = {}
price_range_day_one = ()
for date in dates:
  datedir = args.dir_path + '/' + date
  if is_dir(datedir):
    # Symbols
    symbol_files = os.listdir(datedir)
    symbols_count = len(symbol_files)
    for symbol_file in symbol_files:
      symbol = symbol_file.replace('.json', '')
      if symbol not in out_table.keys():
        out_table[symbol] = {}
      if date not in out_table[symbol].keys():
        out_table[symbol][date] = {}
      points = []
      with open(datedir + '/' + symbol_file) as f:
        d = json.load(f)
        for data_point in d:
          points.append((data_point['o'] + data_point['h'])/2)
      avg = round(sum(points)/len(points), 2)
      out_table[symbol][date]['avg'] = avg
      if i == 0:
        perc = args.perc1
      else:
        perc = args.perc2
      # Get price range
      price_range = get_range_prices(avg, perc)
      price_range = (round(price_range[0], 2), round(price_range[1], 2))
      out_table[symbol][date]['l'] = price_range[0]
      out_table[symbol][date]['h'] = price_range[1]
      # Get count
      if i == 0:
        # First day
        price_range_day_one = price_range
      else:
        # Second day
        price_range = price_range_day_one
      # TODO: Get count
    i += 1
    # TODO: Categorise
    # TODO: Output count
    # TODO: Output table


print('=====')
print('Number of symbols:', symbols_count)
print('Perc 1:', args.perc1)
print('Perc 2:', args.perc2)
pprint.pprint(out_table)
