#!/usr/bin/env python3
# Taken from https://en.wikipedia.org/wiki/Flask_(web_framework)
# This is the API
import json
import os
import requests
import urllib3
from flask import Flask
from requests.exceptions import HTTPError

# Local
import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../'))
import lib.filters


app = Flask(__name__)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
dir_path = '/opt/fintools-ib/data/quotes'
url_health = 'https://localhost:5000/v1/portal/iserver/auth/status'
header = {'Content-Type': 'application/json'}

@app.route("/")
def hello():
  return 'Hello World'

@app.route('/health')
def health():
  msg_err = { 'status': 'ERROR' }
  msg_ok = { 'status': 'SUCCESS' }
  try:
    response = requests.get(url_health, verify=False)
    response.raise_for_status()
  except HTTPError as http_err:
    return json.dumps(msg_err), 500, header
  except Exception as err:
    return json.dumps(msg_err), 500, header
  else:
    # HTTP 200 OK
    res = json.loads(response.content)
    if res['authenticated'] is True and res['connected'] is True:
      return json.dumps(msg_ok), 200, {'Content-Type': 'application/json'}
    else:
      return json.dumps(msg_err), 500, header

@app.route('/lt/<price>')
def lt(price):
  res = filters.get_symbols_cheaper_than(price)
  return json.dumps(res), 200, {'Content-Type': 'application/json'}

@app.route('/ltcontracts/<price>')
def ltcontracts(price):
  res = filters.get_contracts_cheaper_than(price)
  return json.dumps(res), 200, {'Content-Type': 'application/json'}


if __name__ == '__main__':
  app.run(port=80)
