# Get conid from company, and vice versa
# This downloads the data from IB
import ib_web_api
import os
from ib_web_api import ContractApi
from ib_web_api import MarketDataApi
from ib_web_api.rest import ApiException

f_conids = 'data/nasdaq_symbols_ib_conids'

class ICompany:
  # Properties
  conid = None
  symbol = None

  # Constructor
  def __init__(self, info):
    if isinstance(info, int):
      self.conid = info
    else:
      self.symbol = info

  # PUBLIC METHODS
  def get_conid(self):
    if self.conid is None:
      self.conid = self.down_conid()
    return self.conid

  def get_quote(self, period, bar):
    # Get conid, then quote
    try:
      # Get conid
      if self.conid is None:
        self.get_conid()
    except ApiException as e:
      if self.conid is not None:
        detail = self.conid
      else:
        detail = self.symbol
      raise Exception('Could not get conid: %s\n' % symbol)
    try:
      # Get quote
      return self.conid_to_quote(self.conid, '3d', '1d')
    except ApiException as e:
      raise Exception('Could not get quote: %s\n' % self.conid)

  def get_symbol(self):
    if self.symbol is None:
      return find_by('conid', self.conid)
    else:
      return self.symbol



  # PRIVATE
  def down_conid(self):
    if self.conid is None:
      # Download conid
      config = ib_web_api.Configuration()
      config.verify_ssl = False
      client = ib_web_api.ApiClient(config)
      api = ContractApi(client)
      # Main
      try:
        # Get conid
        conid = int
        response = api.iserver_secdef_search_post({ "symbol": self.symbol })
        for item in response:
          if item.description == 'NASDAQ':
            self.conid = item.conid
      except ApiException as e:
        if self.conid is not None:
          detail = self.conid
        else:
          detail = self.symbol
        raise Exception('Could not download conid %s.' % detail)
    return self.conid

  def conid_to_quote(self, conid, period, bar):
    # TODO: Does this need to download 3 days?
    config = ib_web_api.Configuration()
    config.verify_ssl = False
    client = ib_web_api.ApiClient(config)
    api = MarketDataApi(client)
    for i in range(1, 6):
      try:
        # Download conid
        res = api.iserver_marketdata_history_get(
          conid,
          period=period,
          bar=bar
        )
      except Exception as e:
        if i == 6:
          raise Exception('Could not get quote: %s\n' % e)
        else:
          continue
    # If more than one day, pick the last day
    if period == '3d' and bar == '1d':
      point = int(res.points)
      res = res.data[point].to_dict()
    else:
      res = res.data
    return res

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
