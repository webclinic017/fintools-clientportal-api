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
# Local
import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../'))
import config

# Config
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
      try:
        # Download from API as not in cache
        # NOTE: This should be rare, so print it
        print('Not found in cache, download conid for %s: %s' % (symbol, e))
        self.conid = self.down_conid()
        with open(config.dir_conids + '/' + symbol, 'w') as f:
          f.write(str(self.conid))
      except Exception as e:
        print('Could not save conid: %s' % e)

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
    if kind == 'symbol':
      symbol = value
      try:
        file_conid = config.dir_conids + '/' + symbol
        with open(file_conid, 'r') as f:
          return f.read()
      except Exception as e:
        raise Exception('Symbol %s not found' % symbol)
    else:
      raise Exception('Search by conids not yet implemented')
