# Get conid from company, and vice versa
import json
import os

f_conids = '/opt/fintools-ib/data/conids.json'

class Company:
  # Properties
  conid = None
  symbol = None

  # Constructor
  def __init__(self, info):
    if isinstance(info, int):
      self.conid = info
    else:
      self.symbol = info

  # Methods
  def get_conid(self):
    if self.conid is None:
      return self.find_by('symbol', self.symbol)
    else:
      return self.conid

  def get_symbol(self):
    if self.symbol is None:
      return find_by('conid', self.conid)
    else:
      return self.symbol

  # Private
  def find_by(self, kind, value):
    # Convert symbol to conid or conid to symbol
    # kind: conid or symbol
    # value: e.g. 1234 or AAPL
    with open(f_conids) as f:
      f = json.load(f)
      if kind == 'symbol':
        if value in f:
          return f[value]
        else:
          raise Exception('Symbol %s not found' % value)
      else:
        for symbol, conid in f.items():
          if conid == value:
            return symbol
