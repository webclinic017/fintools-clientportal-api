#!/usr/bin/env python3
# Run strategy from command line
import argparse
from perc import Perc

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument(
  'perc',
  metavar='N',
  type=int,
  default=4,
  nargs='?',
  help='an integer for the accumulator')
args = parser.parse_args()

# Run strategy
strategy = Perc()
strategy.run(args.perc)
