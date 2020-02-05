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
parser.add_argument('ticker', metavar='TICKER', type=str,
    help='Ticker, e.g. AAPL')
args = parser.parse_args()

# Instantiate API class
config = ib_web_api.Configuration()
config.verify_ssl = False
client = ib_web_api.ApiClient(config)

# Get conid
api = ContractApi(client)
try:
    conid = int
    response = api.iserver_secdef_search_post({ "symbol": args.ticker })
    for item in response:
        if item.description == 'NASDAQ':
            conid = item.conid
except ApiException as e:
    print("Could not find conid: %s\n" % e)
    exit(1)

# Get market data
api = MarketDataApi(ib_web_api.ApiClient(config))
try:
    response = api.iserver_marketdata_history_get(conid, '1d').data
    #response = response.to_str()
    data = []
    for i in response:
        data.append(i.to_dict())
    print(json.dumps(data, indent=2))
except ApiException as e:
    print("Exception: %s\n" % e)
