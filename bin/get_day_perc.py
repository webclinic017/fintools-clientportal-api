#!/usr/bin/env python3
# For a given symbol, get the day percentage increase
# (highest achievable low to high)
# Note: Gets from cache

import argparse
import json
import os
# Local
import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../'))
from lib.company import Company
from lib.filters import get_winners_lt_perc
from lib.util import error

debug = False

# Parse args
parser = argparse.ArgumentParser(
    description='Display last day data for ticker')
parser.add_argument(
    'symbol',
    metavar='SYMBOL',
    type=str,
    help='Symbol, e.g. AACG')
args = parser.parse_args()
symbol = args.symbol

# Main
try:
  # Get symbol day data
  # ret: ?
  company = Company(symbol)
  data = company.disk_find('day')
except Exception as e:
  print('ERROR: Could not get day data:', e)
  exit(1)

try:
  # Get perc increase
  for point in data:
    print(point['l'])
  pass
except Exception as e:
  print('ERROR: Could not get day perc increase:', e)
  exit(1)
