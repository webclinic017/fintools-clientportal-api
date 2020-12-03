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
dir_contracts = config.dir_contracts

class Company:
  # Properties
  conid = None
  contract = None
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
    # Get quote
    # Note, we already have conid from constructor
    # TODO: Get from cache maybe if not yet have it
    try:
      return self.down_quote(self.conid, period, bar)
    except ApiException as e:
      raise Exception('Could not download quote: %s\n' % self.conid)

  def get_contract(self):
    # Get contract
    # TODO: Get from cache if already there
    try:
     return self.down_contract()
    except ApiException as e:
      raise Exception('Could not download contract: %s (%s): %s\n'
        % (self.symbol, self.conid, e))


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
    ib_cfg = ib_web_api.Configuration()
    ib_cfg.verify_ssl = False
    api = MarketDataApi(ib_web_api.ApiClient(ib_cfg))
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
      if hasattr(res, 'points'):
        point = int(res.points)
        res = res.data[point].to_dict()
      else:
        raise Exception('Missing "points" for %s' % self.conid)
    else:
      if res is not None:
        res = [ i.to_dict() for i in res.data ]
      else:
        raise Exception('Could not get quote', self.conid)
    return res

  def down_contract(self):
    # Download contract from IB and save it to disk
    # Note: Already have conid from cache
    try:
      # Init API
      ib_cfg = ib_web_api.Configuration()
      ib_cfg.verify_ssl = False
      api = ContractApi(ib_web_api.ApiClient(ib_cfg))

      # Get contract (name, industry, etc)
      contract = api.iserver_contract_conid_info_get(self.conid)
      # Remove unnecessary data
      contract = {
        'conid': contract.con_id,
        'category': contract.category,
        'industry': contract.industry,
      }
      self.contract = contract
    except ApiException as e:
      raise e

    try:
      # Save contract to disk
      with open(dir_contracts + '/' + self.symbol + '.json', 'w') as f:
        f.write(json.dumps(contract))
    except ApiException as e:
      raise 'Could not save contract: ' + e
    return self.contract


  def disk_find_by(self, kind, value):
    # Convert symbol to conid or conid to symbol
    # kind: conid or symbol
    # value: e.g. 1234 or AAPL
    # NOTE: Usually used to get conid from symbol
    # TODO: Scrap this, just search by symbol
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

  def disk_find_contract(self)
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
