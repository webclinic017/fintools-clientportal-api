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
from tabulate import tabulate

# Helpers
def is_dir(string):
  if os.path.isdir(string):
    return string
  else:
    raise NotADirectoryError(string)

# Other helpers
def get_dates(path):
  return sorted(os.listdir(path))

def get_symbols(path):
  ret = []
  dates = os.listdir(path)
  datedir = path + '/' + dates[0]
  for s in os.listdir(datedir):
    ret.append(s.replace('.json', ''))
  return ret

# Algorithms
def get_range_prices(average, percentage):
  # input:
  # - average: number, e.g. 102
  # - percentage: number, e.g. 4/100
  # output: a dict of numbers:
  # - l=low price, h=high price, x=average, p=percentage
  x = average
  p = percentage
  return {
    'l': round(2*x/(2+p), 2),
    'h': round(2*x*(1+p)/(2+p), 2)
  }

def get_count(data, lo, hi):
  # Return number of times given ohlc data oscillates between the lo and hi
  # data: lo, hi: numbers, e.g. 100, 102
  ret = 0
  search_low = True
  for i in data:
    if search_low is True:
      if i['l'] <= lo:
        search_low = False
    else:
      if i['h'] >= hi:
        search_low = True
        ret += 1
  return ret

def get_average(f_path):
  points = []
  with open(f_path) as f:
    data = json.load(f)
    for data_point in data:
      points.append((data_point['o'] + data_point['h'])/2)
  avg = round(sum(points)/len(points), 2)
  return avg


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

# Name args
path = args.dir_path


# Pre-populate array
# symbols: {
#   'SYMB': {
#     'date1': { 'avg': ?, 'cnt': ?, 'range': {} },
#     'date2': { 'avg': ?, 'cnt': ?, 'range': {} }
#   }
# }
dates = get_dates(path)
symbols = get_symbols(path)
ret = {}
info = { 'avg': None, 'cnt': None, 'rng': None }
for s in symbols:
  if s not in ret.keys():
    ret.update({ s: {} })
  for d in dates:
    ret[s][d] = info.copy()

# Populate array
for s in symbols:
  i = 0
  for d in dates:
    f_path = path + '/' + d + '/' + s + '.json'
    with open(f_path) as f:
      avg = get_average(f_path)
      ret[s][d]['avg'] = avg
      if i == 0:
        perc = args.perc1/100
      else:
        perc = args.perc2/100
      # Get price range
      price_range = get_range_prices(avg, perc)
      ret[s][d]['rng'] = price_range
      # Get count
      if i == 0:
        yesterday_avg = avg
      else:
        avg = yesterday_avg
      with open(f_path) as f:
        data = json.load(f)
        aa = get_range_prices(avg, perc)
        osc_count = get_count(data, aa['l'], aa['h'])
      ret[s][d]['cnt'] = osc_count
    i += 1

#pprint.pprint(ret)

# Categorise
table = { 'match': {}, 'fail': {}, 'other': {} }
for s in ret:
  pass
  i = ret[s]
  d0 = ret[s][dates[0]]
  d1 = ret[s][dates[1]]
  if d0['cnt'] > 0 and d1['cnt'] > 0:
    # Match
    table['match'][s] = i
  elif d0['cnt'] > 0 and d1['cnt'] == 0:
    table['fail'][s] = i
  elif d0['cnt'] == 0 and d1['cnt'] == 0:
    table['other'][s] = i
order = [ 'match', 'fail', 'other' ]

# Print table
d0 = dates[0]
d1 = dates[1]
print('=====')
print('=====')
print('Number of symbols:', len(symbols))
print('Perc 1:', args.perc1)
print('Perc 2:', args.perc2)
t = table
print('Match:', len(t['match']))
print('Fail:', len(t['fail']))
print('Other:', len(t['other']))
table_format = '%-5s %5s %5s %2s %2s %5s %5s %5s %5s'
for category in order:
  print('=====', category, '=====')
  print(table_format % (
      'SYMB',
      'AVG0',
      'AVG1',
      'C0',
      'C1',
      'RNG0L',
      'RNG0H',
      'RNG1L',
      'RNG1H'
  ))
  for symbol in t[category]:
    i = t[category][symbol]

    print(table_format % (
        symbol,
        i[d0]['avg'],
        i[d1]['avg'],
        i[d0]['cnt'],
        i[d1]['cnt'],
        i[d0]['rng']['l'],
        i[d0]['rng']['h'],
        i[d1]['rng']['l'],
        i[d1]['rng']['h']
    ))
