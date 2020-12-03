#!/usr/bin/env python3
# Get cheap symbols, and their categories

import json
import os
# Local
import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../'))
from lib.filters import get_categories_cheaper_than

# Main
# TODO
try:
  # Get conid
  conid = int
  response = api.iserver_secdef_search_post({ "symbol": args.ticker })
  for item in response:
    if item.description == 'NASDAQ':
      print(item.conid)
      exit(0)
except ApiException as e:
    # Could not get conid, skip for now
    print("Could not get conid: %s\n" % e)
    exit(1)
