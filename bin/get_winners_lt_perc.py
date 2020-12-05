#!/usr/bin/env python3
# Get cheap symbols, and their categories

import json
import os
# Local
import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../'))
from lib.filters import get_winners_lt_perc

price_max = 3
perc_increase = 4

# Main
try:
  # Get winner symbols
  winner_symbols = get_winners_lt_perc(price_max, perc_increase)
  print(json.dumps(winner_symbols))
except Exception as e:
  print('ERROR: Could not get winners:', e)
  exit(1)

try:
  winners = {}
  for symbol, price in winner_symbols:
    # Get industries
    print(symbol)
  print(
