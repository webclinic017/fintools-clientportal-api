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
from lib.config import Config
from lib.util import error

# Config
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Company:
  # Properties
  conid = None
  contract = None
  industry = None
  symbol = None
  cfg = {}

  # Constructor
  def __init__(self, symbol):
    self.symbol = symbol

    # Config
    cfg = Config()
    self.cfg = {
      'dir_conids': cfg['paths']['conids'],
      'dir_contracts': cfg['paths']['contracts'],
      'dir_day': cfg['paths']['day'],
      'dir_quotes': cfg['paths']['quotes'],
    }

    try:
      # Get conid from cache
      self.conid = self.disk_find_by('symbol', self.symbol)
    except Exception as e:
      try:
        # Download from API as not in cache
        # NOTE: This should be rare, so print it
        print('Not found in cache, download conid for %s: %s' % (symbol, e))
        self.conid = self.down_conid()
      except Exception as e:
        print('Could not save conid: %s' % e)
    try:
      # Get industry from cache
      contract = self.disk_find(kind='contract')
      self.industry = contract['industry']
    except Exception as e:
      error('Could not get industry from cache %s: %s' % (symbol, e))


  # PUBLIC METHODS: Aggregates
  def get_quote(self, period, bar):
    # Get quote
    # Note, we already have conid from constructor
    # TODO: Get from cache maybe if not yet have it
    try:
      return self.down_quote(self.conid, period, bar)
    except ApiException as e:
      raise Exception('Could not download quote: %s\n' % self.conid)

  def get_quote_single(self):
    # Get quote for one day
    period = '1d'
    bar = '1d'
    # TODO: Get from cache maybe if not yet have it
    try:
      return self.disk_find('quote')
    except ApiException as e:
      raise Exception('Could not find quote in cache: %s\n' % self.conid)

  def get_contract(self, redownload=False):
    # Get contract
    if not redownload:
      try:
        # Get contract from cache
        self.contract = self.disk_find(kind='contract')
        self.industry = self.contract['industry']
        return self.contract
      except Exception as e:
        # Not in cache, redownload
        print('Contract not in cache. Download %s: %s' % (self.symbol, e))
    try:
      # Re-download: Not in cache, or redownload=True
      self.contract = self.down_contract()
    except ApiException as e:
      raise Exception('Could not download contract: %s (%s): %s\n'
        % (self.symbol, self.conid, e))
    # Populate data
    self.industry = self.contract['industry']
    return self.contract


  # PRIVATE
  def down_conid(self):
    # API: Get conid for symbol
    if self.conid is None:
      # Download conid
      config = ib_web_api.Configuration()
      config.verify_ssl = False
      api = ContractApi(ib_web_api.ApiClient(config))
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
    # Save conid to disk
    with open(self.cfg['dir_conids'] + '/' + self.symbol, 'w') as f:
      f.write(str(self.conid))
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
      with open(self.cfg['dir_contracts'] + '/' + self.symbol + '.json', 'w') as f:
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
        file_conid = self.cfg['dir_conids'] + '/' + symbol
        with open(file_conid, 'r') as f:
          return f.read()
      except Exception as e:
        raise Exception('Symbol %s not found' % symbol)
    else:
      raise Exception('Search by conids not yet implemented')

  def disk_find(self, kind='contract'):
    # Find contract or quote in cache, to decide if we need to download it
    # again
    # kind: contract, quote, day
    if kind == 'contract':
      path = self.cfg['dir_contracts']
    elif kind == 'quote':
      path = self.cfg['dir_quotes']
    elif kind == 'day':
      path = self.cfg['dir_day']
    else:
      raise Exception('Invalid kind specified')
    try:
      # Find in cache
      fpath = path + '/' + self.symbol + '.json'
      with open(fpath, 'r') as f:
        return json.load(f)
    except Exception as e:
      raise Exception('Symbol %s not found' % self.symbol)
