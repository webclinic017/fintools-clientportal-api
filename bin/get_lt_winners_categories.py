#!/usr/bin/env python3
# Get cheap symbols, and their categories

import json
import os
# Local
import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../'))
from lib.company import Company
from lib.filters import get_winners_lt_perc
from lib.util import error

debug = False
price_max = 3
perc_increase = 4

# Main
try:
  # Get winner symbols
  # symbol: {price, perc}
  # TODO: get_winners_lt_perc does not actually use perc_increase
  winner_symbols = get_winners_lt_perc(price_max, perc_increase)
  if debug:
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
  for symbol, price in winner_symbols.items():
    try:
      out[symbol].update({ 'industry': Company(symbol).industry})
    except Exception as e:
      error('ERROR: Could not get industry', e)
except Exception as e:
  error('ERROR: Could not get industries', e)
  exit(1)

# Final print
print(len(out))
print(out['REFR'])
#print(json.dumps(out))
