#!/usr/bin/env python3
# Run this as:
# python 3-save-as-json.py > data.json
import argparse
import ib_web_api
import json
import os
from datetime import datetime
from ib_web_api import MarketDataApi
from ib_web_api import ContractApi
from ib_web_api.rest import ApiException

# Settings
data_dir = 'data-6'


# Helpers
def create_dir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


# Main
# Create data dir
create_dir(data_dir)

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
        api = MarketDataApi(ib_web_api.ApiClient(config))
        response = api.iserver_marketdata_history_get(conid, '2d').data
        datapoints = []
        # Convert to dict
        for datapoint in response:
            datapoints.append(datapoint.to_dict())
        # Split into two days by date
        dates = {}
        for datapoint in datapoints:
            cur_date = datetime \
                .fromtimestamp(int(datapoint['t']/1000)) \
                .strftime('%Y-%m-%d')
            if cur_date not in dates:
                dates[cur_date] = []
            dates[cur_date].append(datapoint)
        # Write data to dirs
        for date in dates:
            date_dir = data_dir + '/' + date
            create_dir(date_dir)
            f = open(date_dir + '/' + symbol + '.json', 'w')
            f.write(json.dumps(dates[date]))
            f.close()
except ApiException as e:
    print("Exception: %s\n" % e)
