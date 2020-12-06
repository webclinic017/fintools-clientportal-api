#!/usr/bin/env python3
# Get ohlc history for given symbol
# Run as:  ./$0 TICKERS
# Example: ./$0 HTBX
import argparse
import json
from lib.company import Company

# Parse args
parser = argparse.ArgumentParser(
  description='Display last day data for symbol'
)
parser.add_argument(
  'symbol',
  metavar='SYMBOL',
  type=str,
  help='Symbol, e.g. HTBX'
)
args = parser.parse_args()
symbol = args.symbol

## MAIN
history = Company(symbol).get_quote('1m', '5min')
print(json.dumps(history, indent=2))
