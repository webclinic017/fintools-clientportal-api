#!/usr/bin/env python3.7
import argparse
import json

parser = argparse.ArgumentParser(description='Compound interest calculator.')
parser.add_argument('file', metavar='FILE',
  type=str,
  help='File name')
args = parser.parse_args()
f = args.file
ret = {}
with open(f) as f:
  lines = f.read().splitlines()
  for l in lines:
    if 'Found' in l:
      continue
    if len(l) < 10:
      symbol = l.split(':')[0]
      ret[symbol] = { 'data': [], 'len': 0 }
      continue
    else:
      ret[symbol]['len'] += 1
    values = [ l for l in l.split(' ') if l is not '' and l is not '-' ]
    time = values[1].rstrip(':').split('-')
    print(values[0])
    ret[symbol]['data'].append({
      'perc': values[4],
      'price': { 'y0': values[2], 'y1': values[3], },
      'time': { 't0': time[0], 't1': time[1], },
      'volume': { 'v0': values[5], 'v1': values[6], },
    })
  print(json.dumps(ret, indent=2))
