#!/usr/bin/env python3
# Run strategy from command line
import argparse
from vol_increase import VolIncrease

# Parse args
parser = argparse.ArgumentParser(description='Run strategy 2.')
parser.add_argument(
  'symbols',
  metavar='SYMBOLS',
  type=str,
  nargs='+',
  help='Symbols'
)
args = parser.parse_args()
symbols = args.symbols

# Run strategy
strategy = VolIncrease()
strategy.run(symbols)
