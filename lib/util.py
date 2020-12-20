# Utilities

# OS
import datetime
import json
import sys
import urllib.request

# Local
import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../'))
from lib.config import Config
from lib.skipsymbols import Skipsymbols

# HELPERS

def error(msg):
  print(msg, file=sys.stderr)

def get(point, kind):
  # point = { o, c, h, l, v, t }
  # kind = 'h' or 'l'
  return { 't': point['t'], 'value': point[kind], 'v': point['v'] }

def down_symbols(cfg, apply_filters=True):
  # Download list of symbols (filter out also)
  url_nasdaq_list = cfg['urls']['nasdaq_list']
  debug = cfg['main']['debug']
  # Limit to conid
  download_conids_quotes_limit = cfg['main']['download_conids_quotes_limit']
  download_conid_limit_enable = cfg.getboolean('main', 'download_conid_limit_enable')
  download_conid_limit_symbol = cfg['main']['download_conid_limit_symbol']

  with urllib.request.urlopen(url_nasdaq_list) as response:
    # Get NASDAQ symbols
    symb_nasdaq = [ line.split('|')[0]
      for line in response.read().decode('utf-8').splitlines()[1:-1]
    ]
    # Take only N symbols (test)
    if debug:
      symb_nasdaq = symb_nasdaq[0:int(download_conids_quotes_limit)]
    # Take only one symbol if specified
    if download_conid_limit_enable:
      symb_nasdaq = [ download_conid_limit_symbol ]
    # Skip bad symbols
    skip = Skipsymbols().get()
    symb_nasdaq = [
      symbol
      for symbol in symb_nasdaq
      if symbol not in skip
    ]
  return symb_nasdaq


def get_symbols():
  # List conids from disk
  # TODO
  try:
    cfg = Config()
  except Exception as e:
    raise Exception('Could not read config')
  l = sorted(os.listdir(cfg['paths']['conids']))
  l.remove('README.md')
  return l

def get_contracts():
  # List contracts from disk
  try:
    cfg = Config()
  except Exception as e:
    raise Exception('Could not read config')
  l = sorted(os.listdir(cfg['paths']['contracts']))
  l = [ el.replace('.json', '') for el in l ]
  return l

def get_quotes():
  # List quotes from disk
  try:
    cfg = Config()
  except Exception as e:
    raise Exception('Could not read config')
  l = sorted(os.listdir(cfg['paths']['quotes']))
  l = [ el.replace('.json', '') for el in l ]
  return l

def get_perc_from_history(data, perc):
  # data = {
  #  { 'o': 1, 'h': 2, 'l': 3, 'c': 4 },
  # ...
  # }
  # perc: e.g. 4 for 4%
  # Sort by timestamp
  data = sorted(data, key=lambda k: k['t'])
  # Get points
  hi = get(data[0], 'h')
  lo = get(data[0], 'l')
  finding_hi = True
  points = []
  for point in data:
    hi = get(point, 'h')
    if point['l'] < lo['value']:
      lo = get(point, 'l')
    if hi['value']/lo['value'] > (100+perc)/100:
      if hi['t'] == lo ['t']:
        extra = '*'
      else:
        extra = ''
      v0 = lo
      v1 = hi
      points.append({
        't0': v0['t'],
        't1': v1['t'],
        'y0': v0['value'],
        'y1': v1['value'],
        'v0': v0['v'],
        'v1': v1['v'],
        'perc': (hi['value']/lo['value'])*100 - 100
      })
      lo = get(point, 'h')
  return points


def log(msg):
  print('%s: %s' %(
    datetime.datetime.today().strftime('%Y%m%d %H:%M'),
    msg
  ))


def timestamp_to_date(timestamp):
  timestamp = int(timestamp)
  return datetime.datetime.fromtimestamp(timestamp/1000).strftime('%Y%m%d')

