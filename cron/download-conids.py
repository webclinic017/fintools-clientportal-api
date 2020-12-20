#!/usr/bin/env python3
# Download nasdaq symbols (their conids)
# Run once a week

# OS
import concurrent.futures
import json
from traceback import print_exc

# Local
import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../'))
from lib.company import Company
from lib.config import Config
from lib.util import down_symbols
from lib.util import log


# Vars (get later from config)
count_done = 0
count_perc = 0
url_nasdaq_list = None

def get_conid(symbol):
  # Download conid and quote from IB
  # Also, update count percentage
  if debug is True:
    log('Start %s' % symbol)
  try:
    global count_done
    global count_perc
    global count_total
    global dir_quote
    ret = {}
    c = Company(symbol)
    conid = c.conid
    count_done += 1
    if (count_done/count_total)*10 >= count_perc:
      log(str(count_perc*10) + '%')
      count_perc = count_perc + 1
    if debug:
      log('End %s' % symbol)
    return conid
  except Exception as e:
    # Failed to get conid, print the ticker
    raise Exception('symbol: %s: %s' %(symbol, e))


### MAIN ###
log('Start')

# Read config
cfg = Config()
dir_quote = cfg['paths']['quotes']
debug = cfg.getboolean('main', 'debug')

log('Get NASDAQ symbols')
symb_nasdaq = down_symbols(cfg)
count_total = len(symb_nasdaq)
print('Got %i symbols' % len(symb_nasdaq))
with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
  future_to_data = {
    executor.submit(get_conid, symbol): symbol
    for symbol in symb_nasdaq
  }
  for future in concurrent.futures.as_completed(future_to_data):
    res = future_to_data[future]
    try:
      res = future.result()
    except Exception as e:
      # Failed to get quote for conid: add conid to skip list, and skip
      # TODO: Add to skip list
      log('Could not get conid: %s' % e)
