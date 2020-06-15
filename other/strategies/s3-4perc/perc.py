import concurrent.futures
import datetime
import glob
import json
import os
import pprint
from lib.company import Company
from lib.util import get_perc_from_history

dir_day = '/opt/fintools-ib/data/day'
url_cheap_symbols = 'http://5.152.176.191/lt/1'
debug = True

def get_quote(symbol):
  pass

def get(point, kind):
  # point = { o, c, h, l, v, t }
  # kind = 'h' or 'l'
  return { 't': point['t'], 'value': point[kind], 'v': point['v'] }

def to_hour(timestamp):
  return datetime.datetime.fromtimestamp(timestamp/1000).strftime('%H%M')


class Perc:
  # Given a list of tickers, return tickers which ...
  def run(self, perc):
    # Get day cheap symbols
    i = 0
    ret = {}
    for f in glob.glob(dir_day + '/*.json'):
      if debug is True and i == 2:
        continue
      symbol = os.path.splitext(os.path.basename(f))[0]
      with open(f) as f:
        # [ { o, c, h, l, v, t }, { o, c, h, l, v, t } ]
        # Get perc
        data = json.load(f)
        if len(data) == 0:
          continue
        ret[symbol] = get_perc_from_history(data, perc)
      i += 1
    # Print
    print('Found %i symbols' % len(ret))
    # Format as JSON
    out = {}
    for symbol in ret:
      out[symbol] = {}
      out[symbol].update({
        'len': len(ret[symbol]),
        'data': [],
      })
      print('%s: %i' % (symbol, len(ret[symbol])))
      for p in ret[symbol]:
        out[symbol]['data'].append({
          'time': {
            't0': to_hour(p['t0']),
            't1': to_hour(p['t1']),
          },
          'price': {
            'y0': p['y0'],
            'y1': p['y1'],
          },
          'perc': round(p['perc'], 2),
          'volume': {
            'v0': p['v0'],
            'v1': p['v1'],
          },
        })
    print(json.dumps(out, indent=2))
