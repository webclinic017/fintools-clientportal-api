#!/usr/bin/env python3
# Run strategy from command line
import argparse
import ib_web_api
import pprint
import urllib3
from ib_web_api import MarketDataApi
from lib.icompany import ICompany

# Settings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument(
  'symbols',
  metavar='SYMBOL',
  type=str,
  nargs='+',
  help='Symbols, e.g. AAPL AMZN'
)
args = parser.parse_args()
symbols = args.symbols

# Helpers

# Get symbol conids
symbols = { symbol: ICompany(symbol).get_conid() for symbol in symbols }
for symbol in symbols:
  quote = ICompany(symbol).get_quote('1m', '5min')
  pprint.pprint(quote)

# TODO
# split into days
