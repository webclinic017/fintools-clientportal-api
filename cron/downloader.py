#!/usr/bin/env python3
import concurrent.futures
import datetime
import glob
import json
import os
import pprint
import urllib.request
import urllib3
from lib.icompany import ICompany

url_nasdaq_list = 'ftp://ftp.nasdaqtrader.com/symboldirectory/nasdaqlisted.txt'
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
quote_dir = '/opt/fintools-ib/data/quotes'

def log(msg):
  print('%s: %s' %(
    datetime.datetime.today().strftime('%Y%m%d %H:%M'),
    msg
  ))

def get_quote(symbol):
  return { symbol:  ICompany(symbol).get_quote() }

# Get NASDAQ symbols
log('Get NASDAQ symbols and their quotes')
quotes = {}
with urllib.request.urlopen(url_nasdaq_list) as response:
  symb_nasdaq = [ line.split('|')[0]
    for line in response.read().decode('utf-8').splitlines()[1:-1]
  ]
  ## DEBUG: Reduce
  #symb_nasdaq = symb_nasdaq[4:6]
  ## END DEBUG
  with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    future_to_data = {
      executor.submit(get_quote, symbol): symbol
      for symbol in symb_nasdaq
    }
    for future in concurrent.futures.as_completed(future_to_data):
      res = future_to_data[future]
      try:
        data = future.result()
        quotes.update(data)
        print('.', end='')
      except Exception as e:
        print('x', end='')
        # Failed to get conid, skip
        pass
  if len(quotes) == 0:
    print('Could not get quotes')
    exit(1)
  # Save to quotes dir
  for f in glob.glob(quote_dir + '/*.json'):
    os.remove(f)
  for symbol in quotes:
    with open(quote_dir + '/' + symbol + '.json', 'w') as f:
      f.write(json.dumps(quotes[symbol]))
log('Finished')
