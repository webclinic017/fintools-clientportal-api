#!/usr/bin/env python3
# Download today's data for tickers under $1/share
# Optionally, supply list of tickers, e.g.
# ./$0 AAPL AMZN
import argparse
import concurrent.futures
import glob
import ib_web_api
import json
import os
import pprint
import urllib3
import urllib.request
from lib.company import Company
from lib.icompany import ICompany
from ib_web_api import MarketDataApi

dir_quote = '/opt/fintools-ib/data/quotes'
dir_day = '/opt/fintools-ib/data/day'
url_cheap_symbols = 'http://5.152.176.191/lt/1'
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
debug = False

def get_quote(symbol):
  # Init client
  conid = Company(symbol).get_conid()
  company = ICompany(conid)
  try:
    quote = ICompany(conid).get_quote('2d', '1min')
  except Exception as e:
    raise Exception('Could not get symbol %s' % symbol)
  return { symbol: quote }

# Main
# Parse args
parser = argparse.ArgumentParser(description='Download today\'s data')
parser.add_argument('symbols',
  metavar='S',
  type=str,
  nargs='*',
  help='List of symbols, e.g. AAPL AMZN'
)
args = parser.parse_args()

# Get cheap symbols
print(get_quote('OTLK'))
