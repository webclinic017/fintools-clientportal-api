# Get conid from company, and vice versa
# This either downloads the data from IB, instead of from disk (cache)
# TODO: Rename to Company
import ib_web_api
import json
import os
import urllib3
import urllib.request
from ib_web_api import ContractApi
from ib_web_api import MarketDataApi
from ib_web_api.rest import ApiException

# Config
f_conids = 'data/conids.json'
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Company:
  # Properties
  conid = None
  symbol = None

  # Constructor
  def __init__(self, symbol):
    self.symbol = symbol
    try:
      # Get conid from cache
      self.conid = self.disk_find_by('symbol', self.symbol)
    except Exception as e:
      # Download from API as not in cache
      self.conid = self.down_conid()

  # PUBLIC METHODS
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
      return self.down_quote(self.conid, period, bar)
    except ApiException as e:
      raise Exception('Could not get quote: %s\n' % self.conid)



  # PRIVATE
  def down_conid(self):
    # API: Get conid for symbol
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

  def down_quote(self, conid, period, bar):
    config = ib_web_api.Configuration()
    config.verify_ssl = False
    client = ib_web_api.ApiClient(config)
    api = MarketDataApi(client)
    res = None
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
    # If three days, pick the last day
    # TODO: Do we need it like this?
    if period == '3d' and bar == '1d':
      point = int(res.points)
      res = res.data[point].to_dict()
    else:
      if res is not None:
        res = [ i.to_dict() for i in res.data ]
      else:
        raise Exception('Could not get quote', self.conid)
    return res

  def disk_find_by(self, kind, value):
    # Convert symbol to conid or conid to symbol
    # kind: conid or symbol
    # value: e.g. 1234 or AAPL
    # NOTE: Usually used to get conid from symbol
    # data_format = [ 'symbol', 'conid' ]
    # Throw exception if data not on disk
    #if kind == 'symbol':
    #  idx_kind = 0
    #  idx_val = 1
    #else:
    #  idx_kind = 1
    #  idx_val = 0
    #with open(f_conids) as f:
    #  lines = [line.rstrip().split(' ') for line in f]
    #  return next(line[idx_val] for line in lines if line[idx_kind] == value)
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
