#!/usr/bin/env python3
# Get cheap symbols, and their categories

import json
import os
# Local
import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../'))
from lib.filters import get_contracts_cheaper_than

# Main
try:
  price = 3
  perc_increase = 4
  winners = get_winners_lt_perc(price, perc_increase)
  print(json.dumps(winners))
except Exception as e:
  print('ERROR: Could not get winners:', e)
  exit(1)
