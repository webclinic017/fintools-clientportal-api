#!/usr/bin/env python3
# Run strategy from command line
import argparse
import datetime
import json

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument(
  'file',
  metavar='FILE',
  type=str,
  help='File name'
)
args = parser.parse_args()
f = args.file

# Helpers
def to_time(timestamp):
  return datetime.datetime.fromtimestamp(timestamp/1000).strftime('%Y%m%d %H%M')
def to_date(timestamp):
  return datetime.datetime.fromtimestamp(timestamp/1000).strftime('%Y%m%d')

# MAIN
with open(f) as f:
  data = json.load(f)
  for symbol in data:
    print(symbol + ': ' + str(len(data[symbol]['data'])))
    for p in data[symbol]['data']:
      print('%s: %s-%s: %.4s - %.4s %6.2s%% %3s - %3s %s' % (
        'DATE',
        p['time']['t0'],
        p['time']['t1'],
        p['price']['y0'],
        p['price']['y1'],
        p['perc'],
        p['volume']['v0'],
        p['volume']['v1'],
        '*' if p['time']['t0'] == p['time']['t1'] else ''
      ))
