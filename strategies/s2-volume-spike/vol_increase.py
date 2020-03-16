import ib_web_api
from lib.company import Company
from datetime import datetime
from ib_web_api import MarketDataApi
from ib_web_api.rest import ApiException
from statistics import mean

class VolIncrease:
  # Given a list of tickers, return tickers which spiked X% volume within last
  # Y time, e.g. 15% increase from the lowest volume over last 15min.
  def run(self, symbols):
    symbols = [i.upper() for i in symbols]
    # Instantiate API class
    config = ib_web_api.Configuration()
    config.verify_ssl = False
    client = ib_web_api.ApiClient(config)
    api = MarketDataApi(client)
    for symbol in symbols:
      print('===> ' + symbol)
      # Get last 15 minutes data
      # TODO: Catch here
      points = api.iserver_marketdata_history_get(
        Company(symbol).get_conid(),
        '15min',
        bar='1min'
      ).data
      # Get just volume
      vol = [ p.to_dict()['v'] for p in points ]
      # Min/max/mean volume points
      lo = min(i for i in vol if i > 0)
      hi = max(vol)
      m = mean(vol)
      # Perc increase from mean
      perc = ((hi-m)/m)*100
      print('LO: ' + str(lo))
      print('HI: ' + str(hi))
      print('ME: ' + str(round(m, 2)))
      print('PERC: ' + str(round(perc, 2)) + '%')
      print('CONID: ' + Company(symbol).get_conid())
