#!/usr/bin/env python3
# Download today's data for tickers under $1/share
# Optionally, supply list of tickers, e.g.
# ./$0 AAPL AMZN
import argparse
import concurrent.futures
import glob
import ib_web_api
import json
import os
import pprint
import urllib3
import urllib.request
from lib.company import Company
from ib_web_api import MarketDataApi

dir_quote = '/opt/fintools-ib/data/quotes'
dir_day = '/opt/fintools-ib/data/day'
url_cheap_symbols = 'http://5.152.176.191/lt/1'
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
debug = False

def get_quote(symbol):
  for i in range(1, 6):
    try:
      # Init client
      config = ib_web_api.Configuration()
      config.verify_ssl = False
      client = ib_web_api.ApiClient(config)
      api = MarketDataApi(client)
      conid = Company(symbol).get_conid()
      response = api.iserver_marketdata_history_get(
        conid,
        '1d',
        bar='1min'
      )
    except Exception as e:
      if i == 6:
        raise Exception('Could not get symbol %s' % symbol)
      else:
        print('Retry %s' % symbol)
        continue
    return { symbol: response.data }

# Main
# Parse args
parser = argparse.ArgumentParser(description='Download today\'s data')
parser.add_argument('symbols',
  metavar='S',
  type=str,
  nargs='*',
  help='List of symbols, e.g. AAPL AMZN'
)
args = parser.parse_args()

# Get Get cheap symbols
with urllib.request.urlopen(url_cheap_symbols) as response:
  symbols = json.loads(response.read().decode('utf-8'))
  day_quotes = {}
  if debug is True:
    symbols = { key: symbols[key] for key in list(symbols)[0:5] }
  if args.symbols:
    symbols = args.symbols
  with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
    future_to_data = {
      executor.submit(get_quote, symbol): symbol
      for symbol in symbols
    }
    for future in concurrent.futures.as_completed(future_to_data):
      try:
        day_quotes.update(future.result())
      except Exception as e:
        # Failed to get conid, skip
        print('EXC: %s' % e)
        pass
  # Save to day dir
  print('Got %i quotes' % len(day_quotes))
  for f in glob.glob(dir_day + '/*.json'):
    os.remove(f)
  for symbol in day_quotes:
    f_path = dir_day + '/' + symbol + '.json'
    with open(f_path, 'w') as f:
      if day_quotes[symbol] is not None:
        data = [ point.to_dict() for point in day_quotes[symbol]]
        f.write(json.dumps(data))
      else:
        print(f'No data for {symbol}')
        os.remove(f_path)
