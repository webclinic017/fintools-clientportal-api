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

# Helpers
def create_dir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

# Main
# Create data dir
date = datetime.today().strftime('%Y-%m-%d')
data_dir = 'data'
create_dir(data_dir)
data_dir_m = data_dir + '/' + date + '-s'
data_dir_d = data_dir + '/' + date + '-d'
create_dir(data_dir_m)
create_dir(data_dir_d)

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

# Get conids
try:
    eprint('Get conids')
    api = ContractApi(client)
    conids = {}
    for ticker in args.tickers:
        conid = int
        for j in range(6):
            # Retry on fail
            try:
                response = api.iserver_secdef_search_post({ "symbol": ticker })
                for item in response:
                    if item.description == 'NASDAQ':
                        conids[ticker] = item.conid
                        break
            except Exception:
                if j == 5:
                    print('Could not get symbol %s' % ticker)
                    failed = True
                    continue
except ApiException as e:
    print("Could not get conids: %s\n" % e)
    exit(1)
if len(conids) == 0:
    print('Could not find any conids')
    exit(1)
# Print summary
eprint('Conids found: %s/%s' % (len(conids), len(args.tickers)))

# Get market data
try:
    eprint('Get market data')
    api = MarketDataApi(client)
    for symbol, conid in conids.items():
        response = api.iserver_marketdata_history_get(
          conid,
          '2d',
          bar='5m'
        ).data
        datapoints = []
        # Convert to dict
        for datapoint in response:
            datapoints.append(datapoint.to_dict())
        # Split into two days by date
        dates = {}
        for datapoint in datapoints:
            cur_date = datetime .fromtimestamp(int(datapoint['t']/1000)) \
                .strftime('%Y-%m-%d')
            if cur_date not in dates:
                dates[cur_date] = []
            dates[cur_date].append(datapoint)
        # Write data to dirs
        for date in dates:
            date_dir = data_dir_m + '/' + date
            create_dir(date_dir)
            f = open(date_dir + '/' + symbol + '.json', 'w')
            f.write(json.dumps(dates[date]))
            f.close()
except ApiException as e:
    print("Exception: %s\n" % e)


try:
    eprint('Get snapshot')
    api = MarketDataApi(client)
    for symbol, conid in conids.items():
        ret = api.iserver_marketdata_snapshot_get(conid)[0]
        # Write data to dir
        path = data_dir_d + '/snapshot'
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
    eprint('Get quotes')
    for symbol, conid in conids.items():
        api = ContractApi(client)
        ret = api.iserver_contract_conid_info_get(conid).to_dict()
        # Write data to dir
        dir_quote = data_dir_d + '/quote'
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
