#!/usr/bin/env python3
# Get NASDAQ conid for given symbol
# Return exitcode 1 if symbol is not NASDAQ or not in IB
# Run as:  ./get_conid_nasdaq.py SYMBOL
# Example: ./get_conid_nasdaq.py AAPL

import argparse
import json
#import numpy as np
from statistics import mean, median
import os
import urllib3

# Local
from lib.company import Company

# Config
urllib3.disable_warnings()

# Parse args
parser = argparse.ArgumentParser(
  description='Display last day data for symbol')
parser.add_argument('symbol', metavar='SYMBOL', type=str,
  help='Symbol, e.g. AAPL')
parser.add_argument(
  '-s',
  dest='small',
  action='store_true',
  help='Print only result (category), without the symbol'
)
args = parser.parse_args()
symbol = args.symbol

### MAIN ###
c = Company(symbol)
day = Company(symbol).get_quote(period='1d', bar='1min')
#print(json.dumps(day))
vol_non_zero = [ e['v'] for e in day if e['v'] != 0.0 ]
vol = [ e['v']  for e in day ]
stats = {
  'vol_len': len(day),
  'vol_non_zero_len': len(vol_non_zero),
  'vol_avg': round(mean(vol), 2),
  'vol_median': round(median(vol), 2),
  'vol_median_non_zero': round(median(vol_non_zero), 2),
  'vol_min': min(vol_non_zero),
  'vol_max': max(vol),
}
print(json.dumps(stats))
