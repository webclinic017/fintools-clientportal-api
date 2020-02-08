#!/usr/bin/env python3
# Create a 'data' dir, which contains today's date dir
# Inside that dir are further two dirs (today, yesterday), which contain market
# data (OHLC) for these tickers
#
# Run as:  ./download.py TICKERS
# Example: ./download.py AAPL AMZN

import argparse
import ib_web_api
import json
import os
from datetime import datetime
from ib_web_api import MarketDataApi
from ib_web_api import ContractApi
from ib_web_api.rest import ApiException

# Settings
data_dir = 'data'


# Helpers
def create_dir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


# Main
# Create data dir
create_dir(data_dir)
data_dir = data_dir \
         + '/snapshot-' \
         + datetime.today().strftime('%Y-%m-%d')
create_dir(data_dir)

# Parse args
parser = argparse.ArgumentParser(
    description='Display last day data for ticker')
parser.add_argument('tickers', metavar='TICKERS', type=str, nargs='+',
    help='Tickers, e.g. AAPL AMZN')
args = parser.parse_args()

# Instantiate API class
config = ib_web_api.Configuration()
config.verify_ssl = False
client = ib_web_api.ApiClient(config)

try:
    # Get conids
    print('Get conids')
    api = ContractApi(client)
    conids = {}
    for ticker in args.tickers:
        conid = int
        try:
            response = api.iserver_secdef_search_post({ "symbol": ticker })
        except Exception:
            # Could not get conid, so skip it
            continue
        for item in response:
            if item.description == 'NASDAQ':
                conids[ticker] = item.conid
except ApiException as e:
    # Could not get conid, skip for now
    print("Could not get conids: %s\n" % e)
    exit(1)
if len(conids) == 0:
    # Terminate if no conids found
    print('Could not find any conids')
    exit(1)

# Print summary
print('Conids supplied:', len(args.tickers))
print('Conids found:', len(conids))

try:
    # Get market data for each conid
    print('Get market data')
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
