import ib_web_api
from datetime import datetime
from ib_web_api import MarketDataApi
from ib_web_api.rest import ApiException
from statistics import mean

class VolIncrease:
  # Given a list of tickers, return tickers which spiked X% volume within last
  # Y time, e.g. 15% increase from the lowest volume over last 15min.
  def run(self, symbols):
    # Instantiate API class
    config = ib_web_api.Configuration()
    config.verify_ssl = False
    client = ib_web_api.ApiClient(config)
    api = MarketDataApi(client)
    # TODO: Use utility method here: translate symbols to conids
    symbols = { 'AAPL': '265598', 'AMZN': '3691937' }
    for symbol, conid in symbols.items():
      # Get last 15 minutes data
      points = api.iserver_marketdata_history_get(
        conid,
        '15min',
        bar='1min'
      ).data
      # Convert to dict
      data = [ p.to_dict() for p in points ]
      # Get just volume
      vol = [i['v'] for i in data]
      # Min/max volume points
      lo = min(i for i in vol if i > 0)
      hi = max(vol)
      m = mean(vol)
      # Perc increase from median
      perc = ((hi-m)/m)*100
      print('SYMBOL: ' + symbol + '(' + conid + ')')
      print('CONID: ' + conid)
      print('LO: ' + str(lo))
      print('HI: ' + str(hi))
      print('ME: ' + str(round(m, 2)))
      print('PERC: ' + str(round(perc, 2)) + '%')
