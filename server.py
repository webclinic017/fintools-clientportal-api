#!/usr/bin/env python3
# Taken from https://en.wikipedia.org/wiki/Flask_(web_framework)
# This is the API
import json
import os
import requests
import urllib3
from flask import Flask
from requests.exceptions import HTTPError

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
  res = {}
  # Get files
  for s_file in os.listdir(dir_path):
    try:
      s = s_file.split('.')[0]
      fname = dir_path + '/' + s_file
      if os.stat(fname).st_size > 1:
        with open(fname) as f:
          p = json.load(f)['c']
          if float(p) <= float(price):
            res[s] = p
      res_sorted = {}
    except Exception as e:
      print('Unable to read %s' % s_file)
    for k, v in sorted(res.items()):
      # Sort by symbol
      res_sorted[k] = v
  return json.dumps(res_sorted), 200, {'Content-Type': 'application/json'}

if __name__ == '__main__':
  app.run(port=80)
