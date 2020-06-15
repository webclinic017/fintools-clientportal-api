#!/usr/bin/env python3.7
# Run strategy from command line
# It uses python3.7 because otherwise json.dumps doesn't preserve dict order
import argparse
import datetime
import ib_web_api
import json
import matplotlib.dates as mdates
import matplotlib.pyplot as plot
import pprint
import test_data
import urllib3
from collections import OrderedDict
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
parser.add_argument(
  '-d', '--dates-only',
  action='store_true',
  help='Get dates for strategies, and chart them',
)
args = parser.parse_args()
symbols = args.symbols
test = args.test
dates_only = args.dates_only

##### HELPERS

## STRATEGIES
# Every method str_* will return:
# {
#   'buy': buy price,
#   'sell': sell price,
# }
# Use these to compute the buy price from a previous day data
def str_perc_avg(data):
  # Average of success buy prices
  d = get_perc_from_history(data, 4)
  if len(d) > 0:
    return mean([ l['y0'] for l in d ])
  else:
    return None

def str_perc_low(data):
  # Low of success buy prices
  d = get_perc_from_history(data, 4)
  if len(d) > 0:
    return min([ l['y0'] for l in d ])
  else:
    return None

def str_perc_first(data):
  # Sort by timestamp
  # Low of success buy prices
  data = get_perc_from_history(data, 4)
  if len(data) > 0:
    return sorted(data, key=lambda k: k['t0'])[0]['y0']
  else:
    return None

def str_low(data):
  # Low price of previous day
  return min([ l['l'] for l in data ])

def str_close(data):
  # Return close price
  # Sort data by timestamp
  data = sorted(data, key=lambda k: k['t'])
  return data[len(data)-1]['c']

def get_buy_price(kind, data):
  # Return buy price: wrapper
  # Call other methods depending on 'kind'/strategy
  # Returns float
  return globals()['str_' + kind](data)

## OTHER
def get_price_plus_perc(price, perc):
  # e.g. given 100 price, 4 perc, return 104
  return price*(1+0.01*perc)

def get_count_from_price(buy_price, data):
  # Given 'prices' range, { 'buy': 1, 'sell': 2 }
  # gives count of how often able to buy and sell at given prices
  # also gives dates
  ret = {
    'count': 0,
    'dates': [],
  }
  # Sort data by timestamp
  data = sorted(data, key=lambda k: k['t'])
  if buy_price is None:
    print('No prices')
    return
  find_buy = True
  for point in data:
    if find_buy:
      if point['l'] <= buy_price:
        find_buy = False
    if not find_buy:
      if point['h'] >= get_price_plus_perc(buy_price, 4):
        find_buy = True
        ret['count'] += 1
        ret['dates'].append(timestamp_to_date(point['t']))
  return ret

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
strategies = [
  'close',
  'low',
  'perc_avg',
  'perc_first',
  'perc_low',
]
ret = {
  'summary': {
    'success_days': 0,
    'success_total': 0,
    'strategies': {},
  }
}

# Get count of successful buy/sell pairs (benchmark)
for date, points in sorted(data_by_date.items()):
  success_count = len(get_perc_from_history(points, 4))
  if success_count > 0:
    ret['summary']['success_days'] += 1
  ret['summary']['success_total'] += success_count

for strategy in strategies:
  strategy_info = {
    'success_total': 0,
    'success_days': 0,
    'success_dates': [],
    'success_days_perc': 0,
  }
  print('====', strategy)
  prev = None
  for date, points in sorted(data_by_date.items()):
    if prev is not None:
      print(date, ':', round(prev, 2), 'and',
        round(get_price_plus_perc(prev, 4), 2)
      )
      day_count = get_count_from_price(prev, points)
      strategy_info['success_total'] += day_count['count']
      if day_count['count'] > 0:
        strategy_info['success_days'] += 1
        strategy_info['success_dates'] += day_count['dates']
    else:
      print('No prev data')
      pass
    prev = get_buy_price(strategy, points)
  # Work out percentage success
  a = strategy_info['success_days']
  b = ret['summary']['success_days']
  strategy_info['success_dates'] = sorted(list(set(strategy_info['success_dates'])))
  strategy_info['success_days_perc'] = round((a/b)*100, 2)
  ret['summary']['strategies'][strategy] = strategy_info
# Sort strategies by percentage
strats = ret['summary']['strategies']
ret['summary']['strategies'] = {
  k: v for k,v in sorted(
    strats.items(),
    key=lambda item: item[1]['success_days_perc']
  )
}

# Print
if dates_only:
  formatter = mdates.DateFormatter('%Y-%m-%d')
  axes = plot.gca() # Get axes
  axes.xaxis.set_major_formatter(formatter)
  strategy_idx = 0
  for strategy in ret['summary']['strategies']:
    strategy_idx += 1
    dates = ret['summary']['strategies'][strategy]['success_dates']
    print(strategy, dates)
    dates = [datetime.datetime.strptime(d,'%Y%m%d').date() for d in dates]
    plot.scatter(dates, [ strategy_idx for i in range(len(dates))])
  plot.show()
else:
  print(json.dumps(ret, indent=2))
