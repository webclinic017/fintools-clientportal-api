import ib_web_api
from ib_web_api import MarketDataApi
from ib_web_api.rest import ApiException

class VolIncrease:
  # Given a list of tickers, return tickers which spiked X% volume within last
  # Y time, e.g. 15% increase from the lowest volume over last 15min.
  def run(self, symbols):
    print('Running on symbols: ' + ' '.join(symbols))
    # Instantiate API class
    # TODO: put this in constructor
    config = ib_web_api.Configuration()
    config.verify_ssl = False
    client = ib_web_api.ApiClient(config)
    api = MarketDataApi(client)
    # TODO: Use utility method here: translate symbols to conids
    conids = [ '265598', '3691937' ]
    for conid in conids:
      # Note: the bar is actually one minute here, quirk of the API
      # 390 minute datapoints, i.e. 6.5 hours of market day data
      points = api.iserver_marketdata_history_get(
        conid,
        '1d',
        bar='5m'
      ).data
      # Get lowest volume
      # TODO: Fix logic here
      # TODO: Can we write this more neatly, with Pythonic one-liner lambda-like
      # generator?
      low = None
      for p in points:
        # c, h, l, o, t, v
        p = p.to_dict()
        if low is None:
          low = p['v']
          continue
        if p['v'] < low:
          low = p['v']
      # TODO: End 'Fix logic here'
      # TODO: see if latest is more than X perc more than lowest
