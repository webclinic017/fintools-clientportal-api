#!/usr/bin/env python3
# Down ticker 2 quote
# Run as:  ./script.py TICKER
# Example: ./script.py AAPL

# OS
import argparse
import json
import os
import urllib3

# Local
import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../'))
from lib.company import Company

# Config
urllib3.disable_warnings()

### MAIN ###
# Parse args
parser = argparse.ArgumentParser(
    description='Get quote for symbol')
parser.add_argument('symbol', metavar='SYMBOL', type=str,
    help='Symbol, e.g. AAPL')
args = parser.parse_args()
symbol = args.symbol

# Get quote
c = Company(symbol)
quote = c.get_quote(period='3d', bar='1d')
print(quote)
