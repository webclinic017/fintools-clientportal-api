#!/usr/bin/env python3
# Get cheap symbols, and their categories

import json
import os
# Local
import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../'))
from lib.filters import get_contracts_cheaper_than

# Main
# Check params
if len(sys.argv) < 2:
  print('Provide industry')
  exit(2)
industry = sys.argv[1]

try:
  contracts = get_contracts_cheaper_than(3)
except Exception as e:
  print('ERROR: Could not get contracts:', e)
  exit(1)

ret = {
  symbol: info
  for symbol, info
  in contracts.items()
  if info['industry'] == industry
}
print(json.dumps(ret))
