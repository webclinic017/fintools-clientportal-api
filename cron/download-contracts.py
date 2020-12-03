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
from lib.company import Company
from lib.filters import get_symbols_cheaper_than

# Helpers
def get_contract(symbol):
  print('Get contract', symbol)
  # get conid from disk (lib.company)
  # get contract
  # save to disk
  try:
    # Get conid from disk
    conid = Company(symbol).conid
  except ApiException as e:
    raise 'Could not get conid for' + symbol

  try:
    # Get contract info (name, industry, etc)
    return api.iserver_contract_conid_info_get(conid)
  except ApiException as e:
    raise 'Could not get contract: ' + e


# Main
# Instantiate API class
ib_cfg = ib_web_api.Configuration()
ib_cfg.verify_ssl = False
api = ContractApi(ib_web_api.ApiClient(ib_cfg))

try:
  # Get cheap symbols
  print('Get cheap symbols')
  symbols = get_symbols_cheaper_than(2)
  print('Got symbols:', len(symbols))
except Exception as e:
  print('ERROR: Could not get cheap symbols:', e)
  exit(1)

try:
  for symbol in symbols:
    contract = get_contract(symbol)
    print(symbol, contract)
except Exception as e:
  print('ERROR: Could not get contracts:', e)

