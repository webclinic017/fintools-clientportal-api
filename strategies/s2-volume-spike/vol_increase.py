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
