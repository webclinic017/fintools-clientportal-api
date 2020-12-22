#!/usr/bin/env python3
# Download today's data for cheap tickers (defined elsewhere)
# and specific industry
# This is fine-grained data, e.g. 1 minute bar width
# Note: This will actually download it, NO CACHE
# Running time:
# - 36 s
# Example:
# ./0 Software

import argparse
import concurrent.futures
import json
import os
import pprint
import urllib3
import urllib.request

# Local
import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../'))
from lib.company import Company
from lib.config import Config
from lib.filters import get_contracts_cheaper_than
from lib.util import log

# Config
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
count_total = 0
count_progress = 0

# Check params
if len(sys.argv) < 2:
  print('Provide industry')
  exit(2)
industry = sys.argv[1]

# Read config
# Read config
cfg = Config()
dir_day = cfg['paths']['day']
debug = cfg.getboolean('main', 'debug')


### HELPERS ###
def down_day(symbol):
  global count_total
  global count_progress
  log('%s: Down' % symbol)
  try:
    quote = Company(symbol).get_quote(period='1d', bar='1min')
    # Log progress
    count_progress += 1
    log('Progress: %i/%i' % (count_progress, count_total))
  
  except Exception as e:
    raise Exception('%s: Could not get symbol: %s' % (symbol, e))

  return {
    'symbol': symbol,
    'data': quote
  }

### MAIN ###
try:
  log('Get cheaper than $3/share')
  symbols = get_contracts_cheaper_than(3)
  symbols = [
    symbol for symbol, info in symbols.items()
    if info['industry'] == industry
  ]
  if debug:
    symbols = [ symbols[0] ]
  print('Got %i symbols' % len(symbols))
except Exception as e:
  print('ERROR: Could not get symbols:', e)
  exit(1)

try:
  log('Download day data')
  count_total = len(symbols)
  with concurrent.futures.ThreadPoolExecutor(max_workers=400) as executor:
    future_to_data = {
      executor.submit(down_day, symbol): symbol
      for symbol in symbols
    }
    for future in concurrent.futures.as_completed(future_to_data):
      try:
        #day_quotes.update(future.result())
        res = future.result()
        symbol = res['symbol']
        #print('res', future.result())
        log('.')
        # Save to disk
        f_path = dir_day + '/' + symbol + '.json'
        print('SAVE TO', f_path)
        with open(f_path, 'w') as f:
          f.write(json.dumps(res['data']))
      except Exception as e:
        print('Fail saving data: %s' % e)
except Exception as e:
  log('FAIL: %s' % e)
