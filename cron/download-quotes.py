#!/usr/bin/env python3
# Run this once a day at market close
# It does:
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
import urllib3

# Local
import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../'))
from lib.config import Config
from lib.util import down_symbols
from lib.util import log
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
debug = None


def exit_handler():
  util.remove_pid(pidfile)
atexit.register(exit_handler)


def get_quote(symbol):
  global debug
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
debug = cfg.getboolean('main', 'debug')
print('Will save quotes to', dir_quote)


try:
  util.check_ib_connectivity()
except Exception as e:
  print('No IB connectivity')
  exit(1)

# Get NASDAQ symbols
log('Get NASDAQ symbols and their quotes')
symb_nasdaq = down_symbols(cfg)
quotes = []

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
      if "'NoneType' object has no attribute points" in str(e) \
        and 'W:' in str(e):
      else:
        print_exc(e)
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
