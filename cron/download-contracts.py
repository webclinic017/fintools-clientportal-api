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

dir_contracts = config.dir_contracts

# Helpers
def get_contract(symbol):
  # Download contract from IB and save it to disk
  print('Get contract', symbol)
  try:
    # Get conid from disk
    conid = Company(symbol).conid
  except ApiException as e:
    raise 'Could not get conid for' + symbol

  try:
    # Get contract (name, industry, etc)
    contract = api.iserver_contract_conid_info_get(conid)
    # Remove unnecessary data
    contract = {
      'conid': contract.con_id,
      'category': contract.category,
      'industry': contract.industry,
    }
  except ApiException as e:
    raise e

  try:
    # Save contract to disk
    with open(dir_contracts + '/' + symbol + '.json', 'w') as f:
      f.write(json.dumps(contract))
  except ApiException as e:
    raise 'Could not save contract: ' + e


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

for symbol in symbols:
  try:
    contract = get_contract(symbol)
  except Exception as e:
    print('ERROR: Could not get contract', symbol, ':', e)

