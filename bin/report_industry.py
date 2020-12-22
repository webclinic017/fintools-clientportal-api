#!/usr/bin/env python3
# Get cheap symbols, and their categories

import json
import os
from statistics import mean, median
from tabulate import tabulate

# Local
import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../'))
from lib.company import Company
from lib.filters import get_contracts_cheaper_than

# Main
# Check params
if len(sys.argv) < 2:
  print('Provide industry')
  exit(2)
industry = sys.argv[1]

try:
  # Get symbols
  print('Get cheaper than')
  contracts = get_contracts_cheaper_than(3)
  # price, category, industry
  symbols_contracts = {
    symbol: info
    for symbol, info
    in contracts.items()
    if info['industry'] == industry
  }
  symbols = symbols_contracts.keys()
  print(symbols_contracts)
  print('Got %i symbols' % len(symbols))
except Exception as e:
  print('ERROR: Could not get contracts:', e)
  exit(1)

try:
  # Generate JSON data
  days_info = {}
  print('Generate report data')
  for symbol in symbols:
    c = Company(symbol)
    day = c.get_day_cache()
    vol_non_zero = [ e['v'] for e in day if e['v'] != 0.0 ]
    vol = [ e['v']  for e in day ]
    days_info[symbol] = {
      'price': symbols_contracts[symbol]['price'],
      'vol_len': len(day),
      'vol_non_zero_len': len(vol_non_zero),
      'vol_avg': round(mean(vol), 2),
      'vol_median': round(median(vol), 2),
      'vol_median_non_zero': round(median(vol_non_zero), 2),
      'vol_min': min(vol_non_zero),
      'vol_max': max(vol),
    }
except Exception as e:
  print('ERROR: Could not build report: %s' % e)
  exit(1)

try:
  # Print report
  print(json.dumps(days_info, indent=2))
  print("""
Legend:
- SYMB: symbol
- P: price
- V1: vol_len
- V2: vol_non_zero_len
- V3: vol_avg
- V4: vol_median
- V5: vol_median_non_zero
- vm: vol_min
- VM: vol_max
""")
  report = []
  headers = [ 'SYMB', 'P', 'V1', 'V2', 'V3', 'V4', 'V5', 'vm', 'VM', ]
  for symbol in symbols:
    d = days_info[symbol]
    report.append([
        symbol,
        d['price'],
        d['vol_len'],
        d['vol_non_zero_len'],
        d['vol_avg'],
        d['vol_median'],
        "%0.2f" % d['vol_median_non_zero'],
        d['vol_min'],
        d['vol_max'],
    ])
  print(tabulate(report, headers=headers, numalign='right', floatfmt=".2f"))
except Exception as e:
  print('ERROR: Could not print report: %s' % e)
  exit(1)

