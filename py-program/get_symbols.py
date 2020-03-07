#!/usr/bin/env python3
# Get symbols under $2 on NASDAQ
#
# Run as:  ./get_symbols.py

import ib_web_api
import json
import pprint
import sys
from ib_web_api import ScannerApi
from ib_web_api.rest import ApiException

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

# Instantiate API class
config = ib_web_api.Configuration()
config.verify_ssl = False
client = ib_web_api.ApiClient(config)

# Get conids
try:
    eprint('Get conids')
    api = ScannerApi(client)
    body = {
        "instrument": "STK",
        "type": "TOP_VOLUME_RATE",
        "location": "STK.US.MAJOR"
    }
    response = api.iserver_scanner_run_post(body)
    #response = api.iserver_scanner_run_post({"type": "TOP_PERC_GAIN", "instrument": 'STK'})
    pprint.pprint(response)
except ApiException as e:
    print("Could not get conids: %s\n" % e)
    exit(1)
