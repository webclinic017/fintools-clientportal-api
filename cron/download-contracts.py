#!/usr/bin/env python3
# Get category of given tickers
# Run as:  ./get_category.py TICKERS
# Example: ./get_category.py AAPL AMZN

import argparse
import ib_web_api
import json
import os
import pprint
import urllib3
import urllib.request
from datetime import datetime
from ib_web_api import ContractApi
from ib_web_api.rest import ApiException

# Local
import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../'))
import config
import lib.filters

# lt/2

# Instantiate API class
ib_cfg = ib_web_api.Configuration()
ib_cfg.verify_ssl = False
client = ib_web_api.ApiClient(ib_cfg)
api = ContractApi(client)

# Main
try:
  # Get cheap symbols
  print('Get cheap symbols')
  with urllib.request.urlopen(config.url_cheap_symbols) as response:
    symbols = json.loads(response.read().decode('utf-8'))
    print('Got symbols:', len(symbols))
except Exception as e:
  print('ERROR:', e)

exit(0)


try:
  # Get conids
  if args.verbose:
    print('Get conids')
  conids = {}
  for ticker in args.tickers:
    conid = int
    try:
      response = api.iserver_secdef_search_post({ "symbol": ticker })
    except Exception:
      # Could not get conid, so skip it
      continue
    for item in response:
      if item.description == 'NASDAQ':
        conids[ticker] = item.conid
except ApiException as e:
  # Could not get conid, skip for now
  print("Could not get conids: %s\n" % e)
  exit(1)
if len(conids) == 0:
  # Terminate if no conids found
  print('Could not find any conids')
  exit(1)

# Print summary
if args.verbose:
  print('Conids found: %s/%s' % (len(conids), len(args.tickers)))

try:
  # Get market data for each conid
  for symbol, conid in conids.items():
    ret = api.iserver_contract_conid_info_get(conid)
    if args.small:
      print(ret.category)
    else:
      print(symbol, ret.category)
except ApiException as e:
  print("Exception: %s\n" % e)
