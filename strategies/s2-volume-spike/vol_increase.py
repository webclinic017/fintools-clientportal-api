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
      print(conid)
      points = api.iserver_marketdata_history_get(conid, '1d').data
      # TODO: Iterate over data here, get lowest, see if latest is
      # more than X perc
      for points as p:
        print(p['v'])
