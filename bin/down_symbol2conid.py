#!/usr/bin/env python3
# Get NASDAQ conid for given ticker
# Return exitcode 1 if ticker is not NASDAQ or not in IB
# Run as:  ./get_conid_nasdaq.py TICKERS
# Example: ./get_conid_nasdaq.py AAPL

import argparse
import ib_web_api
import json
import os
import pprint
import urllib3
from datetime import datetime
from ib_web_api import ContractApi
from ib_web_api.rest import ApiException

# Config
urllib3.disable_warnings()

# Parse args
parser = argparse.ArgumentParser(
    description='Display last day data for ticker')
parser.add_argument('ticker', metavar='TICKER', type=str,
    help='Ticker, e.g. AAPL')
parser.add_argument(
    '-s',
    dest='small',
    action='store_true',
    help='Print only result (category), without the ticker'
)
args = parser.parse_args()

# Instantiate API class
config = ib_web_api.Configuration()
config.verify_ssl = False
client = ib_web_api.ApiClient(config)
api = ContractApi(client)

# Main
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
