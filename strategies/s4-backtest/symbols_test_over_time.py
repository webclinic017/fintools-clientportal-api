#!/usr/bin/env python3
# Run strategy from command line
import argparse
import ib_web_api
import json
import pprint
import test_data
import urllib3
from ib_web_api import MarketDataApi
from lib.icompany import ICompany
from lib.util import get_perc_from_history, timestamp_to_date
from statistics import mean

# Settings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument(
  'symbols',
  metavar='SYMBOL',
  type=str,
  help='Symbols, e.g. AAPL AMZN',
)
parser.add_argument(
  '-t', '--test',
  action='store_true',
  help='If enabled, get real data from IB'
)
args = parser.parse_args()
symbols = args.symbols
test = args.test

##### HELPERS

## STRATEGIES
# Every method str_* will return:
# {
#   'buy': buy price,
#   'sell': sell price,
# }
def str_perc(data):
  # buy: average of buy prices found
  d = get_perc_from_history(data, 4)
  if len(d) > 0:
    return mean([ l['y0'] for l in d ])
  else:
    return None

def str_range(data):
  # Simply return low price
  return min([ l['l'] for l in data ])

def str_max(data):
  # Simply return low price
  return min([ l['h'] for l in data ])

def get_buy_price(kind, data):
  # Return buy price: wrapper
  # Call other methods depending on 'kind'/strategy
  # Returns float
  return globals()['str_' + kind](data)

## OTHER
def get_price_plus_perc(price, perc):
  # e.g. given 100 price, 4 perc, return 104
  return price + (100+perc)*price/100

def get_count_from_price(buy_price, data):
  # Given 'prices' range, { 'buy': 1, 'sell': 2 }
  # gives count of how often able to buy and sell at given prices
  count = 0
  print('-----------')
  # Sort data by timestamp
  data = sorted(data, key=lambda k: k['t'])
  if buy_price is None:
    print('No prices')
    return
  find_buy = True
  for point in data:
    print(point['l'])
    if find_buy:
      if point['l'] <= buy_price:
        find_buy = False
    if not find_buy:
      if point['h'] >= get_price_plus_perc(buy_price, 4):
        find_buy = True
        count += 1
  return count

###### MAIN
if test:
  data = test_data.get_history()
else:
  # TODO: Get IB data here
  data = []
  print('not yet done')
  # Get symbol conid
  #conid = ICompany(symbol).get_conid()
  exit(0)

# Group list into days
data_by_date = {}
for i in data:
  t = timestamp_to_date(i['t'])
  if t not in data_by_date:
    data_by_date[t] = []
  data_by_date[t].append(i)
del data

# Run each strategy
strategy_count = {}
for kind in ['perc', 'max', 'range' ]:
  strategy_count[kind] = { 'total': 0, 'successful_days': 0 }
  print('====', kind)
  prev = None
  for date, points in sorted(data_by_date.items()):
    if prev is not None:
      print('Search', round(prev, 2), 'and', get_price_plus_perc(prev, 4))
      day_count = get_count_from_price(prev, points)
      strategy_count[kind]['total'] += day_count
      if day_count > 0:
        strategy_count[kind]['successful_days'] += 1
    else:
      print('No prev data')
      pass
    prev = get_buy_price(kind, points)
pprint.pprint(strategy_count)
