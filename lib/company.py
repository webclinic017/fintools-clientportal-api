# Get conid from company, and vice versa
import os

f_conids = 'data/nasdaq_symbols_ib_conids'

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
    # data_format = [ 'symbol', 'conid' ]
    if kind == 'symbol':
      idx_kind = 0
      idx_val = 1
    else:
      idx_kind = 1
      idx_val = 0
    with open(f_conids) as f:
      lines = [line.rstrip().split(' ') for line in f]
      return next(line[idx_val] for line in lines if line[idx_kind] == value)
