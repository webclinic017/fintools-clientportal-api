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
import pprint
import sys
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

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

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
eprint('Conids found: %s/%s' % (len(conids), len(args.tickers)))

try:
    # Get market data for each conid
    eprint('Get market data')
    for symbol, conid in conids.items():
        api = MarketDataApi(client)
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

try:
    # Get snapshot
    eprint('Get snapshot')
    for symbol, conid in conids.items():
        api = MarketDataApi(client)
        ret = api.iserver_marketdata_snapshot_get(conid)[0]
        # Write data to dir
        path = data_dir + '/snapshot'
        create_dir(path)
        with open(path + '/' + symbol + '.json', 'w') as f:
            # Clean
            o = {
                'after_hours': ret._31,
                'prev_close': ret._7296,
                'price_chg': ret._82,
                'price_chg_perc': ret._83,
                '52w_hi': ret._7293,
                '52w_lo': ret._7294,
            }
            f.write(json.dumps(o))
            f.close()
except ApiException as e:
    print("Exception: %s\n" % e)

try:
    # Get quote for each conid
    eprint('Get quotes')
    for symbol, conid in conids.items():
        api = ContractApi(client)
        ret = api.iserver_contract_conid_info_get(conid).to_dict()
        # Write data to dir
        dir_quote = data_dir + '/quote'
        create_dir(dir_quote)
        with open(dir_quote + '/' + symbol + '.json', 'w') as f:
            # Clean
            del ret['rules']
            del ret['instrument_type']
            del ret['r_t_h']
            del ret['currency']
            del ret['exchange']
            f.write(json.dumps(ret))
            f.close()
except ApiException as e:
    print("Exception: %s\n" % e)
