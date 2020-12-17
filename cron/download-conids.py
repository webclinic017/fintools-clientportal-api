#!/usr/bin/env python3
# Download nasdaq symbols (their conids)
# Run once a week

# OS
import urllib.request
import concurrent.futures


# Local
import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../'))
from cron import skip_quotes
from lib.company import Company
from lib.config import Config
from lib.util import log

# Vars (get later from config)
count_done = 0
count_perc = 0
count_total = 0
debug = None
url_nasdaq_list = None

def get_conid(symbol):
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


### MAIN ###
print('Start')
cfg = Config()
dir_quote = cfg['paths']['quotes']
url_nasdaq_list = cfg['urls']['nasdaq_list']

log('Get NASDAQ symbols')
with urllib.request.urlopen(url_nasdaq_list) as response:
  # Get quotes for symbols
  symb_nasdaq = [ line.split('|')[0]
    for line in response.read().decode('utf-8').splitlines()[1:-1]
  ]
  # Skip bad symbols
  symb_nasdaq = [
    symbol
    for symbol in symb_nasdaq
    if symbol not in skip_quotes.symbols
  ]
  with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
    future_to_data = {
      executor.submit(get_conid, symbol): symbol
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
        if "'NoneType' object has no attribute points" in str(e) \
          and 'W:' in str(e):
          print('Add conid %s to skip list' % symbol)
        else:
          log('Could not get conid: %s' % e)


