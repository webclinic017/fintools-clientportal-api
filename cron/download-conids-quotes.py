#!/usr/bin/env python3
# Run this once a day
# It does:
# - download nasdaq symbols
# - download quotes
# - download conids. TODO: Only if don't yet have it
# 45 min running time
# OS
import atexit
import concurrent.futures
import datetime
import glob
import json
import os
import skip_quotes
import urllib.request
import urllib3

# Local
import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../'))
from lib.config import Config
import util
from lib.company import Company

# Config
pidfile = '/var/run/download-conids-quotes.pid'

# Settings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Vars
count_done = 0
count_perc = 0
count_total = 0
dir_quote = None
url_nasdaq_list = None
debug = None


def exit_handler():
  util.remove_pid(pidfile)
atexit.register(exit_handler)


def log(msg):
  print('%s: %s' %(
    datetime.datetime.today().strftime('%Y%m%d %H:%M'),
    msg
  ))


def get_quote(symbol):
  # Download conid and quote from IB
  # Also, update count percentage
  if debug:
    log('Start %s' % symbol)
  try:
    global count_done
    global count_perc
    global count_total
    global dir_quote
    ret = {}
    c = Company(symbol)
    quote = c.get_quote(period='3d', bar='1d')
    count_done += 1
    if (count_done/count_total)*10 >= count_perc:
      log(str(count_perc*10) + '%')
      count_perc = count_perc + 1
    with open(dir_quote + '/' + symbol + '.json', 'w') as f:
      # Save quote to dir
      f.write(json.dumps(quote))
    if debug:
      log('End %s' % symbol)
    return {
      'symbol': symbol,
      'data': quote,
    }
  except Exception as e:
    # Failed to get conid, print the ticker
    raise Exception('symbol: %s: %s' %(symbol, e))


## MAIN

if util.is_running(pidfile):
  print('Already running')
  exit(1)
else:
  util.create_pid(pidfile)

# Read config
print('Start')
cfg = Config()
dir_quote = cfg['paths']['quotes']
url_nasdaq_list = cfg['urls']['nasdaq_list']
debug = cfg['main']['debug']
download_conids_quotes_limit = cfg['main']['download_conids_quotes_limit']
download_conid_limit_enable = cfg['main']['download_conid_enable']
download_conid_limit_enable = False
if download_conid_limit_enable:
  download_conid_limit_symbol = cfg['main']['download_conid_limit_symbol']
print('Will save quotes to', dir_quote)


try:
  util.check_ib_connectivity()
except Exception as e:
  print('No IB connectivity')
  exit(1)

# Get NASDAQ symbols
log('Get NASDAQ symbols and their quotes')
quotes = []
with urllib.request.urlopen(url_nasdaq_list) as response:
  # Get NASDAQ symbols
  symb_nasdaq = [ line.split('|')[0]
    for line in response.read().decode('utf-8').splitlines()[1:-1]
  ]
  # Skip bad symbols
  symb_nasdaq = [
    symbol
    for symbol in symb_nasdaq
    if symbol not in skip_quotes.symbols
  ]
  # Take only N symbols (test)
  if debug:
    symb_nasdaq = symb_nasdaq[0:int(download_conids_quotes_limit)]
  # Take only one symbol if specified
  if download_conid_limit_enable:
    symb_nasdaq = download_conid_limit_symbol

  # Download conids and quotes
  count_total = len(symb_nasdaq)
  with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
    future_to_data = {
      executor.submit(get_quote, symbol): symbol
      for symbol in symb_nasdaq
    }
    for future in concurrent.futures.as_completed(future_to_data):
      res = future_to_data[future]
      try:
        res = future.result()
        quotes.append(res['symbol'])
      except Exception as e:
        # Failed to get quote for conid: add conid to skip list, and skip
        # TODO: Add to skip list
        if "'NoneType' object has no attribute points" in e \
          and 'W:' in e:
          print('Add conid %s to skip list' % symbol)
        else:
          log('Could not get conid: %s' % e)
  if len(quotes) == 0:
    log('Could not get quotes')
    exit(1)
  print('Got %i quotes' % len(quotes))
  # TODO: Remove here the quotes which could not find this time round
  # TODO: (delisted)
  #for f in glob.glob(dir_quote + '/*.json'):
  #  os.remove(f)
log('Finish')
