# OS
import json

# Local
import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../'))
import config
from lib.company import Company


def get_symbols_cheaper_than(price):
  res = {}
  dir_quote = config.dir_quote
  for s_file in os.listdir(dir_quote):
    # For each quote, find cheap ones
    try:
      symbol = s_file.split('.')[0]
      fname = dir_quote + '/' + s_file
      if os.stat(fname).st_size > 1:
        with open(fname) as f:
          price_found = json.load(f)['c']
          if float(price_found) <= float(price):
            res[symbol] = price_found
    except Exception as e:
      print('Unable to read %s' % s_file)
    for k, v in sorted(res.items()):
      # Sort by symbol
      res[k] = v
  return res

def get_contracts_cheaper_than(price, redownload=False):
  symbols = get_symbols_cheaper_than(price)
  res = {}
  for symbol, price in symbols:
    company = Company(symbol)
    contract = company.get_contract()
    res['symbol'] = {
      'price': price,
      'category': contract['category'],
      'industry': contract['industry'],
    }
  return res
