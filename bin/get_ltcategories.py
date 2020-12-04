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
  contracts = get_contracts_cheaper_than(3, redownload=True)
  print(json.dumps(contracts))
except Exception as e:
  print('ERROR: Could not get contracts:', e)
  exit(1)
