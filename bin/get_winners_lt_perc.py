#!/usr/bin/env python3
# Get cheap symbols, and their categories

import json
import os
# Local
import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../'))
from lib.company import Company
from lib.filters import get_winners_lt_perc

price_max = 3
perc_increase = 4

# Main
try:
  # Get winner symbols
  # TODO: get_winners_lt_perc does not actually use perc_increase
  winner_symbols = get_winners_lt_perc(price_max, perc_increase)
  print('Got %i winner symbols' % len(winner_symbols))
except Exception as e:
  print('ERROR: Could not get winners:', e)
  exit(1)
# Populate data
out = {}
for symbol, price in winner_symbols.items():
  out[symbol] = {
    'price': price,
    'industry': None,
}

try:
  # Get industry from symbols
  winners = {}
  for symbol, price in winner_symbols.items():
    try:
      out[symbol].update({ 'industry': Company(symbol).industry})
    except Exception as e:
      print('ERROR: Could not get industry', e)
  print(winners)
except Exception as e:
  print('ERROR: Could not get industries', e)
  exit(1)

# Final print
print(json.dumps(out))
