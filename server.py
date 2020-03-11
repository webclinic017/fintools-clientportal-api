#!/usr/bin/env python3
# Taken from https://en.wikipedia.org/wiki/Flask_(web_framework)
import json
import os
from flask import Flask
app = Flask(__name__)

dir_path = '/opt/fintools-ib/data/sh/quotes'

@app.route("/")
def hello():
  return 'Hello World'

@app.route('/lt/<price>')
def lt(price):
  res = []
  # Get file 
  for s in os.listdir(dir_path):
    #res.append(s)
    fname = dir_path + '/' + s
    if os.stat(fname).st_size > 1:
      with open(dir_path + '/' + s) as f:
        p = json.load(f)['c']
        if float(p) < float(price):
          res.append(s + ' ' + str(p))
  return '<br>'.join(res)

if __name__ == '__main__':
  app.run(port=80)
