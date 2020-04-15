# Utilities
import datetime
import json

def get(point, kind):
  # point = { o, c, h, l, v, t }
  # kind = 'h' or 'l'
  return { 't': point['t'], 'value': point[kind], 'v': point['v'] }

def get_perc_from_history(data, perc):
  # data = {
  #  { 'o': 1, 'h': 2, 'l': 3, 'c': 4 },
  # ...
  # }
  # perc: e.g. 4 for 4%
  # Sort by timestamp
  data = sorted(data, key=lambda k: k['t'])
  # Get points
  hi = get(data[0], 'h')
  lo = get(data[0], 'l')
  finding_hi = True
  points = []
  for point in data:
    hi = get(point, 'h')
    if point['l'] < lo['value']:
      lo = get(point, 'l')
    if hi['value']/lo['value'] > (100+perc)/100:
      if hi['t'] == lo ['t']:
        extra = '*'
      else:
        extra = ''
      v0 = lo
      v1 = hi
      points.append({
        't0': v0['t'],
        't1': v1['t'],
        'y0': v0['value'],
        'y1': v1['value'],
        'v0': v0['v'],
        'v1': v1['v'],
        'perc': (hi['value']/lo['value'])*100 - 100
      })
      lo = get(point, 'h')
  return points

def timestamp_to_date(timestamp):
  timestamp = int(timestamp)
  return datetime.datetime.fromtimestamp(timestamp/1000).strftime('%Y%m%d')

