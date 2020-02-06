import ib_web_api as client
from ib_web_api.rest import ApiException

# Instantiate API class
config = client.Configuration()
config.verify_ssl = False
api = client.MarketDataApi(client.ApiClient(config))

try:
    # Market data for Apple (AAPL)
    response = api.iserver_marketdata_history_get(265598, '1d')
    print(response.data)
except ApiException as e:
    print("Exception: %s\n" % e)
