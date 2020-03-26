#!/usr/bin/env python3.7
# Run strategy from command line
import argparse

parser = argparse.ArgumentParser(description='Compound interest calculator.')
parser.add_argument('principal', metavar='PRIN',
  type=int,
  default=100,
  nargs='?',
  help='Principal investment')
parser.add_argument('perc', metavar='PERC',
  type=int,
  default=4,
  nargs='?',
  help='Percent gain on trade')
parser.add_argument('days', metavar='DAYS',
  type=int,
  default=220,
  nargs='?',
  help='How many days')
parser.add_argument('fees', metavar='FEES',
  type=float,
  default=0.46,
  nargs='?',
  help='Fee per trade')
args = parser.parse_args()
principal = args.principal
perc = args.perc
days = args.days
fees = args.fees

# Main
current = principal
for i in range(1, days+1):
  current = current + (perc/100)*current - 2*fees
print(f"{current:,.0f}")
