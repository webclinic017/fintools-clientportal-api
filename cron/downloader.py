#!/usr/bin/env python3
# Run this once a day
# It does:
# - download nasdaq symbols
# - download quotes
# - download conids
import concurrent.futures
import datetime
import glob
import json
import os
import skip_quotes
import urllib.request
import urllib3
from lib.icompany import ICompany

url_nasdaq_list = 'ftp://ftp.nasdaqtrader.com/symboldirectory/nasdaqlisted.txt'
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
quote_dir = '/opt/fintools-ib/data/quotes'
conids_file = '/opt/fintools-ib/data/conids.json'
count_total = 0
count_done = 0
count_perc = 0

def log(msg):
  print('%s: %s' %(
    datetime.datetime.today().strftime('%Y%m%d %H:%M'),
    msg
  ))

def get_quote(symbol):
  # Download conid and quote from IB
  global count_done
  global count_perc
  global count_total
  ret = {}
  c = ICompany(symbol)
  quote = c.get_quote('3d', '1d')
  conid = c.get_conid()
  count_done += 1
  if (count_done/count_total)*10 >= count_perc:
    log(str(count_perc*10) + '%')
    count_perc = count_perc + 1
  return {
    symbol: {
      'conid': conid,
      'quote': quote
    }
  }

# Get NASDAQ symbols
log('Starting')
log('Get NASDAQ symbols and their quotes')
quotes = {}
with urllib.request.urlopen(url_nasdaq_list) as response:
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
        # Failed to get conid, skip
        log('Could not get conid: %s' % e)
        pass
  if len(quotes) == 0:
    log('Could not get quotes')
    exit(1)
  # Save to quotes dir
  log('Save quotes to dir')
  for f in glob.glob(quote_dir + '/*.json'):
    os.remove(f)
  for symbol in quotes:
    with open(quote_dir + '/' + symbol + '.json', 'w') as f:
      f.write(json.dumps((quotes[symbol])['quote']))
  # Save conids
  conids = { symbol: quotes[symbol]['conid'] for symbol in quotes }
  with open(conids_file, 'w') as f:
    f.write(json.dumps(conids))
  log(conids)
log('Finished')
