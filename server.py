#!/usr/bin/env python3
# Taken from https://en.wikipedia.org/wiki/Flask_(web_framework)
import json
import os
from flask import Flask
app = Flask(__name__)

dir_path = '/opt/fintools-ib/data/quotes'

@app.route("/")
def hello():
  return 'Hello World'

@app.route('/lt/<price>')
def lt(price):
  res = {}
  # Get files
  for s_file in os.listdir(dir_path):
    s = s_file.split('.')[0]
    fname = dir_path + '/' + s_file
    if os.stat(fname).st_size > 1:
      with open(fname) as f:
        p = json.load(f)['c']
        if float(p) <= float(price):
          res[s] = p
  return json.dumps(res), 200, {'Content-Type': 'application/json'}

if __name__ == '__main__':
  app.run(port=80)
