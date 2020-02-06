# Run this as:
# python 3-save-as-json.py > data.json
import argparse
import ib_web_api
import json
from ib_web_api import MarketDataApi
from ib_web_api import ContractApi
from ib_web_api.rest import ApiException

# Parse args
parser = argparse.ArgumentParser(
    description='Display last day data for ticker')
parser.add_argument('tickers', metavar='TICKER', type=str, nargs='+',
    help='Ticker, e.g. AAPL')
args = parser.parse_args()

# Instantiate API class
config = ib_web_api.Configuration()
config.verify_ssl = False
client = ib_web_api.ApiClient(config)

try:
    # Get conids
    api = ContractApi(client)
    conids = {}
    for ticker in args.tickers:
        conid = int
        response = api.iserver_secdef_search_post({ "symbol": ticker })
        for item in response:
            if item.description == 'NASDAQ':
                conids[ticker] = item.conid
except ApiException as e:
    print("Could not find conid: %s\n" % e)
    exit(1)

try:
    # Get market data
    for symbol, conid in conids.items():
        print(symbol)
        api = MarketDataApi(ib_web_api.ApiClient(config))
        response = api.iserver_marketdata_history_get(conid, '1d').data
        #response = response.to_str()
        data = []
        for i in response:
            data.append(i.to_dict())
        print(json.dumps(data, indent=2))

except ApiException as e:
    print("Exception: %s\n" % e)
