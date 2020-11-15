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
import cron.config
import util
from lib.company import Company

# Config
pidfile = '/var/run/downloader.pid'

# Settings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Vars
count_done = 0
count_perc = 0
count_total = 0


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
  try:
    global count_done
    global count_perc
    global count_total
    ret = {}
    c = Company(symbol)
    quote = c.get_quote('3d', '1d')
    count_done += 1
    if (count_done/count_total)*10 >= count_perc:
      log(str(count_perc*10) + '%')
      count_perc = count_perc + 1
    return quote
  except Exception as e:
    # Failed to get conid, print the ticker
    raise Exception('symbol: %s: %s' %(symbol, e))


## MAIN
if util.is_running(pidfile):
  print('Already running')
  exit(1)
else:
  util.create_pid(pidfile)


# Get NASDAQ symbols
log('Starting')
log('Init')
util.check_conidsfile(config.file_conids)

log('Get NASDAQ symbols and their quotes')
quotes = {}
with urllib.request.urlopen(config.url_nasdaq_list) as response:
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
  count_total = len(symb_nasdaq)
  # DEBUG: Get only few symbols
  #symb_nasdaq = symb_nasdaq[1:50]
  # END DEBUG
  with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
    future_to_data = {
      executor.submit(get_quote, symbol): symbol
      for symbol in symb_nasdaq
    }
    for future in concurrent.futures.as_completed(future_to_data):
      res = future_to_data[future]
      try:
        quotes.update(future.result())
      except Exception as e:
        # Failed to get quote for conid: add conid to skip list, and skip
        if "'NoneType' object has no attribute points" in e \
          and 'W:' in e:
          print('Add conid %s to skip list' % symbol)
        else:
          log('Could not get conid: %s' % e)
  if len(quotes) == 0:
    log('Could not get quotes')
    exit(1)
  # Save to quotes dir
  log('Save quotes to dir')
  for f in glob.glob(config.dir_quote + '/*.json'):
    os.remove(f)
  for symbol in quotes:
    with open(config.dir_quote + '/' + symbol + '.json', 'w') as f:
      f.write(json.dumps((quotes[symbol])['quote']))
  # Save conids
  # TODO: This should not happen here, but earlier by updating conids
  # TODO: file as we go
  conids = { symbol: quotes[symbol]['conid'] for symbol in quotes }
  with open(config.file_conids, 'w') as f:
    f.write(json.dumps(conids))
  log(conids)
log('Finished')
