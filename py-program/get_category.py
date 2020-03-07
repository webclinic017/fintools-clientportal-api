#!/usr/bin/env python3
# Get category of given tickers
# Run as:  ./get_category.py TICKERS
# Example: ./get_category.py AAPL AMZN

import argparse
import ib_web_api
import json
import os
import pprint
from datetime import datetime
from ib_web_api import ContractApi
from ib_web_api.rest import ApiException

# Parse args
parser = argparse.ArgumentParser(
    description='Display last day data for ticker')
parser.add_argument('tickers', metavar='TICKERS', type=str, nargs='+',
    help='Tickers, e.g. AAPL AMZN')
parser.add_argument('-v', dest='verbose', action='store_true',
                    help='Verbose mode, print info messages')
args = parser.parse_args()

# Instantiate API class
config = ib_web_api.Configuration()
config.verify_ssl = False
client = ib_web_api.ApiClient(config)
api = ContractApi(client)

# Main
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
        print(symbol, ret.category)
except ApiException as e:
    print("Exception: %s\n" % e)
